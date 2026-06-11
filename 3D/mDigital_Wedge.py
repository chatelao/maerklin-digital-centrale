import math
import mDigital_Params as P
import mDigital_Features as F

"""
Märklin Digital 60xx Series - Wedge Geometry Generator
Logic for Top Shell and Bottom Plate primitives.
"""

# Try to import FreeCAD modules, otherwise provide mocks for environment compatibility
try:
    import FreeCAD as App
    import Part
except ImportError:
    from mDigital_Mock import App, Part

def create_wedge_solid(width, depth, h_front, h_back):
    """
    Creates a solid truncated wedge primitive using FreeCAD Part API.
    Vertices V0-V7 are mapped as per MAERKLIN_DIGITAL_3D_PARAMETERS.md.
    """
    v = [App.Vector(x, y, z) for x, y, z in [
        (0, 0, 0),             # 0: V0
        (0, depth, 0),         # 1: V1
        (width, depth, 0),     # 2: V2
        (width, 0, 0),         # 3: V3
        (0, 0, h_front),       # 4: V4
        (0, depth, h_back),    # 5: V5
        (width, depth, h_back),# 6: V6
        (width, 0, h_front)    # 7: V7
    ]]

    # Define faces (CCW when viewed from outside)
    faces_idx = [
        [0, 3, 2, 1], # Bottom
        [4, 5, 6, 7], # Top
        [0, 4, 7, 3], # Front
        [1, 2, 6, 5], # Back
        [0, 1, 5, 4], # Left
        [3, 7, 6, 2]  # Right
    ]

    faces = []
    for idx in faces_idx:
        # Create closed polygon for each face
        pts = [v[i] for i in idx]
        pts.append(v[idx[0]]) # Close loop for valid FreeCAD geometry
        polyline = Part.makePolygon(pts)
        face = Part.Face(polyline)
        faces.append(face)

    shell = Part.makeShell(faces)
    solid = Part.makeSolid(shell)
    return solid

def generate_top_shell(width, include_faceplate=False):
    """
    Generates the hollowed Top Shell as per SHELL_BLUEPRINT.md.
    Includes modular features (Interlocks, Cutouts, Vents, Bosses).
    If include_faceplate=True, subtracts the decorative faceplate pocket.
    """
    outer = create_wedge_solid(width, P.DEPTH, P.H_FRONT, P.H_BACK)

    # Calculate Z-offset for sloped roof thickness to maintain uniform shell thickness
    # thick_z = thick / cos(slope_angle)
    cos_theta = math.cos(math.radians(P.SLOPE_ANGLE))
    thick_z = P.THICK / cos_theta

    # Inner wedge dimensions
    inner_w = width - 2 * P.THICK
    inner_d = P.DEPTH - 2 * P.THICK
    inner_h_f = P.H_FRONT - thick_z
    inner_h_b = P.H_BACK - thick_z

    inner = create_wedge_solid(inner_w, inner_d, inner_h_f, inner_h_b)

    # Translate inner wedge to create walls and open bottom
    # We shift Z down by 1.0mm to ensure the bottom face is completely removed during 'cut'
    inner.translate(App.Vector(P.THICK, P.THICK, -1.0))

    shell = outer.cut(inner)

    # 1. Add Interlocks (Right side = Male)
    male_interlock = F.create_interlock_tool(is_female=False)
    male_interlock.translate(App.Vector(width, 0, 0))
    shell = shell.fuse(male_interlock)

    # 2. Subtract Interlocks (Left side = Female)
    female_interlock = F.create_interlock_tool(is_female=True)
    shell = shell.cut(female_interlock)

    # 3. Subtract DIN Cutouts (Left & Right)
    din_left = F.create_din_cutout_tool()
    shell = shell.cut(din_left)

    din_right = F.create_din_cutout_tool()
    din_right.translate(App.Vector(width, 0, 0))
    shell = shell.cut(din_right)

    # 4. Add Ventilation
    if width == P.W_STD:
        v_left = F.create_ventilation_bank(P.V_STD_L_X, P.V_STD_SLOTS)
        v_right = F.create_ventilation_bank(P.V_STD_R_X, P.V_STD_SLOTS)
        shell = shell.cut(v_left).cut(v_right)
    else:
        v_center = F.create_ventilation_bank(P.V_SLIM_C_X, P.V_SLIM_SLOTS)
        shell = shell.cut(v_center)

    # 5. Add Faceplate Pocket
    if include_faceplate:
        fp_tool = F.create_faceplate_pocket_tool(width, P.FP_LENGTH_STD)
        shell = shell.cut(fp_tool)

    # 6. Add Screw Bosses
    for loc in F.get_fastening_locations(width):
        boss = F.create_screw_boss(is_cavity=False)
        boss.translate(App.Vector(loc[0], loc[1], P.THICK))
        shell = shell.fuse(boss)

        cavity = F.create_screw_boss(is_cavity=True)
        cavity.translate(App.Vector(loc[0], loc[1], P.THICK))
        shell = shell.cut(cavity)

    return shell

def generate_bottom_plate(width):
    """
    Generates the Bottom Plate as per SHELL_BLUEPRINT.md.
    Dimensions are reduced by TOL to ensure fit.
    """
    plate_w = width - 2 * P.TOL
    plate_d = P.DEPTH - 2 * P.TOL

    plate = Part.makeBox(plate_w, plate_d, P.THICK)

    # Center plate within the shell footprint
    plate.translate(App.Vector(P.TOL, P.TOL, 0))

    for loc in F.get_fastening_locations(width):
        # Create counterbore holes
        hole = Part.makeCylinder(P.PLATE_HOLE_DIA/2.0, P.THICK + 2.0)
        hole.translate(App.Vector(loc[0], loc[1], -1.0))
        plate = plate.cut(hole)

        cb = Part.makeCylinder(P.PLATE_CB_DIA/2.0, P.PLATE_CB_DEPTH)
        cb.translate(App.Vector(loc[0], loc[1], -0.1))
        plate = plate.cut(cb)

    return plate

if __name__ == "__main__":
    print("Märklin Digital 60xx - Wedge Geometry Generator")
    print(f"Generating Standard Width Housing ({P.W_STD}mm) with Faceplate...")
    top = generate_top_shell(P.W_STD, include_faceplate=True)
    bottom = generate_bottom_plate(P.W_STD)
    print(f"Top Shell Result: {top}")
    print(f"Bottom Plate Result: {bottom}")
