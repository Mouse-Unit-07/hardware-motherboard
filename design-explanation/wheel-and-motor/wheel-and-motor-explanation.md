# Wheel and Motor Design Explanation

- Notes regarding motherboard wheel and motor design choices and specs

## ServoCity's Premium N20 Gear Motor

- ServoCity's [Premium N20 Gear Motor (5:1 Ratio, 4900 RPM, with Encoder)](https://www.servocity.com/4900-rpm-micro-gear-motor-w-encoder/)
- Magnetic encoder integrated into the motor
- Specs:
  - 4900 RPM
  - 2 oz-in of torque on stall
  - 60.8077 countable events per revolution from encoder
  - Quadrature encoder w/ A & B signals
  - 1.6A current draw on stall
  - Brushed DC motor

## 4 Wheel Drive

- Decimus 4
  - https://micromouseonline.com/2012/05/16/shapeways-motor-mounts-arrive/
  - https://micromouseonline.com/2012/05/24/printed-wheels-complete-decimus-mechanicals/
  - The key is to use ball bearings, spacers, and a screw for a shaft for the wheels to rotate
  - M3 screws and 3mm diameter ball bearings are used for Mouse Unit 07
- Designing gears
  - The key is to design wheels w/ gears on them
  - More details in mechanical design guide

## Wheel Bearing Spacers

- ![ball-bearing](_images/wheel-and-motor-explanation/ball-bearing.png)
- Needed to prevent outer ring of ball-bearings from touching 3D printed mounts and screw heads
- Crucial that they're made of metal- tried to 3D print spacers, but they eventually mold into the shapes of the parts they're spaced between

## Drive Circuit

- Big h-bridge IC
  - There aren't many high-current h-bridge IC's, but the TB6561FG brushed motor driver provides 1.5A per motor channel

## Electrical Protection

- Flyback diodes
  - Flyback didoes for motor control: https://www.microtype.io/h-bridge-circuit-design/
  - If the load can be driven both ways, then each wire coming out of the motor needs two diodes
  - 60V 3A flyback diode used to manage the one direction that the motor moves

## Mechanical Micromouse Specs

- Items include:
  - ServoCity's motor specs
  - Gear ratio of 3D printed gears (44:13)
  - Diameter of 3D printed wheel (32mm)
  - Micromouse wheel to wheel distance (87.56mm)
  - Micromouse maze dimensions
    - 165mm per wall, 12mm per pillar
- Calculated specs:
  - Rising edges (on a single signal, A or B) per wheel revolution: **51.45 rising edges**
  - Rising edges (on a single signal, A or B) per maze square: **90.59 rising edges**
  - Rising edges (on a single signal, A or B) per 90 degree turn: **35.2 rising edges**
  - Top velocity: **8.21m/s**
- **Issues w/ above calculated specs**:
  - Wheel circumference may be 103mm instead of 100.53mm according to tape measure...
  - Wheel to wheel distance varies depending mechanical assembly of spacers, wheel mounts, wheels, etc
  - The motors aren't capable of immediately stopping the wheel upon receiving stop signals, so there's some additional movement after a "stop" is made in firmware
- **Issue solutions**
  - Measure and update default values upon building a mouse for:
    - Wheel to wheel distance
    - Wheel circumference
  - Provide method of modifying parameters at runtime
  - Decelerate micromouse to a stop to get closer to the target rising edge count
  - Slowly accelerate micromouse for similar control at start

```
Calculation for rising edges (on a single signal) per wheel revolution:
Rrev = rising edges (on a single signal) per revolution
rpm = rotations per minute
Gr = gear ratio between each wheel and the drive gear (44:13)
Nevents = number of events per revolution from encoder
NeventTypes = number of types of countable events (rising on A, falling on A, rising on B, falling on B)

Rrev = Gr * (Nevents / NeventTypes)
Rev = (44/13) * (60.8077 / 4) = 51.45


Calculation for rising edges (on a single signal) per maze square
Ls = length of a maze square
Lw = length of a maze wall
Lp = length of a maze pillar
Rs = rising edges (on a single signal) per maze square
Rrev = rising edges (on a single signal) per revolution
Rmm = rising edges (on a single signal) per mm
Dw = wheel diameter (32mm)
Cw = wheel circumference

Ls = Lw + Lp
Ls = 165mm + 12mm = 177mm
Cw = pi * Dw
Cw = pi * 32mm = 100.53mm
Rmm = Rrev / Cw
Rmm = 51.45 / 100.53 = 0.512
Rs = Ls * Rmm
Rs = 177mm * 0.512 = 90.59
Final equation: Rs = (Lw + Lp) * ((Rrev) / (pi * Dw))


Calculation for rising edges per 90 turn:
R90turn = rising edges (on a single signal) per 90 degree turn
L90turn = length of 90 degree turn
L360turn = length of 360 degree turn
Dww = wheel to wheel distance
Rmm = rising edges (on a single signal) per mm

L360turn = pi * Dww
L360turn = pi * 87.56mm = 275.078mm
L90turn = L360turn / 4
L90turn = 68.77mm
R90turn = L90turn * Rmm
R90turn = 35.2
Final equation: R90turn = ((pi * Dww) / 4) * ((Rrev) / (pi * Dw))

Calculation for top velocity:
Vmax = top velocity
rpm = rotations per minute
Cw = wheel circumference

Vmax = (rpm / 60) * Cw
Vmax = (4900 / 60) * 0.10053m = 8.21m/s
```

## Rough Mechanical Calculations

- Theoretical calculations based on more uncertain parameters:
  - Coefficient of friction
  - Weight of micromouse
- ServoCity's [Premium N20 Gear Motor (5:1 Ratio, 4900 RPM, with Encoder)](https://www.servocity.com/4900-rpm-micro-gear-motor-w-encoder/) provide 4900 RPM, 2 oz-in of torque on stall, and 60.8077 countable events per revolution
- Faster motors are fast in exchange for torque, so we need to make sure the motors can still move and accelerate the mouse
- We need enough torque to overcome frictional forces to get the mouse accelerating

```
Provided:
4 wheels total
Tm = torque of each motor (2 oz-in of torque = 0.014N-m of torque)
m = mass (micromouse is about 200g, provided 2024 micromouse was ~140g)
Dw = wheel diameter (32mm)
Gr = gear ratio between each wheel and the drive gear (44:13)
Tw = torque of each wheel
u = coefficient of static friction between rubber and wood (0.95)


Calculation for torque provided by each wheel:
Tw = (Gr * Tm) / 2
Tw = (44/13)*0.014N-m / 2 = 0.0237N-m


Calculation of torque demanded to move micromouse:
F = u(mg)
F = 0.95*(0.2*9.8) = 1.862N
Fw = 1.862N / 4 = 0.466N demanded by each wheel
Tw = 0.466N * 0.032m = 0.0149N-m

We can calculate micromouse acceleration possible w/ the difference of torques


Calculation of possible micromouse acceleration:
(Tw leftover) = (Tw provided) - (Tw demanded)
(Tw leftover) = 0.0237N-m - 0.0149N-m = 0.0088N-m

(Fw leftover) = (Tw leftover) / (Dw / 2)
(Fw leftover) = 0.0088N-m / (0.032m / 2) = 0.55N

(F total) = (Fw leftover) * (wheels total)
(F total) = 0.55N * 4 = 2.2N

Acceleration possible = (F total) / m
Acceleration possible = 2.2N / 0.2kg = 11m/s^2

...Higher acceleration is useful for getting to top speed faster
```
