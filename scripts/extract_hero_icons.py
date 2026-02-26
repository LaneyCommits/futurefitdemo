#!/usr/bin/env python3
"""Extract individual icons from the hero icons source image."""
import os

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    exit(1)

SRC = "/Users/laney/.cursor/projects/Users-laney-Desktop-futurefit/assets/ChatGPT_Image_Feb_25__2026__05_56_55_PM-aee805ba-e722-45a2-aee8-fdefec9cd735.png"
OUT_DIR = "static/images/hero-icons"

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base, OUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    
    # 7 icons: likely 4 in row 1, 3 in row 2. Or try 3+3+1, or 2 rows.
    # 1024x682 - try 4 columns, 2 rows: cell ~256x341
    cols = 4
    rows = 2
    cell_w = w // cols
    cell_h = h // rows
    
    # Order: top-left to right, then next row. 7 icons = (0,0),(1,0),(2,0),(3,0),(0,1),(1,1),(2,1)
    names = [
        "checklist", "resume-pencil", "target", "folder-stack",
        "folder-docs", "shield", "graduation"
    ]
    positions = [
        (0, 0), (1, 0), (2, 0), (3, 0),
        (0, 1), (1, 1), (2, 1)
    ]
    
    for i, (cx, cy) in enumerate(positions):
        if i >= len(names):
            break
        x1 = cx * cell_w
        y1 = cy * cell_h
        x2 = x1 + cell_w
        y2 = y1 + cell_h
        # Small inset to trim edges; avoid cutting into icon content
        inset = 6
        crop = img.crop((
            max(0, x1 + inset),
            max(0, y1 + inset),
            min(w, x2 - inset),
            min(h, y2 - inset)
        ))
        out_path = os.path.join(out_dir, f"{names[i]}.png")
        crop.save(out_path, "PNG")
        print(f"Saved {out_path}")
    
    # Also copy to docs
    docs_dir = os.path.join(base, "docs/images/hero-icons")
    os.makedirs(docs_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        if f.endswith(".png"):
            src = os.path.join(out_dir, f)
            dst = os.path.join(docs_dir, f)
            Image.open(src).save(dst, "PNG")
            print(f"Copied to docs: {f}")

if __name__ == "__main__":
    main()
