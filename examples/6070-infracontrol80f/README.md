# Arduino Simulation: Märklin Digital Infra Control 80f (6070)

This example simulates a Märklin Digital Infra Control 80f (6070) using a Seeed Studio XIAO RP2040. It uses a Samsung IR remote control (BN59-01199F) as the input device to control locomotives and system functions.

## Features

- **XIAO RP2040 Powered**: High-performance MCU with compact form factor.
- **IR Remote Control**: Uses a standard Samsung TV remote to control locomotives.
- **Multi-Master I2C Communication**: Actively sends locomotive commands to the Central Unit (6021).
- **Extended Motorola Format**: Supports f1-f4 and direction indicators.
- **System Control**: Global STOP/GO via remote buttons.

## Software Decoding on Pico 2

For more powerful platforms like the **Raspberry Pi Pico 2**, the IR signal can be decoded 100% in software (e.g., using a library like `IRremote` or custom PIO-based decoders). This allows for even more flexible input handling beyond the basic `pulseIn()` method used in this example.

## Hardware Connections

### 1. IR Sensor Connection
Use a 38kHz IR receiver (e.g., TSOP38238).

| IR Receiver Pin | XIAO RP2040 Pin | Note |
| :--- | :--- | :--- |
| **VCC** | 3V3 | Power from XIAO |
| **GND** | GND | Common ground |
| **OUT** | D0 | IR Signal Input |

#### Alternative Sensors
Instead of an integrated IR receiver, a simple **phototransistor** can be used. This requires a basic circuit with a pull-up or pull-down resistor. For detailed wiring of a phototransistor, refer to the [Samsung Remote Protocol](../../remotes/samsung.md#using-a-phototransistor-simple-setup).

### 2. Power Supply (8V to XIAO)
The Märklin I2C bus provides **8V DC**. The XIAO RP2040's `VIN` (or `5V`) pin is designed for 5V input. Connecting 8V directly will likely damage the board.

**Requirement**: Use a 5V voltage regulator (e.g., **L7805** or a buck converter).

- **Bus 8V (b14/b16)** -> Regulator Input
- **Regulator Output (5V)** -> XIAO RP2040 `VIN` (or `5V` pin)
- **Common GND** -> XIAO GND & Regulator GND

### 3. I2C and Bus Signals (Level Shifting)
The Märklin bus operates at **5V logic**, while the XIAO RP2040 uses **3.3V logic**. The RP2040 pins are **not 5V tolerant**.

**Requirement**: A **Bi-directional Logic Level Shifter** (e.g., based on BSS138) is mandatory for SDA and SCL.

| Signal | Märklin Bus Pin | Level Shifter (High) | Level Shifter (Low) | XIAO Pin |
| :--- | :--- | :--- | :--- | :--- |
| **SDA** | b2 (Right) | HV1 | LV1 | D4 (SDA) |
| **SCL** | b4 (Right) | HV2 | LV2 | D5 (SCL) |
| **STOP** | b6 (Right) | HV3 | LV3 | D1 |
| **GO** | b8 (Right) | HV4 | LV4 | D2 |
| **INIT IN** | b12 (Right) | HV (Special) | LV (Special) | D3 |

> **Note on INIT**: The software addressing (Chain) requires the XIAO to detect and drive the INIT line. Ensure the level shifter supports the bi-directional nature of this protocol.

## Samsung Remote Mapping

Based on the [Samsung Protocol](../../remotes/samsung.md):

| Remote Button | Function |
| :--- | :--- |
| **Power** | System STOP / GO (Toggle) |
| **Volume Up / Down** | Speed Increase / Decrease |
| **Channel Up / Down** | Address Increment / Decrement |
| **Source / Enter** | Direction Change |
| **0-9** | Direct Address Input (Partial implementation) |
| **Color Buttons (R/G/Y/B)** | Functions f1-f4 |
| **Tools / Menu** | Function f0 (Light) |

## References

- [Samsung Remote Protocol](../../remotes/samsung.md)
- [Märklin I2C Datasheet](../../Datasheet_MM1-MM2-Bus.md)
- [Example 6036-control80f](../6036-control80f/)
