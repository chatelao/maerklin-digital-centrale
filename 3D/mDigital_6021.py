import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Digital 6021 Control Unit - Full Assembly
Standard housing with specialized faceplate for display, keypad, and knob.
"""

def create_6021_assembly():
    # 1. Generate the Top Shell (including faceplate pocket subtraction)
    top_shell = W.generate_top_shell(P.W_STD, include_faceplate=True)

    # 2. Generate the specialized Faceplate Inlay
    inlay = F.create_6021_faceplate_inlay()

    # 3. Generate the Bottom Plate
    bottom_plate = W.generate_bottom_plate(P.W_STD)

    # 4. Generate Accessories
    knob = F.create_speed_knob()
    # Position knob relative to the housing
    # Note: Precise 3D positioning logic would be done in FreeCAD or via
    # specific translation/rotation vectors matching the inlay cutout.

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate,
        "Knob": knob
    }

if __name__ == "__main__":
    print("Generating Märklin Digital 6021 Control Unit Assembly...")
    assembly = create_6021_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
