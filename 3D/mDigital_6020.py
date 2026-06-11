import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Digital 6020 Central Unit - Full Assembly
Standard housing with a plain decorative faceplate.
Suitable as a dummy case for modern electronics.
"""

def create_6020_assembly():
    # 1. Generate the Top Shell (including faceplate pocket subtraction)
    top_shell = W.generate_top_shell(P.W_STD, include_faceplate=True)

    # 2. Generate the Plain Faceplate Inlay
    inlay = F.create_faceplate_inlay(P.W_STD, P.FP_LENGTH_STD)

    # 3. Generate the Bottom Plate
    bottom_plate = W.generate_bottom_plate(P.W_STD)

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate
    }

if __name__ == "__main__":
    print("Generating Märklin Digital 6020 Central Unit Assembly...")
    assembly = create_6020_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
