# Wheel and Motor Design Explanation
Notes regarding motherboard wheel and motor design choices and specs.

## Motor Selection
- ServoCity's [Premium N20 Gear Motor (5:1 Ratio, 4900 RPM, with Encoder)](https://www.servocity.com/4900-rpm-micro-gear-motor-w-encoder/)
- magnetic encoder integrated into the motor
- specs:
  - 4900 RPM
  - 2 oz-in of torque on stall
  - 60.8077 countable events per revolution from encoder
  - quadrature encoder w/ A & B signals
  - 1.6A current draw on stall
  - brushed DC motor

## 4 Wheel Drive
- Decimus 4
  - https://micromouseonline.com/2012/05/16/shapeways-motor-mounts-arrive/
  - https://micromouseonline.com/2012/05/24/printed-wheels-complete-decimus-mechanicals/
  - the key is to use ball bearings, spacers, and a screw for a shaft for the wheels to rotate
  - M3 screws and 3mm diameter ball bearings are used for Mouse Unit 07

- Designing Gears
  - the key is to design wheels w/ gears on them
  - more details in mechanical design guide

## Drive Circuit
- Big H-Bridge IC
  - there aren't many high-current H-Bridge IC's, but the TB6561FG brushed motor driver provides 1.5A per motor channel

## Electrical Protection
- Flyback Diodes
  - flyback didoes for motor control: https://www.microtype.io/h-bridge-circuit-design/
  - if the load can be driven both ways, then each wire coming out of the motor needs two diodes
  - 60V 3A flyback diode used to manage the one direction that the motor moves


## Mechanical Micromouse Specs
- calculations we'll consider certain when writing firmware and simulations
- based on (either pretty darn close to or definitely) certain parameters:
  - ServoCity's motor specs
  - gear ratio of 3D printed gears (44:13)
  - diameter of 3D printed wheel (32mm)
  - micromouse wheel to wheel distance (87.56mm)
  - micromouse maze dimensions
    - 165mm per wall, 12mm per pillar

- calculated specs:
  - rising edges (on a single signal, A or B) per wheel revolution: **51.45 rising edges**
  - rising edges (on a single signal, A or B) per maze square: **90.59 rising edges**
  - rising edges (on a single signal, A or B) per 90 degree turn: **35.2 rising edges**
  - top velocity: **8.21m/s**
- **issues w/ above calculated specs**:
  - wheel circumference may be 103mm instead of 100.53mm according to tape measure...
  - wheel to wheel distance varies depending mechanical assembly of spacers, wheel mounts, wheels, etc
  - the motors aren't capable of immediately stopping the wheel upon receiving stop signals, so there's some additional movement after stop is commanded
- **issue solutions**
  - measure and update default values upon building a mouse for:
    - wheel to wheel distance
    - wheel circumference
  - provide method of modifying parameters at runtime
  - decelerate micromouse to a stop to get closer to the target rising edge count
  - slowly accerlate micromouse for similar control at start

```
calculation for rising edges (on a single signal) per wheel revolution:
Rrev = rising edges (on a single signal) per revolution
rpm = rotations per minute
Gr = gear ratio between each wheel and the drive gear (44:13)
Nevents = number of events per revolution from encoder
NeventTypes = number of types of countable events (rising on A, falling on A, rising on B, falling on B)

Rrev = Gr * (Nevents / NeventTypes)
Rev = (44/13) * (60.8077 / 4) = 51.45


calculation for rising edges (on a single signal) per maze square
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
final equation: Rs = (Lw + Lp) * ((Rrev) / (pi * Dw))


calculation for rising edges per 90 turn:
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
final equation: R90turn = ((pi * Dww) / 4) * ((Rrev) / (pi * Dw))

calculation for top velocity:
Vmax = top velocity
rpm = rotations per minute
Cw = wheel circumference

Vmax = (rpm / 60) * Cw
Vmax = (4900 / 60) * 0.10053m = 8.21m/s
```

## Rough Mechanical Calculations
- theoretical calculations based on more uncertain parameters: 
  - coefficient of friction
  - weight of micromouse
- ServoCity's [Premium N20 Gear Motor (5:1 Ratio, 4900 RPM, with Encoder)](https://www.servocity.com/4900-rpm-micro-gear-motor-w-encoder/) provide 4900 RPM, 2 oz-in of torque on stall, and 60.8077 countable events per revolution
- faster motors are fast in exchange for torque, so we need to make sure the motors can still move and accelerate the mouse
- we need enough torque to overcome frictional forces to get the mouse accelerating

```
provided:
4 wheels total
Tm = torque of each motor (2 oz-in of torque = 0.014N-m of torque)
m = mass (micromouse is about 200g, provided 2024 micromouse was ~140g)
Dw = wheel diameter (32mm)
Gr = gear ratio between each wheel and the drive gear (44:13)
Tw = torque of each wheel
u = coefficient of static friction between rubber and wood (0.95)


calculation for torque provided by each wheel:
Tw = (Gr * Tm) / 2
Tw = (44/13)*0.014N-m / 2 = 0.0237N-m


calculation of torque demanded to move micromouse:
F = u(mg)
F = 0.95*(0.2*9.8) = 1.862N
Fw = 1.862N / 4 = 0.466N demanded by each wheel
Tw = 0.466N * 0.032m = 0.0149N-m

we can calculate micromouse acceleration possible w/ the difference of torques


calculation of possible micromouse acceleration:
(Tw leftover) = (Tw provided) - (Tw demanded)
(Tw leftover) = 0.0237N-m - 0.0149N-m = 0.0088N-m

(Fw leftover) = (Tw leftover) / (Dw / 2)
(Fw leftover) = 0.0088N-m / (0.032m / 2) = 0.55N

(F total) = (Fw leftover) * (wheels total)
(F total) = 0.55N * 4 = 2.2N

acceleration possible = (F total) / m
acceleration possible = 2.2N / 0.2kg = 11m/s^2

...higher acceleration is useful for getting to top speed faster
```