#!/usr/bin/python3
# Script gathering solar data from Sofar Solar Inverter (K-TLX) via logger module LSW-3/LSE
# by Michalux (based on DEYE script by jlopez77)
# Version: 1.61
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
from influxdb import InfluxDBClient
from datetime import datetime

def twosComplement_hex(hexval, reg):
    if hexval=="":
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
    ifclient.write_points(IfData);

def PrepareDomoticzData(DData, idx, svalue):
    if isinstance(svalue, str):
        DData.append('{ "idx": '+str(idx)+', "svalue": '+ svalue +' }')
    else:
        DData.append('{ "idx": '+str(idx)+', "svalue": "'+ str(svalue) +'" }')
    return DData

os.chdir(os.path.dirname(sys.argv[0]))

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
prometheus=configParser.get('Prometheus', 'prometheus')
prometheus_file=configParser.get('Prometheus', 'prometheus_file')
influxdb=configParser.get('InfluxDB', 'influxdb')
ifhost=configParser.get('InfluxDB', 'influxdb_host')
ifport=configParser.get('InfluxDB', 'influxdb_port')
ifuser=configParser.get('InfluxDB', 'influxdb_user')
ifpass=configParser.get('InfluxDB', 'influxdb_password')
ifdb=configParser.get('InfluxDB', 'influxdb_dbname')
DomoticzSupport=configParser.get('Domoticz', 'domoticz_support')
# END CONFIG

timestamp=str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

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
pini=reg_start1
pfin=reg_end1
chunks=0
totalpower=0
totaltime=0
PMData=[]
DomoticzData=[]

while chunks<2:
 if verbose=="1": print("*** Chunk no: ", chunks);

# Data frame begin
 start = binascii.unhexlify('A5') #start
 length=binascii.unhexlify('1700') # datalength
 controlcode= binascii.unhexlify('1045') #controlCode
 serial=binascii.unhexlify('0000') # serial
 datafield = binascii.unhexlify('020000000000000000000000000000') #com.igen.localmode.dy.instruction.send.SendDataField
 #pos_ini=str(hex(pini)[2:4].zfill(2))+str(hex(pini)[4:6].zfill(2))
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
  hexpos=str("0x") + str(hex(a+pini)[2:].zfill(4)).upper()
  response=twosComplement_hex(str(''.join(hex(ord(chr(x)))[2:].zfill(2) for x in bytearray(data))+'  '+re.sub('[^\x20-\x7f]', '', ''))[p1:p2], hexpos)
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
            if lang == "PL":
                response='"'+option["valuePL"]+'"'
            else:
                response='"'+option["valueEN"]+'"'
       if hexpos!='0x0015' and hexpos!='0x0016' and hexpos!='0x0017' and hexpos!='0x0018':
        if verbose=="1": print(hexpos+" - "+title+": "+str(response)+unit);
        if prometheus=="1" and graph==1: PMetrics(metric_name, metric_type, label_name, label_value, response);
        if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, response);
        if DomoticzSupport=="1" and DomoticzIdx>0: PrepareDomoticzData(DomoticzData, DomoticzIdx, response);
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
       if hexpos=='0x0017': totaltime+=response*ratio*65536;
       if hexpos=='0x0018':
        totaltime+=response*ratio
        if verbose=="1": print(hexpos+" - "+title+": "+str(response*ratio)+unit);
        output=output+"\""+ title + " (" + unit + ")" + "\":" + str(totaltime)+","
        if prometheus=="1" and graph==1: PMetrics(metric_name, metric_type, label_name, label_value, totaltime);
        if influxdb=="1" and graph==1: PrepareInfluxData(InfluxData, metric_name.split('_')[0]+"_"+label_value, totaltime);
        if DomoticzSupport=="1" and DomoticzIdx>0: PrepareDomoticzData(DomoticzData, DomoticzIdx, response);
  a+=1
 if chunks==0:
  pini=reg_start2
  pfin=reg_end2
 chunks+=1
output=output[:-1]+"}"

# Write data to a prometheus integration file
if prometheus=="1" and invstatus==1:
    prometheus_file = open(prometheus_file, "w");
    for i in range(0, len(PMData)):
        prometheus_file.write(PMData[i])
        if verbose=="1": print(PMData[i]);
    prometheus_file.close();

# Write data to Influx DB
if influxdb=="1" and invstatus==1:
    Write2InfluxDB(InfluxData)
    if verbose=="1": print("Influx data: ",InfluxData);

# MQTT and Domoticz integration
if mqtt==1 and invstatus==1:
    # Initialise MQTT if configured
    client=paho.Client("inverter")
    if mqtt_tls=="1":
        client.tls_set(mqtt_cacert,tls_version=mqtt_tls_ver)
        client.tls_insecure_set(mqtt_tls_insecure)
    client.username_pw_set(username=mqtt_username, password=mqtt_passwd)
    client.connect(mqtt_server, mqtt_port)
    # Send data to Domoticz if support enabled
    if DomoticzSupport=="1":
        if verbose=="1": print("*** MQTT messages for Domoticz:");
        for mqtt_data in DomoticzData:
            if verbose=="1": print(mqtt_topic, mqtt_data);
            result=client.publish(mqtt_topic, mqtt_data)
            if result[0]!=0:
                print("Error publishing data for Domoticz to MQTT")
    else:
        result=client.publish(mqtt_topic+"/attributes",output)
        if result[0]==0:
            print("*** Data has been succesfully published to MQTT with topic: "+mqtt_topic+"/attributes")
        else:
            print("Error publishing data to MQTT")
    client.disconnect()
print("*** JSON output:")
jsonoutput=json.loads(output)
print(json.dumps(jsonoutput, indent=4, sort_keys=False, ensure_ascii=False))
