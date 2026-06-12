import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Digital 6017 Booster - Full Assembly
Standard housing with specialized faceplate for status LEDs.
"""

def create_6017_assembly():
    # 1. Generate the Top Shell (including faceplate pocket subtraction)
    top_shell = W.generate_top_shell(P.W_STD, include_faceplate=True)

    # 2. Generate the specialized Faceplate Inlay
    inlay = F.create_6017_faceplate_inlay()

    # 3. Generate the Bottom Plate
    bottom_plate = W.generate_bottom_plate(P.W_STD)

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate
    }

if __name__ == "__main__":
    print("Generating Märklin Digital 6017 Booster Assembly...")
    assembly = create_6017_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
