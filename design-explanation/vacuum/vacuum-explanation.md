# Vacuum Design Explanation

- Notes regarding motherboard vacuum design choices and specs

## Motor Selection

- 8520 DC motor
  - Typically used for quadcoptor drones- good choice for vacuum for its powerful/small form factor
  - Takes 1S LiPo power, so 3V7

## Switching Circuit

- MOSFET
  - Good for high frequency switching, low power
  - 2.2A 30V n-channel MOSFET used to gate 3V7 power to motor
  - MCU's PWM pin used to control the gate pin to control motor speed
  - 10k resistor pull-down resistor added to ensure low when MCU isn't driving MOSFET gate high
  - Gate resistor
    - Limits current from MCU to MOSFET gate
    - 47 Ohm resistor chosen from below calculations

```
Ig = gate current
Ciss = gate capacitance
Vg = gate voltage
Tsw = switching time desired
Rg = gate resistor

Ig = Ciss * (Vg / Tsw)
Rg = Vg / Ig
Rg = Tsw / Ciss

We choose a resistor provided:
- 3V3 gate voltage from MCU
- 0.25W resistors are most common
- Ciss of MOSFET

Calculations:
3.3V / (0.25 / 3.3V) = 43 Ohms
43 Ohms * 290pF = 12.63nS
1 / 12.63nS = 79.161521MHz max switching frequency possible
```

## Electrical Protection

- A single 60V 3A flyback diode used for EMF protection, provided the motor only moves in one direction
- Same component used as flyback diodes for wheel motor driving

## Impeller Fan Design

- Green Ye's micromouse design allocates 3cm diameter to the vacuum fan, so we're arbitrarily doing the same: http://greenye.net/Pages/Micromouse/Micromouse2016-2017.htm
- Refer to mechanical design guide for references to designing the impeller fan w/ Fusion 360 and for more details

## Rough Mechanical Calculations

- Ideally, the vacuum should be able to provide enough resistive force to counter all centrifugal forces when making sharp turns

```
Fc = centrifugal force, = (mv^2) / r
  m = mass
  r = radius of turn
  v = turning velocity
Ff = frictional forces
Fs = suction force

We need Ff >= Fc

Assuming:
u (coefficient of friction) = 0.7 (rubber on wood)
m (rough mass of micromouse) = 200g
r = 44mm (rotating in place)

Calculating tolerable velocity without suction:

umg >= (mv^2) / r
ugr^0.5 >= v
v <= (0.7*9.8*0.044)^0.5 = 0.5m/s

Fs is a function of how much faster we want to turn

Calculating Fs provided v:

u(mg + Fs) >= (mv^2) / r
Fs >= (((mv^2) / r) / u) - mg
```

## Archived Ideas

- Brushless DC motor
  - Modern quadcoptor drones use brushless DC motors for longer lifespans
  - Requires complex driver IC's and additional pins from MCU
  - Attempted, but shelved due to all the hardware required in contrast to just a motor and a switching gate
- Motor Driver
  - A motor driver IC would be nice- ensures that the vacuum motor is driven safely over inventing a custom switching circuit
  - Shelved due to lack of small form factor single motor driver IC's that supply high current
