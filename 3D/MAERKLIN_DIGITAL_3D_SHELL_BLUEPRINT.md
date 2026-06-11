# Logical Blueprint: Two-Part Shell (Top/Bottom)

This document defines the geometric operations required to create the two-part modular housing (Top Shell and Bottom Plate) using the parametric constants from `MAERKLIN_DIGITAL_3D_PARAMETERS.md`.

## 1. Top Shell Construction (The "Wedge")

The Top Shell is derived from the primary wedge primitive. It is modeled as a hollowed-out shell with an open base.

### 1.1 Outer Geometry
- **Primitive**: Truncated Wedge.
- **Vertices**: V0 through V7 as defined in `PARAMETERS.md`.
- **Logic**: Create a solid volume encompassing these coordinates.

### 1.2 Inner Hollowing (The Cavity)
To create the internal space for electronics, an inner volume is subtracted from the outer wedge.
- **Offset Logic**: The inner volume is the outer wedge shrunk by `thick` (2.5 mm) on the following faces:
    - Left/Right sides (X-axis).
    - Front/Back sides (Y-axis).
    - Top slope (Z/Y-axis).
- **Bottom Face**: The bottom face (Z=0) remains open (no wall).
- **Operation**: `Top_Shell = Outer_Wedge - Inner_Cavity`.

### 1.3 Technical Considerations
- **Fillets**: External vertical edges (V0-V4, V1-V5, etc.) should have a 2.0 mm radius fillet for ergonomics and matching original aesthetics.
- **Draft Angles**: Since this is intended for 3D printing, no specific draft angles are required, but the 14.036° slope acts as a natural draft for the top surface.

## 2. Bottom Plate Construction

The Bottom Plate is a flat removable panel that secures the internal components and provides the mounting interface for the Top Shell.

### 2.1 Geometry
- **Shape**: Rectangular Prism.
- **Dimensions**:
    - **Width**: `w_std` (or `w_slim`) - `(2 * tol)`
    - **Depth**: `depth` - `(2 * tol)`
    - **Thickness**: `thick` (2.5 mm).
- **Logic**: The dimensions are slightly smaller than the outer shell footprint to account for `printing tolerance` and ensure a flush fit inside the shell's rim (if a recessed rim is used).

### 2.2 Rim Interface (Optional but Recommended)
To prevent the plate from sliding:
- **Feature**: A 1.0 mm deep step (recess) around the internal bottom perimeter of the Top Shell.
- **Counterpart**: The Bottom Plate sits within this recess.

## 3. Assembly Logic
- The Top Shell and Bottom Plate are aligned on the XY plane.
- The Bottom Plate's Z-top surface meets the Top Shell's internal "boss" surfaces (see `FASTENING_BLUEPRINT.md`).
- The final Z-height of the assembly remains `h_front` and `h_back` as specified.
