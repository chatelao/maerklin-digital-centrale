import math
import mDigital_Params as P

"""
Märklin Digital 60xx Series - Wedge Geometry Generator
Logic for Top Shell and Bottom Plate primitives.
"""

# Try to import FreeCAD modules, otherwise provide mocks for environment compatibility
try:
    import FreeCAD as App
    import Part
except ImportError:
    class MockApp:
        def Vector(self, x, y, z): return (x, y, z)
    class MockPart:
        def makePolygon(self, pts): return None
        def Face(self, poly): return None
        def makeShell(self, faces): return None
        def makeSolid(self, shell): return None
        def makeBox(self, w, d, h): return None
    App = MockApp()
    Part = MockPart()

def create_wedge_solid(width, depth, h_front, h_back):
    """
    Creates a solid truncated wedge primitive using FreeCAD Part API.
    Vertices V0-V7 are mapped as per MAERKLIN_DIGITAL_3D_PARAMETERS.md.
    """
    # Vertex coordinates from Params
    # We don't use P.get_vertices directly here to allow custom height/depth for inner hollowing
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
        pts.append(v[idx[0]]) # Close loop
        polyline = Part.makePolygon(pts)
        face = Part.Face(polyline)
        faces.append(face)

    shell = Part.makeShell(faces)
    solid = Part.makeSolid(shell)
    return solid

def generate_top_shell(width):
    """
    Generates the hollowed Top Shell as per SHELL_BLUEPRINT.md.
    Uses Boolean subtraction of an inner wedge.
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

    top_shell = outer.cut(inner)

    # Note: Filleting (2.0mm) of vertical edges would be performed here in a live session.
    return top_shell

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
    return plate

if __name__ == "__main__":
    print("Märklin Digital 60xx - Wedge Geometry Generator")
    print(f"Constants: Width Std={P.W_STD}mm, Slim={P.W_SLIM}mm, Depth={P.DEPTH}mm")
    print("Status: Geometry logic defined. Scripts ready for FreeCAD environment.")
