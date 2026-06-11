# Logical Blueprint: Interlocking Side-Panels (Boolean Tool)

This document details the "Boolean Tool" strategy for implementing the patented (DE 84 27 671 U1) interlocking mechanism on the housing side panels.

## 1. The "Boolean Tool" Concept

Instead of sketching tabs and slots directly on the housing, we define a "Tool" object. This tool is a master representation of the interlocking geometry.
- **Addition (Union)**: To the Right Side of a housing to create male tabs.
- **Subtraction (Difference)**: From the Left Side of a housing to create female slots.

## 2. Tool Geometry: `Interlock_Tool`

The tool consists of two identical interlocking blocks positioned along the Y-axis.

### 2.1 Block Dimensions
- **Width (X)**: 5.0 mm (The protrusion depth).
- **Height (Z)**: 10.0 mm (Centered at Z = 12.5 mm).
- **Depth (Y)**: 20.0 mm.
- **Chamfer**: 1.0 mm x 45° on the leading edges (Front/Back/Top/Bottom of the protrusion) to facilitate smooth sliding and account for 3D printing inaccuracies.

### 2.2 Alignment & Position
The tool defines the positions of two blocks relative to the device's origin (V0).
- **Block 1 (Front)**: Y-center = 20.0 mm.
- **Block 2 (Back)**: Y-center = 100.0 mm.
- **Vertical Center**: Z-center = 12.5 mm.

## 3. Implementation Logic

### 3.1 Right Side (Male Interface)
- **Operation**: `Housing_Right = Housing_Base + Interlock_Tool`.
- **Transformation**: Move `Interlock_Tool` to X = `w_std`.
- **Result**: Two tabs protruding 5mm from the right wall.

### 3.2 Left Side (Female Interface)
- **Operation**: `Housing_Left = Housing_Base - Interlock_Tool_Scaled`.
- **Scaling/Tolerance**: The tool used for subtraction is scaled by `tol` (0.2 mm) in every dimension to create a snug but functional fit.
- **Transformation**: Move `Interlock_Tool_Scaled` to X = 0.
- **Result**: Two slots recessed 5mm into the left wall.

## 4. DIN 41612 Cutout Integration

The DIN 41612 cutout is centered between the two interlocking blocks (at Y = 60 mm). This ensures that the electrical coupling (the bus) is protected and aligned by the mechanical interlocking of the shells.

- **Cutout Tool**: A 54.8 mm x 14.8 mm rectangle extruded through the wall.
- **Z-Center**: 12.5 mm (Matching the Interlock axis).
- **Y-Center**: 60.0 mm.
