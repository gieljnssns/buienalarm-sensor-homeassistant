"""Support for Buienalarm weather service."""

from datetime import timedelta
from typing import NamedTuple
import logging

from homeassistant.const import (
    TEMP_CELSIUS,
    LENGTH_MILLIMETERS,
    TIME_MINUTES,
)

SensorType = NamedTuple(
    "SensorType",
    [
        ("name", str),
        ("unit", str),
        ("icon", str),
    ])


LOGGER = logging.getLogger(__package__)
UPDATE_INTERVAL = timedelta(seconds=300)
ATTRIBUTION = "Data provided by Buienalarm B.V."
DEFAULT_TIMEFRAME = 60
DEFAULT_NAME = "ba"
ITEM_TEMP = "temperature"
ITEM_PRECIP_NOW = "precipitation"
ITEM_PRECIP_FORECAST_AVG = "precipitation_forecast_average"
ITEM_PRECIP_FORECAST_TOTAL = "precipitation_forecast_total"
ITEM_NEXT_RAIN_FORECAST = "next_rain_forecast"
SENSOR_TYPES = {
    ITEM_TEMP: SensorType(
        "Temperature",
        TEMP_CELSIUS,
        "mdi:thermometer"),
    ITEM_PRECIP_NOW: SensorType(
        "Precipitation",
        LENGTH_MILLIMETERS + "/h",
        "mdi:weather-pouring"),
    ITEM_PRECIP_FORECAST_AVG: SensorType(
        "Precipitation forecast average",
        LENGTH_MILLIMETERS + "/h",
        "mdi:weather-pouring"),
    ITEM_PRECIP_FORECAST_TOTAL: SensorType(
        "Precipitation forecast total",
        LENGTH_MILLIMETERS,
        "mdi:weather-pouring"),
    ITEM_NEXT_RAIN_FORECAST: SensorType(
        "Next rain forecast",
        TIME_MINUTES,
        "mdi:weather-pouring"),
}
CONF_TIMEFRAME = "timeframe"
CONF_CONDITION_PRECIPITATION = "precipitation"
