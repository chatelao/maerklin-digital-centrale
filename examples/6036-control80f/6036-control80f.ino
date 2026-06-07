/*
 * Arduino Sketch to simulate a Märklin Digital Control 80f (6036)
 *
 * This example simulates a Control 80f locomotive controller connected to the
 * Märklin I2C bus (typically on the left side / Federleiste of a 6021).
 * It extends the Control 80 (6035) with support for extra functions f1-f4
 * and uses the Extended Motorola Format.
 *
 * Variants (selectable via compiler flags):
 * - V_ANALOG: Uses a potentiometer for speed and a button for direction change.
 * - V_DIGITAL: Uses a rotary encoder for speed and direction change (push).
 *
 * Connections (Märklin I2C Bus):
 * ------------------------------
 * Signal   | Pin (Right) | Pin (Left) | Arduino Pin
 * ---------|-------------|------------|------------
 * SDA      | b2          | b16        | A4 (SDA)
 * SCL      | b4          | b14        | A5 (SCL)
 * STOP     | b6          | b12        | A2 (STOP)
 * GO       | b8          | b10        | A3 (GO)
 * INIT IN  | b12         | b6         | D2
 * INIT OUT | -           | -          | D12 (Chain to next device)
 * 8V       | b14, b16    | b2, b4     | VIN (Ensure 8V compatibility)
 * GND      | a2-a16      | a2-a16     | GND
 *
 * User Interface Pins:
 * --------------------
 * D3: System STOP button (triggers global STOP)
 * D4: System GO button (triggers global GO)
 * D5: Function f0 (Light) ON
 * D6: Function f0 (Light) OFF
 * D7: Address UP (increment loco address 1-80)
 * D8: Address DOWN (decrement loco address 1-80)
 *
 * New for 6036 / Control 80f:
 * D0: f1 Button (Note: Conflicts with Serial RX)
 * D1: f2 Button (Note: Conflicts with Serial TX)
 *
 * V-Analog specific:
 * A0: Potentiometer (0-1023 -> Speed 0, 2-15)
 * A1: Direction Button (sends Speed 1)
 * D9:  f3 Button
 * D10: f4 Button
 *
 * V-Digital specific:
 * D9:  Encoder Phase A
 * D10: Encoder Phase B
 * D11: Encoder Button (Direction change)
 * A0:  f3 Button
 * A1:  f4 Button
 */

#include <Wire.h>

// Handle missing SDA/SCL definitions for some cores (e.g. Raspberry Pi Pico)
#ifndef SDA
#define SDA A4
#endif
#ifndef SCL
#define SCL A5
#endif

// --- Configuration ---
#if !defined(V_ANALOG) && !defined(V_DIGITAL)
#define V_ANALOG
#endif

// --- Pin Definitions ---
const int pinSTOP_BTN = 3;
const int pinGO_BTN   = 4;
const int pinFON_BTN  = 5;
const int pinFOFF_BTN = 6;
const int pinADDR_UP  = 7;
const int pinADDR_DN  = 8;

const int pinF1_BTN   = 0;
const int pinF2_BTN   = 1;

#ifdef V_ANALOG
const int pinPOT      = A0;
const int pinDIR_BTN  = A1;
const int pinF3_BTN   = 9;
const int pinF4_BTN   = 10;
#endif

#ifdef V_DIGITAL
const int pinENC_A    = 9;
const int pinENC_B    = 10;
const int pinENC_BTN  = 11;
const int pinF3_BTN   = A0;
const int pinF4_BTN   = A1;
#endif

const int pinINIT_IN  = 2;
const int pinINIT_OUT = 12;

const int pinBUS_STOP = A2;
const int pinBUS_GO   = A3;

// --- Constants ---
const byte CU_ADDR     = 0x7F; // 7-bit address of Central Unit (0xFE >> 1)

// --- State Variables ---
byte SENDER_ADDR      = 0x02; // Dynamically assigned
byte currentLocoAddr = 1;
byte currentSpeed    = 0;
bool f0State         = false;
bool f1State         = false;
bool f2State         = false;
bool f3State         = false;
bool f4State         = false;
bool isSystemGo      = true;

// Change tracking
byte lastSentSpeed    = 255;
bool lastSentF0       = false;
byte lastSentF1to4    = 255; // Packed f1-f4 state
byte lastSentAddr     = 255;

#ifdef V_DIGITAL
int lastA = HIGH;
#endif

void setup() {
  // Serial is disabled by default because D0/D1 are used for f1/f2.
  // If you need Serial for debugging, don't use f1/f2 buttons.
  // Serial.begin(9600);

  // INIT Pins
  pinMode(pinINIT_IN,  INPUT_PULLUP);
  pinMode(pinINIT_OUT, OUTPUT);
  digitalWrite(pinINIT_OUT, HIGH);

  performSoftwareAddressing();

  // Initialize I2C
  Wire.begin();

  // 6036 Initialization (Extended Motorola Format)
  initialize6036();

  // Button Pins
  pinMode(pinSTOP_BTN, INPUT_PULLUP);
  pinMode(pinGO_BTN,   INPUT_PULLUP);
  pinMode(pinFON_BTN,  INPUT_PULLUP);
  pinMode(pinFOFF_BTN, INPUT_PULLUP);
  pinMode(pinADDR_UP,  INPUT_PULLUP);
  pinMode(pinADDR_DN,  INPUT_PULLUP);
  pinMode(pinF1_BTN,   INPUT_PULLUP);
  pinMode(pinF2_BTN,   INPUT_PULLUP);
  pinMode(pinF3_BTN,   INPUT_PULLUP);
  pinMode(pinF4_BTN,   INPUT_PULLUP);

  // Bus Signals
  pinMode(pinBUS_STOP, INPUT_PULLUP);
  pinMode(pinBUS_GO,   INPUT_PULLUP);

#ifdef V_ANALOG
  pinMode(pinPOT,      INPUT);
  pinMode(pinDIR_BTN,  INPUT_PULLUP);
#endif

#ifdef V_DIGITAL
  pinMode(pinENC_A,    INPUT_PULLUP);
  pinMode(pinENC_B,    INPUT_PULLUP);
  pinMode(pinENC_BTN,  INPUT_PULLUP);
  lastA = digitalRead(pinENC_A);
#endif
}

/**
 * Initialization for 6036 / Control 80f to enable extended features.
 */
void initialize6036() {
  // Special initialization sequence for Extended Motorola Format
  Wire.beginTransmission(CU_ADDR);
  Wire.write(0x80); // Special Sender Address for Init
  Wire.write(0x6F); // Decimal 111
  Wire.write(0x40); // Decimal 64
  Wire.endTransmission();
}

/**
 * Sends a locomotive command (Speed/Direction/F0).
 * Uses Extended Motorola Format (Type 001 = Request).
 */
void sendLocoCommand(byte addr, byte speed, bool f0) {
  byte decoderAddr = (addr == 80) ? 0 : addr;

  // Data Byte: Bits 0-3 speed, Bit 4 function (f0), Bits 5-7 = 001 (Request)
  byte dataByte = (speed & 0x0F);
  if (f0) dataByte |= 0x10;
  dataByte |= 0x20; // Extended Motorola Request bit (bit 5)

  Wire.beginTransmission(CU_ADDR);
  Wire.write(SENDER_ADDR);
  Wire.write(decoderAddr);
  Wire.write(dataByte);
  Wire.endTransmission();
}

/**
 * Sends extra functions f1-f4.
 * Protocol: [CU Addr] [Sender Addr 0x40] [Loco Addr] [Data f1-f4]
 */
void sendFunctionCommand(byte addr, bool f1, bool f2, bool f3, bool f4) {
  byte decoderAddr = (addr == 80) ? 0 : addr;

  // Sender Address for f1-f4 is 010X XXX0 (0x40 | (SENDER_ADDR_BITS))
  // Since SENDER_ADDR is already in format 000X XXX0, we can just OR it.
  byte funcSenderAddr = 0x40 | SENDER_ADDR;

  byte dataByte = 0;
  if (f1) dataByte |= 0x01;
  if (f2) dataByte |= 0x02;
  if (f3) dataByte |= 0x04;
  if (f4) dataByte |= 0x08;

  Wire.beginTransmission(CU_ADDR);
  Wire.write(funcSenderAddr);
  Wire.write(decoderAddr);
  Wire.write(dataByte);
  Wire.endTransmission();
}

void triggerBusSignal(int pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delay(100);
  pinMode(pin, INPUT_PULLUP);
}

void performSoftwareAddressing() {
  pinMode(SDA, INPUT_PULLUP);
  pinMode(SCL, INPUT_PULLUP);

  while (digitalRead(pinINIT_IN) == HIGH);
  while (!(digitalRead(SDA) == LOW && digitalRead(SCL) == HIGH));
  while (digitalRead(SCL) == HIGH);

  byte assignedAddr = 0;
  for (int i = 0; i < 8; i++) {
    while (digitalRead(SCL) == LOW);
    assignedAddr <<= 1;
    if (digitalRead(SDA) == HIGH) assignedAddr |= 1;
    while (digitalRead(SCL) == HIGH);
  }

  pinMode(SDA, OUTPUT);
  digitalWrite(SDA, LOW);
  while (digitalRead(SCL) == LOW);
  while (digitalRead(SCL) == HIGH);
  pinMode(SDA, INPUT_PULLUP);

  SENDER_ADDR = assignedAddr;
  digitalWrite(pinINIT_OUT, LOW);
}

void loop() {
  // 1. Monitor Bus Status
  if (digitalRead(pinBUS_STOP) == LOW && isSystemGo) {
    isSystemGo = false;
  } else if (digitalRead(pinBUS_GO) == LOW && !isSystemGo) {
    isSystemGo = true;
  }

  // 2. System Buttons
  if (digitalRead(pinSTOP_BTN) == LOW) {
    triggerBusSignal(pinBUS_STOP);
    delay(200);
  }
  if (digitalRead(pinGO_BTN) == LOW) {
    triggerBusSignal(pinBUS_GO);
    delay(200);
  }

  // 3. Address Selection
  if (digitalRead(pinADDR_UP) == LOW) {
    if (currentLocoAddr < 80) currentLocoAddr++;
    else currentLocoAddr = 1;
    delay(250);
  }
  if (digitalRead(pinADDR_DN) == LOW) {
    if (currentLocoAddr > 1) currentLocoAddr--;
    else currentLocoAddr = 80;
    delay(250);
  }

  // 4. Function Buttons (f0, f1-f4)
  if (digitalRead(pinFON_BTN) == LOW)  f0State = true;
  if (digitalRead(pinFOFF_BTN) == LOW) f0State = false;

  // Toggle f1-f4 on press (simple toggle implementation)
  static bool lastF1 = HIGH, lastF2 = HIGH, lastF3 = HIGH, lastF4 = HIGH;
  bool currF1 = digitalRead(pinF1_BTN);
  bool currF2 = digitalRead(pinF2_BTN);
  bool currF3 = digitalRead(pinF3_BTN);
  bool currF4 = digitalRead(pinF4_BTN);

  if (currF1 == LOW && lastF1 == HIGH) { f1State = !f1State; delay(100); }
  if (currF2 == LOW && lastF2 == HIGH) { f2State = !f2State; delay(100); }
  if (currF3 == LOW && lastF3 == HIGH) { f3State = !f3State; delay(100); }
  if (currF4 == LOW && lastF4 == HIGH) { f4State = !f4State; delay(100); }

  lastF1 = currF1; lastF2 = currF2; lastF3 = currF3; lastF4 = currF4;

  // 5. Throttle
#ifdef V_ANALOG
  int potVal = analogRead(pinPOT);
  if (potVal < 40) currentSpeed = 0;
  else currentSpeed = map(potVal, 40, 1023, 2, 15);

  if (digitalRead(pinDIR_BTN) == LOW) {
    sendLocoCommand(currentLocoAddr, 1, f0State);
    delay(500);
  }
#endif

#ifdef V_DIGITAL
  int currA = digitalRead(pinENC_A);
  if (currA != lastA) {
    if (digitalRead(pinENC_B) != currA) {
      if (currentSpeed < 15) {
        if (currentSpeed == 0) currentSpeed = 2;
        else currentSpeed++;
      }
    } else {
      if (currentSpeed > 2) currentSpeed--;
      else currentSpeed = 0;
    }
    delay(5);
  }
  lastA = currA;

  if (digitalRead(pinENC_BTN) == LOW) {
    sendLocoCommand(currentLocoAddr, 1, f0State);
    delay(500);
  }
#endif

  // 6. Send Commands
  if (isSystemGo) {
    bool addrChanged = (currentLocoAddr != lastSentAddr);
    byte currentF1to4 = (f1State ? 1 : 0) | (f2State ? 2 : 0) | (f3State ? 4 : 0) | (f4State ? 8 : 0);

    // Standard Loco Command (Speed, F0)
    if (currentSpeed != lastSentSpeed || f0State != lastSentF0 || addrChanged) {
      sendLocoCommand(currentLocoAddr, currentSpeed, f0State);
    }

    // Extra Function Command (f1-f4)
    if (currentF1to4 != lastSentF1to4 || addrChanged) {
      sendFunctionCommand(currentLocoAddr, f1State, f2State, f3State, f4State);
    }

    lastSentSpeed = currentSpeed;
    lastSentF0 = f0State;
    lastSentF1to4 = currentF1to4;
    lastSentAddr = currentLocoAddr;
  }

  delay(20);
}
