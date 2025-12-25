"""Coordinator for Grünbeck Cloud integration."""
from __future__ import annotations

import logging
import time
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
    UPDATE_INTERVAL_POLLING,
    UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

_SERIES_POLL_ONLY = "softliQ.SE"

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
        self._sd_polling_enabled = False

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def disconnect(self) -> None:
        """Disconnect from API."""
        await self._stop_sd_polling()
        await self._stop_websocket()

    @staticmethod
    def _use_websocket(device: Device | None) -> bool:
        """Return True if this device should use WebSocket updates."""
        if device is None:
            return False
        series = getattr(device, "series", None)
        return series is not None and series != _SERIES_POLL_ONLY

    async def _ensure_sd_polling(self) -> None:
        """Enable SD polling mode for devices that do not use WebSockets."""
        if self._sd_polling_enabled:
            return
        self.logger.debug(
            "Setting polling mode for %s",
            self.name,
        )

        # Do initial device info refresh before entering SD mode
        await self.api.get_device_infos()
        await self.api.get_device_infos_parameters()

        # update interval for shorter polling
        self.update_interval = UPDATE_INTERVAL_POLLING
        await self.api.refresh_sd()
        await self.api.enter_sd()

        self._sd_polling_enabled = True

    async def _stop_sd_polling(self) -> None:
        """Disable SD polling mode when polling flow must stop."""
        if not self._sd_polling_enabled:
            return
        self.logger.debug(
            "Stopping polling mode for %s",
            self.name,
        )
        try:
            await self.api.leave_sd()
        finally:
            await self.api.off_sd()
            self._sd_polling_enabled = False

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

        self.use_websocket = self._use_websocket(self.api.device)
        self.last_update_time = time.time()
        seconds_since_last_update = time.time() - self.last_update_time

        try:
            if not self.api.device:
                await self.api.set_device_from_id(self._device_id)

            if self.use_websocket:
                # WebSocket series: ensure WS listener is running; do not stop SD polling here.
                self.logger.debug('Using WebSocket for device %s', self.name)
                if not self.api.connected and not self.unsub:
                    self._listen_websocket()
                await self.api.get_device_infos()
                return await self.api.get_device_infos_parameters()
            else:
                # Polling-only series: keep polling enabled, just update each cycle.
                self.logger.debug('Using Polling for device %s', self.name)
                await self._stop_websocket()
                await self._ensure_sd_polling()
                # For polling-only devices, refresh device info less frequently than polling interval.
                if seconds_since_last_update > UPDATE_INTERVAL.total_seconds():
                    self.logger.debug(
                        "Updating device infos and parameters for %s",
                        self.name,
                    )
                    await self.api.get_device_infos()
                    await self.api.get_device_infos_parameters()
                self.logger.debug(
                    "Polling data for %s",
                    self.name,
                )
                return await self.api.update_sd()

        except (
                Exception,
                IndexError,
                KeyError,
                PyGruenbeckCloudResponseStatusError,
        ) as err:
            await self._stop_sd_polling()
            self.logger.error(
                "API failure for %s",
                self.name,
                err
            )
            raise UpdateFailed(f"Unable to get data from API: {err}") from err
