# SOFAR Inverter + LSW-3/LSE
Small utility to read data from SOFAR K-TLX inverters through the Solarman (LSW-3/LSE) datalogger. 
Two scripts to get inverter's statistics and hardware info.
Tested with logger S/N 17xxxxxxx and 21xxxxxxx (protocol V5).
Requires python3 to run.

REMARK: To make it work with other inverter brand/model connected via LSW-3/LSE you might need to alter
the register's addresses in the .xml files accordingly and change register start/end numbers in config.cfg

*Thanks to @jlopez77 https://github.com/jlopez77 for logger/MODBUS protocol code.*

# Required python modules
To run, script requires following python modules:
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

[Prometheus]
prometheus=0                    # set to 1 to export data in Prometheus metrics format
prometheus_file=/xx/xx/metrics/index.html  # Path to Prometheus metrics file served by web server

[InfluxDB]
influxdb=0                      # set to 1 to export data to InfluxDB
influxdb_host=                  # InfluxDB host (i.e. 127.0.0.1)
influxdb_port=8086              # InfluxDB port
influxdb_user=                  # InfluxDB user with permisions to read/write from/to dbname
influxdb_password=              # User password
influxdb_dbname=                # Database name 

[MQTT]
mqtt=0                          # 0: disabled, 1: enabled
mqtt_server=                    # MQTT server IP address
mqtt_port=1883                  # MQTT server tcp port
mqtt_topic=                     # MQTT topic name
mqtt_username=                  # MQTT access username
mqtt_passwd=                    # MQTT user password
mqtt_tls=0                      # Set to 1 to enable TLS support
mqtt_tls_insecure=True          # Set to False to enable strict server's certificate hostname matching
mqtt_tls_version=2              # 1 or 2
mqtt_cacert=                    # CA certificate path/filename

[Domoticz]
domoticz_support=0              # 0: disabled, 1: enabled

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

# MQTT Support (Domoticz compatible)
```
    1. JSON_attributes_topic (unless Domoticz support enabled !): "mqtt_topic/attributes"
    2. For TLS support You'll need at least CA Certificate and TLS enabled MQTT
       To enable TLS for Mosquitto look i.e here: http://www.steves-internet-guide.com/mosquitto-tls/
    3. To turn Domoticz support on:
       a) enable it in config.cfg
       b) set mqtt_topic=domoticz/in in config.cfg
       c) create virtual devices in Domoticz (write down their idx numbers)
       d) in SOFARMap.xml find corresponding variables and for each input idx number
       e) leave "DomoticzIdx":0 for variables You don't want to send data to Domoticz
       WARNING: When enabled, Domoticz support disables normal MQTT message delivery (all values in one message).
    3. Tested with Mosquitto MQTT server (both with and without TLS) and Domoticz 2021.1
```
# Prometheus+Grafana support
```
Steps to run Prometheus+Grafana support:
    1. Configure prometheus options in config.cfg
    2. Serve prometheus metrics file using any web server (name it index.html to be the default page in configured path)
    3. Configure prometheus target to access the file 
    4. Add Prometheus datasource in Grafana
    5. Import grafana_en/pl.json file (Dashboards->Manage->Import).
    Enjoy :)
```
# InfluxDB+Grafana support
```
Steps to run InfluxDB+Grafana support:
    1. Configure InfluxDB options in config.cfg
    2. Create database to store inverter data in InfluxDB (i.e. create database Data)
    3. Add InfluxDB datasource in Grafana (name it InfluxDB)
    4. Import grafana_iflux_en/pl.json file (Dashboards->Manage->Import).
    Enjoy :)
```
