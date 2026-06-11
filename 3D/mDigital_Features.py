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

if __name__ == "__main__":
    print("Märklin Digital 60xx - Feature Library")
    print(f"Interlock Tool: {create_interlock_tool()}")
    print(f"DIN Cutout Tool: {create_din_cutout_tool()}")
    print(f"Ventilation Bank (Std Left): {create_ventilation_bank(P.V_STD_L_X, P.V_STD_SLOTS)}")
