import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_pin_image(title, keyword, filename="ai_tools_pin.png"):
    prompt = f"""
Create a professional vertical Pinterest/blog image for an AI tools article.

Brand: Discover NextGen AI Stack
Article title: {title}
Keyword: {keyword}

Style:
- futuristic but clean
- AI tools / software dashboard / automation theme
- modern blue, purple, cyan lighting
- professional tech blog look
- no fake logos
- no real company logos
- minimal readable text
- vertical format for Pinterest
"""

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536",
        quality="low",
        n=1
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(filename, "wb") as file:
        file.write(image_bytes)

    return filename
