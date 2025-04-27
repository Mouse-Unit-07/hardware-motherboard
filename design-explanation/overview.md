# Motherboard Design Explanation
Notes regarding motherboard design choices and hardware specs.

## Component Overview
![motherboard-components](motherboard-overview-images/motherboard-components.drawio.png)

1. Power Supply
    - JST Connector to 7V4 LiPo Battery
    - routed to 10A fuse, on/off rocker switch, and bulk capacitor

2. Wheel DC Motors w/ Magnetic Encoders
    - JST connector to ServoCity DC motors w/ built-in magnetic encoders
    - routed to MCU IO and interrupt pins and flyback diodes for back-EMF protection
    - each motor is connected to a drive gear, that drives two wheels on each side of the mouse

3. Wheel DC Motor Driver
    - H-bridge IC is routed to MCU IO pins and the DC motors to drive motor pins

4. Wheel Motor Power
    - 12V buck-boost switching regulator takes 7V4 from battery and supplies wheel motors

5. Battery Management
    - A simple op-amp configured as a comparator to detect low battery

6. Vacuum Fan
    - 3D printed impeller vacuum fan to provide traction for fine control at high speeds
    - driven w/ a MOSFET and an MCU's PWM pin
    - motor connectos to PCB via PicoBlade connector

7. Debug LEDs
    - indicators for firmware/hardware troubleshooting

8. USART Jumper Pins
    - USART brekout from MCU to an RS232 cable or USART bridge 

9. Main Processor
    - AT32UC3L0256 MCU
    - Running at 35MHz, programmed via JTAG

10. 3V3 Power
    - step-down switching regulator takes 7V4 from battery and provides 3V3 power
    - supplies MCU and JTAG

11. Vacuum Power
    - step-down switching regulator takes 7V4 from battery and provides 3V7 power
    - routed to vacuum motor w/ MOSFET as an on/off gate

12. 5V Power
    - step-down switching regulator takes 7V4 from battery and provides 5V power
    - supplies IR sensors

13. IR Sensors
    - JST connectors for SHARP 2~15cm infrared sensors
    - output constrained to 0~2V5 w/ a voltage divider to adher to MCU's ADC pin limit

## General References
- Bryant Gonzaga and Team's Micromouse: 
  - https://github.com/gonzagab/WolfieMouse/blob/master/doc/hardware_design/schematic_2017_Feb.pdf
- Green Ye
  - everyone refers to this micromouse design: http://greenye.net/Pages/Micromouse/Micromouse2016-2017.htm

- Decimus 4
  - https://micromouseonline.com/2012/05/16/shapeways-motor-mounts-arrive/
  - thorough documentation

- APEC Micromice
  - beautiful museum of mice: https://micromouseusa.com/?p=496

- Veritasium Micromouse Video
  - https://www.youtube.com/watch?v=ZMQbHMgK2rw&t=14s

- University of Munich, Micromouse Project
  - https://www.shalen.dev/downloads/micromouse-final-report.pdf

- Micromouse Article for Choosing Parts
  - https://medium.com/analytics-vidhya/mm-sensors-and-motors-7fa3a870db67

## Read More
- this document just provides an overview of the Mouse Unit 07 motherboard, and the general references that didn't fit in all the other markdown documents
- check out the other hardware explanation markdown documents for more details