import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Digital 6040 Keyboard - Full Assembly
Standard housing with specialized faceplate for 16-button matrix.
"""

def create_6040_assembly():
    # 1. Generate the Top Shell
    # Note: 6040 has a longer faceplate pocket than standard 6021.
    top_shell = W.generate_top_shell(P.W_STD, include_faceplate=True, faceplate_length=P.FP_LENGTH_6040)

    # 2. Generate the specialized Faceplate Inlay
    inlay = F.create_6040_faceplate_inlay()

    # 3. Generate the Bottom Plate
    bottom_plate = W.generate_bottom_plate(P.W_STD)

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate
    }

if __name__ == "__main__":
    print("Generating Märklin Digital 6040 Keyboard Assembly...")
    assembly = create_6040_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
