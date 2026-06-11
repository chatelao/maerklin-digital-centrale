import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Digital 6050/6051 Interface - Full Assembly
Slim housing (67.5mm) with a plain decorative faceplate.
"""

def create_6050_assembly():
    # 1. Generate the Top Shell (Slim width, including faceplate pocket subtraction)
    top_shell = W.generate_top_shell(P.W_SLIM, include_faceplate=True)

    # 2. Generate the Plain Faceplate Inlay (Slim width)
    inlay = F.create_faceplate_inlay(P.W_SLIM, P.FP_LENGTH_STD)

    # 3. Generate the Bottom Plate (Slim width)
    bottom_plate = W.generate_bottom_plate(P.W_SLIM)

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate
    }

if __name__ == "__main__":
    print("Generating Märklin Digital 6050/6051 Interface Assembly...")
    assembly = create_6050_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
