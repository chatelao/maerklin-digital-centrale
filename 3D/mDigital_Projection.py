import os
from PIL import Image, ImageDraw, ImageFont

def create_projection(top_path, front_path, side_path, output_path):
    """
    Combines three orthographic images into a standard Dreitafelprojektion (First-angle).
    Layout:
    [Front View] [Side View (Left)]
    [Top View]
    """
    try:
        front_img = Image.open(front_path)
        top_img = Image.open(top_path)
        side_img = Image.open(side_path)
    except Exception as e:
        print(f"Error opening images for projection: {e}")
        return

    # Assuming all images have same dimensions from FreeCAD export
    w, h = front_img.size

    # Create a canvas large enough for 2x2 grid (bottom-right will be empty or for title block)
    canvas_w = w * 2
    canvas_h = h * 2

    # Background: White
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")

    # Paste images
    # First Angle Projection (European):
    # Front is top-left
    # Side (from left) is top-right
    # Top is bottom-left

    canvas.paste(front_img, (0, 0))
    canvas.paste(side_img, (w, 0))
    canvas.paste(top_img, (0, h))

    # Draw labels
    draw = ImageDraw.Draw(canvas)

    # Try to load a font, fallback to default
    try:
        # Common paths for linux systems
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path):
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

        font = ImageFont.truetype(font_path, 40)
    except:
        font = ImageFont.load_default()

    # Labels (German)
    draw.text((10, 10), "Vorderansicht", fill="black", font=font)
    draw.text((w + 10, 10), "Seitenansicht (links)", fill="black", font=font)
    draw.text((10, h + 10), "Draufsicht", fill="black", font=font)

    # Draw some separator lines
    draw.line([(w, 0), (w, canvas_h)], fill="lightgrey", width=2)
    draw.line([(0, h), (canvas_w, h)], fill="lightgrey", width=2)

    canvas.save(output_path)
    print(f" - Projection saved to {output_path}")

if __name__ == "__main__":
    # Test/Demo logic if run directly
    print("Märklin Digital 3D - Projection Generator")
