# 3D Modeling Concept: Märklin Digital 60xx Housings (FreeCAD)

## 1. Modeling Philosophy
The objective is to create a fully parametric, modular system for the classic 1990s "wedge" housings using **FreeCAD**.

### Key Principles:
- **Parametric Design**: Every dimension (width, height, angle) must be adjustable via a central spreadsheet.
- **Part Design Workbench**: Use the standard Part Design workflow (Sketch -> Pad -> Pocket/Hole) for maximum compatibility.
- **Top-Down Assembly**: Design components (Top Shell, Bottom Plate, Side Panels) so they reference the same master parameters.

## 2. Global Parameters (Spreadsheet)
A spreadsheet named `Params` should define the core geometry:

| Name | Alias | Description | Typical Value |
| :--- | :--- | :--- | :--- |
| `Width_Std` | `w_std` | Width of standard devices (6021, 6040) | 135 mm |
| `Width_Slim` | `w_slim` | Width of slim devices (6036, 6050) | 67.5 mm |
| `Depth` | `depth` | Total depth of the unit | 120 mm |
| `Height_Front` | `h_front` | Height of the front edge | 25 mm |
| `Height_Back` | `h_back` | Height of the back edge | 55 mm |
| `Wall_Thick` | `thick` | Standard wall thickness for printing | 2.5 mm |
| `Slope_Angle` | `angle` | Calculated angle of the front panel | `atan((h_back-h_front)/depth)` |

## 3. Modeling Steps for the "Standard Wedge"

### Step 3.1: Base Profile Sketch
1. Create a sketch on the YZ-plane (Side View).
2. Draw the characteristic trapezoidal profile using `depth`, `h_front`, and `h_back`.
3. Constrain the top edge to the `angle`.

### Step 3.2: Main Body (Pad)
1. Extrude (Pad) the sketch using the `w_std` or `w_slim` parameter.
2. For symmetric units, pad symmetrically to the plane.

### Step 3.3: Shelling (Top Cover)
1. Select the bottom face and apply the **Thickness** tool (pointing inwards) using `thick`.
2. This creates the hollow shell for the electronics.

### Step 3.4: Side Panels & Interlocking (DE 84 27 671 U1)
1. Model the male (tab) and female (slot) profiles on the side faces.
2. The interlocking mechanism ensures devices "click" together.
3. Ensure exact positioning of the DIN 41612 B/2 connector cutouts (refer to [Pinout_Bus-Maerklin-Digital-6020.md](../Pinout_Bus-Maerklin-Digital-6020.md)).

## 4. Replacement Housings: 6020 and "Transformer"
The first implementation phase focuses on replacing the plain housings of the Central Unit 6020 and the 6001/6002 Transformers.

### 4.1 Central Unit 6020 Style
- **Exterior**: A "clean" wedge without top-side button cutouts or knobs.
- **Interior**: Integrated stand-offs for an Arduino Mega or Raspberry Pi Pico, and a 5V/8V voltage regulator.
- **Connectivity**: Cutouts for a DC barrel jack (input) and terminal blocks (track output) in the rear.

### 4.2 Transformer (6001/6002) Style
- **Exterior**: Matches the standard width but may require increased height or venting if housing a real AC transformer.
- **Application**: Often used as a decorative "dummy" housing for modern DC power supplies or DIY Booster circuits.
- **Cooling**: Model the characteristic ventilation slots on the top sloped surface.

## 5. Export and Printing
- **Format**: Export as `STEP` for CAD exchange and `STL/3MF` for 3D printing.
- **Orientation**: Print the top shell upside down (sloped face on the bed) to minimize supports, or standing on the rear face.
