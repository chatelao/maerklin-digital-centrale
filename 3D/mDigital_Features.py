import math
import mDigital_Params as P

"""
Märklin Digital 60xx Series - Modular Feature Library
Implements the "Boolean Tool" logic for housing features.
"""

# Try to import FreeCAD modules, otherwise provide mocks
try:
    import FreeCAD as App
    import Part
except ImportError:
    from mDigital_Mock import App, Part

def create_interlock_block(tol=0.0):
    """Creates a single interlocking block (tab)."""
    w = P.INTERLOCK_TAB_W + tol
    h = P.INTERLOCK_TAB_H + tol
    d = P.INTERLOCK_TAB_D + tol

    block = Part.makeBox(w, d, h)
    block.translate(App.Vector(0, -d/2.0, -h/2.0))
    return block

def create_interlock_tool(is_female=False):
    """
    Creates the master Interlock Tool (2 blocks).
    If is_female=True, adds TOL to the dimensions for subtraction.
    """
    tol = P.TOL if is_female else 0.0

    b1 = create_interlock_block(tol)
    b1.translate(App.Vector(0, P.INTERLOCK_FRONT_Y, P.INTERLOCK_Z_CENTER))

    b2 = create_interlock_block(tol)
    b2.translate(App.Vector(0, P.INTERLOCK_BACK_Y, P.INTERLOCK_Z_CENTER))

    tool = Part.makeCompound([b1, b2])
    return tool

def create_din_cutout_tool():
    """Creates the tool for the DIN 41612 B/2 side cutout."""
    depth = P.THICK + 2.0
    tool = Part.makeBox(depth, P.DIN_CUTOUT_W, P.DIN_CUTOUT_H)

    tool.translate(App.Vector(-1.0, P.DIN_CUTOUT_Y_CENTER - P.DIN_CUTOUT_W/2.0,
                                P.DIN_CUTOUT_Z_CENTER - P.DIN_CUTOUT_H/2.0))
    return tool

def create_ventilation_bank(x_pos, num_slots):
    """Creates a bank of ventilation slots."""
    slots = []
    for i in range(num_slots):
        slot = Part.makeBox(P.V_SLOT_W, P.V_SLOT_L, P.V_SLOT_D)
        slot.translate(App.Vector(-P.V_SLOT_W/2.0, -P.V_SLOT_L/2.0, -1.0))
        slot.translate(App.Vector(0, i * P.V_SLOT_P, 0))
        slots.append(slot)

    bank = Part.makeCompound(slots)
    bank_len = (num_slots - 1) * P.V_SLOT_P
    bank.translate(App.Vector(x_pos, P.V_START_Y + bank_len/2.0, 0))
    bank.rotate(App.Vector(1,0,0), App.Vector(x_pos, P.V_START_Y, P.H_FRONT), P.SLOPE_ANGLE)

    return bank

def create_screw_boss(is_cavity=False):
    """Creates a single screw boss or its internal cavity."""
    if is_cavity:
        return Part.makeCylinder(P.BOSS_HOLE_DIA/2.0, P.BOSS_HOLE_DEPTH)
    else:
        return Part.makeCylinder(P.BOSS_DIA/2.0, 10.0)

def get_fastening_locations(width):
    """Returns the (X, Y) coordinates for the 4 fastening points."""
    return [
        (P.BOSS_OFFSET, P.BOSS_OFFSET),
        (width - P.BOSS_OFFSET, P.BOSS_OFFSET),
        (P.BOSS_OFFSET, P.DEPTH - P.BOSS_OFFSET),
        (width - P.BOSS_OFFSET, P.DEPTH - P.BOSS_OFFSET)
    ]

def create_faceplate_pocket_tool(width, length):
    """Creates the tool for subtracting the faceplate pocket."""
    w = width - 2 * P.FP_INSET
    # Box from (0,0,0) to (w, length, depth)
    tool = Part.makeBox(w, length, P.FP_POCKET_DEPTH + 2.0)
    # Move so top face is at Z=0
    tool.translate(App.Vector(0, 0, -(P.FP_POCKET_DEPTH + 2.0)))
    # Move to wedge front corner (with inset)
    tool.translate(App.Vector(P.FP_INSET, 0, P.H_FRONT))
    # Rotate around wedge front edge
    tool.rotate(App.Vector(1,0,0), App.Vector(0, 0, P.H_FRONT), P.SLOPE_ANGLE)
    return tool

def create_faceplate_inlay(width, length):
    """Creates the decorative faceplate inlay."""
    w = width - 2 * P.FP_INSET - 2 * P.TOL
    l = length - 2 * P.TOL
    inlay = Part.makeBox(w, l, P.FP_THICK)
    # Top face at Z = FP_THICK. Move so top face is at Z=0 before rotation
    inlay.translate(App.Vector(0, 0, -P.FP_THICK))
    # Move to wedge front corner (with inset + tol)
    inlay.translate(App.Vector(P.FP_INSET + P.TOL, P.TOL, P.H_FRONT))
    # Rotate
    inlay.rotate(App.Vector(1,0,0), App.Vector(0, 0, P.H_FRONT), P.SLOPE_ANGLE)
    return inlay

def create_speed_knob():
    """Creates a standard speed control knob."""
    knob = Part.makeCylinder(P.KNOB_DIA/2.0, P.KNOB_H)
    shaft_hole = Part.makeCylinder(P.KNOB_SHAFT_DIA/2.0, P.KNOB_H - 2.0)
    knob = knob.cut(shaft_hole)
    return knob

def create_square_button():
    """Creates a standard square push button."""
    btn = Part.makeBox(P.BTN_SIZE, P.BTN_SIZE, 10.0)
    btn.translate(App.Vector(-P.BTN_SIZE/2.0, -P.BTN_SIZE/2.0, 0))
    return btn

def create_display_bezel_tool():
    """
    Creates a Boolean tool for the 4-digit 7-segment display.
    Includes a recessed area and the through-cutout for the digits.
    """
    # Outer recess
    recess = Part.makeBox(P.DISPLAY_W, P.DISPLAY_H, P.DISPLAY_RECESS)

    # Through-cutout (inner digits window)
    inner_w = P.DISPLAY_W - 4.0
    inner_h = P.DISPLAY_H - 4.0
    cutout = Part.makeBox(inner_w, inner_h, 10.0)
    cutout.translate(App.Vector(2.0, 2.0, -5.0))

    tool = Part.makeCompound([recess, cutout])
    return tool

def create_6021_faceplate_inlay():
    """
    Creates the specialized faceplate inlay for the Control Unit 6021.
    Includes cutouts for the display, keypad, function buttons, and knob.
    """
    width = P.W_STD
    length = P.FP_LENGTH_STD

    # Create base inlay (unrotated)
    w_inlay = width - 2 * P.FP_INSET - 2 * P.TOL
    l_inlay = length - 2 * P.TOL
    inlay = Part.makeBox(w_inlay, l_inlay, P.FP_THICK)

    # 1. Display Bezel Cutout
    display = create_display_bezel_tool()
    display.translate(App.Vector(P.C6021_DISPLAY_X, P.C6021_DISPLAY_Y, -1.0))
    inlay = inlay.cut(display)

    # 2. Function Buttons (2x2 grid)
    for i in range(2):
        for j in range(2):
            btn = Part.makeBox(P.BTN_CUTOUT, P.BTN_CUTOUT, 10.0)
            btn.translate(App.Vector(-P.BTN_CUTOUT/2.0, -P.BTN_CUTOUT/2.0, -5.0))
            btn.translate(App.Vector(P.C6021_FBTN_GRID_X + i*P.C6021_FBTN_PITCH,
                                     P.C6021_FBTN_GRID_Y + j*P.C6021_FBTN_PITCH, 0.4))
            inlay = inlay.cut(btn)

    # 3. Numeric Keypad (5x2 grid for 0-9)
    for i in range(5):
        for j in range(2):
            btn = Part.makeBox(P.BTN_CUTOUT, P.BTN_CUTOUT, 10.0)
            btn.translate(App.Vector(-P.BTN_CUTOUT/2.0, -P.BTN_CUTOUT/2.0, -5.0))
            btn.translate(App.Vector(P.C6021_KPAD_X + i*P.C6021_KPAD_PITCH_X,
                                     P.C6021_KPAD_Y + j*P.C6021_KPAD_PITCH_Y, 0.4))
            inlay = inlay.cut(btn)

    # 4. Speed Knob Cutout
    knob_hole = Part.makeCylinder(P.KNOB_DIA/2.0 + 1.0, 10.0)
    knob_hole.translate(App.Vector(P.C6021_KNOB_X, P.C6021_KNOB_Y, -5.0))
    inlay = inlay.cut(knob_hole)

    # Position and Rotate to fit the Wedge
    inlay.translate(App.Vector(0, 0, -P.FP_THICK))
    inlay.translate(App.Vector(P.FP_INSET + P.TOL, P.TOL, P.H_FRONT))
    inlay.rotate(App.Vector(1,0,0), App.Vector(0, 0, P.H_FRONT), P.SLOPE_ANGLE)

    return inlay

def create_6040_faceplate_inlay():
    """
    Creates the specialized faceplate inlay for the Keyboard 6040.
    Includes a 2x8 grid of square button cutouts.
    """
    width = P.W_STD
    length = P.FP_LENGTH_6040

    # Create base inlay (unrotated)
    w_inlay = width - 2 * P.FP_INSET - 2 * P.TOL
    l_inlay = length - 2 * P.TOL
    inlay = Part.makeBox(w_inlay, l_inlay, P.FP_THICK)

    # Keyboard matrix (2 columns, 8 rows)
    for i in range(2):
        for j in range(8):
            btn = Part.makeBox(P.BTN_CUTOUT, P.BTN_CUTOUT, 10.0)
            btn.translate(App.Vector(-P.BTN_CUTOUT/2.0, -P.BTN_CUTOUT/2.0, -5.0))
            btn.translate(App.Vector(P.C6040_GRID_X + i*P.C6040_PITCH_X,
                                     P.C6040_GRID_Y + j*P.C6040_PITCH_Y, 0.4))
            inlay = inlay.cut(btn)

    # Position and Rotate to fit the Wedge
    inlay.translate(App.Vector(0, 0, -P.FP_THICK))
    inlay.translate(App.Vector(P.FP_INSET + P.TOL, P.TOL, P.H_FRONT))
    inlay.rotate(App.Vector(1,0,0), App.Vector(0, 0, P.H_FRONT), P.SLOPE_ANGLE)

    return inlay

def create_80f_faceplate_inlay():
    """
    Creates the specialized faceplate inlay for the Control 80f (6036).
    Includes cutouts for display, speed knob, and 4 function buttons.
    """
    width = P.W_SLIM
    length = P.FP_LENGTH_STD

    # Create base inlay (unrotated)
    w_inlay = width - 2 * P.FP_INSET - 2 * P.TOL
    l_inlay = length - 2 * P.TOL
    inlay = Part.makeBox(w_inlay, l_inlay, P.FP_THICK)

    # 1. Display Cutout (Smaller than 6021, but using same bezel tool for now)
    display = create_display_bezel_tool()
    display.translate(App.Vector(P.C80F_DISPLAY_X, P.C80F_DISPLAY_Y, -1.0))
    inlay = inlay.cut(display)

    # 2. Function Buttons (2x2 grid)
    for i in range(2):
        for j in range(2):
            btn = Part.makeBox(P.BTN_CUTOUT, P.BTN_CUTOUT, 10.0)
            btn.translate(App.Vector(-P.BTN_CUTOUT/2.0, -P.BTN_CUTOUT/2.0, -5.0))
            btn.translate(App.Vector(P.C80F_BTN_X + i*P.C80F_BTN_PITCH_X,
                                     P.C80F_BTN_Y + j*P.C80F_BTN_PITCH_Y, 0.4))
            inlay = inlay.cut(btn)

    # 3. Speed Knob Cutout
    knob_hole = Part.makeCylinder(P.KNOB_DIA/2.0 + 1.0, 10.0)
    knob_hole.translate(App.Vector(P.C80F_KNOB_X, P.C80F_KNOB_Y, -5.0))
    inlay = inlay.cut(knob_hole)

    # Position and Rotate to fit the Wedge
    inlay.translate(App.Vector(0, 0, -P.FP_THICK))
    inlay.translate(App.Vector(P.FP_INSET + P.TOL, P.TOL, P.H_FRONT))
    inlay.rotate(App.Vector(1,0,0), App.Vector(0, 0, P.H_FRONT), P.SLOPE_ANGLE)

    return inlay

if __name__ == "__main__":
    print("Märklin Digital 60xx - Feature Library")
    print(f"Interlock Tool: {create_interlock_tool()}")
    print(f"DIN Cutout Tool: {create_din_cutout_tool()}")
    print(f"Ventilation Bank (Std Left): {create_ventilation_bank(P.V_STD_L_X, P.V_STD_SLOTS)}")
    print(f"Display Bezel Tool: {create_display_bezel_tool()}")
    print(f"6021 Faceplate Inlay: {create_6021_faceplate_inlay()}")
    print(f"6040 Faceplate Inlay: {create_6040_faceplate_inlay()}")
    print(f"80f Faceplate Inlay: {create_80f_faceplate_inlay()}")
