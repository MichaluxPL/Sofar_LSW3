Home Assistant Supervisor adoon

Copy this folder to HomeAssistant addons folder after installing Samba Share Addon from store

Example payload mqqt:
inverter/attributes
{"Inverter status":"Normal","Fault 1":"No error","Fault 2":"No error","Fault 3":"No error","Fault 4":"No error","Fault 5":"No error","PV1 Voltage (V)":301.0,"PV1 Current (A)":0.93,"PV2 Voltage (V)":302.7,"PV2 Current (A)":0.88,"PV1 Power (W)":280,"PV2 Power (W)":260,"Output active power (W)":490,"Output reactive power (kVar)":-0.6,"Grid frequency (Hz)":50.04,"L1 Voltage (V)":231.9,"L1 Current (A)":1.14,"L2 Voltage (V)":234.0,"L2 Current (A)":1.13,"L3 Voltage (V)":231.6,"L3 Current (A)":1.12,"Total production (kWh)":6309,"Total generation time (h)":4532,"Today production (Wh)":330,"Today generation time (min)":72,"Inverter module temperature (oC)":18,"Inverter inner termperature (oC)":34,"Inverter bus voltage (V)":636.6,"PV1 voltage sample by slave CPU (V)":299.3,"PV1 current sample by slave CPU (A)":300.8,"Countdown time (s)":60,"Inverter alert message":0,"Input mode":1,"Communication Board inner message":0,"Insulation of PV1+ to ground":1338,"Insulation of PV2+ to ground":1945,"Insulation of PV- to ground":1570,"Country":"Poland","String 1 voltage (V)":11.4,"String 1 current (A)":23.4,"String 2 voltage (V)":11.3,"String 2 current (A)":23.16,"String 3 voltage (V)":11.2,"String 3 current (A)":0.0,"String 4 voltage (V)":630.9,"String 4 current (A)":0.0,"String 5 voltage (V)":453.2,"String 5 current (A)":0.33,"String 6 voltage (V)":7.2,"String 6 current (A)":0.18,"String 7 voltage (V)":3.4,"String 7 current (A)":63.66,"String 8 voltage (V)":299.3,"String 8 current (A)":30.08}

Example Sensor Config mqqt:


sensor sofar: 
  - platform: mqtt
    name: "Inverter status"
    state_topic: "inverter/attributes"
    value_template: "{{ value_json.attributes }}"
  - platform: mqtt
    name: "Fault 1"
    state_topic: "inverter/attributes"
    value_template: "{{ value_json.fault_message }}"
  - platform: mqtt
    name: "Fault 2"
    state_topic: "inverter/attributes"
    value_template: "{{ value_json.fault_message }}"
  - platform: mqtt
    name: "Fault 3"
    state_topic: "inverter/attributes"
    value_template: "{{ value_json.fault_message }}"
  - platform: mqtt
    name: "Fault 4"
    state_topic: "inverter/attributes"
    value_template: "{{ value_json.fault_message }}"
  - platform: mqtt
    name: "Fault 5"
    state_topic: "inverter/attributes"
    value_template: "{{ value_json.fault_message }}"    
  - platform: mqtt
    name: "PV1 Voltage (V)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'V'
    value_template: "{{ value_json.dc_voltage_1 }}"
  - platform: mqtt
    name: "PV1 Current (A)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'A'
    value_template: "{{ value_json.dc_current_1 }}"
  - platform: mqtt
    name: "PV2 Voltage (V)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'V'
    value_template: "{{ value_json.dc_voltage_2 }}"
  - platform: mqtt
    name: "PV2 Current (A)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'A'
    value_template: "{{ value_json.dc_current_2 }}"
  - platform: mqtt
    name: "PV1 Power (W)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'W'
    value_template: "{{ value_json.ac_power }}"
  - platform: mqtt
    name: "PV2 Power (W)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'W'
    value_template: "{{ value_json.ac_power }}"   
  - platform: mqtt
    name: "Output active power (W)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'W'
    value_template: "{{ value_json.ac_power }}" 
  - platform: mqtt
    name: "Output reactive power (kVar)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'kVar'
    value_template: "{{ value_json.ac_power }}"   
  - platform: mqtt
    name: "Grid frequency (Hz)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'Hz'
    value_template: "{{ value_json.ac_frequency }}"
  - platform: mqtt
    name: "L1 Voltage (V)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'V'
    value_template: "{{ value_json.ac_voltage_1 }}"
  - platform: mqtt
    name: "L1 Current (A)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'A'
    value_template: "{{ value_json.ac_current_1 }}"
  - platform: mqtt
    name: "L2 Voltage (V)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'V'
    value_template: "{{ value_json.ac_voltage_2 }}"
  - platform: mqtt
    name: "L2 Current (A)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'A'
    value_template: "{{ value_json.ac_current_2 }}"
  - platform: mqtt
    name: "L3 Voltage (V)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'V'
    value_template: "{{ value_json.ac_voltage_3 }}"
  - platform: mqtt
    name: "L3 Current (A)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'A'
    value_template: "{{ value_json.ac_current_3 }}"    
  - platform: mqtt
    name: "Total production (kWh)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'kWh'
    value_template: "{{ value_json.energy_total }}"
  - platform: mqtt
    name: "Total generation time (h)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'h'
    value_template: "{{ value_json.running_time }}"
  - platform: mqtt
    name: "Today production (Wh)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'kWh'
    value_template: "{{ value_json.energy_today }}"
  - platform: mqtt
    name: "Today production (Wh)"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'h'
    value_template: "{{ value_json.running_time }}"    
  - platform: mqtt
    name: "Inverter module temperature (ºC)"
    state_topic: "inverter/attributes"
    unit_of_measurement: '°C'
    value_template: "{{ value_json.temperature_module }}"
  - platform: mqtt
    name: "Inverter inner termperature (ºC)"
    state_topic: "inverter/attributes"
    unit_of_measurement: '°C'
    value_template: "{{ value_json.temperature_inverter }}"
  - platform: mqtt
    name: "Insulation of PV1+ to ground"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'Ohm'
    value_template: "{{ value_json.temperature_inverter }}"
  - platform: mqtt
    name: "Insulation of PV2+ to ground"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'Ohm'
    value_template: "{{ value_json.temperature_inverter }}"
  - platform: mqtt
    name: "Insulation of PV- to ground"
    state_topic: "inverter/attributes"
    unit_of_measurement: 'Ohm'
    value_template: "{{ value_json.temperature_inverter }}"    
