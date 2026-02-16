import os
import io
import random
import asyncio
import google.generativeai as genai
from PIL import Image

if os.environ.get("GOOGLE_API_KEY"):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

PROMPTS = [
    "Abstract cyberpunk cityscape, neon lights, digital art, high detail, 4k, no text",
    "Mystical forest with glowing mushrooms, fantasy art, oil painting style, complex texture",
    "Futuristic geometric patterns, colorful fractals, 3d render, high contrast",
    "Space nebula background, stars and cosmic dust, realistic style, vivid colors",
    "Abstract fluid art, swirling paint, acrylic pour, vibrant colors, intricate details"
]

async def generate_cover_image() -> bytes:
    """Generate image via Google Gemini and convert to PNG."""
    try:
        selected_prompt = random.choice(PROMPTS)
        model = genai.ImageGenerationModel("imagen-3.0-generate-001")
        
        response = await asyncio.to_thread(
            model.generate_images,
            prompt=selected_prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="block_only_high",
            person_generation="allow_adult"
        )

        image_data = response.images[0].image_bytes
        img = Image.open(io.BytesIO(image_data))
        
        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        
        return output.getvalue()

    except Exception as e:
        print(f"Gemini API error: {e}")
        return await generate_fallback_image()

async def generate_fallback_image() -> bytes:
    """Fallback: generate image locally."""
    from PIL import ImageDraw
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
        draw.rectangle([x1, y1, x2, y2], fill=color)

    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output.getvalue()