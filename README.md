# buienalarm-sensor-homeassistant
Buienalarm custom_component for Home-Assistant

```
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

values for next_rain_forecast can be:
 - -1 No rain forecast withing timeframe
 - 0 It is currently raining
 - N Rain is forecast within N minutes
