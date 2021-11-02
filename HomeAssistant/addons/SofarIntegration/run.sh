#!/usr/bin/bashio
set -e

echo Sofar Integration in run!
cfgpath=./Sofar_LSW3
[ ! -d $cfgpath ] && (echo "No repo in DockerImage -cloning marm..."; rm -Rf $cfgpath; git clone https://github.com/rysiulg/Sofar_LSW3.git  $cfgpath;)
#[ ! -d $cfgpath ] && (echo "No repo in DockerImage -cloning github..."; rm -Rf $cfgpath; git clone https://github.com/MichaluxPL/Sofar_LSW3.git  $cfgpath;)
ls -la 
prometheus=$(bashio::config 'prometheus')
[ "$prometheus" = "true" ] && prometheus="1" || prometheus="0"
influxdb=$(bashio::config 'influxdb')
[ "$influxdb" = "true" ] && influxdb="1" || influxdb="0"
mqtt=$(bashio::config 'mqtt')
[ "$mqtt" = "true" ] && mqtt="1" || mqtt="0"
mqtt_tls=$(bashio::config 'mqtt_tls')
[ "$mqtt_tls" = "true" ] && mqtt_tls="1" || mqtt_tls="0"
mqtt_tls_insecure=$(bashio::config 'mqtt_tls_insecure')
[ "$mqtt_tls_insecure" = "true" ] && mqtt_tls_insecure="1" || mqtt_tls_insecure="0"
echo "[SofarInverter]" >$cfgpath/config.cfg
echo "inverter_ip=$(bashio::config 'inverter_ip')" >>$cfgpath/config.cfg
echo "inverter_port=$(bashio::config 'inverter_port')" >>$cfgpath/config.cfg
echo "inverter_sn=$(bashio::config 'inverter_sn')" >>$cfgpath/config.cfg
echo "register_start1=$(bashio::config 'register_start1')" >>$cfgpath/config.cfg
echo "register_end1=$(bashio::config 'register_end1')" >>$cfgpath/config.cfg
echo "register_start2=$(bashio::config 'register_start2')" >>$cfgpath/config.cfg
echo "register_end2=$(bashio::config 'register_end2')" >>$cfgpath/config.cfg
echo "registerhw_start=$(bashio::config 'registerhw_start')" >>$cfgpath/config.cfg
echo "registerhw_end=$(bashio::config 'registerhw_end')" >>$cfgpath/config.cfg
echo "lang=$(bashio::config 'lang')" >>$cfgpath/config.cfg
echo "verbose=$(bashio::config 'verbose')" >>$cfgpath/config.cfg
echo "[Prometheus]" >>$cfgpath/config.cfg
echo "prometheus=$prometheus" >>$cfgpath/config.cfg
echo "prometheus_file=" >>$cfgpath/config.cfg
echo "[InfluxDB]" >>$cfgpath/config.cfg
echo "influxdb=$influxdb" >>$cfgpath/config.cfg
echo "influxdb_host=$(bashio::config 'influxdb_host')" >>$cfgpath/config.cfg
echo "influxdb_port=$(bashio::config 'influxdb_port')" >>$cfgpath/config.cfg
echo "influxdb_user=$(bashio::config 'influxdb_user')" >>$cfgpath/config.cfg
echo "influxdb_password=$(bashio::config 'influxdb_password')" >>$cfgpath/config.cfg
echo "influxdb_dbname=$(bashio::config 'influxdb_dbname')" >>$cfgpath/config.cfg
echo "[MQTT]" >>$cfgpath/config.cfg
echo "mqtt=$mqtt" >>$cfgpath/config.cfg
echo "mqtt_server=$(bashio::config 'mqtt_server')" >>$cfgpath/config.cfg
echo "mqtt_port=$(bashio::config 'mqtt_port')" >>$cfgpath/config.cfg
echo "mqtt_topic=$(bashio::config 'mqtt_topic')" >>$cfgpath/config.cfg
echo "mqtt_username=$(bashio::config 'mqtt_username')" >>$cfgpath/config.cfg
echo "mqtt_passwd=$(bashio::config 'mqtt_password')" >>$cfgpath/config.cfg
echo "mqtt_tls=$mqtt_tls" >>$cfgpath/config.cfg
echo "mqtt_tls_insecure=$mqtt_tls_insecure" >>$cfgpath/config.cfg
echo "mqtt_tls_version=$(bashio::config 'mqtt_tls_version')" >>$cfgpath/config.cfg
echo "mqtt_cacert=$(bashio::config 'mqtt_cacert')" >>$cfgpath/config.cfg
#cat $cfgpath/config.cfg
update_time_sec=$(bashio::config 'update_time_sec')
watch -n $update_time_sec python3 $cfgpath/InverterData.py


