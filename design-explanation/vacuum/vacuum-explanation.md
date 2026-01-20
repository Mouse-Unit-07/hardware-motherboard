# Vacuum Design Explanation

- Notes regarding motherboard vacuum design choices and specs

## Index

- [Motor Selection](#motor-selection)
- [Switching Circuit](#switching-circuit)
- [Electrical Protection](#electrical-protection)
- [Impeller Fan Design](#impeller-fan-design)
- [Rough Mechanical Calculations](#rough-mechanical-calculations)
- [Archived Ideas](#archived-ideas)

## Motor Selection

- 8520 DC motor
  - Typically used for quadcoptor drones- good choice for vacuum for its powerful/small form factor
  - Takes 1S LiPo power, so 3V7
- PicoBlade vs JST
  - Confusing that these 8520 motors come w/ Molex PicoBlade connectors instead of JST
    - Reddit: https://www.reddit.com/r/AskElectronics/comments/m6mibq/is_a_picoblade_125mm_connector_the_same_as_micro/?rdt=47452
    - Blog: https://blog.kylemanna.com/hardware/molex-picoblade-vs-jst-sh-connectors/
  - Need to visually check whether connector demands blade-like pins or regular through-hole pins

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

- Lack of documentation
  - Very involved- wish we had a mechanical engineer on the team
  - For whatever reason, there's no documentation regarding micromouse vacuum fan designs
  - ...Except for this: https://rt-net.jp/mobility/archives/20915
    - ^implements a turbo impeller fan <3
- Different impeller fan types compared
  - Video here: https://www.youtube.com/watch?v=mafjVYfFgg4
  - Turbo fan provides the most suction
- Impeller fans
  - there is documentation on impeller fans in general
    - impeller blower configuration video: https://youtu.be/YuEaP9kyiFc?si=spyc_kHSI9guTJmH
    - impeller fan crafted by hand video: https://youtu.be/Hyz1TMbNVSo?si=MinbotT-jVyszSr6
  - puller configuration
    - ![impeller-fan-video](_images/vacuum-explanation/impeller-fan-video.png)
      - when a fan's wings scoop the air, it's pusher configuration
      - when a fan's wings swing air out, it's puller configuration
      - in the above image, when the fan moves counter-clockwise it's the most efficient design in terms of power consumption and RPM
- Failed designs
  - ![ball-bearing](_images/vacuum-explanation/failed-vacuum-fans.png)
  - Reasons for failure include lack of suction, lack of durability (fan parts break apart), and noise
    - Second to last failing design is intolerably loud
    - Last design is essentially the working design, but a bit too tall and wide
- Green Ye
  - http://greenye.net/Pages/Micromouse/Micromouse2016-2017.htm
  - Allocates 3cm to vacuum on PCB, and 1.5cm for the hole for suction
  - Mouse Unit 07 arbitrarily does the same
- Excel-9a
  - Video: https://www.youtube.com/watch?v=1_KpQ1bw5I8
  - Documentation: https://sites.google.com/site/myprojectq/robotic/classic-micromouse/excel-9a?pli=1
  - The mouse that defies gravity
- Micromouse online
  - https://micromouseonline.com/2018/02/18/more-suck-less-slip/
  - Yes, vacuum means less slip indeed

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
