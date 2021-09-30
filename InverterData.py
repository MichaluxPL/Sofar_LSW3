#!/usr/bin/python3
# Script gathering solar data from Sofar Solar Inverter (K-TLX) via WiFi module LSW-3
# by Michalux (based on DEYE script by jlopez77)

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
from influxdb import InfluxDBClient
from datetime import datetime

def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val

# Write metrics for Prometheus
def PMetrics(mfile, mname, mtype, mlabel, mlvalue, pdata):
    line="# TYPE "+mname+" "+mtype+"\n"+mname+"{"+mlabel+"=\""+mlvalue+"\"} "+str(pdata)+"\n"
    mfile.write(line)

# InfluxDB support
def PrepareInfluxData(IfData, fieldname, fieldvalue):
    IfData[0]["fields"][fieldname]=float(fieldvalue)
    return IfData

def Write2InfluxDB(IfData):
    ifclient.write_points(IfData);

os.chdir(os.path.dirname(sys.argv[0]))
#os.chdir("/home/pi/solarman/SofarInverter")

# CONFIG
configParser = configparser.RawConfigParser()
configFilePath = r'./config.cfg'
configParser.read(configFilePath)

inverter_ip=configParser.get('SofarInverter', 'inverter_ip')
inverter_port=int(configParser.get('SofarInverter', 'inverter_port'))
inverter_sn=int(configParser.get('SofarInverter', 'inverter_sn'))
mqtt=int(configParser.get('SofarInverter', 'mqtt'))
mqtt_server=configParser.get('SofarInverter', 'mqtt_server')
mqtt_port=int(configParser.get('SofarInverter', 'mqtt_port'))
mqtt_topic=configParser.get('SofarInverter', 'mqtt_topic')
mqtt_username=configParser.get('SofarInverter', 'mqtt_username')
mqtt_passwd=configParser.get('SofarInverter', 'mqtt_passwd')
lang=configParser.get('SofarInverter', 'lang')
verbose=configParser.get('SofarInverter', 'verbose')
prometheus=configParser.get('SofarInverter', 'prometheus')
prometheus_file=configParser.get('SofarInverter', 'prometheus_file')
influxdb=configParser.get('SofarInverter', 'influxdb')
ifhost=configParser.get('SofarInverter', 'influxdb_host')
ifport=configParser.get('SofarInverter', 'influxdb_port')
ifuser=configParser.get('SofarInverter', 'influxdb_user')
ifpass=configParser.get('SofarInverter', 'influxdb_password')
ifdb=configParser.get('SofarInverter', 'influxdb_dbname')
# END CONFIG

timestamp=str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

# Initialise Prometheus support
if prometheus=="1": prometheus_file = open(prometheus_file, "w");

# Initialise InfluxDB support
if influxdb=="1":
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb);
    InfluxData=[
        {
            "measurement": "InverterData",
            "time": timestamp,
            "fields": {}
        }
    ]

# PREPARE & SEND DATA TO THE INVERTER
output="{" # initialise json output
pini=0
pfin=39
chunks=0
totalpower=0
totaltime=0
while chunks<2:
 if verbose=="1": print("Chunk no: ", chunks);

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
 if verbose=="1": print("Sent data: ", frame);
 # Data frame end

 checksum = 0
 frame_bytes = bytearray(frame)
 for i in range(1, len(frame_bytes) - 2, 1):
     checksum += frame_bytes[i] & 255
 frame_bytes[len(frame_bytes) - 2] = int((checksum & 255))

 # OPEN SOCKET
 for res in socket.getaddrinfo(inverter_ip, inverter_port, socket.AF_INET, socket.SOCK_STREAM):
                  family, socktype, proto, canonname, sockadress = res
                  try:
                   clientSocket= socket.socket(family,socktype,proto);
                   clientSocket.settimeout(10);
                   clientSocket.connect(sockadress);
                  except socket.error as msg:
                   print("Could not open socket - inverter/logger turned off");
                   if prometheus=="1": prometheus_file.close();
                   sys.exit(1)

 # SEND DATA
 clientSocket.sendall(frame_bytes);

 ok=False;
 while (not ok):
  try:
   data = clientSocket.recv(1024);
   ok=True
   try:
    data
   except:
    print("No data - Exit")
    sys.exit(1) #Exit, no data
  except socket.timeout as msg:
   print("Connection timeout - inverter and/or gateway is off");
   sys.exit(1) #Exit

# PARSE RESPONSE (start position 56, end position 60)
 if verbose=="1": print("Received data: ", data);
 i=pfin-pini
 a=0
 while a<=i:
  p1=56+(a*4)
  p2=60+(a*4)
  response=twosComplement_hex(str(''.join(hex(ord(chr(x)))[2:].zfill(2) for x in bytearray(data))+'  '+re.sub('[^\x20-\x7f]', '', ''))[p1:p2])
  hexpos=str("0x") + str(hex(a+pini)[2:].zfill(4)).upper()
  with open("./SOFARMap.xml") as txtfile:
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
     for register in item["registers"]:
      if register==hexpos and chunks!=-1:
       response=round(response*ratio,2)
       for option in item["optionRanges"]:
        if option["key"] == response:
            if lang == "PL":
                response='"'+option["valuePL"]+'"'
            else:
                response='"'+option["valueEN"]+'"'
       if hexpos!='0x0015' and hexpos!='0x0016' and hexpos!='0x0017' and hexpos!='0x0018':
        if verbose=="1": print(hexpos+" - "+title+": "+str(response)+unit);
        if prometheus=="1" and graph==1:
         PMetrics(prometheus_file, metric_name, metric_type, label_name, label_value, response)
        if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, response);
        if unit!="":
            output=output+"\""+ title + " (" + unit + ")" + "\":" + str(response)+","
        else:
            output=output+"\""+ title + "\":" + str(response)+","
       if hexpos=='0x0015': totalpower+=response*ratio*65536;
       if hexpos=='0x0016':
        totalpower+=response*ratio
        if verbose=="1": print(hexpos+" - "+title+": "+str(response*ratio)+unit);
        output=output+"\""+ title + " (" + unit + ")" + "\":" + str(totalpower)+","
        if prometheus=="1" and graph==1:
         PMetrics(prometheus_file, metric_name, metric_type, label_name, label_value, (totalpower*1000))
        if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, totalpower);
       if hexpos=='0x0017': totaltime+=response*ratio*65536;
       if hexpos=='0x0018':
        totaltime+=response*ratio
        if verbose=="1": print(hexpos+" - "+title+": "+str(response*ratio)+unit);
        output=output+"\""+ title + " (" + unit + ")" + "\":" + str(totaltime)+","
        if prometheus=="1" and graph==1:
         PMetrics(prometheus_file, metric_name, metric_type, label_name, label_value, totaltime)
        if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, totaltime);
  a+=1
 if chunks==0:
  pini=261
  pfin=276
 chunks+=1
output=output[:-1]+"}"

if prometheus=="1": prometheus_file.close();
if influxdb=="1":
    if verbose=="1": print("Influx data: ",InfluxData);
    Write2InfluxDB(InfluxData)

# MQTT integration
if mqtt==1:
 # Initialise MQTT if configured
 client=paho.Client("inverter")
 if mqtt_username!="":
  client.tls_set()  # <--- even without arguments
  client.username_pw_set(username=mqtt_username, password=mqtt_passwd)
 client.connect(mqtt_server, mqtt_port)
 client.publish(mqtt_topic+"/attributes",output)
 client.publish(mqtt_topic,totalpower)
 print("Data has been sent to MQTT")
else:
 jsonoutput=json.loads(output)
 print(json.dumps(jsonoutput, indent=4, sort_keys=False, ensure_ascii=False))
