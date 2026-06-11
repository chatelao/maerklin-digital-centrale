# Logical Blueprint: Fastening System (Screws & Inlays)

This document specifies the internal mechanical structures for securing the Bottom Plate to the Top Shell using M3 machine screws and heat-set brass inlays.

## 1. Parameters Refresher
Referencing `DESIGN.md`:
- `screw_size`: 3.0 mm (M3)
- `inlay_dia`: 4.6 mm
- `inlay_depth`: 5.0 mm
- `thick`: 2.5 mm

## 2. Screw Bosses (Top Shell)

Four cylindrical bosses are located at the internal corners of the Top Shell to provide a mounting surface for the heat-set inlays.

### 2.1 Boss Geometry
- **Shape**: Cylinder.
- **Outer Diameter**: `inlay_dia + (2 * thick)` (approx. 9.6 mm).
- **Height**: Extends from the internal top surface down to Z = `thick` (the mating surface with the bottom plate).
- **Cavity**: A central hole of diameter `inlay_dia` and depth `inlay_depth` + 0.5mm (for plastic melt displacement).

### 2.2 Placement (Standard Width)
Four bosses positioned symmetrically to avoid interference with the side-interlocks.
- **Front-Left**: X = 15 mm, Y = 15 mm
- **Front-Right**: X = `w_std` - 15 mm, Y = 15 mm
- **Back-Left**: X = 15 mm, Y = `depth` - 15 mm
- **Back-Right**: X = `w_std` - 15 mm, Y = `depth` - 15 mm

## 3. Counter-bored Holes (Bottom Plate)

The Bottom Plate features four matching holes to allow M3 screws to pass through and sit flush or recessed.

### 3.1 Hole Geometry
- **Pass-through Hole**: Diameter 3.4 mm (Clearance for M3).
- **Counter-bore**: Diameter 6.5 mm, Depth 3.0 mm (to accommodate DIN 912 or ISO 4762 socket head caps).
- **Logic**: `Bottom_Plate = Plate_Body - (Pass_Hole_Set + Counterbore_Set)`.

### 3.2 Placement
Must be perfectly concentric with the Top Shell bosses:
- Same (X, Y) coordinates as defined in Section 2.2.

## 4. Hardware Specification
- **Fastener**: M3 x 8mm or M3 x 10mm Socket Head Cap Screw (ISO 4762).
- **Inlay**: M3 Heat-set Insert for plastics (e.g., Ruthex or similar, 4.6mm OD).

## 5. Boolean Logic Summary
- `Top_Shell_Final = Top_Shell_Body + Boss_Set - Inlay_Cavity_Set`.
- `Bottom_Plate_Final = Bottom_Plate_Body - Counterbore_Hole_Set`.
