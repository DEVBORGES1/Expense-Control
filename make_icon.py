
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    size = (256, 256)
    # Create transparent image
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw Green Circle/Rounded Box
    # Center circle
    margin = 20
    draw.ellipse((margin, margin, size[0]-margin, size[1]-margin), fill="#2cc985", outline="#1e8e5d", width=5)
    
    # Draw Dollar Sign
    # Since we might not have a bold font easily, we'll draw simple lines or text if default font works
    # Using basic text drawing
    try:
        # Try to load a standard font if possible, else default
        font = ImageFont.truetype("arial.ttf", 160)
    except:
        font = ImageFont.load_default()
    
    # Text positioning (rough center)
    text = "$"
    # Get bounding box
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    # Center
    x = (size[0] - w) / 2
    y = (size[1] - h) / 2 - 20 # Adjustment
    
    draw.text((x, y), text, font=font, fill="white")
    
    # Save as ICO
    img.save("app_icon.ico", format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("Icon created: app_icon.ico")

if __name__ == "__main__":
    create_icon()
