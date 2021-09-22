# SOFAR Inverter
Small utility to read data from SOFAR K-TLX inverters through the Solarman (WLS-3) datalogger. Tested with logger S/N 17xxxxxxx and 21xxxxxxx (protocol V5).

REMARK: To make it work with other inverter brand/model connected via WLS-3 you need to alter the .xml file accordingly + change pini and pfin values in the InverterData.py to point the register's position start/end.

*Thanks to @jlopez77 https://github.com/jlopez77 for 90% of the code.*

# Configuration

Edit the config.cfg and enter the following data:
```
[SofarInverter]
inverter_ip=X.X.X.X             # data logger IP
inverter_port=8899              # data logger port
inverter_sn=XXXXXXXXXX          # data logger S/N
mqtt=1                          # set to 1 for MQTT output, 0 for JSON output.
mqtt_server=192.168.X.X
mqtt_port=1883
mqtt_topic=XXXXXXXXXXXX
mqtt_username=
mqtt_passwd=
lang=PL/EN                      # Output language
prometheus=0                    # 1 to export data in Prometheus metrics format
prometheus_file=/xx/xx/metrics/index.html  # Path to Prometheus metrics file
verbose=0                       # 1 for additional info to be presented (registers, binary packets)

File SOFARMap.xml contains MODBUS inverter's registers mapping for Sofar Solar K-TLX
product line and Prometheus metrics configuration.
Edit to get i.e. different language, other Prometheus metrics names or
if Your inverter has different register's numbers.
```

# Run

```
bash:/python3 InverterData.py (or ./InverterData.py)

{
    "Inverter status": "Normal",
    "Fault 1": 0,
    "Fault 2": 0,
    "Fault 3": 0,
    "Fault 4": 0,
    "Fault 5": 0,
    "PV1 Voltage (V)": 403.7,
    "PV1 Current (A)": 0.14,
    "PV2 Voltage (V)": 78.9,
    "PV2 Current (A)": 0.0,
    "PV1 Power (W)": 50,
    "PV2 Power (W)": 0,
    "Output active power (W)": 20,
    "Output reactive power (kVar)": -0.65,
    "Grid frequency (Hz)": 49.98,
    "L1 Voltage (V)": 241.8,
    "L1 Current (A)": 0.93,
    "L2 Voltage (V)": 240.4,
    "L2 Current (A)": 0.91,
    "L3 Voltage (V)": 240.4,
    "L3 Current (A)": 0.93,
    "Total production (kWh)": 297,
    "Total generation time (h)": 249,
    "Today production (kWh)": 14010.0,
    "Today generation time (min)": 679,
    "Inverter module temperature (ºC)": 29,
    "Inverter inner termperature (ºC)": 45,
    "Inverter bus voltage (V)": 655.8,
    "PV1 voltage sample by slave CPU (V)": 402.6,
    "PV1 current sample by slave CPU (A)": 79.1,
    "Countdown time (s)": 60,
    "Inverter alert message": 0,
    "Input mode": 1,
    "Communication Board inner message": 0,
    "Insulation of PV1+ to ground": 1379,
    "Insulation of PV2+ to ground": 2387,
    "Insulation of PV- to ground": 1917,
    "Country": "Poland",
    "String 1 voltage (V)": 9.3,
    "String 1 current (A)": 24.04,
    "String 2 voltage (V)": 9.1,
    "String 2 current (A)": 24.04,
    "String 3 voltage (V)": 9.3,
    "String 3 current (A)": 0.0,
    "String 4 voltage (V)": 29.7,
    "String 4 current (A)": 0.0,
    "String 5 voltage (V)": 24.9,
    "String 5 current (A)": 14.01,
    "String 6 voltage (V)": 67.9,
    "String 6 current (A)": 0.29,
    "String 7 voltage (V)": 4.5,
    "String 7 current (A)": 65.58,
    "String 8 voltage (V)": 402.6,
    "String 8 current (A)": 7.91
}
```

# Known Issues
You tell me :)

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
# Prometheus support (by Michalux).
```
In order to enable Prometheus support:
    1. Configure prometheus options in config.cfg
    2. Serve prometheus metrics file using any web server (name it index.html to be the default page in configured path)
    3. Configure prometheus target to access the file 
```
