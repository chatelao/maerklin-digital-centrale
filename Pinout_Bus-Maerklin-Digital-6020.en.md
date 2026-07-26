# Datasheet: Märklin Digital I2C-Bus (MM1 & MM2)

## Overview
This document specifies the data communication of Märklin Digital input devices via the I2C bus. The system utilizes a multi-master architecture where control units (e.g., Control 80f) actively send commands to the central unit and receive feedback.

## Physical Layer

### Interface Pinout
Communication takes place via the side contact strips of the central units (6020/6021) and expansion devices. These are 32-pin connectors according to **DIN 41612 design form B/2**/[EN 60603-2](https://webstore.iec.ch/en/publication/2696) (e.g., ept [102-90065](https://www.ept.de/102-90005TH_de), ept [101-90014](https://www.ept.de/101-90014_de)).

The pin assignment is mirrored between the right side (plug/male connector) and the left side (socket/female connector). For row 'b', the following rule applies: Pin **n** (Right) corresponds to Pin **18-n** (Left).

| Signal | Pin (Left) | Pin (Right) | Description |
| :--- | :--- | :--- | :--- |
| **SDA** | b16 | b2 | Serial data line (I2C Data) |
| **SCL** | b14 | b4 | Serial clock line (I2C Clock) |
| **STOP** | b12 | b6 | Emergency stop signal / Power Off |
| **GO** | b10 | b8 | Operation signal / Power On |
| **INIT** | b6 | b12 | Address chain line (b12) for software addressing |
| **8V** | b4 | b14 | Supply voltage (+8V DC) |
| **8V** | b2 | b16 | Supply voltage (+8V DC) |
| **GND** | a16-a2 | a2-a16 | Common ground (all pins of row 'a') |

- b = top, b1 = left, b16 = right
- a = bottom

### Power Supply and Logic Levels
* **I2C Logic:** The system operates with **5V** logic levels. The SDA and SCL lines should be pulled up to 5V with pull-up resistors (typically 10 kΩ).
* **Power Supply:** The supply voltage on pins b14/b16 (Right) and b4/b2 (Left) is **8V DC**.
* **Power Consumption:** Devices such as the Keyboard 6040 have a significant current consumption of approx. **120 mA** per device.

### Interface Details
The side connectors are used to connect expansion devices. Different sides are used depending on the function:
* **Right Side:** Connection for cabs/control units (Control 80, Control 80f), infrared controllers (Infra Control 80f), and computer interfaces (6050, 6051). Addressing here is done via software using the **b12** chain line.
* **Left Side:** Connection for Keyboards (6040, 6041) and Memorys (6043). These devices are addressed on the hardware side via DIP switches on the back; a chain line is not required here.

### Bus Rules
* **Idle State:** Both lines (SDA, SCL) are at a logical HIGH potential.
* **Level Change:** Data on the SDA line may only change when SCL is LOW.
* **Data Validity:** When SCL is HIGH, the level on SDA must remain stable.
* **Start Condition:** A master pulls SDA to LOW while SCL is HIGH.
* **Acknowledge (Q):** After each byte (8 bits), the receiver sends a LOW bit as an acknowledgment. If this is missing, a stop signal is generated.
* **Stop Condition:** Transition of SDA from LOW to HIGH while SCL is HIGH. In this system, two stop bits are often used for synchronization when changing master/slave roles.

## Addressing and Identification

### Software Addressing (Chain Method)
After powering up or a RESET, devices on the right side (Control 80, Interface, etc.) must be addressed. This is done via a chain line at pin b12.

1. The central unit pulls b12 to LOW for the first device.
2. The device receives its address via I2C, acknowledges it, and pulls b12 to LOW for the next device in the chain.
3. This process continues until all devices are addressed.

![Addressing Sequence](https://kroki.io/plantuml/svg/eNp90bEKgzAQBuA9T3G4lg65bA5FSZbSQgsinVOTIWCtaPT5a6opaaqdAvf_3BeSrLeys8OjJu10msq0srGQcN3YTtZQNsYmIHvg5XdB6NFUGug7FHQ1xDnE1ZDNISOEl7A_TEAK16Gu4U4RzpfbMhY0hSNyKNw1YQe5Up3ue0hoQmRlzSitdr6gvl3YZ6d9b5m75W5Lzk--iRGndLjO67ihY6gjEejbkY4_-txkf3T86GxDZ6HOiGC-Heks1kNmevlMN8p9_QvzcZM1)

### Device Identifiers
Identification of the command type is done using bits 5, 6, and 7 of the device address. The actual device address (0-15) is located in bits 1-4. Bit 0 is usually 0.

**Note on I2C Addressing:** I2C addresses are 7-bit wide by standard. In the Märklin system, however, these addresses are often represented as 8-bit values (shifted left), which corresponds to the actual transmission on the bus (7-bit address + R/W bit).
* The central unit uses the 7-bit address **0x7F**, which appears as **0xFE** in the protocol.
* Keyboard 0 uses the 7-bit address **0x10**, which appears as **0x20** in the protocol.

| Type | Bit 7 | Bit 6 | Bit 5 | Binary Format |
| :--- | :---: | :---: | :---: | :--- |
| Central Unit | 1 | 1 | 1 | `1111 1110` |
| Locomotive Command | 0 | 0 | 0 | `000X XXX0` |
| Solenoid Accessory Command | 0 | 0 | 1 | `001X XXX0` |
| Additional Functions (f1-f4) | 0 | 1 | 0 | `010X XXX0` |

### Address Byte Structure
![Address Byte](https://kroki.io/wavedrom/svg/eNqrVlAqSk1XslKI5lJQqFbKS8xNBXKUDJR0FJSSMkuKgRxDIDOxpKQIJB6UWpxaVJaaolSrg6LeMSWlKLW4WEHDJ9hJT8832EkTyQATJANcUssyk1MVYOoN9PQMTdEN83RB0myMpNnAwEDBFqY3My9dqZYrFiidnJ-XlgnyQzVMkwVQNCcxLxXs_NpaLgA8tz9J)

## Protocol Specification and Command Sets

### Communication Flow
Commands are transmitted in packets of 3 to 4 bytes. Since this is a multi-master system, the sending device temporarily assumes the master role.

![Communication Flow](https://kroki.io/plantuml/svg/eNp9klFLwzAUhd_zKy57amEO1D31Qba1gsMNh6H4HNPbLpglJb2d7N9701VxIntKuDnf6elJFh2pQP3BipZXo02rHMFEoqswQCKtOiKoDraqIwzpJO7lpTZHR0FZKJ0hSM7CQRbZM5GXQjhPCP7IZ3LKgwzWlUWQpHicyHwzBVks4ck0-1RIuHkAmcGut3YYb17eWBSjjofRYHVi9DaDV-QohlPAsqoCdh0keZmKvBxdlvnzH-gug_EPf4gCj0bjVeo-g0KRggRnzQwK1P7b4So2v8Bki1j9p-e9JN_CylCM4_v3oR6e1J47OzmdihGL1rvgdQy-dh2FXpPx7pep_nD-02LV4CH2smWlarjn-RCpS8-3EbhsAl8Pho967yF-iW-kj761FwsuKb6NL4gFpQI=)

### Locomotive Commands (Standard H0 Mode)
Used for standard Motorola decoders (MM1).

* **Packet Length:** 4 bytes (Receiver, Sender, Decoder Address, Data Byte)
* **Address Range:** 00 to 79 (Address 80 is transmitted as 00)

![Loco Command H0](https://kroki.io/wavedrom/svg/eNpdj8sKwjAQRff9iiErCyE2PkCELCzSlYpYd-Ii1rEGNaltKkjpv5sWhOhuXvfcOw2QEnMyh0MA0BAtH-gakhaI5-HWVDBYpTFj6zQOCQVyUrZy-4krpbVldxqJ1JqCAhdLVVIYMcanoteTlv5AE4_APUJS68wqo52Xyq82_Nft3wV60rFvHkVih88aK-sScC42mEurXgiL7Eba4OhuM6Mvqnux-RJmbnqXGvsgbRt8AHspSKQ=)

### Locomotive Commands (Extended Motorola Format / MM2)
Supports absolute direction of travel and forced address takeover.

![Loco Command MM2](https://kroki.io/wavedrom/svg/eNpdkE2LwjAQhu_9FUNOLYSaqAuLkEOL9KSybPcgyB5iOtagJlqzyFL63526LFRP8_28L9MCa7BmM9hEAC1z-oRUsPKMWI0-_BXiRZmn6bLME8aBbW240nxKqQ6h6VeFmqOujt4cOEg1tw2HcZrKN_VgsI4_gYsBRQ4oxY8zwXpHerbeh-T17uv3jIPTydCAkOoTL6Qu1oosZ-YA8XomVK7_PBW3KqEohVphnfU9QXnhG4Osi74JZbzb2f4L7b_AO3WP2uHDZ9dFd-YyUWM=)

### Additional Functions (f1 to f4)
Commands for controlling special functions.

![Function Command](https://kroki.io/wavedrom/svg/eNqrVlAqSk1XslKI5lJQqFbKS8xNBXKU0gyVdBSUkjJLioE8w1odVEkjfJLG-CRN8EiG5pUWp6YgKTABMhNLSopAko455YmVxQoGSrVcsUDh5Py8tTyQs6thii2AojmJeakQk2u5AALGOdw=)

### Solenoid Accessory Commands (Turnouts/Signals)
* **Packet Length:** 3 bytes
* **Data Byte:** Contains output number (Bits 1-2), direction (Bit 0), power (Bit 3), and section address (Bits 4-5).

![Solenoid Accessory Command](https://kroki.io/wavedrom/svg/eNp1kM0KgkAQgO8-xTBnEa1LBB4EoeNG0Sk6bO4YC7rG7oqE7Ls3BoH9eJu_b75hRkBLN9zCOQIY0ciWOMFSW4wBr9o7TjMOpfd26qT5gVQMWb6zRAZD_MGJ3s-41YwrqeoUWeCJe-8hTZL1N7wflqWiriep-DEeqVowcsfrzkChlCXn_ipPpnekFhYUzSAfzGGILlyuOlPr6VXje3jD1UYaep0bQvQEMkhb2w==)

## System Behavior and Special Functions

### Differences between Central Unit (6020) vs. Control Unit (6021)
* **Central Unit 6020:** In STOP mode, the bus is blocked after the first byte (SCL/SDA at LOW) until switching back to GO mode.
* **Control Unit 6021:** Uses the extended Motorola format (MM2) when configured via the corresponding DIP switch setting.

### Undocumented Functions (6021)
These functions are accessible via address entry on the control unit (only in MM2 format):

* **91 + 93:** Clear the refresh memory and set all directions to "forward".
* **92 + 93:** Include all 80 locomotive addresses in the refresh cycle.
* **94 + 93:** Software version test (LED blinks).
* **97 + 93:** Restore last operating state (Recall).

## Appendix: LocoNet Interface
In addition to the I2C bus, some newer components (such as the connect6021 light) also support the LocoNet interface.

### LocoNet Pinout (RJ12)
View of the socket from above, pins from 1 to 6:

| Pin | Signal | Voltage (typ.) | Description |
| :--- | :--- | :--- | :--- |
| 1 | **PWR** | +8V to +12V | Power supply (RailSync+) |
| 2 | **GND** | 0V | Ground |
| 3 | **DATA** | +10V to +14V | LocoNet data line |
| 4 | **DATA** | +10V to +14V | LocoNet data line |
| 5 | **GND** | 0V | Ground |
| 6 | **PWR** | +8V to +12V | Power supply (RailSync-) |

*Note: The voltage levels on the DATA lines can vary depending on the central unit (e.g. Intellibox).*

## Device Overview
A detailed overview of the most famous devices of the classic Märklin Digital system (60xx series) and their functions can be found in the separate [Device Overview](Geraeteuebersicht.md).
