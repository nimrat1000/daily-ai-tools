from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import math

def get_font(size, bold=False):
    font_path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    return ImageFont.truetype(font_path, size)


def get_daily_theme():
    """
    Cycles through color themes based on day of year — like the moon changing nightly.
    Every day has a unique palette. Repeats yearly.
    """
    day_of_year = datetime.now().timetuple().tm_yday  # 1 to 365

    # Use sine wave to smoothly shift hue across the year (0.0 to 1.0)
    cycle = (math.sin(2 * math.pi * day_of_year / 365) + 1) / 2  # 0.0 to 1.0
    cycle2 = (math.cos(2 * math.pi * day_of_year / 365) + 1) / 2  # offset wave

    themes = [
        {   # Deep blue night
            "bg_top":      (12,  20,  42),
            "bg_bottom":   (32,  50, 112),
            "border":      (95,  135, 210),
            "card_light":  (245, 248, 255),
            "card_dark":   (22,  43,  86),
            "accent":      (65,  210, 125),
            "text_light":  (190, 210, 255),
            "text_dim":    (150, 175, 220),
            "title_color": (10,  25,  50),
        },
        {   # Warm sunset orange
            "bg_top":      (42,  18,  10),
            "bg_bottom":   (112, 55,  20),
            "border":      (210, 140, 80),
            "card_light":  (255, 248, 240),
            "card_dark":   (86,  35,  15),
            "accent":      (255, 180, 50),
            "text_light":  (255, 220, 180),
            "text_dim":    (220, 180, 140),
            "title_color": (50,  20,  5),
        },
        {   # Purple galaxy
            "bg_top":      (20,  10,  40),
            "bg_bottom":   (60,  20,  100),
            "border":      (160, 90,  220),
            "card_light":  (248, 242, 255),
            "card_dark":   (45,  15,  80),
            "accent":      (200, 80,  255),
            "text_light":  (220, 190, 255),
            "text_dim":    (180, 150, 220),
            "title_color": (25,  5,   50),
        },
        {   # Forest green
            "bg_top":      (8,   30,  15),
            "bg_bottom":   (20,  70,  40),
            "border":      (80,  190, 120),
            "card_light":  (240, 255, 245),
            "card_dark":   (15,  55,  30),
            "accent":      (50,  220, 100),
            "text_light":  (180, 240, 200),
            "text_dim":    (140, 200, 160),
            "title_color": (5,   30,  15),
        },
        {   # Crimson red
            "bg_top":      (35,  8,   8),
            "bg_bottom":   (90,  20,  20),
            "border":      (210, 70,  70),
            "card_light":  (255, 242, 242),
            "card_dark":   (70,  15,  15),
            "accent":      (255, 80,  80),
            "text_light":  (255, 200, 200),
            "text_dim":    (220, 160, 160),
            "title_color": (45,  5,   5),
        },
        {   # Teal ocean
            "bg_top":      (8,   35,  40),
            "bg_bottom":   (15,  80,  90),
            "border":      (60,  190, 200),
            "card_light":  (240, 255, 255),
            "card_dark":   (10,  60,  70),
            "accent":      (40,  210, 220),
            "text_light":  (170, 235, 240),
            "text_dim":    (130, 195, 205),
            "title_color": (5,   35,  40),
        },
        {   # Gold luxury
            "bg_top":      (30,  25,  5),
            "bg_bottom":   (75,  60,  10),
            "border":      (210, 175, 50),
            "card_light":  (255, 252, 235),
            "card_dark":   (60,  48,  8),
            "accent":      (230, 190, 40),
            "text_light":  (245, 220, 130),
            "text_dim":    (210, 185, 100),
            "title_color": (35,  28,  3),
        },
    ]

    # Pick theme based on week of year (changes weekly, smooth feel)
    theme_index = (day_of_year // 7) % len(themes)
    base = themes[theme_index]
    next_theme = themes[(theme_index + 1) % len(themes)]

    # Blend slightly toward next theme using daily cycle (subtle daily shift)
    blend = cycle * 0.25  # max 25% blend so it's noticeable but not jarring

    def blend_color(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    return {k: blend_color(base[k], next_theme[k], blend) for k in base}


def draw_gradient(draw, width, height, top_color, bottom_color):
    for y in range(height):
        t = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def wrap_text(text, max_chars):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


def create_pin_image(title, keyword, filename="ai_tools_pin.png"):
    width, height = 1000, 1500
    theme = get_daily_theme()

    img = Image.new("RGB", (width, height), theme["bg_top"])
    draw = ImageDraw.Draw(img)

    title_font   = get_font(58, True)
    subtitle_font = get_font(34)
    small_font   = get_font(26)
    footer_font  = get_font(22)

    # Background gradient
    draw_gradient(draw, width, height, theme["bg_top"], theme["bg_bottom"])

    # Outer border
    draw.rounded_rectangle([55, 55, 945, 1445], radius=36, outline=theme["border"], width=4)

    # Header
    draw.text((80, 90),  "AI TOOLS DAILY",                       font=small_font,  fill=theme["text_light"])
    draw.text((80, 135), datetime.now().strftime("%B %d, %Y"),   font=footer_font, fill=theme["text_dim"])

    # Title card
    draw.rounded_rectangle([80, 240, 920, 570], radius=32, fill=theme["card_light"])
    draw.multiline_text((115, 285), wrap_text(title, 24), font=title_font,
                        fill=theme["title_color"], spacing=12)

    # Keyword card
    draw.rounded_rectangle([80, 650, 920, 1000], radius=32, fill=theme["card_dark"])
    draw.text((115, 700), "Today's AI Tool Topic", font=subtitle_font, fill="white")
    draw.multiline_text((115, 770), wrap_text(keyword, 32), font=small_font,
                        fill=theme["text_light"], spacing=10)

    # CTA card
    draw.rounded_rectangle([80, 1080, 920, 1280], radius=32, fill=theme["accent"])
    draw.text((115, 1135), "Read the full guide",                           font=subtitle_font, fill=theme["title_color"])
    draw.text((115, 1195), "Tools • Tips • Automation • Productivity",      font=small_font,    fill=theme["title_color"])

    # Footer
    draw.text((80, 1380), "Educational content • Affiliate disclosure included",
              font=footer_font, fill=theme["text_dim"])

    img.save(filename)
    return filename
