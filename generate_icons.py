#!/usr/bin/env python3
"""
Generate placeholder icons for the Nepal Forms Assistant Chrome extension.
This script creates simple colored square icons of different sizes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, output_path):
    """Create a simple icon with the given size and save it to the output path."""
    # Create a new image with a white background
    img = Image.new('RGBA', (size, size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a red square with a blue border
    draw.rectangle(
        [(0, 0), (size, size)],
        fill=(230, 57, 70, 255),  # Red fill (primary color)
        outline=(69, 123, 157, 255),  # Blue outline (secondary color)
        width=max(1, size // 16)  # Scale border width with icon size
    )
    
    # Try to add "NF" text if the icon is large enough
    if size >= 48:
        try:
            # Try to use a built-in font
            font_size = size // 2
            font = ImageFont.truetype("Arial", font_size)
            text = "NF"
            text_width, text_height = draw.textsize(text, font=font)
            position = ((size - text_width) // 2, (size - text_height) // 2)
            draw.text(position, text, fill=(255, 255, 255, 255), font=font)
        except Exception:
            # If font rendering fails, just draw a simple N
            draw.line(
                [(size//4, size//4), (size//4, 3*size//4), (3*size//4, size//4), (3*size//4, 3*size//4)],
                fill=(255, 255, 255, 255),
                width=max(1, size // 16)
            )
    
    # Save the icon
    img.save(output_path, "PNG")
    print(f"Created icon: {output_path}")

def main():
    # Ensure the icons directory exists
    icons_dir = "frontend/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Create icons of different sizes
    icon_sizes = [16, 32, 48, 128]
    
    for size in icon_sizes:
        output_path = os.path.join(icons_dir, f"icon{size}.png")
        create_icon(size, output_path)
    
    # Copy icon files to the root icons directory for manifest.json
    os.makedirs("icons", exist_ok=True)
    for size in icon_sizes:
        src_path = os.path.join(icons_dir, f"icon{size}.png")
        dst_path = os.path.join("icons", f"icon{size}.png")
        
        # Use PIL to open and save again to ensure the file exists
        try:
            img = Image.open(src_path)
            img.save(dst_path, "PNG")
            print(f"Copied icon to: {dst_path}")
        except Exception as e:
            print(f"Error copying icon: {e}")

if __name__ == "__main__":
    main()
    print("Icon generation complete. Run this script to create placeholder icons for the extension.") 