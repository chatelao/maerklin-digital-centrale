# Arduino Simulation: Märklin Digital Control 80 (6035)

This example simulates a Märklin Digital Control 80 locomotive controller using an Arduino. It connects to the classic Märklin I2C bus and can control locomotive speed, direction, and function (f0).

## Features

- **Multi-Master I2C Communication**: Actively sends locomotive commands to the Central Unit (6021/6020).
- **System Control**: Physical buttons for global STOP and GO signals.
- **Software Addressing (Enumeration)**: Supports the Märklin I2C "Chain" addressing protocol to dynamically receive a device address from the Central Unit.
- **Locomotive Control**:
    - Speed control (0, 2-15).
    - Direction change (Speed 1).
    - Function (Fon/Foff).
- **Loco Address Selection**: Buttons to cycle through locomotive addresses 1-80.
- **Two Hardware Variants**:
    - **Analog**: Potentiometer for speed + Button for direction.
    - **Digital**: Rotary Encoder for speed and direction (push-to-change).

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

### User Interface

| Arduino Pin | Function |
| :--- | :--- |
| **D3** | System STOP (Global) |
| **D4** | System GO (Global) |
| **D5** | Function ON (Fon) |
| **D6** | Function OFF (Foff) |
| **D7** | Address UP |
| **D8** | Address DOWN |

## Software Addressing (Enumeration)

Devices connected to the Right side of a Central Unit (6021/6020) are dynamically addressed during system startup. This simulator handles the process as follows:

1. **Wait for INIT**: The device waits for the `INIT IN` signal (D2) to be pulled LOW by the Central Unit or a preceding device.
2. **Capture Address**: It bit-bangs the I2C bus (`SDA`/`SCL`) to read the first byte sent by the Central Unit, which contains the assigned device address.
3. **Acknowledge**: It sends an I2C ACK to the Central Unit.
4. **Chain Signal**: It pulls `INIT OUT` (D12) LOW to signal the next device in the chain that it can now receive its address.

### Bus Chain Connection

To connect multiple simulated Control 80s, connect the `INIT OUT` (D12) of the first Arduino to the `INIT IN` (D2) of the second Arduino.

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
