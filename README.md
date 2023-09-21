# SOFAR Inverter + LSW-3/LSE
Small utility to read data from SOFAR K-TLX inverters through the Solarman (LSW-3/LSE) datalogger. 
Two scripts to get inverter's statistics and hardware info.
Tested with logger S/N 17xxxxxxx and 21xxxxxxx (protocol V5).
Requires python3 to run.

REMARK: To make it work with other inverter brand/model connected via LSW-3/LSE you might need to alter
the register's addresses in the .xml files accordingly and change register start/end numbers in config.cfg

*Thanks to @jlopez77 https://github.com/jlopez77 for logger/MODBUS protocol code.*
*Thanks to @pablolite for HomeAssistant initial code.*

# Required python modules
```
libscrc
paho-mqtt
influxdb
```
# Configuration

Edit the config.cfg and enter the following data:
```
[SofarInverter]
inverter_ip=X.X.X.X             # data logger IP
inverter_port=8899              # data logger port
inverter_sn=XXXXXXXXXX          # data logger S/N
register_start1=0x0000          # Inverter register's first MODBUS address for the first register's range.
register_end1=0x0027            # Inverter register's last MODBUS address for the first register's range
register_start2=0x0105          # Inverter register's first MODBUS address for a second register's range
register_end2=0x0114            # Inverter register's last MODBUS address for a second register's range
registerhw_start=0x2000         # Like above, but for InverterHWData.py
registerhw_end=0x200D           # Like above, but for InverterHWData.py
lang=                           # Output language (available: PL,EN)
verbose=0                       # Set to 1 for additional info to be presented (registers, binary packets etc.)
debug=0                         # Set to 1 to log additional debug data to a log file
log_file=InverterData.log       # Log file name with a path

[Prometheus]
prometheus=0                    # set to 1 to export data in Prometheus metrics format
prometheus_file=/xx/xx/metrics/index.html  # Path to Prometheus metrics file served by web server

[InfluxDB]
influxdb=0                      # set to 1 to export data to InfluxDB
influxdb_url=http://x.x.x.x:8086 #InfluxDB server access URL
influxdb_bucket=SolarData       # InfluxDB bucket to store Inverter's data
influxdb_org=                   # InfluxDB organization
influxdb_token=                 # InfluxDB access token

[InfluxDB]
influxdb_host=                  # InfluxDB host (i.e. 127.0.0.1)
influxdb_port=8086              # InfluxDB port
influxdb_user=                  # InfluxDB user with permisions to read/write from/to dbname
influxdb_password=              # User password
influxdb_dbname=                # Database name 

[MQTT]
mqtt=0                          # 0: disabled, 1: enabled
mqtt_server=                    # MQTT server IP address
mqtt_port=1883                  # MQTT server tcp port
mqtt_topic=                     # MQTT topic name for basic output
mqtt_username=                  # MQTT access username
mqtt_passwd=                    # MQTT user password
mqtt_tls=0                      # Set to 1 to enable TLS support
mqtt_tls_insecure=True          # Set to False to enable strict server's certificate hostname matching
mqtt_tls_version=2              # 1 or 2
mqtt_cacert=                    # CA certificate path/filename
mqtt_basic=0                    # 0: disabled, 1: enabled (basic output to MQTT - all values in one message)

[Domoticz]
domoticz_support=0              # 0: disabled, 1: enabled
domoticz_topic=                 # MQTT topic name for Domoticz integration

[HomeAssistant]
homeassistant_support=0         # 0: disabled, 1: enabled
homeassistant_topic=            # MQTT topic name for HomeAssistant integration

Files SOFARMap.xml and SOFARHWMap.xml contain MODBUS inverter's registers mapping for Sofar Solar K-TLX product line
and Prometheus/InfluxDB metrics configuration.
Edit i.e. to get captions in a different language, change Prometheus/InfluxDB metrics names or
if Your inverter has different register's numbers.
Example SOFARMap.xml structure and fields definition (similar for SOFARHWMap.xml):
"directory": "solar",               # Id
    "items": [
      {
        "titleEN": "PV1 Power",     # English JSON output name 
        "titlePL": "Moc PV1",       # Polish JSON output name
        "registers": ["0x000A"],    # Inverter's register address (must be in range configured in the config file)
        "DomoticzIdx": 0,           # Domoticz virtual device idx number (for Domoticz support)
        "optionRanges": [],         # For numeric value to text label mappings
        "ratio": 10,                # Value ratio (will be used to multiply response value)
        "unit": "W",                # Value unit
        "graph": 1,                 # Set to 1, to export value to Prometheus/InfluxDB
        "metric_type": "gauge",     # Prometheus metric type
        "metric_name": "SolarPower",# Prometheus/InfluxDB container name
        "label_name": "Power",      # Prometheus/InfluxDB label name
        "label_value": "PV1"        # Prometheus/InfluxDB value name
      }
```
# Run

```
bash:/python3 InverterData.py  (or ./InverterData.py)
{
    "Inverter status": "Normal",
    "Fault 1": "No error",
    "Fault 2": "No error",
    "Fault 3": "No error",
    "Fault 4": "No error",
    "Fault 5": "No error",
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
    "Inverter inner temperature (ºC)": 45,
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
bash:/python3 /InverterHWData.py (or ./InverterHWData.py)
{
    "Product code": "5kW",
    "Serial Number": "SXXXXXXXXXXX",
    "Software Version": "V270",
    "Hardware Version": "V100",
    "DSP Version": "V270"
}
```
# Known Issues
You tell me :)

# Contrib
Feel free to suggest :)
If You want to rewrite or/add change anything - please fork Your own project.

# FAQ
```
Q: I get "No value in response for register 0x0001"
A: Most probable causes for this: 
  a) Your Inverter keeps it's production data in a different registers than current default.
     What You can do is:
     1. Contact inverter's manufacturer to get register's specification (MODBUS specification).
     2. Play around with different register ranges
  b) Response from a logger is too short, so it does not contain the actual data
     Correct response should look something like this:
     b'\xa5c\x00\x10\x15\x00%l\x90Pi\x02\x014\x92R7(\x19\x00\x00\xc6\x9b\x17+\x01\x03P\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11y\x00\xd8\x03$\x00\x00\x00`\x00\x00\x00Y\xff\xc0\x13\x86\tq\x00\x9a\tN\x00\x9b\t\x81\x00\x9a\x00\x00\x07\xcb\x00\x00\t\x86\x00\x8c\x00\xa8\x00\x1d\x00,\x19\xcd\x11g\x032\x00<\x00\x00\x00\x01\x00\x00\x05M\t\x97\x07\xb9\x00\x0c\x98I\xff\x15'

Q: I've changed register's numbers in config.cfg, but received data does not match parameter's names
A: You have to update those numbers in SOFARMap.xml to match parameter's names.
   Important: Changing register's numbers may require some fix in the code for values kept in more than one register (i.e. 2 byte values)

Q: Sometimes I get wrong values (i.e. negative)
A: Unfortunately logger is not bug free :( so it can happen from time to time.
```

# MQTT Support
```
    1. To enable set all variables in MQTT section in config.cfg
    2. For MQTT TLS support You'll need at least CA Certificate and TLS enabled MQTT
       To enable TLS for Mosquitto look i.e here: http://www.steves-internet-guide.com/mosquitto-tls/
    3. If You want basic MQTT message output (all values in one message) - set mqtt_basic=1
    4. Tested with Mosquitto MQTT server (both with and without TLS)
    5. Configuration also required by Domoticz and HomeAssistant support
```
# Domoticz (via MQTT) Support
```
    1. Requires MQTT configuration in config.cfg (see section MQTT Support)
    2. To turn Domoticz support on:
       a) enable it in config.cfg
       b) set domoticz_mqtt_topic=domoticz/in in config.cfg
       c) create virtual devices in Domoticz (write down their idx numbers)
       d) in SOFARMap.xml find corresponding variables and for each input idx number
       e) leave "DomoticzIdx":0 for variables You don't want to send data to Domoticz
    3. Tested with Domoticz 2021.1
```
# HomeAssistant (via MQTT) Support
```
    1. Requires MQTT configuration in config.cfg (see section MQTT Support)
    2. To turn HomeAssistant support on:
        a) enable it in config.cfg
        b) set ha_mqtt_topic in config.cfg
    3. Hardcoded auto-discovery MQTT topic name: homeassistant/sensor/SofarLogger/{Inverter's SN}_ID/config
    4. Code prepared/tested by @pablolite, optimized by Michalux
```
# Prometheus+Grafana support
```
Steps to run Prometheus+Grafana support:
    1. Configure prometheus options in config.cfg
    2. Serve prometheus metrics file using any web server (name it index.html to be the default page in configured path)
    3. Configure prometheus target to access the file 
    4. Add Prometheus datasource in Grafana
    5. Import grafana_en/pl.json file (Dashboards->Manage->Import).
```
# InfluxDB+Grafana support
```
Steps to run InfluxDB+Grafana support:
    1. Configure InfluxDB options in config.cfg
    2. Create database to store inverter data in InfluxDB (i.e. create database Data)
    3. Add InfluxDB datasource in Grafana (name it InfluxDB)
    4. Import grafana_iflux_en/pl.json file (Dashboards->Manage->Import).
    Important: From version 1.9 the script requires InfluxDB v2.x
```
Enjoy :)
