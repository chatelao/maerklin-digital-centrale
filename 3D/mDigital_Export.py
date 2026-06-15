import os
import sys
import glob
import importlib
import mDigital_Projection as Projection

# Add current directory to path to import local modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

try:
    import FreeCAD as App
    import FreeCADGui as Gui
    import Part
    import Mesh
    import Import
    REAL_FREECAD = True
except ImportError:
    from mDigital_Mock import App, Part, Mesh, Import, Gui
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
    export_dir = os.path.join(os.path.dirname(__file__), "exports", name)
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

    # 4. Render Screenshots & Projection
    try:
        # In headless/scripted mode, we often need to get the GUI document explicitly
        gui_doc = None
        if REAL_FREECAD:
            gui_doc = Gui.getDocument(doc.Name)
        else:
            gui_doc = Gui.ActiveDocument()

        if gui_doc and hasattr(gui_doc, "ActiveView"):
            view = gui_doc.ActiveView

            # A. Axometric View
            png_path = os.path.join(export_dir, f"{name}.png")
            view.viewAxometric()
            view.fitAll()
            view.saveImage(png_path, 1600, 1200, "White")
            print(f" - Rendered {png_path}")

            # B. Orthographic Views for Projection
            view.setCameraType("Orthographic")

            top_png = os.path.join(export_dir, f"{name}_top.png")
            view.viewTop()
            view.fitAll()
            view.saveImage(top_png, 1600, 1200, "White")

            front_png = os.path.join(export_dir, f"{name}_front.png")
            view.viewFront()
            view.fitAll()
            view.saveImage(front_png, 1600, 1200, "White")

            left_png = os.path.join(export_dir, f"{name}_left.png")
            view.viewLeft()
            view.fitAll()
            view.saveImage(left_png, 1600, 1200, "White")

            # C. Create Combined Projection
            projection_path = os.path.join(export_dir, f"{name}_projection.png")
            Projection.create_projection(top_png, front_png, left_png, projection_path)

            # Clean up intermediate orthographic views if desired,
            # but keeping them for now as individual assets.

        else:
            print(f" - No ActiveView available for {name}")
    except Exception as e:
        print(f" - Could not render screenshots/projection for {name}: {e}")

    App.closeDocument(name)

def discover_assemblies():
    """Dynamically find all modules in the 3D directory that have a create_*_assembly function."""
    assemblies = {}
    base_dir = os.path.dirname(__file__)
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
