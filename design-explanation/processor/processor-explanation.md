# Processor Design Explanation

- Notes regarding motherboard processor design choices and specs

## AT32UC3L0256

- Atmel's 32-bit MCU
  - Advertised to run at 50MHz, but we're seeing that it runs at 35MHz w/ DFLL
- An arbitrary choice- we have experience w/ Atmel's MCU's and Microchip Studio through Stony Brook's ESE280/381 labs
- There's room for improvement and speed by switching to an MCU w/ ARM architecture
- For now it's a decent upgrade from the Arduino Nano running at 20MHz, and taking up a whole lot of PCB real estate

## Programming

- Keyed JTAG is standard- no reason not to go for JTAG regardless of what processor we choose

## USART

- Serial out can be provided to a laptop via DE-9 to USB-A cable, and a TTL to RS232 translator

## Archived Ideas

- 1mm pitch 10 pin header for programming
  - Requires an adapter board to go from 2.54mm JTAG to 1mm 10 pin header
  - The standard keyed JTAG shroud is only available on 2.54mm- the key saves some sanity each time you program the micromouse, so archived idea
- Reset switch
  - Archived due to doing the same thing as flipping power on/off
  - ...Need to bring this back- we should avoid constantly flipping power
