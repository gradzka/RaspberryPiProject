# RaspberryPiProject

## Overview
Project with Raspberry Pi 3 B+:
- MQTT communication between 2 subscribers (share data about LED and switch state) with Mosquitto broker,
- testing external modules with Raspberry Pi: gyroscope, switches & LEDs and camera. Gathered data is displayed on web page using Flask server.

## Description
Features was tested on Raspberry Pi 3 B+  with Arch Linux ARM on SD card.

### MQTT Communication
- subscriber 1 publish information for toggling diode state and subscribe topic about switch state,
- subscriber 2 publish information about actual switch state and subscribe topic about toggling diode,
- Mosquitto broker installed on external device.

### Web page
Served by nginx server, based on Flask server, show information (refreshed once per second) about:
- processor temperature,
- processor percentage usage,
- RAM percentage usage,
- gyroscope registers values.

Enables to toggle diode state by slider and stream live video from camera module.

![Web page presentation](https://github.com/gradzka/RaspberryPiProject/blob/master/web_page.png)

### How to connect?
```
Raspberry Pi <---> Gyroscope (L3GD20H)
3V3 <---> VIN
Ground <---> GND
GPIO2  <---> SDA
GPIO3 <---> SCL

Raspberry Pi <---> Switches & LEDs Module
GPIO13 <---> SW2
GPIO26 <---> LED+
Ground <---> GND

Raspberry Pi <---> Camera Module V2
CSI Camera Connector <---> ribbon cable
```

## Attributions
- https://github.com/Mjrovai/Video-Streaming-with-Flask/blob/master/camWebServer/camera_pi.py
- https://github.com/taniarascia/sandbox/tree/master/ghibli

## Credits
* Monika Grądzka
* Robert Kazimierczak

The project was conducted during the Microprocessor Lab course held by the Institute of Control and Information Engineering, Poznan University of Technology.
