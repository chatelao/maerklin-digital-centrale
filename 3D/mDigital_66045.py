import mDigital_Params as P
import mDigital_Wedge as W
import mDigital_Features as F

"""
Märklin Delta Control 4f (66045) - Full Assembly
Standard housing with specialized faceplate for selection knob, button and speed knob.
"""

def create_66045_assembly():
    # 1. Generate the Top Shell (including faceplate pocket subtraction)
    top_shell = W.generate_top_shell(P.W_STD, include_faceplate=True, faceplate_length=P.FP_LENGTH_66045)

    # 2. Generate the specialized Faceplate Inlay
    inlay = F.create_66045_faceplate_inlay()

    # 3. Generate the Bottom Plate
    bottom_plate = W.generate_bottom_plate(P.W_STD)

    # 4. Generate Accessories
    main_knob = F.create_speed_knob()
    sel_knob = F.create_small_knob()
    button = F.create_round_button()

    return {
        "TopShell": top_shell,
        "Inlay": inlay,
        "BottomPlate": bottom_plate,
        "MainKnob": main_knob,
        "SelectionKnob": sel_knob,
        "FunctionButton": button
    }

if __name__ == "__main__":
    print("Generating Märklin Delta Control 4f (66045) Assembly...")
    assembly = create_66045_assembly()
    for name, part in assembly.items():
        print(f" - {name}: {part}")
