import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Digital 6043 Memory - Full Assembly
Standard housing with specialized faceplate for 24-button matrix and 2-digit display.
"""

def create_6043_assembly():
    # 1. Generate the Top Shell
    # 6043 has a longer faceplate pocket than 6040.
    top_shell = W.generate_top_shell(P.W_STD, include_faceplate=True, faceplate_length=P.FP_LENGTH_6043)

    # 2. Generate the specialized Faceplate Inlay
    inlay = F.create_6043_faceplate_inlay()

    # 3. Generate the Bottom Plate
    bottom_plate = W.generate_bottom_plate(P.W_STD)

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate
    }

if __name__ == "__main__":
    print("Generating Märklin Digital 6043 Memory Assembly...")
    assembly = create_6043_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
