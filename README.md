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

Your sensors default name will be `sensor.buienalarm_{monitored_condition}`.

You can provide a timeframe: Minutes to look ahead for precipitation forecast (min: 5 / max: 120) - Default value: 60

values for next_rain_forecast can be:

- Unknown: No rain forecast within timeframe
- 0: It is currently raining
- N: Rain is forecasted within N minutes


## Next rain forecast in minutes

The `buienalarm_next_rain_forecast` sensor returns a date/time of the next rain forecast. To get the time-in-minutes to the next rain forecast a template sensor can be used. Add this template sensor to your configuration:

```yaml
template:
  - sensor:
    - name: "Buienalarm Next rain forecast (min)"
      unit_of_measurement: "min"
      state: >
        {% if as_timestamp(states('sensor.buienalarm_next_rain_forecast')) %}
          {{ ( ( as_timestamp(states('sensor.buienalarm_next_rain_forecast')) - as_timestamp(now()) ) / 60 ) | round }}
        {% else %}
          {{ states('nonexistent') }}
        {% endif %}
```
