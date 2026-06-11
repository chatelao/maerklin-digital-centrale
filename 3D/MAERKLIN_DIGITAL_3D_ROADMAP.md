# Roadmap: 3D Modeling of Märklin Digital 60xx Series Housings

This roadmap outlines the plan for creating accurate 3D models of the classic Märklin Digital "60xx" series device housings from the 1990s.

## Progress Overview

| Phase | Description | Status |
| :--- | :--- | :--- |
| Phase 0 | Conceptualization & High-Level Architecture | ✅ |
| Phase 1 | Detailed Design & Technical Specifications | ✅ |
| Phase 2 | Data Collection & Measurement | ✅ |
| Phase 3 | Logical & Primitive Modeling | ⏳ |
| Phase 4 | Modular Features (Logical Blueprinting) | ⏳ |
| Phase 5 | Device-Specific Implementation | ⏳ |

## Goals
- Create high-fidelity 3D CAD models of the modular housing system. ✅
- Document precise physical dimensions and geometric features. 🚧
- Model the physical interlocking and electrical coupling interfaces. 🚧
- Specify material properties and visual styles (colors, textures). 🚧

## Phases

### Phase 0: Conceptualization
- [x] Define Vision and Business Cases in `CONCEPT.md`.
- [x] Establish high-level functional architecture.

### Phase 1: Detailed Design
- [x] Derive technical choices in `DESIGN.md`.
- [x] Define global parametric spreadsheet aliases.
- [x] Create top-level component diagram (`TOP_ARCHITECTURE.puml`).

### Phase 2: Data Collection & Measurement
- [x] Measure total width, height (front/back), and depth for each modular size.
- [x] Document the slope angle of the front panel in `MAERKLIN_DIGITAL_3D_PARAMETERS.md`.
- [x] Map the exact coordinates of the DIN 41612 connector cutouts on the side panels.
- [x] Formalize all geometric constants in `MAERKLIN_DIGITAL_3D_PARAMETERS.md`.

### Phase 3: Primitive Modeling
- [ ] Create base "wedge" templates in FreeCAD for standard and slim widths.
- [ ] Implement the `Params` spreadsheet logic.
- [ ] Model the basic two-part shell (Top/Bottom).
- [ ] Implement screw bosses and inlay cavities for durable fastening.

### Phase 4: Modular Features
- [ ] Create the Boolean Tool library for interlocking side-panels (DE 84 27 671 U1).
- [ ] Create the Boolean Tool for DIN 41612 connector cutouts.
- [ ] Implement a library of common ventilation slot patterns.
- [ ] Develop template for faceplate inlays and dual-color accents for printing efficiency.

### Phase 5: Device-Specific Implementation
- [ ] Model the **Control Unit 6021** (including knob and buttons).
- [ ] Model the **Keyboard 6040** (membrane grid).
- [ ] Model the **Control 80f (6036)**.
- [ ] Model the **6020/Transformer** dummy cases for modern electronics.

## Reference Documentation
- [CONCEPT.md](MAERKLIN_DIGITAL_3D_CONCEPT.md)
- [DESIGN.md](MAERKLIN_DIGITAL_3D_DESIGN.md)
- [PARAMETERS.md](MAERKLIN_DIGITAL_3D_PARAMETERS.md) - Geometric constants and logic.
- [Geraeteuebersicht.md](../Geraeteuebersicht.md) - List of system components.
- [Pinout_Bus-Maerklin-Digital-6020.md](../Pinout_Bus-Maerklin-Digital-6020.md) - Connector specifications.
- [patents/README.md](../patents/README.md) - Design protection and coupling mechanism details.
