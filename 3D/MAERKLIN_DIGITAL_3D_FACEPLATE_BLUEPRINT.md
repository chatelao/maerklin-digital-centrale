# Logical Blueprint: Faceplate Inlay & Control Components

This document defines the geometric operations for creating the decorative faceplate inlays and the standard control components (knobs and buttons) for the 60xx series housings.

## 1. Faceplate Inlay System

The faceplate system enables dual-color printing by separating the front panel's decorative surface from the main top shell.

### 1.1 Faceplate Pocket (Subtraction)
- **Host**: Top Shell (sloped surface).
- **Shape**: Rectangular area on the front-half of the sloped top.
- **Dimensions**:
    - **Width**: `width - (2 * FP_INSET)`
    - **Length (Y-axis along slope)**: Covers the area from the front edge to a specified depth (e.g., 60mm).
- **Depth**: `FP_POCKET_DEPTH` (1.0 mm), subtracted perpendicular to the sloped face.
- **Logic**: A Boolean tool is used to subtract this volume from the top shell, creating a recessed "bed" for the inlay.

### 1.2 Faceplate Inlay (Add-on)
- **Shape**: Matches the pocket dimensions.
- **Thickness**: `FP_THICK` (0.8 mm).
- **Tolerance**: A 0.2 mm air gap is maintained between the inlay and the pocket walls to ensure a smooth fit after printing.
- **Customization**: This part contains the specific cutouts for displays, buttons, and knobs for each device (e.g., 6021 vs 6040).

## 2. Control Components

Standardized physical controls used across multiple 60xx devices.

### 2.1 Speed Control Knob (Standard Style)
- **Primary Shape**: Cylinder.
- **Dimensions**:
    - **Diameter**: `KNOB_DIA` (30.0 mm).
    - **Height**: `KNOB_H` (15.0 mm).
- **Details**:
    - **Top**: Slightly domed or with a small circular recess.
    - **Sides**: Fine vertical knurling or a single "pointer" notch.
    - **Internal**: A 6.0 mm hole for the potentiometer shaft.

### 2.2 Square Push Buttons
- **Primary Shape**: Box.
- **Dimensions**:
    - **Top Surface**: `BTN_SIZE` x `BTN_SIZE` (12.0 mm x 12.0 mm).
    - **Height**: ~10.0 mm total.
- **Bezel/Cutout**: The faceplate inlay features square cutouts of `BTN_CUTOUT` (12.4 mm) to allow clearance for the button caps.

## 3. Assembly Logic
1. The **Top Shell** is printed with the recessed pocket.
2. The **Faceplate Inlay** (printed in a contrasting color, e.g., black or white) is glued or snapped into the pocket.
3. **Buttons and Knobs** are mounted through the cutouts onto the internal PCBs.
