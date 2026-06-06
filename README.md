# Märklin Digital I2C-Bus Documentation

This repository contains technical documentation, protocol specifications, and historical references for the Märklin Digital-System I2C-Bus (MM1 & MM2).

## Source of Knowledge

A significant portion of the modern technical insights and hardware pinouts in this repository is sourced from or inspired by the [deltaphi/c6021light](https://github.com/deltaphi/c6021light) project. The `c6021light` project provides invaluable information on connecting classic Märklin hardware (like the Keyboard 6040) to modern interfaces.

## Documentation Index

- **[Datasheet: Märklin Digital I2C-Bus (MM1 & MM2)](Datasheet_MM1-MM2-Bus.md)**: A modern, structured datasheet covering the physical layer, addressing (including the chain mechanism), and command protocols for locomotives and accessories.
- **[Geräteübersicht Märklin Digital (60xx Serie)](Geraeteuebersicht.md)**: Eine detaillierte Übersicht der Hardware-Komponenten und Dekoder.
- **[Data communication on the I2C-Bus (EI2C.md)](EI2C.md)**: An English translation of the classic documentation by Walter Fiedler, originally hosted on Dr. König's Märklin-Digital-Page.

## Repository Structure

- `/sources`: Original source materials, including PDFs of manuals and historical HTML/ZIP files from `drkoenig.de`.
- `/diagrams`: PlantUML source files for sequence and flow diagrams used in the documentation.
- `/images_6015`, `/images_6017`, `/images_6021`, `/images_6050`: Image assets related to specific Märklin Digital components.

## Technical Highlights

- **Multi-Master Architecture**: Any device on the bus can act as a master to send commands.
- **Addressing Chain**: Dynamic software addressing using the `b12` pin.
- **Protocol Formats**: Detailed breakdown of MM1 and MM2 (extended Motorola) formats.
- **Connector Pinouts**: Standard DIN 41612 B/2 pinouts for the I2C bus and RJ12 for LocoNet.

## Connector Samples

The following DIN 41612 B/2 style 90° THT (Through-Hole Technology) connectors are recommended for custom hardware interfacing with classic Märklin components:

- **Male Connector (Messerleiste)**: ept [101-90014](https://www.ept.de/101-90014_de)
- **Female Connector (Federleiste)**: ept [120-90064](https://www.ept.de/120-90064_de)

---
*Note: This repository is intended for educational and reference purposes for hobbyists working with legacy Märklin Digital equipment.*
