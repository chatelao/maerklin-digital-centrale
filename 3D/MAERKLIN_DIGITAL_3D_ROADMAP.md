# Roadmap: 3D Modeling of Märklin Digital 60xx Series Housings

This roadmap outlines the plan for creating accurate 3D models of the classic Märklin Digital "60xx" series device housings from the 1990s.

## Progress Overview

| Phase | Description | Status |
| :--- | :--- | :--- |
| Phase 0 | Conceptualization & High-Level Architecture | ✅ |
| Phase 1 | Detailed Design & Technical Specifications | ✅ |
| Phase 2 | Data Collection & Measurement | ✅ |
| Phase 3 | Logical & Primitive Modeling | ✅ |
| Phase 4 | Modular Features (Logical Blueprinting) | ✅ |
| Phase 5 | Device-Specific Implementation | ⏳ |

## Goals
- Create high-fidelity 3D CAD models of the modular housing system. ✅
- Document precise physical dimensions and geometric features. ✅
- Model the physical interlocking and electrical coupling interfaces. ✅
- Specify material properties and visual styles (colors, textures). ✅

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
- [x] Create base "wedge" logic in `mDigital_Wedge.py` for standard and slim widths.
- [x] Create the parametric constants module `mDigital_Params.py`.
- [x] Formalize the `Params` spreadsheet logic in `PARAMETERS.md`.
- [x] Create logical blueprint for the basic two-part shell (Top/Bottom).
- [x] Create logical blueprint for screw bosses and inlay cavities.

### Phase 4: Modular Features
- [x] Create the Boolean Tool blueprint for interlocking side-panels (DE 84 27 671 U1).
- [x] Create the Boolean Tool blueprint for DIN 41612 connector cutouts.
- [x] Create the logical blueprint for ventilation slot patterns.
- [x] Implement the modular feature library in Python (Interlocks, DIN, Vents).
- [x] Develop template for faceplate inlays and dual-color accents for printing efficiency.

### Phase 5: Device-Specific Implementation
- [ ] **Component Library**:
    - [x] Model the speed control knob (standard 6021/6035 style).
    - [x] Model the square momentary push-buttons (red/gray).
    - [x] Model the 4-digit 7-segment display bezel.
- [ ] **Full Assemblies**:
    - [x] Model the **Control Unit 6021** (Main housing + specialized faceplate).
    - [x] Model the **Keyboard 6040** (Key matrix layout).
    - [x] Model the **Control 80f (6036)** (Slim housing + throttle knob).
    - [ ] Model the **6020/Transformer** dummy cases for modern electronics.

## Reference Documentation
- [CONCEPT.md](MAERKLIN_DIGITAL_3D_CONCEPT.md)
- [DESIGN.md](MAERKLIN_DIGITAL_3D_DESIGN.md)
- [PARAMETERS.md](MAERKLIN_DIGITAL_3D_PARAMETERS.md) - Geometric constants and logic.
- [SHELL_BLUEPRINT.md](MAERKLIN_DIGITAL_3D_SHELL_BLUEPRINT.md) - Two-part shell logic.
- [FASTENING_BLUEPRINT.md](MAERKLIN_DIGITAL_3D_FASTENING_BLUEPRINT.md) - Screws and inlays.
- [INTERLOCK_BLUEPRINT.md](MAERKLIN_DIGITAL_3D_INTERLOCK_BLUEPRINT.md) - Side interlocking logic.
- [Geraeteuebersicht.md](../Geraeteuebersicht.md) - List of system components.
- [Pinout_Bus-Maerklin-Digital-6020.md](../Pinout_Bus-Maerklin-Digital-6020.md) - Connector specifications.
- [patents/README.md](../patents/README.md) - Design protection and coupling mechanism details.
