# Processor Design Explanation
Notes regarding motherboard processor design choices and specs.

## AT32UC3L0256
- an arbitrary choice- it's Atmel's 32-bit MCU, and it felt like an extension to Stony Brook's ESE280/381 labs w/ development on Microchip Studio
- there's room for improvement and speed by switching MCU's, but it's a lot easier said than done
- advertised to run at 50MHz, but we're seeing that it runs at 35MHz w/ DFLL
- for now it's a decent upgrade from the Arduino Nano running at 20MHz, and taking up a whole lot of PCB real estate

## Programming
- keyed JTAG is nice and standard

## USART
- serial out can be provided to a laptop via DE-9 to USB-A cable, and a TTL to RS232 translator

## Archived Ideas
- 1mm Pitch 10 Pin Header for Programming
  - requires an adapter board to go from 2.54mm JTAG to 1mm 10 pin header
  - the standard JTAG key is only available on 2.54mm, and it saves some thinking each time you program the micromouse, so archived idea

- Reset Switch
  - archived due to doing the same thing as flipping power on/off