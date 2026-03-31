"""Coordinator for Grünbeck Cloud integration."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from typing import Any

from pygruenbeck_cloud import PyGruenbeckCloud
from pygruenbeck_cloud.exceptions import (
    PyGruenbeckCloudConnectionClosedError,
    PyGruenbeckCloudConnectionError,
    PyGruenbeckCloudError,
    PyGruenbeckCloudResponseStatusError,
    PyGruenbeckCloudUpdateParameterError,
)
from pygruenbeck_cloud.models import Device

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import (
    CALLBACK_TYPE,
    Event,
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    callback,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_DEVICE_ID,
    DOMAIN,
    SERVICE_PARAM_PARAMETER,
    SERVICE_PARAM_VALUE,
    UPDATE_INTERVAL,
    UPDATE_INTERVAL_POLLING,
)

_LOGGER = logging.getLogger(__name__)

_SERIES_POLL_ONLY = "softliQ.SE"

# Suppress UpdateFailed for this long before letting entities go unavailable.
_ERROR_GRACE_PERIOD = timedelta(minutes=10)

# How many SE polling cycles between full device-info refreshes.
# UPDATE_INTERVAL / UPDATE_INTERVAL_POLLING = 360 / 60 = 36.
_POLL_CYCLES_PER_FULL_REFRESH = max(
    1, int(UPDATE_INTERVAL.total_seconds() / UPDATE_INTERVAL_POLLING.total_seconds())
)


class GruenbeckCloudCoordinator(DataUpdateCoordinator[Device]):
    """Grünbeck Cloud Coordinator."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize Coordinator."""
        self.api = PyGruenbeckCloud(
            username=config_entry.data[CONF_USERNAME],
            password=config_entry.data[CONF_PASSWORD],
        )
        self.api.logger = _LOGGER
        self._device_id = config_entry.data[CONF_DEVICE_ID]

        self.unsub: CALLBACK_TYPE | None = None
        self._poll_cycle: int = 0
        self._error_since: datetime | None = None

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def disconnect(self) -> None:
        """Disconnect from API."""
        await self._stop_websocket()

    @staticmethod
    def _use_websocket(device: Device | None) -> bool:
        """Return True if this device should use WebSocket updates."""
        if device is None:
            return False
        series = getattr(device, "series", None)
        return series is not None and series != _SERIES_POLL_ONLY

    async def _stop_websocket(self) -> None:
        """Stop WebSocket listener and disconnect if needed."""
        if self.api.connected:
            await self.api.disconnect()
        if self.unsub:
            self.unsub()
            self.unsub = None

    @callback
    def _listen_websocket(self) -> None:
        """Listen to WebSocket updates."""

        async def listen() -> None:
            """Listen for state changes."""
            try:
                await self.api.connect()
            except (PyGruenbeckCloudError, PyGruenbeckCloudResponseStatusError) as err:
                self.logger.error(err)
                if self.unsub:
                    self.unsub()
                    self.unsub = None
                return

            try:
                await self.api.listen(callback=self.async_set_updated_data)
            except (
                PyGruenbeckCloudConnectionError,
                PyGruenbeckCloudConnectionClosedError,
                PyGruenbeckCloudResponseStatusError,
            ) as err:
                self.last_update_success = False
                self.logger.error(err)
            except PyGruenbeckCloudError as err:
                self.last_update_success = False
                self.async_update_listeners()
                self.logger.error(err)

            # Ensure we disconnect
            await self.api.disconnect()
            if self.unsub:
                self.unsub()
                self.unsub = None

        async def close_websocket(_: Event) -> None:
            """Close WebSocket connection."""
            self.unsub = None
            await self.api.disconnect()

        # Clean disconnect WebSocket on Home Assistant shutdown
        self.unsub = self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, close_websocket
        )

        # Start listener
        self.config_entry.async_create_background_task(
            self.hass, listen(), "gruenbeck-cloud-listen"
        )

    async def service_get_device_salt_measurements(
        self, call: ServiceCall
    ) -> ServiceResponse:
        """Service to get Salt measurements."""
        device = await self.api.get_device_salt_measurements()
        if device.salt is None:
            return {"entries": []}

        return {
            "entries": [
                {
                    "date": item.date.isoformat(),
                    "value": item.value,
                }
                for item in device.salt
            ],
        }

    async def service_get_device_water_measurements(
        self, call: ServiceCall
    ) -> ServiceResponse:
        """Service to get Water measurements."""
        device = await self.api.get_device_water_measurements()
        if device.water is None:
            return {"entries": []}

        return {
            "entries": [
                {
                    "date": item.date.isoformat(),
                    "value": item.value,
                }
                for item in device.water
            ],
        }

    async def service_regenerate(self, call: ServiceCall) -> None:
        """Service to start manual regeneration."""
        await self.api.regenerate()

    async def service_change_settings(self, call: ServiceCall) -> None:
        """Service for update device settings."""
        data = {
            call.data[SERVICE_PARAM_PARAMETER]: call.data[SERVICE_PARAM_VALUE],
        }

        await self.update_device_infos_parameters(data)

    async def update_device_infos_parameters(self, data: dict[str, Any]) -> None:
        """Update Device parameters."""
        try:
            self.data = await self.api.update_device_infos_parameters(data)
        except PyGruenbeckCloudUpdateParameterError as err:
            raise HomeAssistantError(err) from err

    @callback
    def async_set_updated_data(self, data: Device) -> None:
        """Manually update data from WebSocket, avoid stopping refresh interval."""
        self.data = data
        self.last_update_success = True

        self.logger.debug(
            "Manually updated %s data",
            self.name,
        )
        self.async_update_listeners()

    async def _async_update_data(self) -> Device:
        """Update regularly data from API."""
        self.logger.debug(
            "Regularly updated %s data",
            self.name,
        )

        try:
            if not self.api.device:
                await self.api.set_device_from_id(self._device_id)

            if self._use_websocket(self.api.device):
                # WebSocket-capable series (SL, SD, …): use WS for realtime data.
                self.logger.debug("Using WebSocket for device %s", self.name)
                if not self.api.connected and not self.unsub:
                    self._listen_websocket()
                await self.api.get_device_infos()
                data = await self.api.get_device_infos_parameters()

            else:
                # SE-series: per-poll stateless cycle (refresh→enter→update→leave→off).
                # Do NOT hold a persistent realtime session — the server drops it after
                # ~10-15 minutes, causing updates to silently stall.
                self.logger.debug("Using polling for device %s", self.name)
                await self._stop_websocket()

                # Switch coordinator to shorter polling interval on first SE poll.
                if self.update_interval != UPDATE_INTERVAL_POLLING:
                    self.update_interval = UPDATE_INTERVAL_POLLING

                # Refresh static device info every _POLL_CYCLES_PER_FULL_REFRESH cycles.
                if self._poll_cycle % _POLL_CYCLES_PER_FULL_REFRESH == 0:
                    self.logger.debug(
                        "Full device info refresh for %s (cycle %d)",
                        self.name,
                        self._poll_cycle,
                    )
                    await self.api.get_device_infos()
                    await self.api.get_device_infos_parameters()

                self._poll_cycle += 1

                data = await self.api.poll_sd()

            self._error_since = None
            return data

        except (
            Exception,
            IndexError,
            KeyError,
            PyGruenbeckCloudResponseStatusError,
        ) as err:
            now = datetime.now(timezone.utc)
            if self._error_since is None:
                self._error_since = now
            elapsed = now - self._error_since
            if self.data is not None and elapsed < _ERROR_GRACE_PERIOD:
                self.logger.warning(
                    "API error for %s (%.0fs elapsed, grace period %ds): %s — keeping last data",
                    self.name,
                    elapsed.total_seconds(),
                    _ERROR_GRACE_PERIOD.total_seconds(),
                    err,
                )
                return self.data
            self._error_since = None
            raise UpdateFailed(f"Unable to get data from API: {err}") from err
