# Roadmap: 3D Modeling of Märklin Digital 60xx Series Housings

This roadmap outlines the plan for creating accurate 3D models of the classic Märklin Digital "60xx" series device housings from the 1990s. These models will serve as a basis for digital preservation, technical documentation, and potential custom hardware integration.

## 1. Project Objectives
- Create high-fidelity 3D CAD models of the modular housing system.
- Document precise physical dimensions and geometric features (the "wedge" shape).
- Model the physical interlocking and electrical coupling interfaces.
- Specify material properties and visual styles (colors, textures).

## 2. Target Devices
Based on the [Geräteübersicht](../Geraeteuebersicht.md), the initial modeling focus will be on the following core units:
- **Control Unit 6021**: The system master, featuring a speed knob and 'Stop/Go' buttons.
- **Control 80 / 80f (6035/6036)**: Slim locomotive control units.
- **Keyboard 6040**: Solenoid accessory control with a characteristic membrane button grid.
- **Interface 6050/6051**: Communication module with serial port.

## 3. Design Specifications

### 3.1 Housing Geometry
- **Form Factor**: The devices utilize a characteristic "wedge" or "sloped" design, optimizing ergonomics for desk-top use.
- **Modular Widths**: The system employs a modular width system.
    - *Standard Units*: (e.g., 6021, 6040)
    - *Slim Units*: (e.g., 6036, 6050)
- **Assembly**: Housings typically consist of a top shell, a bottom plate, and side panels for the bus connectors.

### 3.2 Coupling Mechanism
Models must accurately reflect the utility model **DE 84 27 671 U1** ([see Patent documentation](../patents/README.md)):
- **Electrical Interface**: 32-pin DIN 41612 Bauform B/2 connectors.
- **Physical Interlocking**: Side-mounted slots and tabs that allow devices to "click" together, ensuring a stable physical bus.

### 3.3 Visual Identity
- **Primary Color**: "Märklin-Grau" (Märklin Grey).
- **Accent Elements**: Red 'Stop' and 'Go' buttons, black knobs, and specific membrane keyboard layouts.

## 4. Modeling Roadmap

### Phase 1: Data Collection & Measurement
*Prerequisite: Physical specimens required for vernier caliper measurement.*
- [ ] Measure total width, height (front/back), and depth for each modular size.
- [ ] Document the slope angle of the front panel.
- [ ] Map the exact coordinates of the DIN 41612 connector cutouts on the side panels.
- [ ] Measure button and knob diameters and positions.

### Phase 2: Primitive Modeling
- [ ] Create base "wedge" templates for standard and slim widths.
- [ ] Implement the interlocking side-panel profiles.
- [ ] Model the DIN 41612 connector shells for integration.

### Phase 3: Detail & Aesthetics
- [ ] Add surface features (cooling vents, screw holes on the bottom).
- [ ] Model interactive elements: Knobs (6021), Sliders (6036), and Buttons.
- [ ] Apply "Märklin-Grau" PBR materials and textures for membrane keyboards.

### Phase 4: Export & Integration
- [ ] Export to standard formats (STL, STEP, OBJ).
- [ ] Create renders for technical documentation.

## 5. Reference Documentation
- [Geraeteuebersicht.md](../Geraeteuebersicht.md) - List of system components.
- [Pinout_Bus-Maerklin-Digital-6020.md](../Pinout_Bus-Maerklin-Digital-6020.md) - Connector specifications.
- [patents/README.md](../patents/README.md) - Design protection and coupling mechanism details.
