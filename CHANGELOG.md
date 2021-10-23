# Change Log
Get Sofart Inverter's data from solarman logger.
Tested with LSW-3 (SN 17xxxxxxx, 21xxxxxx)
 
## [1.0] - 2021-09-22
Clone whole project from github and put in crontab to run in intervals.

### Added
1. Sofar Inverter support.
2. Language support (Polish, English).
3. Cleaned SOFARMap.xml file.
 
### Changed
 
### Fixed

## [1.1] - 2021-09-23
To upgrade overwrite all previous project files.
To use prometheus+graphana support:
1. Configure prometheus options in config.cfg
2. Serve prometheus metrics file using any web server (name it index.html to be the default page in configured path)
3. Configure prometheus target to access the file
4. Add Prometheus datasource in Grafana
5. Import grafana_en/pl.json file (Dashboards->Manage->Import).
Enjoy :)

### Added
1. Prometheus + grafana support.
2. Verbose mode.
 
### Changed
 
### Fixed
1. 4-byte values (Total production, Total generation time) calculated correctly.

## [1.2] - 2021-09-29
To upgrade overwrite all previous project files.
To use prometheus+graphana support:
1. Configure prometheus options in config.cfg
2. Serve prometheus metrics file using any web server (name it index.html to be the default page in configured path)
3. Configure prometheus target to access the file
4. Add Prometheus datasource in Grafana
5. Import grafana_en/pl.json file (Dashboards->Manage->Import).

To use InfluxDB support:
1. Install InfluxDB
2. Create database to store data (i.e: create database Data)
3. Configure InfluxDB options in config.cfg
4. Add InfluxDB datasource in Grafana (name it InfluxDB)
5. Import grafana_ifdb_en/pl.json file (Dashboards->Manage->Import).
Enjoy :)

### Added
1. InfluxDB support

### Changed

### Fixed
1. Totaltime and totalpower zeroed befor being sent to MQTT (thx to pablolite for pointing that one out)

## [1.21] - 2021-10-21
To upgrade overwrite all previous project files.

### Added

### Changed
1. Prometheus integration code (write to a file all data at once).
2. Script writes values to InfluxDB/Promtheus/MQTT only if inverter status is Normal.
   In other states values can be unreliable - especially when inverter is starting in the morning.
3. Grafana dashboard for InfluxDB datasource was changed and fixed in a few places.

### Fixed

## [1.3] - 2021-10-23
To upgrade overwrite all previous project files.

### Added
1. New script to read hardware/software/SN info from inverter.
   Two new files: InverterHWData.py (main script) and SOFARHWMap.xml (register configuration)

### Changed

### Fixed
