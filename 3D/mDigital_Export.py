import os
import sys

print("Initializing mDigital_Export.py...")

import glob
import importlib

# Add current directory to path to import local modules
# In FreeCAD's embedded interpreter, __file__ may not be defined.
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback to sys.argv[0] or current working directory
    if len(sys.argv) > 0 and sys.argv[0]:
        SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        SCRIPT_DIR = os.getcwd()

sys.path.append(SCRIPT_DIR)

try:
    import FreeCAD as App
    import FreeCADGui as Gui
    import Part
    import Mesh
    import Import
    REAL_FREECAD = True
except ImportError:
    from mDigital_Mock import App, Part, Mesh, Import
    # Mock Gui if not available
    class MockGui:
        def getDocument(self, name): return self.ActiveDocument()
        def ActiveDocument(self): # FreeCAD uses case-sensitive names
            class MockDocGui:
                def __init__(self):
                    self.ActiveView = MockView()
            class MockView:
                def viewAxometric(self): pass
                def fitAll(self): pass
                def saveImage(self, filename, w, h, bg):
                    print(f"Mock Save Image: {filename}")
                    with open(filename, "w") as f: f.write("Mock PNG")
            return MockDocGui()
    Gui = MockGui()
    REAL_FREECAD = False

def export_assembly(name, assembly_func):
    print(f"Exporting {name}...")

    # Create Document
    doc = App.newDocument(name)

    # Generate Assembly
    parts = assembly_func()

    # Add parts to document
    fc_objs = []
    for part_name, part_shape in parts.items():
        obj = doc.addObject("Part::Feature", part_name)
        obj.Shape = part_shape
        fc_objs.append(obj)

    doc.recompute()

    # Create export directory
    export_dir = os.path.join(SCRIPT_DIR, "exports", name)
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # 1. Save .FCStd
    fcstd_path = os.path.join(export_dir, f"{name}.FCStd")
    doc.saveAs(fcstd_path)
    print(f" - Saved {fcstd_path}")

    # 2. Export .step
    step_path = os.path.join(export_dir, f"{name}.step")
    Import.export(fc_objs, step_path)
    print(f" - Exported {step_path}")

    # 3. Export .stl
    stl_path = os.path.join(export_dir, f"{name}.stl")
    meshes = []
    for obj in fc_objs:
        if hasattr(Mesh, "Mesh"):
            mesh = Mesh.Mesh(obj.Shape)
            meshes.append(mesh)
    if meshes:
        Mesh.export(meshes, stl_path)
        print(f" - Exported {stl_path}")

    # 4. Render Screenshot
    try:
        png_path = os.path.join(export_dir, f"{name}.png")

        # In headless/scripted mode, we often need to get the GUI document explicitly
        gui_doc = None
        if REAL_FREECAD:
            gui_doc = Gui.getDocument(doc.Name)
        else:
            gui_doc = Gui.ActiveDocument()

        if gui_doc and hasattr(gui_doc, "ActiveView"):
            view = gui_doc.ActiveView
            view.viewAxometric()
            view.fitAll()
            # Use a high resolution and transparent or white background
            view.saveImage(png_path, 1600, 1200, "White")
            print(f" - Rendered {png_path}")
        else:
            print(f" - No ActiveView available for {name}")
    except Exception as e:
        print(f" - Could not render screenshot for {name}: {e}")

    App.closeDocument(name)

def discover_assemblies():
    """Dynamically find all modules in the 3D directory that have a create_*_assembly function."""
    assemblies = {}
    base_dir = SCRIPT_DIR
    for py_file in glob.glob(os.path.join(base_dir, "mDigital_6*.py")):
        module_name = os.path.basename(py_file)[:-3]
        try:
            module = importlib.import_module(module_name)
            # Look for functions like 'create_6021_assembly'
            for attr_name in dir(module):
                if attr_name.startswith("create_") and attr_name.endswith("_assembly"):
                    func = getattr(module, attr_name)
                    if callable(func):
                        assemblies[module_name] = func
                        break
        except Exception as e:
            print(f"Could not load module {module_name}: {e}")
    return assemblies

if __name__ == "__main__":
    print("Main execution started.")
    print(f"Starting 3D Asset Export (Real FreeCAD: {REAL_FREECAD})")
    assemblies = discover_assemblies()

    if not assemblies:
        print("No assemblies found!")
        sys.exit(1)

    print(f"Found {len(assemblies)} assemblies: {', '.join(assemblies.keys())}")

    success_count = 0
    for name, func in assemblies.items():
        try:
            export_assembly(name, func)
            success_count += 1
        except Exception as e:
            print(f"Error exporting {name}: {e}")

    print(f"Export completed: {success_count}/{len(assemblies)} succeeded.")

    if success_count < len(assemblies):
        sys.exit(1)

    # Explicitly exit to prevent hanging in headless CI environments
    sys.exit(0)
