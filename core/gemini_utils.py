import io
import random
from PIL import Image, ImageDraw

async def generate_cover_image() -> bytes:
    """Generate random abstract image for steganography container"""
    width, height = 512, 512
    bg_color = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    for _ in range(100):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(10, 100)
        y2 = y1 + random.randint(10, 100)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
        shape_type = random.choice(['rect', 'ellipse'])
        if shape_type == 'rect':
            draw.rectangle([x1, y1, x2, y2], fill=color, outline=None)
        else:
            draw.ellipse([x1, y1, x2, y2], fill=color, outline=None)

    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output.getvalue()