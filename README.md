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
```
