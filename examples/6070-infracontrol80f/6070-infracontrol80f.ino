/*
 * Arduino Sketch to simulate a Märklin Digital Infra Control 80f (6070)
 * Target Hardware: Seeed Studio XIAO RP2040
 * Input Device: Samsung IR Remote (BN59-01199F)
 *
 * This example adapts the Control 80f logic for the XIAO RP2040 and
 * integrates an IR receiver to decode Samsung remote signals.
 *
 * IMPORTANT: XIAO RP2040 is 3.3V logic. Use level shifters for 5V Märklin Bus.
 * Power the XIAO via a 5V regulator from the 8V bus.
 */

#include <Wire.h>

// Handle missing pin definitions for some cores (e.g. Raspberry Pi Pico)
#ifndef D0
#define D0 0
#define D1 1
#define D2 2
#define D3 3
#define D4 4
#define D5 5
#define D6 6
#endif
#ifndef SDA
#define SDA 4
#endif
#ifndef SCL
#define SCL 5
#endif

// --- Pin Definitions (XIAO RP2040) ---
const int pinIR_RECV  = D0; // IR Sensor Output
const int pinBUS_STOP = D1; // To Level Shifter -> Bus b6
const int pinBUS_GO   = D2; // To Level Shifter -> Bus b8
const int pinINIT_IN  = D3; // To Level Shifter -> Bus b12
const int pinINIT_OUT = D6; // To Level Shifter -> next device INIT IN
// SDA: D4, SCL: D5 (Standard XIAO I2C)

// --- Samsung IR Remote Codes (BN59-01199F) ---
const uint32_t IR_POWER    = 0xE0E040BF;
const uint32_t IR_VOL_UP   = 0xE0E0E01F;
const uint32_t IR_VOL_DOWN = 0xE0E0D12E;
const uint32_t IR_CH_UP    = 0xE0E048B7;
const uint32_t IR_CH_DOWN  = 0xE0E008F7;
const uint32_t IR_ENTER    = 0xE0E016E9;
const uint32_t IR_TOOLS    = 0xE0E0D22D; // Mapping to f0
const uint32_t IR_RED      = 0xE0E036C9; // f1
const uint32_t IR_GREEN    = 0xE0E028D7; // f2
const uint32_t IR_YELLOW   = 0xE0E0A857; // f3
const uint32_t IR_BLUE     = 0xE0E06897; // f4

// --- Constants ---
const byte CU_ADDR = 0x7F;

// --- State Variables ---
byte SENDER_ADDR      = 0x02;
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
byte lastSentF1to4    = 255;
byte lastSentAddr     = 255;

void setup() {
  Serial.begin(115200);

  pinMode(pinIR_RECV, INPUT);
  pinMode(pinBUS_STOP, INPUT_PULLUP);
  pinMode(pinBUS_GO, INPUT_PULLUP);
  pinMode(pinINIT_IN, INPUT_PULLUP);
  pinMode(pinINIT_OUT, OUTPUT);
  digitalWrite(pinINIT_OUT, HIGH);

  // Note: XIAO RP2040 might need special handling for I2C and software addressing
  // during the performSoftwareAddressing() phase due to 3.3V/5V differences.
  performSoftwareAddressing();

  Wire.begin(); // Standard XIAO D4 (SDA), D5 (SCL)
  initialize6036();
}

void initialize6036() {
  Wire.beginTransmission(CU_ADDR);
  Wire.write(0x80);
  Wire.write(0x6F);
  Wire.write(0x40);
  Wire.endTransmission();
}

void sendLocoCommand(byte addr, byte speed, bool f0) {
  byte decoderAddr = (addr == 80) ? 0 : addr;
  byte dataByte = (speed & 0x0F);
  if (f0) dataByte |= 0x10;
  dataByte |= 0x20;

  Wire.beginTransmission(CU_ADDR);
  Wire.write(SENDER_ADDR);
  Wire.write(decoderAddr);
  Wire.write(dataByte);
  Wire.endTransmission();
}

void sendFunctionCommand(byte addr, bool f1, bool f2, bool f3, bool f4) {
  byte decoderAddr = (addr == 80) ? 0 : addr;
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
  // Simplified version for XIAO, assuming level shifters are transparent
  while (digitalRead(pinINIT_IN) == HIGH);

  // Wait for I2C Start
  while (!(digitalRead(SDA) == LOW && digitalRead(SCL) == HIGH));
  while (digitalRead(SCL) == HIGH);

  byte assignedAddr = 0;
  for (int i = 0; i < 8; i++) {
    while (digitalRead(SCL) == LOW);
    assignedAddr <<= 1;
    if (digitalRead(SDA) == HIGH) assignedAddr |= 1;
    while (digitalRead(SCL) == HIGH);
  }

  // Send ACK
  pinMode(SDA, OUTPUT);
  digitalWrite(SDA, LOW);
  while (digitalRead(SCL) == LOW);
  while (digitalRead(SCL) == HIGH);
  pinMode(SDA, INPUT);

  SENDER_ADDR = assignedAddr;
  digitalWrite(pinINIT_OUT, LOW);
}

// Minimal Samsung IR Decoding
uint32_t readSamsungIR() {
  if (digitalRead(pinIR_RECV) == HIGH) return 0;

  // Measure Header Space
  unsigned long duration = pulseIn(pinIR_RECV, HIGH, 10000);
  if (duration > 4000 && duration < 5000) {
    uint32_t decodedData = 0;
    for (int i = 0; i < 32; i++) {
      unsigned long bitSpace = pulseIn(pinIR_RECV, HIGH, 3000);
      if (bitSpace > 1000) {
        decodedData |= (1UL << i);
      }
    }
    return decodedData;
  }
  return 0;
}

void handleIRCommand(uint32_t cmd) {
  if (cmd == 0) return;

  switch (cmd) {
    case IR_POWER:
      if (isSystemGo) triggerBusSignal(pinBUS_STOP);
      else triggerBusSignal(pinBUS_GO);
      break;

    case IR_VOL_UP:
      if (currentSpeed < 15) {
        if (currentSpeed == 0) currentSpeed = 2;
        else currentSpeed++;
      }
      break;

    case IR_VOL_DOWN:
      if (currentSpeed > 2) currentSpeed--;
      else currentSpeed = 0;
      break;

    case IR_CH_UP:
      if (currentLocoAddr < 80) currentLocoAddr++;
      else currentLocoAddr = 1;
      break;

    case IR_CH_DOWN:
      if (currentLocoAddr > 1) currentLocoAddr--;
      else currentLocoAddr = 80;
      break;

    case IR_ENTER:
      sendLocoCommand(currentLocoAddr, 1, f0State); // Dir Change
      delay(200);
      break;

    case IR_TOOLS:  f0State = !f0State; break;
    case IR_RED:    f1State = !f1State; break;
    case IR_GREEN:  f2State = !f2State; break;
    case IR_YELLOW: f3State = !f3State; break;
    case IR_BLUE:   f4State = !f4State; break;
  }
}

void loop() {
  // 1. Monitor Bus Status
  if (digitalRead(pinBUS_STOP) == LOW && isSystemGo) {
    isSystemGo = false;
  } else if (digitalRead(pinBUS_GO) == LOW && !isSystemGo) {
    isSystemGo = true;
  }

  // 2. IR Input
  uint32_t irCmd = readSamsungIR();
  if (irCmd != 0) {
    handleIRCommand(irCmd);
    delay(200); // Simple debounce
  }

  // 3. Send Commands
  if (isSystemGo) {
    bool addrChanged = (currentLocoAddr != lastSentAddr);
    byte currentF1to4 = (f1State ? 1 : 0) | (f2State ? 2 : 0) | (f3State ? 4 : 0) | (f4State ? 8 : 0);

    if (currentSpeed != lastSentSpeed || f0State != lastSentF0 || addrChanged) {
      sendLocoCommand(currentLocoAddr, currentSpeed, f0State);
    }

    if (currentF1to4 != lastSentF1to4 || addrChanged) {
      sendFunctionCommand(currentLocoAddr, f1State, f2State, f3State, f4State);
    }

    lastSentSpeed = currentSpeed;
    lastSentF0 = f0State;
    lastSentF1to4 = currentF1to4;
    lastSentAddr = currentLocoAddr;
  }

  delay(50);
}
