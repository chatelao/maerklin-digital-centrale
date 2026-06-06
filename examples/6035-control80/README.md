# Arduino Simulation: Märklin Digital Control 80 (6035)

This example simulates a Märklin Digital Control 80 locomotive controller using an Arduino. It connects to the classic Märklin I2C bus and can control locomotive speed, direction, and function (f0).

## Features

- **Multi-Master I2C Communication**: Actively sends locomotive commands to the Central Unit (6021/6020).
- **System Control**: Physical buttons for global STOP and GO signals.
- **Locomotive Control**:
    - Speed control (0, 2-15).
    - Direction change (Speed 1).
    - Function (Fon/Foff).
- **Loco Address Selection**: Buttons to cycle through locomotive addresses 1-80.
- **Two Hardware Variants**:
    - **Analog**: Potentiometer for speed + Button for direction.
    - **Digital**: Rotary Encoder for speed and direction (push-to-change).

## Connections

### Märklin I2C Bus (Left Side / Federleiste)

| Signal | Pin (Links) | Arduino Pin |
| :--- | :--- | :--- |
| **SDA** | b16 | A4 (SDA) |
| **SCL** | b14 | A5 (SCL) |
| **STOP** | b12 | A2 (STOP signal) |
| **GO** | b10 | A3 (GO signal) |
| **8V** | b2, b4 | VIN (Ensure 8V compatibility) |
| **GND** | a2-a16 | GND |

### User Interface

| Arduino Pin | Function |
| :--- | :--- |
| **D3** | System STOP (Global) |
| **D4** | System GO (Global) |
| **D5** | Function ON (Fon) |
| **D6** | Function OFF (Foff) |
| **D7** | Address UP |
| **D8** | Address DOWN |

#### Variant: V-Analog (`#define V_ANALOG`)

| Arduino Pin | Function |
| :--- | :--- |
| **A0** | Potentiometer (Speed) |
| **A1** | Direction Button |

#### Variant: V-Digital (`#define V_DIGITAL`)

| Arduino Pin | Function |
| :--- | :--- |
| **D9** | Encoder Phase A |
| **D10** | Encoder Phase B |
| **D11** | Encoder Button (Direction) |

## Configuration

The hardware variant is selected at the top of the `.ino` file:

```cpp
#define V_ANALOG   // Uncomment for Potentiometer control
// #define V_DIGITAL // Uncomment for Rotary Encoder control
```

## Protocol Details

The Control 80 uses a 4-byte I2C packet to send commands:

1. **Recipient Address**: `0x7F` (Central Unit).
2. **Sender Address**: `0x02` (Controller Address 1).
3. **Locomotive Address**: `0x00` to `0x4F` (Addresses 1-80, where 80 is `0x00`).
4. **Data Byte**:
    - Bits 0-3: Speed (0=Stop, 1=Change Dir, 2-15=Speed steps).
    - Bit 4: Function (1=ON, 0=OFF).
    - Bits 5-7: Command Type (000 for standard loco command).

## References

- [Datasheet: Märklin Digital I2C-Bus](../../Datasheet_MM1-MM2-Bus.md)
- [Data communication on the I2C-Bus (EI2C.md)](../../EI2C.md)
