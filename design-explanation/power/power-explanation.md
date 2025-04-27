# Power Design Explanation
Notes regarding motherboard power design choices and specs.

## Vacuum Power
- ~2A is ideal for a 8520 quadcoptor motor
  - experiment done here: https://notblackmagic.com/projects/motor-test-stand/
- TI generated circuit: https://webench.ti.com/appinfo/webench/scripts/SDP.cgi?ID=3EACC4ED5253923B
  - 3V7, 2A circuit

## Wheel Motor Power
- ServoCity's [Premium N20 Gear Motor (5:1 Ratio, 4900 RPM, with Encoder)](https://www.servocity.com/4900-rpm-micro-gear-motor-w-encoder/) demand 1.6A on stall, and 12V nominal
- TI generated circuit tool: https://webench.ti.com/appinfo/webench/scripts/SDP.cgi?ID=AA12043C39DD7B4B
  - 12V, 3A circuit

## IR Sensor Power & Processor Power
- both 3V3 and 5V step-down regulators were picked out by hand
- schematics were designed w/ the TI datasheets

## Battery Selection
  - smallest form factor 2S LiPo battery chosen on Amazon

- Current Draw
  - most RC car LiPo batteries are capable of providing high current
  - w/ rough math, we find that we need at least 7A to comfortably drive the micromouse
  - LiPo batteries' capacity multiplier tells us how much current the battery can safely discharge continuously
  - 900 mAh 30C means 27A max current draw
  - 900 mAh at 7A current draw means 7.7 minutes of activity
- Rocker Switch
  - many rocker switches don't provide DC current limits when current you're dealing w/ is high...
  - we're going for a switch that safely operates w/ 15A AC, and hoping that it's sufficient
```
total current draw calculation:
2A for vacuum
1A for MCU
  30mA per LED * 4 + MCU = 120mA
  174uA per MHz, * 50MHz = 8.7mA
1A for IR sensors
  22mA per sensor * 4 = 88mA
3A for 12V motors
  1.5A for each motor
= 7A total


total current dischargeable calculation:
900 mAh, 30C rating
900 mA * 30 = 27A dischargeable continuously


micromouse active time calculation:
900 mAh, 7A draw max
0.9Ah / 7A = 7.7 minutes

```

## Power Management
  - Op-Amp Comparator Configuration
    - minimal circuit w/ 1 IC and resistors
    - takes input battery voltage, and compares it to desired low battery voltage
    - output result of comparator must be scaled to match MCU high/low logic 
      - voltage divider calculator: https://ohmslawcalculator.com/voltage-divider-calculator
    - 3.74k Ohm resistor chosen for R2 to get 3.2V max from comparator output
    - 2S LiPo batteries are considered dead when they reach 6.4V-6.6V, so low voltage of 6.5V chosen
    - 100k and 118k resistors chosen for R1 and R2 to get 6.49V on 2nd comparator input
```
voltage divider for 2nd low battery compare signal 
12V input, 100k for R1 (from example schematic on op-amp datasheet), 6.5V output
R2 = 118k

voltage divider for result signal:
12V input, 10k for R1 (arbitrarily recycled resistor), 3.3V output
Vout = Vin * (R2 / (R2 + R1))
R2 = 3.793k
```
  - Enable Signal
    - every switching regulator, except the 3V3 regulator, has an enable signal that can be toggled by the MCU

## Electrical Protection
  - Battery to Regulator Input Diode
    - Added to prevent reverse current from regulator to battery
    - 1V voltage drop, 6A standard rectifier between battery and all switching regulators
  
  - Fuse
    - 10A fuse for entire mouse, provided a rough 7A consumption max
    - 125% of circuit's normal operating current is good rule of thumb
  
  - Bulk Capacitor
    - 1.2mF 16V bulk capacitor for entire mouse
    - good rule of thumb is:
      - 100uF per A of max load current for general cases
      - 200~470uF per A for high-power and noisier circuits

## Archived Ideas
- Full-on BMS Circuit
  - would be cool to get battery SOH and SOC w/ columb counting IC, but requires more hardware and involved schemes
  - archived due to complexity

- Current & Voltage Monitoring
  - requires more pins from MCU and extra hardware (shunt resistors, sensing IC's)
  - archived due to complexity


