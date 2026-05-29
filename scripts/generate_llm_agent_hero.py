#!/usr/bin/env python3
"""Generate a technical blueprint-style hero image for LLM to Agent Fundamentals."""

from PIL import Image, ImageDraw, ImageFont
import os

# Image dimensions (16:9 landscape)
WIDTH = 1920
HEIGHT = 1080

# Color palette (neon blueprint style)
BG_COLOR = (10, 14, 23)  # #0a0e17 - deep dark blue
GRID_COLOR = (20, 30, 50)  # subtle grid lines
CYAN_NEON = (0, 255, 255)  # cyan neon
PURPLE_NEON = (180, 100, 255)  # purple neon
TEAL_NEON = (64, 224, 208)  # teal neon
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Output path
OUTPUT_PATH = "/root/obelisk-design.github.io/src/assets/llm-to-agent-hero.webp"

def draw_glow_circle(draw, center, radius, color, intensity=3):
    """Draw a glowing circle effect."""
    for i in range(intensity, 0, -1):
        alpha = 255 // (i + 1)
        glow_color = (color[0], color[1], color[2])
        r = radius + i * 4
        draw.ellipse(
            [(center[0] - r, center[1] - r), (center[0] + r, center[1] + r)],
            outline=glow_color, width=2
        )

def draw_neural_network(draw, center_x, center_y, size=100):
    """Draw a simplified neural network brain icon."""
    # Draw outer circle (brain shape)
    draw.ellipse(
        [(center_x - size, center_y - size * 0.8), 
         (center_x + size, center_y + size * 0.8)],
        outline=CYAN_NEON, width=3
    )
    
    # Draw inner nodes
    nodes = [
        (center_x - 40, center_y - 30),
        (center_x - 40, center_y + 30),
        (center_x, center_y - 50),
        (center_x, center_y),
        (center_x, center_y + 50),
        (center_x + 40, center_y - 30),
        (center_x + 40, center_y + 30),
    ]
    
    for node in nodes:
        draw.ellipse(
            [(node[0] - 8, node[1] - 8), (node[0] + 8, node[1] + 8)],
            fill=CYAN_NEON, outline=WHITE, width=1
        )
    
    # Draw connections
    connections = [
        (0, 2), (0, 3), (0, 4),
        (1, 3), (1, 4),
        (2, 5), (3, 5), (3, 6), (4, 6),
        (5, 6), (2, 3), (3, 4)
    ]
    for i, j in connections:
        draw.line([nodes[i], nodes[j]], fill=(0, 200, 200), width=1)

def draw_hexagon_framework(draw, center_x, center_y, size=80):
    """Draw a hexagonal framework structure."""
    import math
    
    # Draw hexagon outline
    points = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        x = center_x + size * math.cos(angle)
        y = center_y + size * math.sin(angle)
        points.append((x, y))
    
    draw.polygon(points, outline=PURPLE_NEON, width=3)
    
    # Draw internal connections
    for i in range(6):
        for j in range(i + 2, 6):
            if abs(i - j) != 3:  # Skip opposite connections
                draw.line([points[i], points[j]], fill=(120, 70, 180), width=1)
    
    # Draw center node
    draw.ellipse(
        [(center_x - 15, center_y - 15), (center_x + 15, center_y + 15)],
        fill=PURPLE_NEON, outline=WHITE, width=2
    )
    
    return points

def create_blueprint_image():
    """Create a blueprint-style technical infographic hero image."""
    
    # Create image with dark background
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fallback to default
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        tiny_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        tiny_font = ImageFont.load_default()
    
    # Draw grid pattern (blueprint style)
    grid_spacing = 40
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(0, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)
    
    # Draw thicker major grid lines
    major_spacing = 160
    for x in range(0, WIDTH, major_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=(30, 45, 70), width=2)
    for y in range(0, HEIGHT, major_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=(30, 45, 70), width=2)
    
    # Title - main heading
    title = "LLM to Agent"
    draw.text((WIDTH//2, 70), title, font=title_font, fill=CYAN_NEON, anchor="mt")
    
    # Subtitle
    subtitle = "Understanding the Fundamental Architecture"
    draw.text((WIDTH//2, 150), subtitle, font=subtitle_font, fill=GRAY, anchor="mt")
    
    # Draw horizontal divider line
    draw.line([(100, 210), (WIDTH-100, 210)], fill=CYAN_NEON, width=2)
    
    # === LEFT SIDE: LLM BRAIN ===
    llm_x = 300
    llm_y = 450
    
    # Draw section label
    draw.text((llm_x, 260), "LLM BRAIN", font=label_font, fill=CYAN_NEON, anchor="mt")
    
    # Draw neural network brain
    draw_neural_network(draw, llm_x, llm_y, 100)
    
    # Key concepts around the brain
    concepts = [
        ("TOKEN", (llm_x - 180, llm_y - 100)),
        ("PROMPT", (llm_x + 180, llm_y - 100)),
        ("CONTEXT", (llm_x, llm_y + 150)),
    ]
    
    for text, pos in concepts:
        draw.text(pos, text, font=label_font, fill=TEAL_NEON, anchor="mm")
    
    # Draw arrows from concepts to brain
    for text, pos in concepts:
        angle_to_center = math.atan2(llm_y - pos[1], llm_x - pos[0])
        arrow_start = (pos[0] + 50 * math.cos(angle_to_center), 
                       pos[1] + 50 * math.sin(angle_to_center))
        draw.line([arrow_start, (llm_x, llm_y)], fill=(0, 150, 150), width=1)
    
    # === CENTER: TRANSFORMATION ===
    center_x = WIDTH // 2
    center_y = 450
    
    # Draw large arrow
    arrow_y_start = 320
    arrow_y_end = 580
    
    # Arrow shaft
    draw.line([(center_x, arrow_y_start), (center_x, arrow_y_end - 30)], fill=PURPLE_NEON, width=4)
    
    # Arrow head
    draw.polygon([
        (center_x - 20, arrow_y_end - 30),
        (center_x + 20, arrow_y_end - 30),
        (center_x, arrow_y_end)
    ], fill=PURPLE_NEON)
    
    # Labels on arrow
    draw.text((center_x + 50, 380), "SCALING", font=label_font, fill=PURPLE_NEON, anchor="lm")
    draw.text((center_x + 50, 420), "LAW", font=label_font, fill=PURPLE_NEON, anchor="lm")
    draw.text((center_x + 50, 480), "EMERGENCE", font=label_font, fill=PURPLE_NEON, anchor="lm")
    
    # === RIGHT SIDE: AGENT FRAMEWORK ===
    agent_x = WIDTH - 350
    agent_y = 450
    
    # Draw section label
    draw.text((agent_x, 260), "AGENT BODY", font=label_font, fill=PURPLE_NEON, anchor="mt")
    
    # Draw hexagonal framework
    hex_points = draw_hexagon_framework(draw, agent_x, agent_y, 100)
    
    # Component labels
    components = [
        ("TOOLS", hex_points[0]),
        ("MEMORY", hex_points[1]),
        ("ENV", hex_points[2]),
        ("FEEDBACK", hex_points[3]),
        ("PERMS", hex_points[4]),
        ("LOOP", hex_points[5]),
    ]
    
    for text, pos in components:
        # Calculate offset for label
        dx = pos[0] - agent_x
        dy = pos[1] - agent_y
        label_x = pos[0] + (dx * 0.5)
        label_y = pos[1] + (dy * 0.5)
        draw.text((label_x, label_y), text, font=tiny_font, fill=GRAY, anchor="mm")
    
    # === EQUATION AT BOTTOM ===
    equation_y = 700
    
    # Draw decorative box
    box_width = 600
    box_height = 80
    box_x = (WIDTH - box_width) // 2
    draw.rectangle(
        [(box_x, equation_y), (box_x + box_width, equation_y + box_height)],
        outline=PURPLE_NEON, width=2
    )
    
    # Equation
    equation = "Agent = LLM + Harness"
    draw.text((WIDTH//2, equation_y + 40), equation, font=subtitle_font, fill=PURPLE_NEON, anchor="mm")
    
    # === KEY INSIGHTS SECTION ===
    insights_y = 820
    draw.line([(100, insights_y), (WIDTH-100, insights_y)], fill=TEAL_NEON, width=1)
    
    draw.text((WIDTH//2, insights_y + 20), "KEY INSIGHTS", font=label_font, fill=TEAL_NEON, anchor="mt")
    
    # Two-column insights
    insights_left = [
        "Token-by-token prediction",
        "Context window constraints",
    ]
    insights_right = [
        "Predictable performance gains",
        "Qualitative leaps at scale",
    ]
    
    for i, insight in enumerate(insights_left):
        draw.ellipse([(200, insights_y + 55 + i * 35), (210, insights_y + 65 + i * 35)], fill=CYAN_NEON)
        draw.text((220, insights_y + 50 + i * 35), insight, font=small_font, fill=WHITE)
    
    for i, insight in enumerate(insights_right):
        draw.ellipse([(WIDTH//2 + 100, insights_y + 55 + i * 35), (WIDTH//2 + 110, insights_y + 65 + i * 35)], fill=CYAN_NEON)
        draw.text((WIDTH//2 + 120, insights_y + 50 + i * 35), insight, font=small_font, fill=WHITE)
    
    # === DECORATIONS ===
    # Corner decorations (blueprint style)
    corner_size = 30
    
    # Top-left corner
    draw.line([(20, 20), (20, 20 + corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(20, 20), (20 + corner_size, 20)], fill=CYAN_NEON, width=2)
    
    # Top-right corner
    draw.line([(WIDTH - 20, 20), (WIDTH - 20, 20 + corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(WIDTH - 20, 20), (WIDTH - 20 - corner_size, 20)], fill=CYAN_NEON, width=2)
    
    # Bottom-left corner
    draw.line([(20, HEIGHT - 20), (20, HEIGHT - 20 - corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(20, HEIGHT - 20), (20 + corner_size, HEIGHT - 20)], fill=CYAN_NEON, width=2)
    
    # Bottom-right corner
    draw.line([(WIDTH - 20, HEIGHT - 20), (WIDTH - 20, HEIGHT - 20 - corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(WIDTH - 20, HEIGHT - 20), (WIDTH - 20 - corner_size, HEIGHT - 20)], fill=CYAN_NEON, width=2)
    
    # Add version info
    draw.text((WIDTH - 30, HEIGHT - 30), "v1.0", font=tiny_font, fill=GRAY, anchor="rb")
    
    # Save as WebP
    img.save(OUTPUT_PATH, 'WEBP', quality=95)
    print(f"Hero image saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH

import math

if __name__ == "__main__":
    create_blueprint_image()