![image](http://www.drkoenig.de/digital/bahn7.gif)

### ![Dr. König´s Märklin-Digital-Page](http://www.drkoenig.de/digital/mk2.gif)

![image](http://www.drkoenig.de/digital/bahn8.gif)

## Data communication on the I2C-Bus

---

_This documentation was made by Mr. Walter Fiedler, Thüringer Straße 22, 63329 Egelsbach. Because he does not has Internet-access he has choosen this way of publishing.

The translation was made by [Matthew Romer](MAILTO:mromer@onlink.net).

Neither I can comment this documentation nor I can answer questions; so please contact Mr. Fiedler - or in case of problems with the translation Mr. Romer - directly. My part of this pulbication is limites to the WWW-adapting ; I did not change the content or it´s translation in any way. You can download the [original](http://www.drkoenig.de/digital/i2c.zip) and it´s [translation](http://www.drkoenig.de/digital/ei2c.zip). So I am not responsible for the content of this documentation and any results and consequences of it´s usage._

---

### Contents

* [Introduction](#introduction)

* [The I2C-Bus](#the-i2c-bus)

* [Identifying devices in the Märklin System](#device-identifications-with-the-mrklin-digital-system)

* [Addressing of the control modules](#addressing-of-the-control-modules)

* [Initialization of the control modules](#initialization-of-the-controllers)

* [Controlling locomotives in the H0-Modus](#control-of-locomotives-in-the-h0-modus)

* [Controlling locomotives with extended Motorola format](#control-of-locomotives-with-extended-motorola-format)

* [Controlling locomotive functions](#transfer-of-function-instruction)

* [Controlling solenoid accessories](#transfer-of-switch-adjusting-commands)

* [Operation with Interfaces (6050 or 6051)](#operation-with-interfaces-6050-or-6051)

* [Differences in the communication flow between Central Unit (6020) and Control Unit (6021)](#differences-in-the-communication-flow-between-central-unit-6020-and-control-unit-6021)

* [Undocumented functions for the Control Unit (6021)](#undocumented-functions-for-the-control-unit-6021)

* - [Erase previously stored data](#data-delete-input--91--and--93-)

* - [Put all 80 addresses through a Refresh cycle](#all-80-addresses-in-refresh-cycle-take-up-input--92--and--93-)

* - [Version test](#version-test-input--94--and--93-)

* - [Recall the last operating condition](#recall-the-last-operating-condition-input--97--and--93-)

### Introduction

This document describes the data exchange of the Märklin Digital input devices which takes place over the I2C-Bus which is integrated in the side lateral plug connectors. The possibilities for the I2C-Bus are unlimited, but this document will focus on the switching and control commands for the different operating situations of the Märklin Digital-Systems.  All specifications concerning the instruction format refer to the operation of the Digital-Systems and the Control Unit (6021) as Central Unit. Some the specifications in the comparison of the Central Unit (6020) may look different please refer to the section "Differences in the communication flow between Central Unit (6020) and Control Unit (6021)".

Information published in this document was obtained with the help of additionally connecting homemade electronic circuits with counters and shift registers to the I2C-Bus. Since no special measuring instruments were used such as oscilloscope or the like, predications about the respective temporal behavior are unknown (e.g. clock frequency or the like).

Note:

At some places in this document references are made to the driving direction. It is to be noted that only newer delta or digital decoder (with ICs of the type 701.17, 701,21 and 701,22) are able to interpret this absolute direction of travel information.  All older decoders (with ICs of the type ZyMOS and 701,13) do not understand this absolute direction of travel information, but modify the driving direction only by the switch " Drive position " " 1 ".  Therefore it can occur with these older decoders that the driving direction displayed in the controllers control 80f (6036) and Infra control 80f (6070) do not correspond with the actual driving direction of the decoder.

I will not be held responsible for any damage that may occur from the use of the information contained in this document.  You are to use this information at your own risk.

### The I2C-Bus

The I2C-Bus places bi-directional, serial data communication equipment between one or more so-called Master System and one or more Slave System.  Märklin digitally uses a so-called "Multi-Master System", i.e. that different devices (e.g. the control 80f (6036)) between transmitting switching or control instructions and the receipt of the pertinent acknowledgement message of the Slave operation on master operation switches.

Note:

In the examples of switching or control requests two stop bits are indicated. These two stop bits are created by switching a device from a Slave operation to a Master operation, resulting in a normal stop bit.  The two stop bits are also used to check whether a certain device actually adapts to another operating mode. This does not apply to the control 80 (6035) module.

On the hardware side the I2C-Bus consists of two lines:

* SCL, serial Clock = timing clock line (controlled by the master)

* SDA, serial DATA = serial data line (bi-directional).

These two lines are used to communicate with the Märklin Digital devices, contact strips on pin b4 (SCL) or on pin b2 (SDA) that are attached on the right of the central processing unit.  These devices include the control 80 (6035), control 80f (6036), Infra control 80f (6070) as well as the INTERFACE (6050 or 6051).  The digital devices which are attached to the left of the central processing unit via the contact strips on pin b14 (SCL) or on pin b16 (SDA) include the keyboard (6040), SWITCH board (6041) or the SWITCH board 2000 of the company SES and the MEMORY (6043).

The following rules generally applies with the I2C-Bus:

* In a state of rest both lines are at a logic high potential.

* Only if the clocking line SCL is at a logic low potential, may the data on the SDA line change levels.

* If the clocking line SCL is at a high potential, the level of the data line SDA remains stable, allowing the receiving device to read the data on the data line SDA.

* When a transfer is about to initiate, the transmitting device pulls the data line SDA to a logic low potential when SCL = high.  Resulting in the master device to generate a clock pulse on the line SCL.

* The first byte during the transfer always indicates the recipient address, the second byte the sender address.  Afterwards two more bytes will follow with the Märklin Digital-System depending upon device or depending upon instruction type in the data bytes.

* After 8 bits = 1 byte is transmitted the recipient in each case transmits one bit = low as an acknowledgement. If this acknowledgement is missing, or the transfer is interrupted, a bit = low is transmitted as a stop signal.  Afterwards both lines go again on quiescent level (both lines high).

* After the receipt of a switching or a control instruction the Control Unit sends an acknowledged instruction.

* After the Control Unit acknowledged the execution of an instruction with an acknowledgement message, both lines (SDA and SCL) go again on quiescent level (both lines high).

### Device identifications with the Märklin Digital-System

So that the Märklin Digital-System can differentiate which type of switching or control instructions are being transmitted, the different types of devices use different identifiers in the respective device address, in the bits 5, 6 and 7. The actual device address is indicated in the bits 1, 2, 3 and 4. Bit 0 is always " 0 " (exception: Switching commands for extra functions " f1 " to " f4 ", when transmitted over the INTERFACE (6050 or 6051)).

The individual device identifications read (XXXX = Device address within the area 0 to 15):

Control Unit

1111 1110

Locomotive instruction

000X XXX0

Switching commands for solenoid devices

001X XXX0

Switching commands for extra functions " f1 " to " f4 " of control 80f (6036)

010X XXX0

Switching commands for extra functions " f1 " to " f4 " of INTERFACES (6050 or 6051)

0100 0001

### Addressing of the control modules

After turning the Digital-Systems on or after a RESET the devices attached on the right side of the central processing unit must be addressed via software.  These devices include control 80 (6035), control 80f (6036), Infra control 80f (6070) and INTERFACE (6050 or 6051).  During the addressing procedure a chain line between the devices is used so that each device can be individually configured.  This is accomplished by connecting pin b12 from contact strip of the central unit to the contact strip pin b12 of the first device attached to the right side of the central unit.  From the processor of this device again a line goes over pin b12 to the next device.

After a RESET these lines read first a high potential.  At the beginning of the initialization phase the central unit pulls this line on pin b12 to a logic low, generates a start condition on the I2C-Bus and sends the first address, address " 1 ".  The first attached device acknowledges the received byte with a bit " 0 " and pulls the line on pin b12 for the next unit to a low potential.

The central unit generates another start condition and sends the next address.  This process continues until all available addresses (15 addresses with central unit 6020 or 10 addresses with control unit 6021) are assigned or until the acknowledgement bit remains at a logic level high.  With the central unit 6021 the controller built into it receives the address " 1 ".

Note:

For the third quarter 2000 there will be a new keyboard (6040) from Märklin.  These devices are able to immediately display the current settings for each accessory; by adjusting the DIP switches on the back of the keyboard.  This allows for the display of all possible 256 accessory settings.

Hereunder applies: If several of these new devices are attached to a central unit, the central unit always assigns all available addresses, independently of how many devices of the types specified above are actually attached. That is because of the fact that these new keyboards (6040) acknowledge each byte, which will transfer on the I2C-Bus with an acknowledgement bit. This behavior does not disturb however by any means with other communication within the Digital-Systems.

The devices such as key board (6040), SWITCH board (6041) or the SWITCH board 2000 of the company SES, attached left to the central processing unit, do not need to be addressed by software. With these devices the addressing is done via hardware by the DIP switches on the back of the units.

Here is an example of the software related addressing. In addition to the built in controller of the control unit (6021) there are two more devices, which are connected to the control unit (6021). Thus altogether four addresses will be assigned, but only three devices are available and acknowledge the receipt of an address (Q = acknowledgement bit).

Structure of the addressing bytes:

```

Address 		Address 		Address 		Address
0000 0010	0	0000 0100	0	0000 0110	0	0000 1000	1
Device 1	Q	Device 2	Q	Device 3	Q	Device 4	Q

```

### Initialization of the controllers

Still after this addressing the controllers control 80f (6036) and Infra control 80f (6070) must be initialized.  Depending on which control unit you have (6020 or 6021) determines whether the direction indicators integrated in the address displays are operated or not; and whether the address input for functions permits the range from " 01 " to " 99 " or only the range from " 01 " to " 80 ".  The address range of " 01 " to " 99 " was used for the 2-Rail-Digital-System at that time (DCC format for H0 and 1 Gauge). With the control unit (6021) the addresses are greater than " 80 " are used for special internal system functions (see paragraph "Undocumented functions for the Control Unit (6021)" at the end of this document).  To initialize all of these devices mentioned, a special instruction is transmitted to all devices connected to the right of the central unit. If unit (6021) is set for extended Motorola format (switch 2 at the rear side the control unit (6021) switched " ON "), these instructions are completely acknowledged.

Initialization attempt for extended Motorola format:

```

Recipient 		sender 			data byte 		data byte 		stop bit
1111 1110	0	1000 0000	0	0110 1111	0	0100 0000	0	10
Central unit	Q	Special addr.	Q	Decimal 111		Q		Q

```

The complete acknowledgement reads:

```

Recipient 		sender 			data byte 		data byte 		stop bit
1000 0000	0	1111 1110	0	0110 1111	0	0100 0000	0	0
Special addr.	Q	Central unit		Q	Decimal 111	Q		Q

```

If the control unit (6021) is in the H0-Modus (switch 2 at the rear side switched " OFF "), or the controllers control 80f (6036) or Infra control 80f (6070) are connected to the central unit (6020), the first initialization attempt is not recognized resulting in an incomplete acknowledgement.

This incomplete acknowledgement reads:

```

Recipient 		stop bits
1000 0000	0	0
Special addr.	Q

```

Thus the central unit does not accept this operating mode of the controllers.

The controllers control 80f (6036) and Infra control 80f (6070) transmit another initialization code to the central unit, for which each sending address the respective device address is indicated.

Initialization for H0-Modus:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	000X XXX0	0	0110 0011	0	0000 0000	0	10
Central Unit 	Q 	device addr.	Q	decimal 99	Q			Q

```

The acknowledgement for it reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0110 0011	0	1110 0000	0	0
Device addr.  	Q 	Central Unit	Q	decimal 99	Q			Q

```

Thus the devices control 80f (6036) and Infra control 80f (6070) are initialized.

By the link between these devices and the central unit, the central unit transmits first continuously a locomotive module instruction with (genuine) the decoder address " 80 " (this corresponds at a locomotive decoder all eight switches placed on " OFF ") and the data byte " 0 " to the track (Idle State). Thus one avoids, by negative DC voltage the locomotives briefly jerking while resting against the track (stop state) when switching accessories.

Only if at a controller or at the INTERFACE another valid locomotive decoder address is input, the genuine decoder address " 80 " (Idle State) is no longer transmitted to the track.

### Control of locomotives in the H0-Modus

If with the control unit (6021) the switch present at the rear side 1 and 2 are placed on " OFF ", this central unit is in the (old) H0-Modus and behaves as far as possible like the central unit (6020).

For the transfer of locomotive decoder instruction, four bytes are needed as control request. These bytes are comprised of recipient (central unit), controller number (1 to 15 with central unit (6020) or 1 to 10 with control unit (6021)), decoder address (range from " 00 " to " 79 ", address " 80 " as " 00 " transferred) and a data byte.

The control request looks identical in this operating mode for the central unit and all controllers, which includes the control 80 (6035), control 80f (6036), Infra control 80f (6070) and INTERFACE (6050 or 6051).

The individual bits in the data byte are designated as follows:

```

- Bit 0 to 3 	 = drive position (0=Stop, 1=change direction, 2 to 15=speed)
- Bit 4		 = direction of travel dependent auxiliary function " function "
- Bit 5 to 7	 = 000 = request or positive acknowledgement
		 = 111 = negative acknowledgement, address invalid or already occupied.

```

Control request for locomotives in the H0-Modus:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	000X XXX0	0	0XXX XXXX	0	000X XXXX	0	10
Central Unit	Q 	device addr.  	Q 	00 to 79 	Q 	drive position	Q

```

If this control request is accepted, then the acknowledgement reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0XXX XXXX	0	000X XXXX	0	0
Device addr.	Q	Central Unit	Q	00 to 79	Q	drive position	Q

```

If the control request is not accepted e.g. with occupied decoder address, then the acknowledgement message from the central unit reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0XXX XXXX	0	111X XXXX	0	0
Device addr.	Q	Central Unit	Q	00 to 79	Q	111=occupied	Q

```

Note:

Even if the control unit (6021) is adjusted to the extended Motorola format (switch 2 at the rear side of the central unit is switched " ON "), the control requests of control 80 (6035) and INTERFACE (6050 or 6051) as well as the pertinent acknowledgement messages during more accepted and not accepted control requests are exactly the same from the appropriate messages in the H0-Modus described here.

### Control of locomotives with extended Motorola format

If the control unit (6021) is adjusted to the extended Motorola data format (switch 2 at the rear side is switched " ON "), then the controllers control 80f (6036) and Infra control 80f (6070) are able to display the driving direction and the possibility to force a transfer of a locomotive address from another controller. These possibilities are only available on the above-mentioned controllers and only in this particular operating mode of the central processing unit.  The following controllers, control 80 (6035) and INTERFACE (6050 or 6051) will always behave in the H0-Modus mode.

The individual bits in the data byte mean in the extended Motorola format:

```

- Bit 0 to 3	= drive position (0 = deadlock, 1 = change direction of travel, 2 to 15 = speed)
- Bit 4 	= direction of travel dependent auxiliary function " function "
- Bit 5 to 7 	= 001 = request
		= 10X = positive acknowledgement, X = 0 driving direction backwards, X = 1 forward
		= 110 = negative acknowledgement, address invalid or already occupied.
		= 010 = request " force transfer "

```

Data communication with control 80f in the extended Motorola format, control request:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	000X XXX0	0	0XXX XXXX	0	001X XXXX	0	10
Central unit	Q 	device addr.  	Q 	00 to 79 	Q 	drive position	Q

```

The acknowledgement for it, if the request is accepted, reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0XXX XXXX	0	10XX XXXX	0	0
Device addr.	Q	Central unit	Q	00 to 79	Q	drive position	Q
									Direction

```

If another controller already occupies the requested address, a special acknowledgement of the central unit is returned.  The fourth byte contains the controller's address of which the locomotive address is already called instead of the drive position information.  This device address is indicated in such a way so that the sender or the recipient is able to decipher the information:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0XXX XXXX	0	110X XXX0	0	0
Device addr.  	Q 	Central unit 	Q 	00 to 79 	Q 	occupies of	Q
									Device addr.

```

At the controller with the flashing address display if the same address is again entered, the address is taken over on this device and on the previous device that already occupied the address.

This special control request reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	000X XXX0	0	0XXX XXXX	0	010X XXXX	0	10
Central unit	Q 	device addr.  	Q 	00 to 79 	Q 	drive position	Q
									Transfer control

```

An acknowledgement from the central unit, which accepts this request, follows:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0XXX XXXX	0	10XX XXXX	0	0
Device addr.	Q	Central unit	Q	00 to 79	Q	drive position	Q
									Direction

```

### Transfer of function instruction

For the transfer of function instruction, four bytes are needed in the switching request.  These bytes are comprised of recipient (central unit), controller number (1 to 15 with central unit (6020) or 1 to 10 with control unit (6021)), decoder address (with control unit in the H0-Modus within the range of " 00 " to " 79 ", in the other modes and with central unit (6020) within the range of " 00 " to " 99 ", whereby the incoming address will transfer " 80 " in all operating mode as address " 00 ") and the byte for the status of the functions, whereby the functions are indicated in the bits 0 to 3 (" 0 " = off, " 1 " =on):

* Bit 0 = Function "f1"

* Bit 1 = Function "f2"

* Bit 2 = Function "f3"

* Bit 3 = Function "f4"

The bits 4 to 7 are so far not used and are always " 0 ".

Note:

With the control unit (6021) decoder addresses are transmitted starting from " 81 " not to the track but to serve (partly) to the call of special system functions of the central unit. See in addition also the paragraph " Undocumented functions for the Control Unit (6021) " at the end of this document.

Structure of the switching request for function instruction:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	010X XXX0	0	0XXX XXXX	0	0000 XXXX	0	10
Central unit	Q 	device addr.  	Q 	00 to 79 or	Q 	f1 to f4	Q
						00 to 99

```

The acknowledgement of the central unit reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
010X XXX0	0	1111 1110	0	0XXX XXXX	0	0000 XXXX	0	0
Device addr.	Q	Central unit	Q	00 to 79 or	Q	f1 to f4	Q
						00 to 99

```

Since addresses for function decoders can be called also with several devices at the same time, no acknowledgement message with e.g. address already occupied can occur here.

### Transfer of switch adjusting commands

For the transfer of switch adjusting commands three bytes are sufficient for the switching request.

These bytes are comprised of recipient (central unit), Keyboard number (0 to 15) and the data byte.

The data byte contains the specification of the decoder output number (bit 0 to 3) and the decoder section address (bit 4 and 5).

With bit 0 the switching direction (0 = red, 1 = green) is selected, and bit 3 determines if power is on or off for the selected contact.

Since the keyboard (6040) can address four decoders at any given time, the bits 4 and 5 determine which group of four the keyboard is responsible for in sending the switching commands.

With the knowledge of the real decoder address (in the binary format of numbers) these two bits represent the bits 0 and 1.  The four bits of the keyboard address form then the bits 2 to 5 of the decoder address.  This decoder address is increased still by 1, since the decoder addressing in the Märklin Digital-System always begins with the address " 01 ".  Thus max. 64 decoders can be addressed within the range of " 01 " to " 64 ".

Structure of the data byte:

* Bit 0 = Switching direction, 0 = red, 1 = green
* Bit 1 = Decoder output LSB (Least Significant Bit)
* Bit 2 = Decoder output MSB (Most Significant Bit)
* Bit 3 = Current on contact, 0 = off, 1 = on
* Bit 4 = Decoder section address LSB
* Bit 5 = Decoder section address MSB

Structure of the switching request:

```

Recipient 		sender 			data byte 		stop bit
1111 1110	0	001X XXX0	0	00XX XXXX	0	10
Central unit	Q	device addr.	Q			Q

```

The acknowledgement of the central unit reads:

```

Recipient 		sender 			data byte 		stop bit
001X XXX0	0	1111 1110	0	00XX XXXX	0	0
Device addr.	Q	Central unit	Q			Q

```

If the central unit is however in the " stop" mode, the receipt of the switching request is only shortened acknowledged:

```

Recipient 		stop bits
001X XXX0	0	0
Device addr.	Q

```

During this state the keyboard (6040), SWITCH board (6041) or MEMORY (6043) regularly transmits a new switching request to the central unit (if one is selected from the above mentioned controllers), until the central unit is in the " go" mode and the switching request is completely acknowledged.

Only when the switching request is completely acknowledged, the display in the keyboard (6040) is updated.

Once the appropriate key is released at the keyboard (6040), the keyboard (6040) will send a power-off instruction to the central unit.  In the data byte the four bits of the decoder output number (bit 0 to 3) are reset. The two bits for the decoder section address (bit 4 and 5) must remain unchanged thereby.

Switching request for power-off instruction:

```

Recipient 		sender 			data byte 		stop bit
1111 1110	0	001X XXX0	0	00XX 0000	0	10
Central		Q	device addr.	Q			Q

```

The acknowledgement of the central unit reads:

```

Recipient		sender			data byte		stop bit
001X XXX0	0	1111 1110	0	00XX 0000	0	0
Device addr.	Q	Central	Q			Q

```

Note:

If a switching request is transmitted by the MEMORY (6043), the MEMORY address is not transferred, but the appropriate keyboard address and decoder section address for this instruction.
Please note that the four switches at the rear of the MEMORY (6043) are not structured the same way as the four switches at the rear of the keyboard (6040) or the switchboard (6041).  Only switches 1 and 2 are used to determine the address of the MEMORY (6043).  This means that only four MEMORY (6043) units can be connected to the I2C-Bus in the Märklin Digital-System.

### Operation with INTERFACES (6050 or 6051)

When operating the Digital-Systems with the INTERFACE (6050 or 6051), the transfer of instructions over the I2C-Bus mimic those of the control 80 (6035) to a large extent and exactly the same for the keyboard (6040) also for switching of functions in the control 80f (6036).

With locomotive decoder instructions the extended possibilities of the control 80f (6036) and Infra control 80f (6070) are not supported, thus direction indicator and the possibility of forcing the transfer of one address to another controller via the INTERFACES (6050 or 6051) is not possible. Locomotive decoder instructions that are sent to the control unit (6021) in the extended Motorola format (switch 2 at the rear side on " ON ") via the INTERFACE (6050 or 6051) look the same as instructions being sent in the H0-Modus or as with the control 80 (6035). If the control request is occupied by another device, the locomotive decoder address for this control request is not repeated, resulting in an incomplete transmission.

Only with the INTERFACES (6050 or 6051) the locomotive decoder address " 80 " and the function decoder address " 80 " is actually transferred as " 80 ", with control 80 (6035) and control 80f (6036) however always as " 00 ".

When controlling switching accessories the INTERFACE (6050 or 6051) produces the same transmissions just like the MEMORY (6043).  Only with the power-off instruction is there a small difference in the data being transmitted.  The INTERFACE (6050 or 6051) resets in the data byte only the bit for placing (bit 3) to an off state.  The keyboard (6040) resets against it with the power-off instruction all four bits (for decoder output), thus the bits 0 to 3. The two bits for the decoder section address (bit 4 and 5) must remain unchanged also here.

Only when switching functions a special device address is output, i.e. the address 0, although during the software related addressing only addresses are turned off including 1. Computer interface gives it a small difference: The INTERFACE (6050 or 6051) resets the data byte by only changing the bit (bit 3), the key board (6040) resets against it with the power-off instruction all four bits (for decoder output), thus the bits 0 to 3. The two bits for the decoder section address (bit 4 and 5) must remain unchanged also here.

Beyond that also " f1 " to " f4 " is set over the INTERFACE (6050 or 6051) with the specification of the sender address, the bit 0 only with switching request for extra functions. During the pertinent acknowledgement message from the central unit this bit 0 is again reset.

Therefore the instruction structure for switch commands for the interface here in detail:

```

Recipient 		sender 			decoder			data byte 		stop bit
1111 1110	0	0100 0001	0	0XXX XXXX	0	0000 XXXX	0	10
Central unit	Q	device addr.	Q	01 to 80 or	Q	f1 to f4	Q
						01 to 99

```

The acknowledgement of the central unit reads:

```

Recipient 		sender 			decoder			data byte 		stop bit
0100 0000	0	1111 1110	0	0XXX XXXX	0	0000 XXXX	0	0
Device addr.	Q	Central unit	Q	01 to 80 or	Q	f1 to f4	Q
						01 to 99

```

### Differences in the communication flow between central unit (6020) and control unit (6021)

With the operation of the control modules control 80 (6035), control 80f (6036), Infra control 80f (6070) and INTERFACE (6050 or 6051) with the central unit (6020) data exchange runs exactly the same as operation with the control unit (6021) in the H0-Modus.

However there is an exception, if the central unit (6020) is in the " stop" mode a control or a switching request is sent only the first byte which acknowledges the address of the requesting device is sent from the central unit.  Afterwards the clocking line SCL and the data line SDA remain low until the central unit is again in the " go" mode.  Once the central unit is again in the " go" mode will the remainder of the acknowledgement be transferred.

The controllers are put into a temporary delay between request and acknowledgement to transmit a new switching request to the central unit.  The devices control 80 (6035) and INTERFACE (6050 or 6051) both transmit information which overrides existing information in the " stop" mode of changing of locomotive address or drive position, therefore making its information the current valid information.
With the devices control 80f (6036) and Infra control 80f (6070) the information is transferred in a further packet.

A locomotive control request from the central unit (6020) in the " stop" mode reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	000X XXX0	0	0XXX XXXX	0	000X XXXX	0	10
Central 	Q 	device addr.  	Q 	00 to 79 	Q 	drive position	Q

```

The shortened acknowledgement reads then:

```

Recipients
000X XXX0	0
Device addr.	Q

```

The clocking line SCLK and the data line SDA remain low until the central processing unit is again in the " go" mode.  The I2C-Bus is thus blocked.

However with control 80 (6035) and INTERFACES 46 clock cycles have passed, with control 80f (6036) and Infra control 80f (6070) 48 clock cycles have passed due to the switching of slave to master operation.

After the change to the " go" mode the acknowledgement is again continued here.

```

			Sender 			decoder 		data byte 		stop bit
			1111 1110	0	0XXX XXXX	0	000X XXXX	0	0
			Central unit	Q	00 to 79	Q	drive position	Q

```

Now a new control request follows due to the temporal delay:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	000X XXX0	0	0XXX XXXX	0	000X XXXX	0	10
Central unit	Q 	device addr.  	Q 	00 to 79 	Q 	drive position	Q

```

And in addition the appropriate acknowledgement:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0XXX XXXX	0	000X XXXX	0	0
Device addr.	Q	Central unit	Q	00 to 79	Q	drive position	Q

```

Since the change of the central unit (6020) into the " go" mode 102 clock cycles passed, with control 80f (6036) and Infra control 80f (6070) and 104 clock cycles with the control 80 (6035) and INTERFACES (6050 or 6051).

At a control 80f (6036) during the " stop" mode if a new address was entered, then a further control request with 76 clock cycles will follow:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	000X XXX0	0	0XXX XXXX	0	000X XXXX	0	10
Central unit	Q 	device addr.  	Q 	00 to 79 	Q 	drive position	Q

```

And the pertinent acknowledgement:

```

Recipient 		sender 			decoder 		data byte 		stop bit
000X XXX0	0	1111 1110	0	0XXX XXXX	0	000X XXXX	0	0
Device addr.	Q	Central unit	Q	00 to 79	Q	drive position	Q

```

Also when switching functions in the " stop" mode of the central unit (6020) the switching request is acknowledged first by a shortened by acknowledgement statement from the central unit, and the clocking line SCL as well as the data line SDA thereafter held low until the central unit is again in " the go" mode.

Switching request for functions in the " stop" mode:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	010X XXX0	0	0XXX XXXX	0	0000 XXXX	0	10
Central unit 	Q 	device addr.  	Q 	00 to 79 or	Q 	f1 to f4	Q
						00 to 99

```

The shortened acknowledgement of the central unit reads:

```

Recipients
010X XXX0	0
Device addr.	Q

```

The clocking line SCL and the data line SDA remain low until the central processing unit is again in the " go" mode. The I2C-Bus is thus blocked.  With control 80f (6036) and Infra control 80f (6070) 48 clock cycles will have passed.

Bei Control 80f (6036) und Infra Control 80f (6070) vergingen bis hierher 48 Taktzyklen.

After the change to the " go" mode the acknowledgement is again continued here.

```

			Sender 			decoder 		data byte 		stop bit
			1111 1110	0	0XXX XXXX	0	0000 XXXX	0	0
			Central unit	Q	00 to 79 or	Q	f1 to f4	Q
						00 to 99

```

Now a new switching request follows due to the temporal delay:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	010X XXX0	0	0XXX XXXX	0	0000 XXXX	0	10
Central unit	Q 	device addr.  	Q 	00 to 79 or	Q 	f1 to f4	Q
						00 to 99

```

The acknowledgement of the central unit reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
010X XXX0	0	1111 1110	0	0XXX XXXX	0	0000 XXXX	0	0
Device addr.  	Q 	central unit 	Q 	00 to 79 or	Q 	f1 to f4	Q
						00 to 99

```

Since the change of the central unit (6020) into the " go" mode 104 clock cycles have passed.
At the control 80f (6036) during the " stop" mode if a further function was switched or if a new function decoder address was input, then now a further switching request with 76 clock cycles follows:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	010X XXX0	0	0XXX XXXX	0	0000 XXXX	0	10
Central unit	Q 	device addr.  	Q 	00 to 79 or	Q 	f1 to f4	Q
						00 to 99

```

The acknowledgement of the central unit reads:

```

Recipient 		sender 			decoder 		data byte 		stop bit
010X XXX0	0	1111 1110	0	0XXX XXXX	0	0000 XXXX	0	0
Device addr.  	Q 	central unit 	Q 	00 to 79 or	Q 	f1 to f4	Q
						00 to 99

```

Note:

Functions, which were switched during the " stop" mode before an address change, are transmitted to the track once the system is change into " the go" mode, but are not stored in the calling device.

Also when switching accessories in the " stop" mode of the central unit (6020) the switching request is acknowledged afterwards only by a shortened acknowledgement by the central unit and the clocking line SCL as well as the data line SDA is held low until the central unit is again switched in " the go" mode.

Switching request for accessories in the " stop" mode:

```

Recipient 		sender 			data byte 		stop bit
1111 1110	0	001X XXX0	0	00XX XXXX	0	10
Central unit	Q 	device addr.	Q			Q

```

The shortened acknowledgement of the central unit reads:

```

Recipients
001X XXX0	0
Device addr.	Q

```

The clocking line SCL and the data line SDA remain now on Low until the central processing unit is again in the " go" mode. The I2C-Bus is thus blocked.

With keyboard (6040), MEMORY (6043) and INTERFACES (6050 or 6051) passed to here 37 clock cycles.

After the change to the " go" mode the acknowledgement is again continued here.

```

			Sender 			data byte 		stop bit
			1111 1110	0	0000 XXXX	0	0
			Central unit	Q			Q

```

If before the change into the " stop" mode an accessory was switched on and during " the stop" mode the key were again released, then the transfer is hereby terminated.

Otherwise the switching request is repeated now:

```

Recipient 		sender 			data byte 		stop bit
1111 1110	0	001X XXX0	0	00XX XXXX	0	10
Central unit	Q 	device addr.	Q			Q

```

The complete acknowledgement of the central unit reads:

```

Recipient 		sender 			data byte 		stop bit
001X XXX0	0	1111 1110	0	00XX XXXX	0	0
Device addr.  	Q 	central unit	Q			Q

```

Since the change of the central unit (6020) into the " go" mode 75 clock cycles have passed.
If during the " stop" mode a keyboard key were pressed and released again, still the power-off instruction is transferred and acknowledged to ensure the accessory is turned off.

Switching request for power-off instruction:

```

Recipient 		sender 			data byte 		stop bit
1111 1110	0	001X XXX0	0	00XX 0000	0	10
Central unit	Q 	device addr.	Q			Q

```

The acknowledgement of the central unit reads:

```

Recipient 		sender 			data byte 		stop bit
001X XXX0	0	1111 1110	0	00XX 0000	0	0
Device addr.  	Q 	central unit	Q			Q

```

Since the change of the central unit into the " go" mode 131 clock cycles passed.

### Undocumented functions for the Control Unit (6021)

Only if the control unit (6021) is adjusted to the extended Motorola format (at least switch 2 at the rear side placed in the " ON " position), will it be possible to access certain functions that are not documented so far.  The function " recalling the last operating condition " is probably the most interesting and function which can be used often.

Here are the undocumented functions in detail:

### Data delete (input " 91 " and " 93 ")

When the address sequence " 91 " and " 93 " is entered, the data in the buffer for the Refresh cycle is deleted.  Also the driving direction is switched to " forward ".

This deletion should take place when starting a new program, but can also be done during a program.

After this sequence is entered all addresses are still sent in a continuous refresh cycle to the track, however the data is deleted (switched to " 0 ") and set the driving direction to forward.  The data in the buffer is again updated when an appropriate addresses is selected or by changing settings on any of the controllers or switching of functions.

Note:

Only newer decoders of the type c90 (60901 or 60902) " understand " the specification of the driving direction.  With older decoders only the drive position is set to " 0 " (stop) and the direction of travel dependent auxiliary function is switched off.  The last driving direction is preserved in the decoder however and can thereby be different from the display in the controller.

### All 80 addresses in Refresh cycle take up (input " 92 " and " 93 ")

The input of the address sequence " 92 " and " 93 " causes that all 80 possible Locomotive addresses are put into the refresh cycle, even if these addresses were not previously called yet.  The data bytes for the drive position and the status of the extra functions " f1 " to " f4 " are added to the refresh cycle starting with the first value " 00 ". This value is updated accordingly with the call of these decoder addresses.

### Version test (input " 94 " and " 93 ")

With the input of the address sequence " 94 " and " 93 " the software-Version can be displayed on the control unit (6021).  At present the current version will flash the LED once, independently of whether the central unit is in the " stop" mode or in " the go" mode.

### Recall the last operating condition (input " 97 " and " 93 ")

This is probably the most interesting and probably most frequently used additional function of the control unit (6021).  Thus the last recorded status before switching the Digital-Systems off is again recalled after restarting.  In addition the address sequence " 97 " and " 93 " must be input at the controller in the central processing unit or any attached control 80f (6036) after switching on the system or after a RESET.

The control unit (6021) will generate for all locomotive decoders and function decoders, with which the data byte is not equal to "00", a switching or a control request in the same manner as it would be generated by a control 80f (6036) or Infra control 80f (6070).  Address " 1 " is always indicated, even if the address sequence " 97 " and " 93 " were input from another device.

For each attached control 80f (6036) and Infra control 80f (6070), the switching or control request information, the functions " function " and " f1 " to " f4 " for the controllers are restored in this procedure.
Since the central unit generates the control request, no acknowledgement takes place.

The switching request for functions, generated by the central unit, read:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	0100 0010	0	0XXX XXXX	0	0000 XXXX	0	10
Central unit	Q 	device 1 	Q 	00 to 99 	Q 	f1 to f4	Q

```

Control request for locomotive data read:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	0000 0010	0	0XXX XXXX	0	01XX XXXX	0	10
Central unit 	Q 	device 1 	Q 	00 to 79 	Q 	drive position	Q

```

The bit sequence 01XX XXXX in the data byte is used otherwise with forced address transfer.  For the control request for locomotive data the driving direction is falsely indicated normally as (the driving direction is only indicated for the acknowledgement message by the central unit, not however during the control request).  That leads to the fact that during driving direction " forward " the data of the attached devices control 80f (6036) and Infra control 80f (6070) are not recognized and with the first call of a locomotive the direction of travel dependent auxiliary function " function " are always switched off.

The specification of the driving direction is usually transmitted in the acknowledgement of the Control unit (6021).

After the control unit (6021) has processed all switching or control requests, still another control request for driving equipment No. 1 follows, for which the decoder address " 99 " is indicated:

```

Recipient 		sender 			decoder 		data byte 		stop bit
1111 1110	0	0000 0010	0	0110 0011	0	001X XXXX	0	10
Central unit	Q 	device 1 	Q 	dec. 99 	Q 	drive position	Q

```

This is acknowledged as invalid:

```

Recipient 		sender 			decoder 		data byte 		stop bit
0000 0010	0	1111 1110	0	0110 0011	0	111X XXXX	0	0
Device 1 	Q 	central unit 	Q 	dec. 99 	Q 	111=occupied	Q

```

If any input device control 80 (6035), control 80f (6036), INTERFACE (6050 or 6051) or Infra control 80f (6070) a valid locomotive decoder address within the range of " 01 " to " 80 ", the control unit begins the Refresh cycle.

All decoder addresses are now contained in the Refresh cycle, which were stored before being powered off or before the RESET of the Digital-Systems where the data byte is not equal to " 00 ".  The addresses, with which both the data byte for functions " f1 " to " f4 " as well as the data byte for locomotive drive position contained and the " function " have a value " 0 " and where the adjusted driving direction is set to " forward ", these addresses are not added to the refresh cycle.

Note:

Only newer decoders of the type c90 (60901 or 60902) " understand " the specification of the driving direction.  Older decoders which have been resting for some time will set the driving direction to " forward ", even if the driving direction was previously set to " backwards ".  Thus it can occur that the driving direction displayed in the controllers control 80f (6036) and Infra control 80f (6070) does not correspond the actual driving direction.

![image](http://www.drkoenig.de/digital/bahn8.gif)

### Translation

The translation was made by [Matthew Romer](MAILTO:mromer@onlink.net). © 2002. Many thanks to him for this grateful work.

![image](http://www.drkoenig.de/digital/bahn8.gif)

The WWW-adaption was made by Dr. M. Michael König. © 2002.

![image](http://www.drkoenig.de/digital/bahn8.gif)

[_Homepage_](http://www.drkoenig.de/digital/digital.htm) | [![Deutsch](http://www.drkoenig.de/digital/d-flag.gif)](http://www.drkoenig.de/digital/i2c.htm)

![image](http://www.drkoenig.de/digital/bahn6.gif)
