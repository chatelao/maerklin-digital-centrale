"""
Mock FreeCAD API for environments where FreeCAD is not installed.
Provides enough functionality to run the Märklin Digital 3D modeling scripts.
"""

class MockVector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    def multiply(self, factor):
        return MockVector(self.x * factor, self.y * factor, self.z * factor)
    def add(self, other):
        return MockVector(self.x + other.x, self.y + other.y, self.z + other.z)

class MockObject:
    def __init__(self, name="Object"):
        self.name = name
        self.Shape = self
    def translate(self, vector):
        return self
    def rotate(self, axis, center, angle):
        return self
    def fuse(self, other):
        return MockObject(f"Fused({self.name}, {getattr(other, 'name', 'Other')})")
    def cut(self, other):
        return MockObject(f"Cut({self.name}, {getattr(other, 'name', 'Other')})")
    def __repr__(self):
        return self.name

class MockPart:
    def makePolygon(self, pts): return MockObject("Polygon")
    def Face(self, poly): return MockObject("Face")
    def makeShell(self, faces): return MockObject("Shell")
    def makeSolid(self, shell): return MockObject("SolidWedge")
    def makeBox(self, w, d, h): return MockObject(f"Box({w}x{d}x{h})")
    def makeCylinder(self, r, h): return MockObject(f"Cylinder(r={r}, h={h})")
    def makeCompound(self, list_objs): return MockObject(f"Compound({list_objs})")

class MockApp:
    def Vector(self, x, y, z): return MockVector(x, y, z)
    def newDocument(self, name): return MockDocument(name)
    def closeDocument(self, name): pass

class MockDocument:
    def __init__(self, name):
        self.name = name
    def addObject(self, type, name): return MockObject(name)
    def recompute(self): pass
    def saveAs(self, filename):
        print(f"Mock Save: {filename}")
        with open(filename, "w") as f: f.write("Mock FCStd")

class MockMesh:
    def __init__(self, shape=None): pass
    def Mesh(self, shape): return self
    def export(self, list_meshes, filename):
        print(f"Mock Mesh Export: {filename}")
        with open(filename, "w") as f: f.write("Mock STL")

class MockImport:
    def export(self, list_objs, filename):
        print(f"Mock Import Export: {filename}")
        with open(filename, "w") as f: f.write("Mock STEP")

class MockView:
    def viewAxometric(self): pass
    def viewTop(self): pass
    def viewFront(self): pass
    def viewLeft(self): pass
    def setCameraType(self, cam_type): pass
    def fitAll(self): pass
    def saveImage(self, filename, w, h, bg):
        print(f"Mock Save Image: {filename}")
        try:
            from PIL import Image
            img = Image.new("RGB", (w, h), "white")
            img.save(filename)
        except ImportError:
            with open(filename, "w") as f: f.write("Mock PNG")

class MockDocGui:
    def __init__(self):
        self.ActiveView = MockView()

class MockGui:
    def getDocument(self, name): return self.ActiveDocument()
    def ActiveDocument(self): return MockDocGui()

App = MockApp()
Part = MockPart()
Mesh = MockMesh()
Import = MockImport()
Gui = MockGui()
