# buienalarm-sensor-homeassistant

Buienalarm custom_component for Home-Assistant

```yaml
sensor:
  - platform: buienalarm
    timeframe: 15
    name: buienalarm
    monitored_conditions:
      - temperature
      - precipitation
      - precipitation_forecast_average
      - precipitation_forecast_total
      - next_rain_forecast
```

Your sensors default name will be sensor.ba_{monitored_condition}

You can provide a timeframe: Minutes to look ahead for precipitation forecast (min: 5 / max: 120) - Default value: 60

values for next_rain_forecast can be:

- -1 No rain forecast withing timeframe
- 0 It is currently raining
- N Rain is forecast within N minutes
