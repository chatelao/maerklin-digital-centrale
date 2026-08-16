# Märklin Digital Research Results

## First Central Unit
The first central unit was the **Märklin Digital 6020 Central Unit**, introduced in 1985. It served as the brain of the system, receiving commands from controllers and generating the digital track signal.

## Components
- **Control 80 (6035)**: Loco controller for one locomotive address at a time.
- **Control 80f (6036)**: Enhanced version of the Control 80, adding function keys (f1-f4) and support for the new Motorola protocol features.
- **Keyboard (6040)**: Control panel for 16 solenoid accessories (turnouts, signals).
- **Switchboard (6041)**: Feedback and control device.

## The Lateral Bus (Seitenbus)
The devices are connected via a 10-pin connector on the side. This bus is technically based on the **I2C protocol**.

### Bus Pinout (10-pin connector)
Typical pinout for the lateral bus:
1. **SDA** (Serial Data) - I2C data line.
2. **SCL** (Serial Clock) - I2C clock line.
3. **GND** (Ground).
4. **+5V** (Logic supply).
5. **+20V** (Unregulated DC power).
6. **L** (Lok-Daten) - Loco data signal.
7. **K** (Keyboard-Daten) - Accessory data signal.
8. **P** (Programming/Power?)
9. **Reset** - System reset line.
10. **GND** (or similar).

### Protocol Details
- The communication between the controllers (Keyboard, Control 80) and the Central Unit happens over I2C.
- **Keyboards (6040)** use I2C addresses usually in the range of `0x38` to `0x3F` (PCX8574 based or similar logic).
- The Central Unit acts as the I2C Master (or coordinates the bus), polling the devices or receiving data.
- The protocol used on the track is the **Märklin Motorola (MM)** protocol. The lateral bus carries the data which the Central Unit then modulates into the MM signal.
