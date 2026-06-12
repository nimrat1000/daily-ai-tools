from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def get_font(size, bold=False):
    font_path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    return ImageFont.truetype(font_path, size)


def create_pin_image(title, keyword, filename="ai_tools_pin.png"):
    width, height = 1000, 1500

    img = Image.new("RGB", (width, height), (12, 20, 42))
    draw = ImageDraw.Draw(img)

    title_font = get_font(58, True)
    subtitle_font = get_font(34)
    small_font = get_font(26)
    footer_font = get_font(22)

    for y in range(height):
        r = int(12 + (y / height) * 20)
        g = int(20 + (y / height) * 30)
        b = int(42 + (y / height) * 70)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    draw.rounded_rectangle(
        [55, 55, 945, 1445],
        radius=36,
        outline=(95, 135, 210),
        width=4
    )

    draw.text((80, 90), "AI TOOLS DAILY", font=small_font, fill=(190, 210, 255))
    draw.text((80, 135), datetime.now().strftime("%B %d, %Y"), font=footer_font, fill=(150, 175, 220))

    draw.rounded_rectangle([80, 240, 920, 570], radius=32, fill=(245, 248, 255))

    wrapped_title = wrap_text(title, 24)
    draw.multiline_text(
        (115, 285),
        wrapped_title,
        font=title_font,
        fill=(10, 25, 50),
        spacing=12
    )

    draw.rounded_rectangle([80, 650, 920, 1000], radius=32, fill=(22, 43, 86))

    draw.text((115, 700), "Today's AI Tool Topic", font=subtitle_font, fill="white")

    wrapped_keyword = wrap_text(keyword, 32)
    draw.multiline_text(
        (115, 770),
        wrapped_keyword,
        font=small_font,
        fill=(190, 210, 255),
        spacing=10
    )

    draw.rounded_rectangle([80, 1080, 920, 1280], radius=32, fill=(65, 210, 125))

    draw.text(
        (115, 1135),
        "Read the full guide",
        font=subtitle_font,
        fill=(8, 18, 38)
    )

    draw.text(
        (115, 1195),
        "Tools • Tips • Automation • Productivity",
        font=small_font,
        fill=(8, 18, 38)
    )

    draw.text(
        (80, 1380),
        "Educational content • Affiliate disclosure included",
        font=footer_font,
        fill=(180, 195, 225)
    )

    img.save(filename)
    return filename


def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)
