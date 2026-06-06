# Keyboard 6040 Simulation

This example demonstrates how to simulate a Märklin Digital Keyboard (6040) using an Arduino.
The Arduino connects to the I2C bus of a Märklin Central Unit (6021 or 6020) and sends solenoid switching commands.

## Pinout Mapping

### Märklin I2C Bus Connection
The connection is made to the **left side** (Federleiste/Socket) of the Central Unit or a previous device in the chain.

| Signal | DIN 41612 Pin (Links) | Arduino Pin | Description |
| :--- | :--- | :--- | :--- |
| **SDA** | b16 | A4 | I2C Data |
| **SCL** | b14 | A5 | I2C Clock |
| **STOP** | b12 | A2 | Stop Signal (Input) |
| **GO** | b10 | A1 | Go Signal (Input) |
| **INIT** | b6 | A0 | Address Chain Signal |
| **8V** | b2, b4 | VIN | Power Supply (+8V DC) |
| **GND** | a2-a16 | GND | Ground |

*Note: Ensure your Arduino can handle 8V on the VIN pin (standard for Arduino Uno, Nano, Mega). The STOP and GO signals are monitored to inhibit commands when the track power is off.*

### Keyboard Address Selection
The keyboard address is set via digital pins D9-D12. Connect these pins to GND (or use DIP switches) to set the bits.

| Pult Nr. | S1 (D9) | S2 (D10) | S3 (D11) | S4 (D12) |
| :---: | :---: | :---: | :---: | :---: |
| 1 | OFF | OFF | OFF | OFF |
| 2 | ON | OFF | OFF | OFF |
| 3 | OFF | ON | OFF | OFF |
| 4 | ON | ON | OFF | OFF |
| 5 | OFF | OFF | ON | OFF |
| 6 | ON | OFF | ON | OFF |
| 7 | OFF | ON | ON | OFF |
| 8 | ON | ON | ON | OFF |
| 9 | OFF | OFF | OFF | ON |
| 10 | ON | OFF | OFF | ON |
| 11 | OFF | ON | OFF | ON |
| 12 | ON | ON | OFF | ON |
| 13 | OFF | OFF | ON | ON |
| 14 | ON | OFF | ON | ON |
| 15 | OFF | ON | ON | ON |
| 16 | ON | ON | ON | ON |

*OFF = Pin High (Open), ON = Pin Low (Connected to GND)*

### Turnout Button Inputs
Connect momentary push buttons between the specified digital pin and **D8** (which acts as a common ground).

| Button | Arduino Pin | Function |
| :--- | :--- | :--- |
| 1 Red | D0 | Turnout 1 Red |
| 1 Green | D1 | Turnout 1 Green |
| 2 Red | D2 | Turnout 2 Red |
| 2 Green | D3 | Turnout 2 Green |
| 3 Red | D4 | Turnout 3 Red |
| 3 Green | D5 | Turnout 3 Green |
| 4 Red | D6 | Turnout 4 Red |
| 4 Green | D7 | Turnout 4 Green |
| Common | D8 | Common Ground for buttons |

**Warning:** Pins D0 and D1 are the hardware Serial pins. Using them for buttons prevents the use of the Serial Monitor and may interfere with uploading new sketches if a button is held down.

## How it works
The Arduino acts as an I2C Master. When a button is pressed, it sends a 3-byte solenoid command packet to the Central Unit (Address 0x7F).

- **Byte 1:** Sender Address (defines the keyboard address).
- **Byte 2:** Data Byte (defines turnout index, direction G/R, and power ON/OFF).
- **Stop Bits:** Handled by the I2C library.

The sketch monitors the **STOP** and **GO** signals from the Central Unit. If the system is in STOP mode (emergency stop), the keyboard will not send command packets until the GO button on the Central Unit is pressed.
