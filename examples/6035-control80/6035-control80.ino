/*
 * Arduino Sketch to simulate a Märklin Digital Control 80 (6035)
 *
 * This example simulates a Control 80 locomotive controller connected to the
 * Märklin I2C bus (typically on the left side / Federleiste of a 6021).
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
 * D5: Function ON (Fon)
 * D6: Function OFF (Foff)
 * D7: Address UP (increment loco address 1-80)
 * D8: Address DOWN (decrement loco address 1-80)
 *
 * V-Analog specific:
 * A0: Potentiometer (0-1023 -> Speed 0, 2-15)
 * A1: Direction Button (sends Speed 1)
 *
 * V-Digital specific:
 * D9:  Encoder Phase A
 * D10: Encoder Phase B
 * D11: Encoder Button (Direction change)
 */

#include <Wire.h>

// --- Configuration ---
// One of these must be defined. You can also define these via compiler flags.
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

const int pinINIT_IN  = 2;  // Connected to Bus b12 (Right) / b6 (Left)
const int pinINIT_OUT = 12; // Chain to next device's INIT_IN

const int pinBUS_STOP = A2; // Connected to Bus b6 (Right) / b12 (Left)
const int pinBUS_GO   = A3; // Connected to Bus b8 (Right) / b10 (Left)

#ifdef V_ANALOG
const int pinPOT      = A0;
const int pinDIR_BTN  = A1;
#endif

#ifdef V_DIGITAL
const int pinENC_A    = 9;
const int pinENC_B    = 10;
const int pinENC_BTN  = 11;
#endif

// --- Constants ---
const byte CU_ADDR     = 0x7F; // 7-bit address of Central Unit (0xFE >> 1)

// --- State Variables ---
byte SENDER_ADDR      = 0x02; // Dynamically assigned (default to 0x02)
byte currentLocoAddr = 1;
byte currentSpeed    = 0;     // 0=Stop, 1=Change Dir, 2-15=Speed steps
bool functionState   = false;
bool isSystemGo      = true;

// Change tracking to minimize I2C traffic
byte lastSentSpeed    = 255;
bool lastSentFunction = false;
byte lastSentAddr     = 255;

#ifdef V_DIGITAL
int lastA = HIGH;
#endif

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for Serial on some boards
  Serial.println(F("--- Märklin Control 80 Simulator ---"));

  // INIT Pins
  pinMode(pinINIT_IN,  INPUT_PULLUP);
  pinMode(pinINIT_OUT, OUTPUT);
  digitalWrite(pinINIT_OUT, HIGH); // Inactive

  // Perform Software Addressing (Enumeration)
  performSoftwareAddressing();

  // Initialize I2C
  Wire.begin();

  // Button Pins
  pinMode(pinSTOP_BTN, INPUT_PULLUP);
  pinMode(pinGO_BTN,   INPUT_PULLUP);
  pinMode(pinFON_BTN,  INPUT_PULLUP);
  pinMode(pinFOFF_BTN, INPUT_PULLUP);
  pinMode(pinADDR_UP,  INPUT_PULLUP);
  pinMode(pinADDR_DN,  INPUT_PULLUP);

  // Bus Signals (Open-collector style)
  pinMode(pinBUS_STOP, INPUT_PULLUP);
  pinMode(pinBUS_GO,   INPUT_PULLUP);

#ifdef V_ANALOG
  pinMode(pinPOT,      INPUT);
  pinMode(pinDIR_BTN,  INPUT_PULLUP);
  Serial.println(F("Variant: ANALOG (Pot on A0, Dir on A1)"));
#endif

#ifdef V_DIGITAL
  pinMode(pinENC_A,    INPUT_PULLUP);
  pinMode(pinENC_B,    INPUT_PULLUP);
  pinMode(pinENC_BTN,  INPUT_PULLUP);
  lastA = digitalRead(pinENC_A);
  Serial.println(F("Variant: DIGITAL (Encoder on D9/D10, Dir on D11)"));
#endif

  Serial.print(F("Initial Loco Address: "));
  Serial.println(currentLocoAddr);
}

/**
 * Sends a locomotive command to the Central Unit.
 * Protocol (4 bytes): [CU Addr] [Sender Addr] [Loco Addr] [Data]
 */
void sendLocoCommand(byte addr, byte speed, bool function) {
  // Address 80 is transmitted as 0
  byte decoderAddr = (addr == 80) ? 0 : addr;

  // Data Byte: Bits 0-3 speed, Bit 4 function, Bits 5-7 = 000
  byte dataByte = (speed & 0x0F);
  if (function) dataByte |= 0x10;

  Wire.beginTransmission(CU_ADDR);
  Wire.write(SENDER_ADDR);
  Wire.write(decoderAddr);
  Wire.write(dataByte);
  byte error = Wire.endTransmission();

  if (error == 0) {
    Serial.print(F("I2C Success: Addr=")); Serial.print(addr);
    Serial.print(F(" Speed=")); Serial.print(speed);
    Serial.print(F(" Func=")); Serial.println(function ? F("ON") : F("OFF"));
  } else {
    Serial.print(F("I2C Error: ")); Serial.println(error);
  }
}

/**
 * Triggers a bus signal by pulling the line LOW (open-collector style)
 */
void triggerBusSignal(int pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delay(100); // Hold for 100ms
  pinMode(pin, INPUT_PULLUP);
}

/**
 * Performs software addressing (enumeration) over the I2C bus.
 * Captures the assigned address from the CU via bit-banging.
 */
void performSoftwareAddressing() {
  Serial.println(F("Waiting for Software Addressing (INIT)..."));

  // Ensure I2C pins are inputs before bit-banging
  pinMode(SDA, INPUT_PULLUP);
  pinMode(SCL, INPUT_PULLUP);

  // 1. Wait for INIT IN to go LOW
  while (digitalRead(pinINIT_IN) == HIGH) {
    delay(1);
  }

  // 2. Capture I2C address byte (8 bits)
  // Wait for START condition: SDA falls while SCL is HIGH
  while (!(digitalRead(SDA) == LOW && digitalRead(SCL) == HIGH));

  // Wait for SCL to fall for the first bit
  while (digitalRead(SCL) == HIGH);

  byte assignedAddr = 0;
  for (int i = 0; i < 8; i++) {
    while (digitalRead(SCL) == LOW); // Wait for SCL HIGH
    assignedAddr <<= 1;
    if (digitalRead(SDA) == HIGH) assignedAddr |= 1;
    while (digitalRead(SCL) == HIGH); // Wait for SCL LOW
  }

  // 3. Send ACK: SDA LOW during 9th clock pulse
  pinMode(SDA, OUTPUT);
  digitalWrite(SDA, LOW);
  while (digitalRead(SCL) == LOW); // Wait for SCL HIGH (9th clock)
  while (digitalRead(SCL) == HIGH); // Wait for SCL LOW
  pinMode(SDA, INPUT_PULLUP); // Release SDA

  SENDER_ADDR = assignedAddr;

  // 4. Enable next device in chain
  digitalWrite(pinINIT_OUT, LOW);

  Serial.print(F("Assigned Address: 0x"));
  Serial.println(SENDER_ADDR, HEX);
}

void loop() {
  // 1. Monitor Bus Status (Signals from CU or other devices)
  if (digitalRead(pinBUS_STOP) == LOW && isSystemGo) {
    isSystemGo = false;
    Serial.println(F(">> SYSTEM STOP <<"));
  } else if (digitalRead(pinBUS_GO) == LOW && !isSystemGo) {
    isSystemGo = true;
    Serial.println(F(">> SYSTEM GO <<"));
  }

  // 2. Handle System Control Buttons
  if (digitalRead(pinSTOP_BTN) == LOW) {
    triggerBusSignal(pinBUS_STOP);
    delay(200);
  }
  if (digitalRead(pinGO_BTN) == LOW) {
    triggerBusSignal(pinBUS_GO);
    delay(200);
  }

  // 3. Handle Function Buttons
  if (digitalRead(pinFON_BTN) == LOW) {
    functionState = true;
  }
  if (digitalRead(pinFOFF_BTN) == LOW) {
    functionState = false;
  }

  // 4. Handle Address Selection
  if (digitalRead(pinADDR_UP) == LOW) {
    if (currentLocoAddr < 80) currentLocoAddr++;
    else currentLocoAddr = 1;
    Serial.print(F("Loco Address: ")); Serial.println(currentLocoAddr);
    delay(250);
  }
  if (digitalRead(pinADDR_DN) == LOW) {
    if (currentLocoAddr > 1) currentLocoAddr--;
    else currentLocoAddr = 80;
    Serial.print(F("Loco Address: ")); Serial.println(currentLocoAddr);
    delay(250);
  }

  // 5. Handle Throttle
#ifdef V_ANALOG
  int potVal = analogRead(pinPOT);
  // Map 0-1023 to 0 (Stop) and 2-15 (Speed steps)
  if (potVal < 40) {
    currentSpeed = 0;
  } else {
    currentSpeed = map(potVal, 40, 1023, 2, 15);
  }

  if (digitalRead(pinDIR_BTN) == LOW) {
    sendLocoCommand(currentLocoAddr, 1, functionState); // Speed 1 = Dir Change
    delay(500); // Prevent multiple triggers
  }
#endif

#ifdef V_DIGITAL
  int currA = digitalRead(pinENC_A);
  if (currA != lastA) {
    if (digitalRead(pinENC_B) != currA) {
      // Clockwise - Increase
      if (currentSpeed < 15) {
        if (currentSpeed == 0) currentSpeed = 2;
        else currentSpeed++;
      }
    } else {
      // Counter-clockwise - Decrease
      if (currentSpeed > 2) currentSpeed--;
      else currentSpeed = 0;
    }
    delay(5); // Debounce
  }
  lastA = currA;

  if (digitalRead(pinENC_BTN) == LOW) {
    sendLocoCommand(currentLocoAddr, 1, functionState); // Dir Change
    delay(500);
  }
#endif

  // 6. Send Loco Command if state changed and system is in GO mode
  if (isSystemGo) {
    if (currentSpeed != lastSentSpeed ||
        functionState != lastSentFunction ||
        currentLocoAddr != lastSentAddr) {

      sendLocoCommand(currentLocoAddr, currentSpeed, functionState);

      lastSentSpeed = currentSpeed;
      lastSentFunction = functionState;
      lastSentAddr = currentLocoAddr;
    }
  }

  delay(20);
}
