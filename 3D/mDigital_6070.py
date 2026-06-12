import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Digital 6070 Infra Control 80f - Full Assembly
Slim housing (67.5mm) with specialized faceplate for display, knob, buttons and IR window.
"""

def create_6070_assembly():
    # 1. Generate the Top Shell (Slim width)
    top_shell = W.generate_top_shell(P.W_SLIM, include_faceplate=True, faceplate_length=P.FP_LENGTH_80F)

    # 2. Generate the specialized Faceplate Inlay
    inlay = F.create_6070_faceplate_inlay()

    # 3. Generate the Bottom Plate (Slim width)
    bottom_plate = W.generate_bottom_plate(P.W_SLIM)

    # 4. Generate Accessories
    knob = F.create_speed_knob()

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate,
        "Knob": knob
    }

if __name__ == "__main__":
    print("Generating Märklin Digital 6070 Infra Control 80f Assembly...")
    assembly = create_6070_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
