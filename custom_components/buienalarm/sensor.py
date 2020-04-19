"""Support for Buienalarm weather service."""
# import asyncio
# from datetime import datetime, timedelta
# import time
import logging
import json

# import async_timeout
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_LATITUDE, CONF_LONGITUDE, CONF_MONITORED_CONDITIONS,
    CONF_NAME, TEMP_CELSIUS)
# from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
# from homeassistant.helpers.event import async_track_point_in_utc_time
# from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


DEFAULT_TIMEFRAME = 60


SENSOR_TYPES = {
    'temperature': ['Temperature', TEMP_CELSIUS, 'mdi:thermometer'],
    'precipitation': ['Precipitation', 'mm/h', 'mdi:weather-pouring'],
    'precipitation_forecast_average': ['Precipitation forecast average',
                                       'mm/h', 'mdi:weather-pouring'],
    'precipitation_forecast_total': ['Precipitation forecast total',
                                     'mm', 'mdi:weather-pouring'],
    'next_rain_forecast': ['Next rain forecast', 'minutes', 'mdi:weather-pouring']
}

CONF_TIMEFRAME = 'timeframe'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_MONITORED_CONDITIONS,
                 default=['precipitation']): vol.All(
                     cv.ensure_list, vol.Length(min=1),
                     [vol.In(SENSOR_TYPES.keys())]),
    vol.Inclusive(CONF_LATITUDE, 'coordinates',
                  'Latitude and longitude must exist together'): cv.latitude,
    vol.Inclusive(CONF_LONGITUDE, 'coordinates',
                  'Latitude and longitude must exist together'): cv.longitude,
    vol.Optional(CONF_TIMEFRAME, default=60):
        vol.All(vol.Coerce(int), vol.Range(min=5, max=120)),
    vol.Optional(CONF_NAME, default='ba'): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up Buienalarm."""

    # import buienalarm
    from buienalarm.pybuienalarm import Buienalarm

    latitude = config.get(CONF_LATITUDE, hass.config.latitude)
    longitude = config.get(CONF_LONGITUDE, hass.config.longitude)
    timeframe = config.get(CONF_TIMEFRAME, DEFAULT_TIMEFRAME)

    if None in (latitude, longitude):
        _LOGGER.error("Latitude or longitude not set in HomeAssistant config")
        return False

    b = Buienalarm(lon=longitude, lat=latitude, timeframe=timeframe)

    dev = []

    for sensor in config[CONF_MONITORED_CONDITIONS]:
        dev.append(BaSensor(b, sensor, timeframe, config.get(CONF_NAME)))

    add_entities(dev)


class BaSensor(Entity):
    """Representation of Buienalarm."""

    def __init__(self, ba_data, sensor_type, timeframe, client_name):
        """Initialize the sensor."""
        self.client_name = client_name
        self._name = SENSOR_TYPES[sensor_type][0]
        self.type = sensor_type
        self.buienalarm = ba_data
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format(self.client_name, self._name)

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return icon."""
        return self._icon

    def update(self):
        """Update buienalarm data."""
        if self.type == 'temperature':
            self._state = self.buienalarm.get_temperature()

        elif self.type == 'precipitation':
            self._state = self.buienalarm.get_precipitation_now()

        elif self.type == 'precipitation_forecast_total':
            self._state = self.buienalarm.get_precipitation_forecast_total()

        elif self.type == 'precipitation_forecast_average':
            self._state = self.buienalarm.get_precipitation_forecast_average()

        elif self.type == 'next_rain_forecast':
            p_forecast = json.loads(self.buienalarm.get_forecast())
            next_rain_minutes = -1
            periods = 0
            for precip in p_forecast:
                periods += 1
                if precip > 0:
                    next_rain_minutes = 5*periods
                    break
            self._state = next_rain_minutes
