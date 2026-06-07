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
 * STOP   | b12         | A2 (STOP)
 * GO     | b10         | A1 (GO)
 * INIT   | b6          | A0 (INIT)
 * 8V     | b2, b4      | VIN (Ensure 8V compatibility)
 * GND    | a2-a16      | GND
 *
 * Keyboard Address (D9-D12):
 * --------------------------
 * Use DIP switches or jumpers to GND.
 * Logic: Switch CLOSED (ON) = bit is 1.
 */

#include <Wire.h>

// Märklin I2C Constants
#define CENTRAL_UNIT_ADDR 0x7F

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

const int pinADDR[] = {9, 10, 11, 12};

const int pinBUTTONS[] = {0, 1, 2, 3, 4, 5, 6, 7};
const int pinCommon = 8;
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
    lastButtonState[i] = HIGH;
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
  keyboardAddress = 0;
  for (int i = 0; i < 4; i++) {
    if (digitalRead(pinADDR[i]) == LOW) {
      keyboardAddress |= (1 << i);
    }
  }
}

/**
 * Sends a solenoid command to the Central Unit.
 */
void sendSolenoidCommand(int turnoutIdx, bool isGreen, bool powerOn) {
  byte senderAddr = 0x20 | (keyboardAddress << 1);

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
  if (digitalRead(pinSTOP) == LOW) {
    isPowerOn = false;
  } else if (digitalRead(pinGO) == LOW) {
    isPowerOn = true;
  }

  // Scan buttons
  for (int i = 0; i < 8; i++) {
    bool currentState = digitalRead(pinBUTTONS[i]);

    if (currentState != lastButtonState[i]) {
      delay(20);
      if (digitalRead(pinBUTTONS[i]) == currentState) {
        if (isPowerOn) {
          int turnoutIdx = i / 2;
          bool isGreen = (i % 2 == 1);

          if (currentState == LOW) {
            sendSolenoidCommand(turnoutIdx, isGreen, true);
          } else {
            sendSolenoidCommand(turnoutIdx, isGreen, false);
          }
        }
        lastButtonState[i] = currentState;
      }
    }
  }
}
