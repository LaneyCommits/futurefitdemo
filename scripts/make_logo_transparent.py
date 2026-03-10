#!/usr/bin/env python3
"""Make black background transparent in header logo."""
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    sys.exit(1)

SRC = "static/images/header-logo.png"
OUT = "static/images/header-logo.png"

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(base, SRC)
    out = os.path.join(base, OUT)
    if not os.path.exists(src):
        print(f"Not found: {src}")
        sys.exit(1)
    img = Image.open(src).convert("RGBA")
    data = list(getattr(img, "get_flattened_data", img.getdata)())
    new_data = []
    # Treat dark pixels (near black) as transparent so logo blends with dark navbar
    for item in data:
        r, g, b, a = item
        if r < 70 and g < 70 and b < 70:
            new_data.append((r, g, b, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(out, "PNG")
    print(f"Saved: {out}")
    # Copy to docs
    docs_out = os.path.join(base, "docs/images/header-logo.png")
    img.save(docs_out, "PNG")
    print(f"Saved: {docs_out}")

if __name__ == "__main__":
    main()
