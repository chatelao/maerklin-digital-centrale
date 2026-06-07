/*
 * Arduino Sketch to simulate a Märklin Digital Keyboard 6040
 *
 * This example simulates a 6040 keyboard connected to the left side
 * of a Central Unit (6021/6020).
 *
 * WARNING: Pins D0 and D1 are used for turnout buttons. This prevents
 * the use of Serial communication (Hardware Serial) and may interfere
 * with sketch uploads if buttons are held down.
 *
 * Connections (Märklin I2C Bus - Left Side / Federleiste):
 * -------------------------------------------------------
 * Signal | Pin (Links) | Arduino Pin
 * -------|-------------|------------
 * SDA    | b16         | A4 (SDA)
 * SCL    | b14         | A5 (SCL)
 * STOP   | b12         | A2 (STOP signal from CU)
 * GO     | b10         | A1 (GO signal from CU)
 * INIT   | b6          | A0 (INIT signal / address chain)
 * 8V     | b2, b4      | VIN (Ensure your Arduino can handle 8V on VIN, e.g. Uno/Nano)
 * GND    | a2-a16      | GND
 *
 * Keyboard Address (D9-D12):
 * --------------------------
 * Use DIP switches or jumpers to GND.
 * Logic: Switch CLOSED (ON) = bit is 1.
 * Pult 1  (Addr 0): All Open (HIGH)
 * Pult 2  (Addr 1): D9 to GND (LOW), others Open
 * Pult 3  (Addr 2): D10 to GND (LOW), others Open
 * ...
 * Pult 16 (Addr 15): D9-D12 to GND (LOW)
 *
 * Turnout Inputs (D0-D8):
 * -----------------------
 * D0: Turnout 1 Red
 * D1: Turnout 1 Green
 * D2: Turnout 2 Red
 * D3: Turnout 2 Green
 * D4: Turnout 3 Red
 * D5: Turnout 3 Green
 * D6: Turnout 4 Red
 * D7: Turnout 4 Green
 * D8: Common Ground for buttons (Output LOW)
 *
 * (Connect buttons between the digital pin D0-D7 and D8)
 */

#include <Wire.h>

// Märklin I2C Constants
#define CENTRAL_UNIT_ADDR 0x7F // 7-bit I2C address of the Central Unit (0xFE >> 1)

// Pin Definitions
#if defined(ARDUINO_ARCH_RP2040)
// Raspberry Pi Pico Pinout
const int pinINIT = 2;
const int pinGO   = 3;
const int pinSTOP = 6;
const int pinETC  = 7;

const int pinADDR[] = {10, 11, 12, 13};

const int pinBUTTONS[] = {14, 15, 16, 17, 18, 19, 20, 21};
const int pinCommon = 22;
#else
// Default (Arduino Nano) Pinout
const int pinINIT = A0;
const int pinGO   = A1;
const int pinSTOP = A2;
const int pinETC  = A3;

const int pinADDR[] = {9, 10, 11, 12}; // D9=S1, D10=S2, D11=S3, D12=S4

const int pinBUTTONS[] = {0, 1, 2, 3, 4, 5, 6, 7}; // D0-D7
const int pinCommon = 8; // D8 used as common ground for buttons
#endif

byte keyboardAddress = 0;
bool lastButtonState[8];
bool isPowerOn = true;

void setup() {
  // Initialize Address Pins with Pull-ups
  for (int i = 0; i < 4; i++) {
    pinMode(pinADDR[i], INPUT_PULLUP);
  }

  // Initialize Button Pins with Pull-ups
  for (int i = 0; i < 8; i++) {
    pinMode(pinBUTTONS[i], INPUT_PULLUP);
    lastButtonState[i] = HIGH; // Pull-up means HIGH is unpressed
  }

  // D8 as common ground for the buttons
  pinMode(pinCommon, OUTPUT);
  digitalWrite(pinCommon, LOW);

  // Initialize Control Signal Pins
  pinMode(pinINIT, INPUT_PULLUP);
  pinMode(pinGO, INPUT_PULLUP);
  pinMode(pinSTOP, INPUT_PULLUP);
  pinMode(pinETC, INPUT_PULLUP);

  // Initialize I2C (Arduino as Master)
  Wire.begin();

  // Wait a bit for power to stabilize
  delay(100);

  // Read Keyboard Address from D9-D12
  // Logic: Switch ON = Low, Switch OFF = High
  keyboardAddress = 0;
  for (int i = 0; i < 4; i++) {
    if (digitalRead(pinADDR[i]) == LOW) {
      keyboardAddress |= (1 << i);
    }
  }
}

/**
 * Sends a solenoid command to the Central Unit.
 *
 * Protocol:
 * Byte 1: Sender Address (0x20 | keyboardAddress << 1)
 *         Format: 001X XXX0 (X XXX = 4-bit keyboard address)
 * Byte 2: Data Byte
 *         Bit 0: Direction (0=Red, 1=Green)
 *         Bit 1-2: Output Number (0-3)
 *         Bit 3: Power (1=ON, 0=OFF)
 *         Bit 4-5: Section (0-3)
 */
void sendSolenoidCommand(int turnoutIdx, bool isGreen, bool powerOn) {
  // Sender Address for Keyboard: 001X XXX0
  byte senderAddr = 0x20 | (keyboardAddress << 1);

  // Data Byte construction
  byte dataByte = 0;
  if (isGreen) dataByte |= 0x01;
  dataByte |= ((turnoutIdx & 0x03) << 1);
  if (powerOn) dataByte |= 0x08;

  Wire.beginTransmission(CENTRAL_UNIT_ADDR);
  Wire.write(senderAddr);
  Wire.write(dataByte);
  Wire.endTransmission();
}

void loop() {
  // Check System Status (GO/STOP)
  // GO and STOP signals are active LOW on the Märklin bus
  if (digitalRead(pinSTOP) == LOW) {
    isPowerOn = false;
  } else if (digitalRead(pinGO) == LOW) {
    isPowerOn = true;
  }

  // Scan buttons
  for (int i = 0; i < 8; i++) {
    bool currentState = digitalRead(pinBUTTONS[i]);

    if (currentState != lastButtonState[i]) {
      // Debounce delay
      delay(20);
      if (digitalRead(pinBUTTONS[i]) == currentState) {

        // Only send commands if system is in GO mode
        if (isPowerOn) {
          int turnoutIdx = i / 2;
          bool isGreen = (i % 2 == 1);

          if (currentState == LOW) {
            // Button Pressed
            sendSolenoidCommand(turnoutIdx, isGreen, true);
          } else {
            // Button Released
            sendSolenoidCommand(turnoutIdx, isGreen, false);
          }
        }

        lastButtonState[i] = currentState;
      }
    }
  }
}
