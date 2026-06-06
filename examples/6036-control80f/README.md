# Arduino Simulation: Märklin Digital Control 80f (6036)

This example simulates a Märklin Digital Control 80f locomotive controller using an Arduino. It extends the Control 80 (6035) with support for extra functions f1-f4 and absolute direction indicator (via protocol initialization).

## Features

- **Multi-Master I2C Communication**: Actively sends locomotive commands to the Central Unit (6021).
- **Extended Motorola Format**: Supports the 6021 extended protocol for functions f1-f4.
- **System Control**: Physical buttons for global STOP and GO signals.
- **Software Addressing (Enumeration)**: Supports the Märklin I2C "Chain" addressing protocol.
- **Locomotive Control**:
    - Speed control (0, 2-15).
    - Direction change (Speed 1).
    - Function f0 (Light).
    - **Extra Functions f1-f4**.
- **Loco Address Selection**: Buttons to cycle through locomotive addresses 1-80.
- **Two Hardware Variants**:
    - **Analog**: Potentiometer for speed + Button for direction + Buttons for f3/f4.
    - **Digital**: Rotary Encoder for speed and direction + Buttons for f3/f4.

## Connections

### Märklin I2C Bus

| Signal | Pin (Right) | Pin (Left) | Arduino Pin |
| :--- | :--- | :--- | :--- |
| **SDA** | b2 | b16 | A4 (SDA) |
| **SCL** | b4 | b14 | A5 (SCL) |
| **STOP** | b6 | b12 | A2 (STOP signal) |
| **GO** | b8 | b10 | A3 (GO signal) |
| **INIT IN** | b12 | b6 | D2 |
| **INIT OUT** | - | - | D12 (Chain) |
| **8V** | b14, b16 | b2, b4 | VIN (Ensure 8V compatibility) |
| **GND** | a2-a16 | a2-a16 | GND |

### User Interface (General)

| Arduino Pin | Function |
| :--- | :--- |
| **D0** | **Function f1** (Note: Conflicts with Serial RX) |
| **D1** | **Function f2** (Note: Conflicts with Serial TX) |
| **D3** | System STOP (Global) |
| **D4** | System GO (Global) |
| **D5** | Function f0 (Light) ON |
| **D6** | Function f0 (Light) OFF |
| **D7** | Address UP |
| **D8** | Address DOWN |

> **⚠️ WARNING**: Pins **D0** and **D1** are used for functions f1 and f2. This prevents the use of Serial communication (Hardware Serial) and may interfere with sketch uploads if buttons are held down.

#### Variant: V-Analog (`#define V_ANALOG`)

| Arduino Pin | Function |
| :--- | :--- |
| **A0** | Potentiometer (Speed) |
| **A1** | Direction Button |
| **D9** | **Function f3** |
| **D10** | **Function f4** |

#### Variant: V-Digital (`#define V_DIGITAL`)

| Arduino Pin | Function |
| :--- | :--- |
| **D9** | Encoder Phase A |
| **D10** | Encoder Phase B |
| **D11** | Encoder Button (Direction) |
| **A0** | **Function f3** |
| **A1** | **Function f4** |

## Protocol Details

### Initialization
The 6036 sends a special 3-byte packet to the Central Unit (6021) to enable the Extended Motorola Format:
`[0x7F] [0x80] [0x6F] [0x40]` (7-bit address 0x7F is 8-bit 0xFE).

### Locomotive Commands
Uses a 4-byte I2C packet. Bit 5 of the data byte is set to `1` to indicate a "Request" in Extended Motorola format.

### Function Commands (f1-f4)
Uses a 4-byte I2C packet with a modified sender address:
1. **Recipient Address**: `0x7F` (Central Unit).
2. **Sender Address**: `0x40 | (Original Assigned Address)`. (Identifier `010` in bits 5-7).
3. **Locomotive Address**: `0x00` to `0x4F`.
4. **Data Byte**:
    - Bit 0: f1
    - Bit 1: f2
    - Bit 2: f3
    - Bit 3: f4
    - Bits 4-7: Always 0.

## References

- [Datasheet: Märklin Digital I2C-Bus](../../Pinout_Bus-Maerklin-Digital-6020.md)
- [Data communication on the I2C-Bus (EI2C.md)](../../EI2C.md)
