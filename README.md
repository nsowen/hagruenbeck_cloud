# Grünbeck Cloud Homeassistant Component

<p align="center">
    <a href="https://www.gruenbeck.com/" target="_blank"><img src="https://www.gruenbeck.com/typo3conf/ext/sitepackage_gruenbeck/Resources/Public/Images/gruenbeck-logo.svg" alt="Gruenbeck" /></a>
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/p0l0/hagruenbeck_cloud)](https://github.com/p0l0/hagruenbeck_cloud/releases)
![Build Pipeline](https://img.shields.io/github/actions/workflow/status/p0l0/hagruenbeck_cloud/validate.yaml)
![License](https://img.shields.io/github/license/p0l0/hagruenbeck_cloud)

![Project maintenance](https://img.shields.io/badge/maintainer-%40p0l0-blue.svg)
[![BuyMeCoffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/p0l0)

Custom Component to integrate Grünbeck Cloud based Water softeners into [Home Assistant](https://www.home-assistant.io/).

## Supported series

| Series     | Update mechanism | Update interval |
|------------|------------------|-----------------|
| softliQ.SL | WebSocket (push) | Real-time       |
| softliQ.SD | WebSocket (push) | Real-time       |
| softliQ.SE | HTTP polling     | 60 seconds      |

> [!NOTE]
> The softliQ.SE uses a stateless per-poll HTTP cycle instead of a persistent WebSocket connection. Entities that are only available for specific series are marked in the tables below.

**This integration will set up the following entities.**

> [!NOTE]
> Entity names use translation — they will have a different name if you are not using English.

| Platform | Description | Enabled by default | Supported series |
|----------|-------------|--------------------|------------------|
| __Binary sensor__ ||||
| `binary_sensor.<device_name>_has_error` | Binary sensor showing if the device has an error<br /><br />The `errors` attribute contains error history | :white_check_mark: | All |
| __Sensor__ ||||
| `sensor.<device_name>_next_regeneration` | Sensor showing when next regeneration will be | :white_check_mark: | All |
| `sensor.<device_name>_raw_water` | Sensor showing configured raw water hardness value | :white_check_mark: | All |
| `sensor.<device_name>_soft_water` | Sensor showing the configured soft water hardness value | :white_check_mark: | All |
| `sensor.<device_name>_startup` | Sensor showing start-up date | :white_check_mark: | All |
| `sensor.<device_name>_last_service` | Sensor showing when last service was | :white_check_mark: | SL/SD |
| `sensor.<device_name>_regeneration_counter` | Sensor showing current regeneration counter | :white_check_mark: | All |
| `sensor.<device_name>_regeneration_step` | Sensor showing the current regeneration step | :white_check_mark: | All |
| `sensor.<device_name>_current_flow_rate` | Sensor showing current flow rate in m³/h | :white_check_mark: | All |
| `sensor.<device_name>_remaining_capacity_percentage` | Sensor showing remaining capacity of exchanger 1 in % | :white_check_mark: | All |
| `sensor.<device_name>_remaining_capacity_volume` | Sensor showing remaining capacity of exchanger 1 in m³ | :white_check_mark: | All |
| `sensor.<device_name>_salt_consumption` | Sensor showing current salt consumption in kg<br /><br />The `daily_usage` attribute contains the salt usage of the last 3 days | :white_check_mark: | All |
| `sensor.<device_name>_salt_range` | Sensor showing how many days left until salt is empty | :white_check_mark: | All |
| `sensor.<device_name>_soft_water_quantity` | Sensor showing current soft water quantity in liters<br /><br />The `daily_usage` attribute contains the soft water usage of the last 3 days | :white_check_mark: | All |
| `sensor.<device_name>_lime_scale_indicator` | Sensor showing the lime scale indicator in % | :white_check_mark: | SE |
| `sensor.<device_name>_regeneration_progress_2` | Sensor showing the regeneration progress of exchanger 2 in % | :white_check_mark: | SE |
| `sensor.<device_name>_next_service` | Sensor showing how many days until next service | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_regeneration_remaining_time` | Sensor showing the remaining amount/time of the current regeneration step | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_current_flow_rate_2` | Sensor showing current flow rate for exchanger 2 in m³/h | :no_entry_sign: | All |
| `sensor.<device_name>_remaining_capacity_percentage_2` | Sensor showing remaining capacity of exchanger 2 in % | :no_entry_sign: | All |
| `sensor.<device_name>_remaining_capacity_volume_2` | Sensor showing remaining capacity of exchanger 2 in m³ | :no_entry_sign: | All |
| `sensor.<device_name>_soft_water_quantity_2` | Sensor showing current soft water quantity of exchanger 2 in liters | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_make_up_water_volume` | Sensor showing the make-up water volume | :no_entry_sign: | All |
| `sensor.<device_name>_blending_flow_rate` | Sensor showing the blending flow rate | :no_entry_sign: | All |
| `sensor.<device_name>_capacity_figure` | Sensor showing the capacity figure | :no_entry_sign: | All |
| `sensor.<device_name>_remaining_amount_of_water` | Sensor showing the adsorber remaining amount of water | :no_entry_sign: | All |
| `sensor.<device_name>_regeneration_flow_rate_exchanger_2` | Sensor showing the regeneration flow rate for exchanger 2 | :no_entry_sign: | All |
| `sensor.<device_name>_step_indication_regeneration_valve_2` | Sensor showing the step indication for regeneration valve 2 | :no_entry_sign: | All |
| `sensor.<device_name>_actual_value_soft_water_hardness` | Sensor showing the actual soft water hardness value | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_current_chlorine` | Sensor showing the current chlorine (chlorine cell) | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_exchanger_peak_value` | Sensor showing the exchanger 1 peak flow rate | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_exchanger_peak_value_2` | Sensor showing the exchanger 2 peak flow rate | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_exhausted_percentage` | Sensor showing the adsorber exhaustion in % | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_flow_rate_peak_value` | Sensor showing the overall flow rate peak value | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_last_regeneration_exchanger` | Sensor showing the time of last regeneration for exchanger 1 | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_last_regeneration_exchanger_2` | Sensor showing the time of last regeneration for exchanger 2 | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_regeneration_flow_rate_exchanger` | Sensor showing the regeneration flow rate for exchanger 1 | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_step_indication_regeneration_valve` | Sensor showing the step indication for regeneration valve 1 | :no_entry_sign: | SL/SD |
| `sensor.<device_name>_days_until_inspection` | Sensor showing days until next inspection | :no_entry_sign: | SE |
| `sensor.<device_name>_regeneration_counter_service` | Sensor showing the regeneration counter since last service | :no_entry_sign: | SE |
| `sensor.<device_name>_water_usage_today` | Sensor showing water usage today in liters | :no_entry_sign: | SE |
| `sensor.<device_name>_salt_usage_today` | Sensor showing salt usage today in kg | :no_entry_sign: | SE |
| `sensor.<device_name>_lime_today` | Sensor showing today's lime value | :no_entry_sign: | SE |
| `sensor.<device_name>_regeneration_progress_1` | Sensor showing the regeneration progress of exchanger 1 in % | :no_entry_sign: | SE |
| __Switch__ ||||
| `switch.<device_name>_buzzer` | Activate/Deactivate audio signal on error | :white_check_mark: | All |
| `switch.<device_name>_dlst` | Activate/Deactivate daylight saving time | :white_check_mark: | All |
| `switch.<device_name>_email_notification` | Activate/Deactivate email notifications | :white_check_mark: | All |
| `switch.<device_name>_push_notification` | Activate/Deactivate push notifications | :white_check_mark: | All |
| `switch.<device_name>_disinfection_monitoring` | Activate/Deactivate disinfection monitoring<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `switch.<device_name>_ntp_sync` | Activate/Deactivate getting date/time automatically (NTP)<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `switch.<device_name>_fault_signal_contact` | Activate/Deactivate function fault signal contact<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `switch.<device_name>_knx` | Activate/Deactivate KNX connection<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `switch.<device_name>_led_ring_flash_on_signal` | Activate/Deactivate LED ring flash for pre-alarm salt supply | :no_entry_sign: | SL/SD |
| `switch.<device_name>_nominal_flow_monitoring` | Activate/Deactivate monitoring of nominal flow<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| __Text__ ||||
| `text.<device_name>_installer_email` | Set the installer email<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `text.<device_name>_installer_name` | Set the installer name<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `text.<device_name>_installer_phone` | Set the installer phone<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| __Time__ ||||
| `time.<device_name>_regeneration_time_monday_1` | Set regeneration time Monday slot #1 (`--:--` = unset / IQ mode) | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_monday_2` | Set regeneration time Monday slot #2 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_monday_3` | Set regeneration time Monday slot #3 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_tuesday_1` | Set regeneration time Tuesday slot #1 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_tuesday_2` | Set regeneration time Tuesday slot #2 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_tuesday_3` | Set regeneration time Tuesday slot #3 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_wednesday_1` | Set regeneration time Wednesday slot #1 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_wednesday_2` | Set regeneration time Wednesday slot #2 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_wednesday_3` | Set regeneration time Wednesday slot #3 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_thursday_1` | Set regeneration time Thursday slot #1 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_thursday_2` | Set regeneration time Thursday slot #2 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_thursday_3` | Set regeneration time Thursday slot #3 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_friday_1` | Set regeneration time Friday slot #1 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_friday_2` | Set regeneration time Friday slot #2 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_friday_3` | Set regeneration time Friday slot #3 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_saturday_1` | Set regeneration time Saturday slot #1 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_saturday_2` | Set regeneration time Saturday slot #2 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_saturday_3` | Set regeneration time Saturday slot #3 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_sunday_1` | Set regeneration time Sunday slot #1 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_sunday_2` | Set regeneration time Sunday slot #2 | :white_check_mark: | All |
| `time.<device_name>_regeneration_time_sunday_3` | Set regeneration time Sunday slot #3 | :white_check_mark: | All |
| __Number__ ||||
| `number.<device_name>_raw_water_hardness` | Set the raw water hardness in °dH | :white_check_mark: | All |
| `number.<device_name>_soft_water_hardness` | Set the soft water hardness in °dH | :white_check_mark: | All |
| `number.<device_name>_backwash` | Set the backwash value in liters<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_blending_water_meter_pulse_rate` | Set the blending water meter pulse rate in l/Imp<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_capacity_figure_monday` | Set the capacity figure for Monday in m³x°dH<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_capacity_figure_tuesday` | Set the capacity figure for Tuesday in m³x°dH<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_capacity_figure_wednesday` | Set the capacity figure for Wednesday in m³x°dH<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_capacity_figure_thursday` | Set the capacity figure for Thursday in m³x°dH<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_capacity_figure_friday` | Set the capacity figure for Friday in m³x°dH<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_capacity_figure_saturday` | Set the capacity figure for Saturday in m³x°dH<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_capacity_figure_sunday` | Set the capacity figure for Sunday in m³x°dH<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_charge` | Set the charge value in mAmin<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_current_setpoint` | Set the current setpoint in mA<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_end_frequency_blending_valve` | Set the end frequency blending valve in Hz<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_end_frequency_regeneration_valve` | Set the end frequency regeneration valve 1 in Hz<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_end_frequency_regeneration_valve_2` | Set the end frequency regeneration valve 2 in Hz<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_interval_forced_regeneration` | Set the interval of forced regeneration in days<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_led_ring_brightness` | Set the LED ring brightness in % | :no_entry_sign: | All |
| `number.<device_name>_longest_switch_on_time_chlorine_cell` | Set the longest switch-on time for chlorine cell in minutes<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_maintenance_interval` | Set the maintenance interval in days<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_minimum_filling_volume_largest_cap` | Set the minimum filling volume for largest cap in liters<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_maximum_filling_volume_largest_cap` | Set the maximum filling volume for largest cap in liters<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_minimum_filling_volume_smallest_cap` | Set the minimum filling volume for smallest cap in liters<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_maximum_filling_volume_smallest_cap` | Set the maximum filling volume for smallest cap in liters<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_maximum_remaining_time_regeneration` | Set the maximum remaining time for regeneration in minutes<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_nominal_flow_rate` | Set the nominal flow rate in m³/h<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_regeneration_monitoring_time` | Set the regeneration monitoring time in minutes<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_regeneration_water_meter_pulse_rate` | Set the regeneration water meter pulse rate in l/Imp<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_residual_capacity_limit` | Set the residual capacity limit in %<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_salting_monitoring_time` | Set the salting monitoring time in minutes<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_slow_rinse` | Set the slow rinse value in minutes<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_soft_water_meter_pulse_rate` | Set the soft water meter pulse rate in l/Imp<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `number.<device_name>_treatment_volume` | Set the treatment volume in m³<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | SL/SD |
| `number.<device_name>_washing_out` | Set the washing out value in liters<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| __Select__ ||||
| `select.<device_name>_mode` | Select the operation mode | :white_check_mark: | All |
| `select.<device_name>_regeneration_mode` | Select the regeneration mode | :white_check_mark: | All |
| `select.<device_name>_water_hardness_unit` | Select the water hardness unit | :white_check_mark: | All |
| `select.<device_name>_language` | Select the interface language<br /><br />__API returns HTTP 500 when trying to change__ | :no_entry_sign: | All |
| `select.<device_name>_led_ring_mode` | Select the LED ring mode | :no_entry_sign: | All |
| `select.<device_name>_mode_individual_monday` | Select individual operation mode for Monday | :no_entry_sign: | SL/SD |
| `select.<device_name>_mode_individual_tuesday` | Select individual operation mode for Tuesday | :no_entry_sign: | SL/SD |
| `select.<device_name>_mode_individual_wednesday` | Select individual operation mode for Wednesday | :no_entry_sign: | SL/SD |
| `select.<device_name>_mode_individual_thursday` | Select individual operation mode for Thursday | :no_entry_sign: | SL/SD |
| `select.<device_name>_mode_individual_friday` | Select individual operation mode for Friday | :no_entry_sign: | SL/SD |
| `select.<device_name>_mode_individual_saturday` | Select individual operation mode for Saturday | :no_entry_sign: | SL/SD |
| `select.<device_name>_mode_individual_sunday` | Select individual operation mode for Sunday | :no_entry_sign: | SL/SD |

> [!CAUTION]
> Unfortunately some parameters cannot be changed via the API — they always return HTTP 500 with `unexpectedException`. These are marked above.

**This integration provides following services.**

| Service                       | Description                                                           | Fields                                                                                                                                                                                                                      |
|-------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| change_settings               | Changes the setting for the water softener.                           | `parameter`: The name of the parameter, check [pygruenbeck_cloud](https://github.com/p0l0/pygruenbeck_cloud?tab=readme-ov-file#available-configuration-parameter) for available parameters.<br/>`value`: New value to be set |
| get_device_salt_measurements  | Returns a list with the salt measurement for each day since startup   | None                                                                                                                                                                                                                        |
| get_device_water_measurements | Returns a list with the water measurement for each day since startup  | None                                                                                                                                                                                                                        |
| regenerate                    | Starts a manual regeneration                                          | None                                                                                                                                                                                                                        |


# Installation
## HACS (Recommended)
This is currently not an official HACS integration and repository needs to be added to HACS.

Assuming you have already installed and configured HACS, follow these steps:

1. Navigate to the HACS integrations page
2. Choose Integrations under HACS
3. Click on the three small dots in the upper right corner and select `Custom repositories` and add this URL:
```bash
https://github.com/p0l0/hagruenbeck_cloud/
```
4. Click the '+' button on the bottom of the page
5. Search for "Grünbeck Cloud", choose it, and click install in HACS
6. Ready! Now continue with the configuration.

# Configuration

## Through the interface
1. Navigate to `Settings > Devices & Services` and then click `Add Integration`
2. Search for `Grünbeck Cloud`
4. Enter your credentials for the Grünbeck Cloud

## Energy/Water Dashboard

To get the real water consumption (at least for most people in Germany), you need to create a template sensor with the following calculation (replace the sensor names with your actual entity names):

```yaml
template:
  - sensor:
      - name: "Total Water Usage"
        unit_of_measurement: L
        icon: mdi:water-pump
        state_class: total_increasing
        device_class: water
        state: >
          {%- set soft_water = states('sensor.<device_name>_soft_water') | float(0) -%}
          {%- set raw_water = states('sensor.<device_name>_raw_water') | float(0) -%}
          {%- set soft_water_quantity = states('sensor.<device_name>_soft_water_quantity') | float(0) -%}
          {%- if (is_number(soft_water_quantity) and (soft_water_quantity > 1)) and (is_number(raw_water) and (raw_water > 1)) and (is_number(soft_water) and (soft_water > 1)) -%}
            {%- set water_usage = ((soft_water*soft_water_quantity)/(raw_water-soft_water)+soft_water_quantity) | round(4) | float(unavailable) -%}
            {%- if is_number(water_usage) -%}
              {{water_usage}}
            {%- endif -%}
          {%- endif -%}
```

> [!NOTE]
> For **SL/SD** series: `sensor.<device_name>_soft_water_quantity` is not pushed via WebSocket on every change — to avoid overloading the Grünbeck Cloud API it is refreshed every 360 seconds.
>
> For **SE** series: all data is polled every 60 seconds using a stateless HTTP cycle.

If you get an error about missing statistics, it's because the entity needs to collect some data first — it will resolve itself after a while.

__REMEMBER__: _Entity names use translation, so they will have a different name if you are not using English._

# LED Ring

If you have a Grünbeck model with an LED ring, the communication between the integration and the Grünbeck cloud is considered as "operation by user". You should configure the ring to only be active _in case of failure_ to avoid the ring being permanently lit.

# Known Issues

If you change the operation mode and nothing changes, check if the app shows the message _"The mode of operation will be changed after next regeneration"_ when you try to change the operation mode there. It is currently not possible to identify this state via the API.

Water hardness unit is currently hardcoded to be shown in HA as °dH — it is only a display suffix and no recalculation is done if you have a different unit configured.

# Legal notice
This is a personal project and isn't in any way affiliated with, sponsored or endorsed by [Grünbeck](https://www.gruenbeck.com/).

All product names, trademarks and registered trademarks in (the images in) this repository, are property of their respective owners. All images in this repository are used by the project for identification purposes only.
