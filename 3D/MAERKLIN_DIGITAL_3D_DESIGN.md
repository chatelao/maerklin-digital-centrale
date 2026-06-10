# 3D Modeling Design: Märklin Digital 60xx Housings

## 1. Technical Architecture
The design follows a top-down parametric approach in FreeCAD, where a master spreadsheet drives the geometry of all components to ensure perfect interlocking and modularity.

![Top Architecture](https://kroki.io/plantuml/svg/eJxdkk1Lw0AQhu_7K4acFCykpfTgQfqlUrASrOhBpGyzk3Zpsht2J2oQ_7v7YRNqTjvzPvvuzEumlrihpipZzfMj3yMkGTe8QkJjE_hm4L63TW2QC3tAJLgIur18B24hntkP66_PuUW4R-0sTNs5vKJwYmZ0IUuEzREpP0SH2IrUmkvlPEVQfDHXoj1zX2vRlNzAHXJqDPYjrpSbuNT5Uao9PMid4aYNNp0QueXqEcbDyXAEi4Z0Q4Fxzai-oCJZcpLaz0HuprKB8ML5nkv8kLlbpcZcFjLvJ5mkoxSWTVXF930ZhWfDlS20qdDAwqUU5NCM-qKxpCt4ykbpOO2JWPu3Y9owGNx0SV5D8rm1JK7gsC2MVuQPOzdjwk6Ix09Zev72i0wjMGFd0xNdTB6Za10iVzCr67L9B_oAHZI5FClhrL_o1bCtR7qChehCHXcN-fjyb1FnNhMC3I-ohC4K6zynqIT7J38BrInOPg==)

## 2. Global Parameters (Spreadsheet `Params`)
To maintain consistency, all models must reference the following aliases from a `Params` spreadsheet:

| Alias | Description | Dimension |
| :--- | :--- | :--- |
| `w_std` | Standard width (6021, 6040) | 135 mm |
| `w_slim` | Slim width (6036, 6050) | 67.5 mm |
| `depth` | Total depth | 120 mm |
| `h_front`| Front edge height | 25 mm |
| `h_back` | Back edge height | 55 mm |
| `thick`  | Wall thickness | 2.5 mm |
| `tol`    | Printing tolerance | 0.2 mm |

Detailed derived constants and vertex coordinates are maintained in [MAERKLIN_DIGITAL_3D_PARAMETERS.md](MAERKLIN_DIGITAL_3D_PARAMETERS.md).

## 3. Technical Interfaces

### 3.1 Side Interlocking (Bus Coupling)
The interlocking mechanism is based on Patent DE 84 27 671 U1. It consists of:
- **Left Side**: Female slots (grooves) to receive the neighboring unit's tabs.
- **Right Side**: Male tabs positioned to match the neighbor's slots.
- **Alignment**: The vertical center of the interlocking features is aligned with the DIN 41612 connector center.

### 3.2 Electrical Cutouts
- **DIN 41612 B/2**: A rectangular cutout of 50mm x 15mm (approx.) located on the side panels.
- **Position**: Must be mirrored between left and right sides to allow a straight pass-through of the I2C bus.

## 4. Modeling Workflow
1. **Sketching**: Profiles are drawn on the YZ-plane using spreadsheet-driven constraints.
2. **Padding**: Extrusion length is set to `w_std` or `w_slim`.
3. **Thicknessing**: Shelling is performed using the `PartDesign Thickness` tool.
4. **Boolean Operations**: Standardized "Tool" objects (for DIN cutouts and interlocks) are subtracted from or added to the main body.

## 5. Major Choices

### Choice 5.1: Side Interlocking Implementation
The interlocking tabs and slots must be precise.

| Alternative | Description | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **A: Integrated Sketch** | Draw tabs/slots directly in the side panel sketch. | Simple file structure. | Difficult to reuse across different models; prone to breakage if width changes. |
| **B: Boolean Tooling** | **[CHOSEN]** Create separate "Interlock_Tool" parts and use Boolean fragments or subtractions. | High modularity; tools can be reused for every new device. | Slightly more complex part tree. |
| **C: PartDesign Multi-transform** | Use linear patterns to create multiple tabs. | Efficient for repetitive features. | Side interlocking is asymmetric (tabs one side, slots other), making simple transforms difficult. |

**Justification for Boolean Tooling**: This allows us to maintain a single "master" definition of the interlocking geometry that is applied to every new housing design, ensuring 100% compatibility between 3D-printed units.

### Choice 5.2: Cooling Vent Logic
Original units have specific ventilation patterns.

| Alternative | Description | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **A: Modeled Geometry** | Vents are cut out of the 3D model. | **[CHOSEN]** High fidelity; looks original; allows heat dissipation for DIY boosters. | Increases STL file size and slicing time. |
| **B: Texture Mapping** | Vents are only represented as a visual texture. | Very lightweight model. | Useless for functional 3D printing. |
| **C: Infill-based Vents** | Leave gaps in the top surface for the slicer infill to show. | Easy to print; unique look. | Does not match the historical appearance. |

**Justification for Modeled Geometry**: Since the goal includes both preservation and custom hardware (which might generate heat), physical ventilation slots are necessary.
