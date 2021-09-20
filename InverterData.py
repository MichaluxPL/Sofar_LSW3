#!/usr/bin/python3
# Script gathering solar data from Sofar Solar Inverter (K-TLX) via WiFi module LSW-3
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

def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val

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
# END CONFIG

# PREPARE & SEND DATA TO THE INVERTER
output="{" # initialise json output
pini=0
pfin=39
chunks=0
while chunks<2:
 #print("Chunks: ", chunks)
 if chunks==-1: # testing initialisation
  pini=235
  pfin=235
  print("Initialise Connection")
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
 #print("Sent: ", frame)
 
 checksum = 0
 frame_bytes = bytearray(frame)
 for i in range(1, len(frame_bytes) - 2, 1):
     checksum += frame_bytes[i] & 255
 frame_bytes[len(frame_bytes) - 2] = int((checksum & 255))
 
 # OPEN SOCKET
 for res in socket.getaddrinfo(inverter_ip, inverter_port, socket.AF_INET,
                                            socket.SOCK_STREAM):
                  family, socktype, proto, canonname, sockadress = res
                  try:
                   clientSocket= socket.socket(family,socktype,proto);
                   clientSocket.settimeout(10);
                   clientSocket.connect(sockadress);
                  except socket.error as msg:
                   print("Could not open socket");
                   break
 
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
 #print("Received: ", data)
 totalpower=0
 totaltime=0
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
     for register in item["registers"]:
      if register==hexpos and chunks!=-1:
       response=round(response*ratio,2)
       for option in item["optionRanges"]:
        if option["key"] == response:
            if lang == "PL":
                response='"'+option["valuePL"]+'"'
            else:
                response=option["valueEN"]
       if hexpos!='0x0015' and hexpos!='0x0016' and hexpos!='0x0017' and hexpos!='0x0018':
        print(hexpos+" - "+title+": "+str(response)+unit)
        if unit!="":
            output=output+"\""+ title + " (" + unit + ")" + "\":" + str(response)+","
        else:
            output=output+"\""+ title + "\":" + str(response)+","
       if hexpos=='0x0015': totalpower+=response*ratio;
       if hexpos=='0x0016':
        totalpower+=response*ratio
        print(hexpos+" - "+title+": "+str(response*ratio)+unit)
        output=output+"\""+ title + " (" + unit + ")" + "\":" + str(totalpower)+","
       if hexpos=='0x0017': totaltime+=response*ratio;
       if hexpos=='0x0018':
        totaltime+=response*ratio
        print(hexpos+" - "+title+": "+str(response*ratio)+unit)
        output=output+"\""+ title + " (" + unit + ")" + "\":" + str(totaltime)+","

  a+=1
 if chunks==0:
  pini=261
  pfin=276
 chunks+=1
output=output[:-1]+"}"

# MQTT integration
if mqtt==1:
 # Initialise MQTT if configured
 client=paho.Client("inverter")
 if mqtt_username!="":
  client.tls_set()  # <--- even without arguments
  client.username_pw_set(username=mqtt_username, password=mqtt_passwd)
 client.connect(mqtt_server, mqtt_port)
 client.publish(mqtt_topic,totalpower)
 client.publish(mqtt_topic+"/attributes",output)
 print("Data has been sent to MQTT")
else:
 jsonoutput=json.loads(output)
 print(json.dumps(jsonoutput, indent=4, sort_keys=False, ensure_ascii=False))
 #print(output)
