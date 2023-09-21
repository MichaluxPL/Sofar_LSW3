#!/usr/bin/python3
# Script gathering solar data from Sofar Solar Inverter (K-TLX) via logger module LSW-3/LSE
# by Michalux (based on DEYE script by jlopez77, HA initial code by pablolite).
# Version: 1.9
#

import sys
import socket
import binascii
import re
import libscrc
import json
import paho.mqtt.client as paho
import os
import configparser
import datetime
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def twosComplement_hex(hexval, reg):
  if hexval=="" or (" " in hexval):
    print("No value in response for register "+reg)
    print("Check register start/end values in config.cfg")
    sys.exit(1)
  bits = 16
  val = int(hexval, bits)
  if val & (1 << (bits-1)):
    val -= 1 << bits
  return val

# Prepare metrics for Prometheus
def PMetrics(mname, mtype, mlabel, mlvalue, pdata):
  line="# TYPE "+mname+" "+mtype+"\n"+mname+"{"+mlabel+"=\""+mlvalue+"\"} "+str(pdata)+"\n"
  PMData.append(line)

# Prepare data to write do InfluxDB
def PrepareInfluxData(IfData, fieldname, fieldvalue):
  IfData[0]["fields"][fieldname]=float(fieldvalue)
  return IfData

def Write2InfluxDB(IfData):
  influxdb_api.write(ifbucket, iforg, IfData)

def PrepareDomoticzData(DData, idx, svalue):
  if isinstance(svalue, str):
    DData.append('{ "idx": '+str(idx)+', "svalue": '+ svalue +' }')
  else:
    DData.append('{ "idx": '+str(idx)+', "svalue": "'+ str(svalue) +'" }')
  return DData

def Write2LogFile(log, text):
  log.write(localtimestamp+": "+text+"\n")

def WriteDebug(log, text):
  if debug=="1":
    log.write(localtimestamp+": "+text+"\n")

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# CONFIG
configParser = configparser.RawConfigParser()
configFilePath = r'./config.cfg'
configParser.read(configFilePath)

inverter_ip=configParser.get('SofarInverter', 'inverter_ip')
inverter_port=int(configParser.get('SofarInverter', 'inverter_port'))
inverter_sn=int(configParser.get('SofarInverter', 'inverter_sn'))
reg_start1=(int(configParser.get('SofarInverter', 'register_start1'),0))
reg_end1=(int(configParser.get('SofarInverter', 'register_end1'),0))
reg_start2=(int(configParser.get('SofarInverter', 'register_start2'),0))
reg_end2=(int(configParser.get('SofarInverter', 'register_end2'),0))
mqtt=int(configParser.get('MQTT', 'mqtt'))
mqtt_basic=configParser.get('MQTT', 'mqtt_basic')
mqtt_server=configParser.get('MQTT', 'mqtt_server')
mqtt_port=int(configParser.get('MQTT', 'mqtt_port'))
mqtt_topic=configParser.get('MQTT', 'mqtt_topic')
mqtt_username=configParser.get('MQTT', 'mqtt_username')
mqtt_passwd=configParser.get('MQTT', 'mqtt_passwd')
mqtt_tls=configParser.get('MQTT', 'mqtt_tls')
mqtt_tls_insecure=configParser.get('MQTT', 'mqtt_tls_insecure')
mqtt_tls_ver=int(configParser.get('MQTT', 'mqtt_tls_version'))
mqtt_cacert=configParser.get('MQTT', 'mqtt_cacert')
lang=configParser.get('SofarInverter', 'lang')
verbose=configParser.get('SofarInverter', 'verbose')
debug=configParser.get('SofarInverter', 'debug')
config_logfile=configParser.get('SofarInverter', 'log_file')
prometheus=configParser.get('Prometheus', 'prometheus')
prometheus_file=configParser.get('Prometheus', 'prometheus_file')
influxdb=configParser.get('InfluxDB', 'influxdb')
ifurl=configParser.get('InfluxDB', 'influxdb_url')
ifbucket=configParser.get('InfluxDB', 'influxdb_bucket')
iforg=configParser.get('InfluxDB', 'influxdb_org')
iftoken=configParser.get('InfluxDB', 'influxdb_token')
DomoticzSupport=configParser.get('Domoticz', 'domoticz_support')
domoticz_mqtt_topic=configParser.get('Domoticz', 'domoticz_mqtt_topic')
HomeAssistantSupport=configParser.get('HomeAssistant', 'homeassistant_support')
ha_mqtt_topic=configParser.get('HomeAssistant', 'ha_mqtt_topic')
# END CONFIG

timestamp=str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
localtimestamp=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

logfile = open(config_logfile, "a")

# Initialise InfluxDB support
if influxdb=="1":
  WriteDebug(logfile, "Initialising InfluxDB connection")
  ifclient = influxdb_client.InfluxDBClient(url=ifurl, token=iftoken, org=iforg)
  influxdb_api = ifclient.write_api(write_options=SYNCHRONOUS)
  InfluxData=[
    {
      "measurement": "InverterData",
      "time": timestamp,
      "fields": {}
    }
  ]

# PREPARE & SEND DATA TO THE INVERTER
output="{" # initialise json output
pini=reg_start1
pfin=reg_end1
chunks=0
totalpower=0
totaltime=0
PMData=[]
DomoticzData=[]
HomeAssistantData=[]
invstatus=1

# OPEN CONNECTION TO LOGGER
if verbose=="1": print("Connecting to logger... ", end='');
WriteDebug(logfile, "Opening connection to logger")
for res in socket.getaddrinfo(inverter_ip, inverter_port, socket.AF_INET, socket.SOCK_STREAM):
  family, socktype, proto, canonname, sockadress = res
  try:
    clientSocket=socket.socket(family, socktype, proto);
    clientSocket.settimeout(10);
    clientSocket.connect(sockadress);
  except socket.error as msg:
    print("Could not open socket - inverter/logger turned off");
    Write2LogFile(logfile, "Could not open socket - inverter/logger turned off")
    invstatus=0;

if verbose=="1" and invstatus==1:
  print("connected successfully !");
  WriteDebug(logfile, "Inverter connected successfully !")
if invstatus==1:
  while chunks<2:
    WriteDebug(logfile, "Gathering data from the inverter. Chunks loop nr: "+str(chunks+1))
    # Data frame begin
    start = binascii.unhexlify('A5') #start
    length=binascii.unhexlify('1700') # datalength
    controlcode= binascii.unhexlify('1045') #controlCode
    serial=binascii.unhexlify('0000') # serial
    datafield = binascii.unhexlify('020000000000000000000000000000') #com.igen.localmode.dy.instruction.send.SendDataField
    pos_ini=str(hex(pini)[2:4].zfill(4))
    pos_fin=str(hex(pfin-pini+1)[2:4].zfill(4))
    businessfield= binascii.unhexlify('0103' + pos_ini + pos_fin) # sin CRC16MODBUS
    crc=binascii.unhexlify(str(hex(libscrc.modbus(businessfield))[4:6])+str(hex(libscrc.modbus(businessfield))[2:4])) # CRC16modbus
    checksum=binascii.unhexlify('00') #checksum F2
    endCode = binascii.unhexlify('15')

    inverter_sn2 = bytearray.fromhex(hex(inverter_sn)[8:10] + hex(inverter_sn)[6:8] + hex(inverter_sn)[4:6] + hex(inverter_sn)[2:4])
    frame = bytearray(start + length + controlcode + serial + inverter_sn2 + datafield + businessfield + crc + checksum + endCode)
    # Data frame end

    checksum = 0
    frame_bytes = bytearray(frame)
    for i in range(1, len(frame_bytes) - 2, 1):
      checksum += frame_bytes[i] & 255
    frame_bytes[len(frame_bytes) - 2] = int((checksum & 255))

    # SEND DATA
    if verbose=="1":
      print("*** Chunk no: ", chunks);
      print("Sent data: ", frame);
    WriteDebug(logfile, "Sending a request to inverter")
    clientSocket.sendall(frame_bytes);

    # RECEIVE DATA
    ok=False;
    while (not ok):
      WriteDebug(logfile, "Receiving data from inverter")
      try:
        data = clientSocket.recv(1024);
        ok=True
        try:
          data
        except:
          print("No data - Exit")
          Write2LogFile(logfile, "No data received ! Exiting.")
          sys.exit(1) #Exit, no data
      except socket.timeout as msg:
        print("Connection timeout - inverter and/or gateway is offline");
        Write2LogFile(logfile, "Connection timeout - inverter and/or gateway is offline")
        invstatus=0;

    if invstatus==1:
      # PARSE RESPONSE (start position 56, end position 60)
      WriteDebug(logfile, "Parsing received data")
      if verbose=="1": print("Received data: ", data);
      i=pfin-pini
      a=0
      while a<=i:
        p1=56+(a*4)
        p2=60+(a*4)
        hexpos=str("0x") + str(hex(a+pini)[2:].zfill(4)).upper()
        response=twosComplement_hex(str(''.join(hex(ord(chr(x)))[2:].zfill(2) for x in bytearray(data))+'  '+re.sub('[^\x20-\x7f]', '', ''))[p1:p2], hexpos)
        with open("./SOFARMap.xml", encoding="utf-8") as txtfile:
          parameters=json.loads(txtfile.read())
        for parameter in parameters:
          for item in parameter["items"]:
            if lang=="PL":
              title=item["titlePL"]
            else:
              title=item["titleEN"]
            ratio=item["ratio"]
            unit=item["unit"]
            graph=item["graph"]
            metric_name=item["metric_name"]
            label_name=item["label_name"]
            label_value=item["label_value"]
            metric_type=item["metric_type"]
            DomoticzIdx=item["DomoticzIdx"]
            for register in item["registers"]:
              if register==hexpos and chunks!=-1:
                response=round(response*ratio,2)
                for option in item["optionRanges"]:
                  if option["key"] == response:
                    if label_name=="Status":
                      if response==2:
                        invstatus=1
                      else:
                        invstatus=0
                        chunks+=1
                        Write2LogFile(logfile, "Inverter not ready to talk. Inverter status code: "+str(response))
                    if lang == "PL":
                      response='"'+option["valuePL"]+'"'
                    else:
                      response='"'+option["valueEN"]+'"'
                if hexpos!='0x0015' and hexpos!='0x0016' and hexpos!='0x0017' and hexpos!='0x0018':
                  if verbose=="1": print(hexpos+" - "+title+": "+str(response)+unit);
                  if prometheus=="1" and graph==1: PMetrics(metric_name, metric_type, label_name, label_value, response);
                  if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, response);
                  if DomoticzSupport=="1" and DomoticzIdx>0: PrepareDomoticzData(DomoticzData, DomoticzIdx, response);
                  if HomeAssistantSupport=="1": HomeAssistantData.append([title, ratio, unit, metric_type, metric_name, label_name, label_value, response, register]);
                  if unit!="":
                    output=output+"\""+ title + " (" + unit + ")" + "\":" + str(response)+","
                  else:
                    output=output+"\""+ title + "\":" + str(response)+","
                if hexpos=='0x0015': totalpower+=response*ratio*65536;
                if hexpos=='0x0016':
                  totalpower+=response*ratio
                  if verbose=="1": print(hexpos+" - "+title+": "+str(response*ratio)+unit);
                  output=output+"\""+ title + " (" + unit + ")" + "\":" + str(totalpower)+","
                  if prometheus=="1" and graph==1: PMetrics(metric_name, metric_type, label_name, label_value, (totalpower*1000));
                  if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, totalpower);
                  if DomoticzSupport=="1" and DomoticzIdx>0: PrepareDomoticzData(DomoticzData, DomoticzIdx, response);
                  if HomeAssistantSupport=="1": HomeAssistantData.append([title, ratio, unit, metric_type, metric_name, label_name, label_value, response, (totalpower*1000)]);
                if hexpos=='0x0017': totaltime+=response*ratio*65536;
                if hexpos=='0x0018':
                  totaltime+=response*ratio
                  if verbose=="1": print(hexpos+" - "+title+": "+str(response*ratio)+unit);
                  output=output+"\""+ title + " (" + unit + ")" + "\":" + str(totaltime)+","
                  if prometheus=="1" and graph==1: PMetrics(metric_name, metric_type, label_name, label_value, totaltime);
                  if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, totaltime);
                  if DomoticzSupport=="1" and DomoticzIdx>0: PrepareDomoticzData(DomoticzData, DomoticzIdx, response);
                  if HomeAssistantSupport=="1": HomeAssistantData.append([title, ratio, unit, metric_type, metric_name, label_name, label_value, response, totaltime]);
        a+=1
      if chunks==0:
        pini=reg_start2
        pfin=reg_end2
    chunks+=1
    if chunks>1:
      WriteDebug(logfile, "Exiting chunks loop")
output=output[:-1]+"}"
if invstatus>0:
  jsonoutput=json.loads(output)
  print("*** JSON output:")
  print(json.dumps(jsonoutput, indent=4, sort_keys=False, ensure_ascii=False))

# Write data to a prometheus integration file
if prometheus=="1" and invstatus==1:
  WriteDebug(logfile, "Writing data to prometheus")
  prometheus_file = open(prometheus_file, "w");
  for i in range(0, len(PMData)):
    prometheus_file.write(PMData[i])
    if verbose=="1": print(PMData[i]);
  prometheus_file.close();

# Write data to Influx DB (if offline - write 0 for each parameter)
if influxdb=="1" and invstatus==1:
  WriteDebug(logfile, "Writing data to InfluxDB")
  Write2InfluxDB(InfluxData)
  if verbose=="1": print("Influx data: ", json.dumps(InfluxData, indent=4, sort_keys=False, ensure_ascii=False));
if influxdb=="1" and invstatus==0:
  WriteDebug(logfile, "Writing empty data to InfluxDB")
  with open("./SOFARMap.xml", encoding="utf-8") as txtfile:
    parameters=json.loads(txtfile.read())
  for parameter in parameters:
    for item in parameter["items"]:
      metric_name=item["metric_name"]
      label_name=item["label_name"]
      label_value=item["label_value"]
      graph=item["graph"]
      if graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, 0);
  Write2InfluxDB(InfluxData)
  if verbose=="1": print("Influx data: ", json.dumps(InfluxData, indent=4, sort_keys=False, ensure_ascii=False))

# MQTT integration (Domoticz, HA, pure MQTT)
if mqtt==1:
  WriteDebug(logfile, "Writing data to MQTT")
  # Initialise MQTT connection
  client=paho.Client("inverter")
  if mqtt_tls=="1":
    client.tls_set(mqtt_cacert,tls_version=mqtt_tls_ver)
    client.tls_insecure_set(mqtt_tls_insecure)
  client.username_pw_set(username=mqtt_username, password=mqtt_passwd)
  client.connect(mqtt_server, mqtt_port)
  client.loop_start()
  if invstatus==1:
    # Send data to MQTT in basic format
    if mqtt_basic=="1":
      result=client.publish(mqtt_topic, output)
      result.wait_for_publish()
      if result.is_published:
        if verbose=="1": print("*** Data has been succesfully published to MQTT with topic: "+mqtt_topic)
        WriteDebug(logfile, "Data has been succesfully published to MQTT with topic: "+mqtt_topic)
      else:
        print("Error publishing data to MQTT")
        Write2LogFile(logfile, "Error publishing data to MQTT")
    # Send data to Domoticz if support enabled
    if DomoticzSupport=="1":
      if verbose=="1": print("*** MQTT messages for Domoticz:");
      for mqtt_data in DomoticzData:
        if verbose=="1": print(domoticz_mqtt_topic, mqtt_data);
        result=client.publish(domoticz_mqtt_topic, mqtt_data, retain=True)
        result.wait_for_publish()
        if not result.is_published:
          print("Error publishing data for Domoticz to MQTT")
          Write2LogFile(logfile, "Error publishing data for Domoticz to MQTT")
    # Send data to HomeAssistant if support enabled
    if HomeAssistantSupport=="1":
      if verbose=="1": print("*** MQTT messages for HomeAssistant:");
      # Send messages in case of unexpected disconnection
      client.will_set(ha_mqtt_topic+str(inverter_sn)+"/state/connected","false")
      # Send status of the device: enabled = true
      result=client.publish(ha_mqtt_topic+str(inverter_sn)+"/enabled","true")
      result.wait_for_publish()
      if not result.is_published:
        print("Error publishing device status for HomeAssistant to MQTT")
        Write2LogFile(logfile, "Error publishing data for HomeAssistant to MQTT")
      # Send state of the device: connected = true
      result=client.publish(ha_mqtt_topic+str(inverter_sn)+"/state/connected","true")
      result.wait_for_publish()
      if not result.is_published:
        print("Error publishing device state for HomeAssistant to MQTT")
        Write2LogFile(logfile, "Error publishing data for HomeAssistant to MQTT")
      HAcount=0
      for mqtt_data in HomeAssistantData:
        # Sensors for ENERGY module with kWh, Wh, W
        if mqtt_data[2] in ['kWh', 'Wh', 'W']:
          # Send auto-discover device sensor template
          result=client.publish("homeassistant/sensor/SofarLogger/"+str(inverter_sn)+"_"+str(HAcount)+"/config","{\"avty\":{\"topic\":\""+ha_mqtt_topic+str(inverter_sn)+"/state/connected\",\"payload_available\":\"true\",\"payload_not_available\":\"false\"},\"~\":\""+ha_mqtt_topic+str(inverter_sn)+"/\",\"device\":{\"ids\":\""+str(inverter_sn)+"\",\"mf\":\"Sofar\",\"name\":\"WLS-3\",\"sw\":\"x.x.x\"},\"name\":\""+(mqtt_data[0])+" ["+(mqtt_data[2])+"]\",\"uniq_id\":\""+str(inverter_sn)+"_"+str(HAcount)+"\",\"qos\":0,\"unit_of_meas\":\""+(mqtt_data[2])+"\",\"stat_t\":\"~state/"+(mqtt_data[4])+(mqtt_data[6])+"\",\"val_tpl\":\"{{ value | round(5) }}\",\"dev_cla\":\"energy\",\"state_class\":\"total_increasing\"}")
        # Rest of the sensors
        else:
          # Send auto-discover device sensor template
          result=client.publish("homeassistant/sensor/SofarLogger/"+str(inverter_sn)+"_"+str(HAcount)+"/config","{\"avty\":{\"topic\":\""+ha_mqtt_topic+str(inverter_sn)+"/state/connected\",\"payload_available\":\"true\",\"payload_not_available\":\"false\"},\"~\":\""+ha_mqtt_topic+str(inverter_sn)+"/\",\"device\":{\"ids\":\""+str(inverter_sn)+"\",\"mf\":\"Sofar\",\"name\":\"WLS-3\",\"sw\":\"x.x.x\"},\"name\":\""+(mqtt_data[0])+" ["+(mqtt_data[2])+"]\",\"uniq_id\":\""+str(inverter_sn)+"_"+str(HAcount)+"\",\"qos\":0,\"unit_of_meas\":\""+(mqtt_data[2])+"\",\"stat_t\":\"~state/"+(mqtt_data[4])+(mqtt_data[6])+"\",\"val_tpl\":\"{{ value | round(5) }}\",\"dev_cla\":\"current\",\"state_class\":\"measurement\"}")
        result.wait_for_publish()
        if not result.is_published:
          print("[",str(HAcount),"]", "Error publishing data for HomeAssistant to MQTT")
          Write2LogFile(logfile, "Error publishing data for HomeAssistant to MQTT")
        else:
          if verbose=="1": print("[",str(HAcount),"]", mqtt_data[0], ": ", mqtt_data[7]);
        # Send sensor values data
        result=client.publish(ha_mqtt_topic+str(inverter_sn)+"/state/"+(mqtt_data[4])+(mqtt_data[6]), (mqtt_data[7]))
        result.wait_for_publish()
        if not result.is_published:
          print("[",str(HAcount),"]","Error publishing data for HomeAssistant to MQTT")
          Write2LogFile(logfile, "Error publishing data for HomeAssistant to MQTT")
        HAcount+=1
  else:
      # Send offline message
      if mqtt_basic=="1":
        result=client.publish(mqtt_topic, "{\"Status\": \"Offline\"}")
        result.wait_for_publish()
        if not result.is_published:
          print("Error publishing device status to MQTT")
          Write2LogFile(logfile, "Error publishing device status to MQTT")
      if DomoticzSupport=="1":
        with open("./SOFARMap.xml", encoding="utf-8") as txtfile:
          parameters=json.loads(txtfile.read())
        result=client.publish(domoticz_mqtt_topic, "{ \"idx\": "+str(parameters[2]['items'][0]['DomoticzIdx'])+", \"svalue\": \"Off\" }", retain=True)
        result.wait_for_publish()
        if not result.is_published:
          print("Error publishing device status for Domoticz to MQTT")
          Write2LogFile(logfile, "Error publishing device status for Domoticz to MQTT")
      if HomeAssistantSupport=="1":
        result=client.publish(ha_mqtt_topic+str(inverter_sn)+"/state/connected","false")
        result.wait_for_publish()
        if not result.is_published:
          print("Error publishing device status for HomeAssistant to MQTT")
          Write2LogFile(logfile, "Error publishing device status for HomeAssistant to MQTT")
  client.loop_stop()
  client.disconnect()
clientSocket.close()
WriteDebug(logfile, "Script end")
logfile.close()
