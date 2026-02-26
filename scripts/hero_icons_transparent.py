#!/usr/bin/env python3
"""Make dark backgrounds transparent in hero icons."""
import os

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    exit(1)

ICONS_DIR = "static/images/hero-icons"
DOCS_DIR = "docs/images/hero-icons"

def make_transparent(img_path, out_path, threshold=50):
    img = Image.open(img_path).convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        r, g, b, a = item
        if r < threshold and g < threshold and b < threshold:
            new_data.append((r, g, b, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(out_path, "PNG")

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_dir = os.path.join(base, ICONS_DIR)
    docs_dir = os.path.join(base, DOCS_DIR)
    os.makedirs(docs_dir, exist_ok=True)
    
    for f in os.listdir(icons_dir):
        if not f.endswith(".png"):
            continue
        src = os.path.join(icons_dir, f)
        make_transparent(src, src)
        print(f"Processed: {f}")
        # Copy to docs
        Image.open(src).save(os.path.join(docs_dir, f), "PNG")

if __name__ == "__main__":
    main()
