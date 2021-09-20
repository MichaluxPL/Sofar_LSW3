# SOFAR Inverter
Small utility to read data from SOFAR K-TLX inverters through the Solarman (WLS-3) datalogger. Tested with logger S/N 17xxxxxxx (protocol V5).
File SOFARMap.xml contains MODBUS inverter's registers mapping for Sofar Solar K-TLX product line.

REMARK: To make it work with other inverter brand/model connected via WLS-3 you need to alter the .xml file accordingly + change pini and pfin values in the InverterData.py to point the variable position start/end.

*Thanks to @jlopez77 https://github.com/jlopez77 for 99% of the code.*

# Configuration

Edit the config.cfg and enter the following data:
```
[SofarInverter]
inverter_ip=X.X.X.X
inverter_port=8899
inverter_sn=17XXXXXXXX
mqtt=0  # set to 1 for MQTT output, 0 for JSON output.
mqtt_server=X.X.X.X
mqtt_port=1883
mqtt_topic=XXXXXXXXXXXX
mqtt_username=
mqtt_passwd=
lang=PL/EN
```

# Run
```
python3 InverterData.py (or ./InverterData.py)

{
    "Inverter status": "Normal",
    "Fault 1": 0,
    "Fault 2": 0,
    "Fault 3": 0,
    "Fault 4": 0,
    "Fault 5": 0,
    "PV1 Voltage (V)": 463.8,
    "PV1 Current (A)": 1.06,
    "PV2 Voltage (V)": 80.3,
    "PV2 Current (A)": 0.0,
    "PV1 Power (W)": 480,
    "PV2 Power (W)": 0,
    "Output active power (kW)": 0.44,
    "Output reactive power (kVar)": -0.66,
    "Grid frequency (Hz)": 50.0,
    "L1 Voltage (V)": 242.0,
    "L1 Current (A)": 1.12,
    "L2 Voltage (V)": 241.1,
    "L2 Current (A)": 1.12,
    "L3 Voltage (V)": 242.3,
    "L3 Current (A)": 1.13,
    "Total production (kWh)": 265,
    "Total generation time (h)": 214,
    "Today production (kWh)": 0.07,
    "Today generation time (min)": 81,
    "Inverter module temperature (ºC)": 26,
    "Inverter inner termperature (ºC)": 43,
    "Inverter bus vultage (V)": 658.0,
    "PV1 voltage sample by slave CPU (V)": 463.0,
    "PV1 current sample by slave CPU (A)": 80.5,
    "Countdown time (s)": 60,
    "Inverter alert message": 0,
    "Input mode": 1,
    "Communication Board inner message": 0,
    "Insulation of PV1+ to ground": 1373,
    "Insulation of PV2+ to ground": 2389,
    "Insulation of PV- to ground": 1920,
    "Country": "Poland",
    "String 1 voltage (V)": 11.2,
    "String 1 current (A)": 24.11,
    "String 2 voltage (V)": 11.2,
    "String 2 current (A)": 24.23,
    "String 3 voltage (V)": 11.3,
    "String 3 current (A)": 0.0,
    "String 4 voltage (V)": 26.5,
    "String 4 current (A)": 0.0,
    "String 5 voltage (V)": 21.4,
    "String 5 current (A)": 0.07,
    "String 6 voltage (V)": 8.1,
    "String 6 current (A)": 0.26,
    "String 7 voltage (V)": 4.3,
    "String 7 current (A)": 65.8,
    "String 8 voltage (V)": 463.0,
    "String 8 current (A)": 8.05
}
```

# Known Issues
Haven't found any so far ;-)

# Contrib
Feel free to suggest, rewrite or add whatever you feel is necessary.

# Home Assistant support (by jlopez77)
MQTT support into Home Assistant:

```
  - platform: mqtt
    name: "SofarInverter"
    state_topic: "mqtt_topic"
    unit_of_measurement: "W"
    json_attributes_topic: "mqtt_topic/attributes"
```
