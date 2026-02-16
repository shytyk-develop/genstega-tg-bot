import os
import io
import random
import math
import re
import asyncio
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

if os.environ.get("GOOGLE_API_KEY"):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

PROMPTS = [
    "Draw a cyberpunk neon city pattern with glowing lines.",
    "Draw a smooth fluid gradient background with floating bubbles.",
    "Draw a complex geometric fractal with triangles and circles.",
    "Draw a retro 80s synthwave sunset grid style.",
    "Draw a chaotic digital glitch art texture."
]

async def generate_cover_image() -> bytes:
    """Generate image via Gemini or fallback to procedural generation."""
    try:
        return await asyncio.wait_for(generate_with_gemini(), timeout=6.0)
    except Exception as e:
        print(f"⚠️ Gemini API failed or timed out: {e}")
        print("⚡ Switching to Local Procedural Generation...")
        return await generate_complex_local_art()

async def generate_with_gemini() -> bytes:
    selected_prompt = random.choice(PROMPTS)
    
    prompt_text = (
        f"Write Python code using 'PIL' (Pillow) to draw on an image: {selected_prompt}. "
        "CONTEXT: Variables 'draw' (ImageDraw) and 'width', 'height' (512) exist. "
        "RULES: \n"
        "1. Do NOT use imports.\n"
        "2. Do NOT create 'img' or 'Image.new'.\n"
        "3. Use ONLY 'draw.line', 'draw.rectangle', 'draw.ellipse', 'draw.polygon'.\n"
        "4. Use 'random.randint' for variety.\n"
        "5. Output ONLY the code lines inside code blocks."
    )

    response = await model.generate_content_async(prompt_text)
    code = response.text
    
    clean_code = re.sub(r"```python|```|import .*|from .* import .*|img = .*|show\(\)", "", code, flags=re.IGNORECASE).strip()
    
    width, height = 512, 512
    img = Image.new('RGB', (width, height), color=(10, 10, 20))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    local_scope = {
        'draw': draw,
        'width': width,
        'height': height,
        'random': random,
        'math': math
    }
    
    exec(clean_code, {}, local_scope)
    
    return _save_img(img)


async def generate_complex_local_art() -> bytes:
    """Generate procedural art locally as fallback."""
    width, height = 512, 512
    
    c1 = (random.randint(0, 100), random.randint(0, 100), random.randint(50, 150))
    c2 = (random.randint(0, 50), random.randint(0, 50), random.randint(100, 255))
    
    img = Image.new('RGB', (width, height), c1)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    for i in range(height):
        r = int(c1[0] + (c2[0] - c1[0]) * i / height)
        g = int(c1[1] + (c2[1] - c1[1]) * i / height)
        b = int(c1[2] + (c2[2] - c1[2]) * i / height)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    style = random.choice(['circles', 'lines', 'rects'])
    
    for _ in range(random.randint(30, 80)):
        x = random.randint(-50, width+50)
        y = random.randint(-50, height+50)
        size = random.randint(20, 150)
        
        color = (
            random.randint(100, 255), 
            random.randint(100, 255), 
            random.randint(100, 255), 
            random.randint(50, 150)
        )
        
        if style == 'circles':
            draw.ellipse([x, y, x+size, y+size], fill=color, outline=None)
        elif style == 'lines':
            x2 = x + random.randint(-100, 100)
            y2 = y + random.randint(-100, 100)
            draw.line([x, y, x2, y2], fill=color, width=random.randint(2, 10))
        elif style == 'rects':
            draw.rectangle([x, y, x+size, y+size], fill=color)

    pixels = img.load()
    for _ in range(10000):
        rx, ry = random.randint(0, width-1), random.randint(0, height-1)
        r, g, b = pixels[rx, ry]
        noise = random.randint(-30, 30)
        pixels[rx, ry] = (
            max(0, min(255, r + noise)),
            max(0, min(255, g + noise)),
            max(0, min(255, b + noise))
        )

    return _save_img(img)

def _save_img(img):
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output.getvalue()