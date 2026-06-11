# Physical Parameters: Märklin Digital 60xx Housings

This document serves as the primary "Source of Truth" for the geometric and parametric logic used to recreate the 3D models of the 60xx series.

## 1. Global Dimensions & Constants

| Parameter | Alias | Value | Calculation / Source |
| :--- | :--- | :--- | :--- |
| **Standard Width** | `w_std` | 135.0 mm | Measurement |
| **Slim Width** | `w_slim` | 67.5 mm | Measurement |
| **Total Depth** | `depth` | 120.0 mm | Measurement |
| **Front Height** | `h_front` | 25.0 mm | Measurement |
| **Back Height** | `h_back` | 55.0 mm | Measurement |
| **Wall Thickness** | `thick` | 2.5 mm | Structural Requirement |
| **Printing Tolerance** | `tol` | 0.2 mm | 3D Printing Standard |
| **Slope Angle** | `slope` | ~14.036° | `atan((55-25)/120)` |

## 2. Geometric Primitive: The Wedge
The base chassis is defined by 8 vertices forming a truncated wedge.

| Vertex | Location | X (mm) | Y (mm) | Z (mm) |
| :--- | :--- | :---: | :---: | :---: |
| **V0** | Bottom-Front-Left | 0 | 0 | 0 |
| **V1** | Bottom-Back-Left | 0 | 120 | 0 |
| **V2** | Bottom-Back-Right | `w_std` | 120 | 0 |
| **V3** | Bottom-Front-Right | `w_std` | 0 | 0 |
| **V4** | Top-Front-Left | 0 | 0 | 25 |
| **V5** | Top-Back-Left | 0 | 120 | 55 |
| **V6** | Top-Back-Right | `w_std` | 120 | 55 |
| **V7** | Top-Front-Right | `w_std` | 0 | 25 |

## 3. Modular Interfaces

### 3.1 DIN 41612 B/2 Cutout (Bus Coupling)
The cutout allows the 32-pole I2C bus connector to pass through the side panels.

- **Bounding Box (L x H x D)**: 54.8 mm x 14.8 mm x `thick`
- **Center Y (Depth)**: 60.0 mm (Centered)
- **Center Z (Height)**: 12.5 mm (Aligned with front-half height)
- **Rotation**: Parallel to XY plane.

### 3.2 Interlocking Side-Panels (Patent DE 84 27 671 U1)
The mechanical interlock uses asymmetric tabs and slots.

- **Tab Profile**: Rectangular with chamfered edges.
- **Quantity**: 2 per side (Front/Back pair).
- **Positioning**:
    - **Front Tab/Slot**: Y = 20 mm
    - **Back Tab/Slot**: Y = 100 mm
- **Vertical Alignment**: Centered at Z = 12.5 mm (matching DIN 41612 axis).
- **Asymmetry**:
    - **Right Side (Male)**: Protruding tabs (Width = 5.0 mm).
    - **Left Side (Female)**: Inset slots (Depth = 5.2 mm including tolerance).

### 3.3 Faceplate Inlay & Controls
To support dual-color printing and device-specific layouts.

- **Faceplate Pocket Depth**: 1.0 mm (Boolean subtraction from Top Shell).
- **Faceplate Thickness**: 0.8 mm (providing 0.2 mm clearance/tolerance).
- **Speed Control Knob**:
    - **Diameter**: 30.0 mm
    - **Height**: 15.0 mm
    - **Shaft Hole**: 6.0 mm (D-shape or knurled).
- **Push Buttons (Square)**:
    - **Size**: 12.0 mm x 12.0 mm
    - **Bezel Cutout**: 12.4 mm x 12.4 mm

## 4. Materials & Aesthetics

| Feature | Specification | RAL / Hex |
| :--- | :--- | :--- |
| **Main Housing** | Märklin-Grau (Pebble Grey) | RAL 7032 / `#B1B1B1` |
| **Control Knobs** | Black | RAL 9005 / `#000000` |
| **Accent Buttons** | Signal Red | RAL 3001 / `#A52019` |
| **Finish** | Fine Matte Texture | - |
