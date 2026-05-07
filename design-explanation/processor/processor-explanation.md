# Processor Design Explanation

- Notes regarding motherboard processor design choices and specs

## Index

- [Selection: AT32UC3L0256](#selection-at32uc3l0256)
- [Programming](#programming)
- [USART](#usart)
- [Archived Ideas](#archived-ideas)

## Selection: AT32UC3L0256

- Atmel's 32-bit MCU
  - Advertised to run at 50MHz, but we're seeing that it runs at 35MHz w/ DFLL
- An arbitrary choice- we have experience w/ Atmel's MCU's and Microchip Studio through Stony Brook's ESE280/381 labs
- There's room for improvement and speed by switching to an MCU w/ ARM architecture
- For now it's a decent upgrade from the Arduino Nano running at 20MHz, and taking up a whole lot of PCB real estate

## Programming

- Keyed JTAG is standard- no reason not to go for JTAG regardless of what processor we choose

## USART

- Serial out can be provided to a laptop via DE-9 to USB-A cable, and a TTL to RS232 translator

## Configuration Pushbutton

- Pushbutton for any user requests
- Debounced w/ full debounce circuit

```

given:
- ~50ms debounce
- 100k resistors
- AT32UC3L0256 MCU logic levels of 0.3*Vdd for input low max, 0.7*Vdd for input high min
- 0.7V drop on diode

press:
V(t) = Vdd * e^(-t/r2c)
t = -r2c * ln(Vinput_low_max / Vdd)
Vinput_low_max = 0.3 * Vdd = 0.99V
50ms = -100k * c * ln(0.3)
c = 0.415uF

release:
V(t) = (Vdd - Vdiode) * (1 - e^(-t/r1c))
t = -r1c * ln(1 - (Vinput_high_max / (Vdd - Vdiode)))
Vinput_high_max = 0.7 * Vdd = 2.31V
50ms = -100k * c * ln(1 - (2.31 / (3.3 - 0.7)))
c = 0.228uF

we'll go w/ the higher capacitor value and go for 0.47uF

```

## Archived Ideas

- 1mm pitch 10 pin header for programming
  - Requires an adapter board to go from 2.54mm JTAG to 1mm 10 pin header
  - The standard keyed JTAG shroud is only available on 2.54mm- the key saves some sanity each time you program the micromouse, so archived idea
- Reset switch
  - Archived due to doing the same thing as flipping power on/off
  - ...Need to bring this back- we should avoid constantly flipping power
