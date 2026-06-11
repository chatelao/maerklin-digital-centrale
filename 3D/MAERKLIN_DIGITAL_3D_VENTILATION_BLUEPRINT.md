# Logical Blueprint: Ventilation Patterns

This document defines the geometric parameters and Boolean logic for the characteristic ventilation slots found on the top sloped surface of the Märklin Digital 60xx series housings.

## 1. Ventilation Slot "Tool"

Each slot is modeled as a rounded-end rectangular cutout (oblong hole) that is subtracted from the Top Shell.

### 1.1 Single Slot Parameters
| Parameter | Alias | Value | Description |
| :--- | :--- | :--- | :--- |
| **Slot Width** | `v_slot_w` | 2.0 mm | Width of the opening. |
| **Slot Length**| `v_slot_l` | 35.0 mm | Total length along the Y-axis (sloped). |
| **Slot Pitch** | `v_slot_p` | 4.0 mm | Center-to-center distance between slots. |
| **Full Depth** | `v_slot_d` | `thick` + 2mm | Extrusion depth to ensure a clean cut. |

## 2. Pattern Layouts

Slots are organized into "Banks" depending on the device width.

### 2.1 Standard Width (135mm) - e.g., 6021, 6040
The standard housing typically features two symmetrical banks of slots on the top sloped surface.

- **Slots per Bank**: 12
- **Bank 1 (Left)**:
  - **Center X**: 30.0 mm
  - **Start Y**: 40.0 mm (relative to front edge V4-V7)
- **Bank 2 (Right)**:
  - **Center X**: 105.0 mm (symmetrical to left)
  - **Start Y**: 40.0 mm

### 2.2 Slim Width (67.5mm) - e.g., 6036, 6050
The slim housing features a single central bank.

- **Slots per Bank**: 8
- **Bank 1 (Center)**:
  - **Center X**: 33.75 mm (Width / 2)
  - **Start Y**: 40.0 mm

## 3. Boolean Implementation Logic

1. **Create the Tool**: Generate a single slot primitive (Box or Cylinder-capped Box).
2. **Apply Array**: Use a Linear Array (Draft or PartDesign MultiTransform) to repeat the slot `v_slot_p` apart.
3. **Alignment**:
   - Rotate the bank by `slope` (14.036°) around the X-axis.
   - Position the bank so it is centered on the top sloped face according to the coordinates above.
4. **Subtraction**: `Top_Shell_Vented = Top_Shell - (Bank_1 + Bank_2)`.

## 4. Aesthetic Variations
While the 6021 (Central Unit) requires these slots for cooling the internal booster, the 6040 (Keyboard) often utilizes the same housing for manufacturing efficiency. For historical accuracy, these patterns should be maintained across all 3D models in the series.
