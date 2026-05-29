#!/usr/bin/env python3
"""Generate a technical blueprint-style hero image for AI Agent Tool Calling article."""

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
ORANGE_NEON = (255, 165, 0)  # orange neon
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Output path
OUTPUT_PATH = "/root/obelisk-design.github.io/src/assets/ai-agent-tool-calling-hero.webp"

def draw_glow(draw, pos, radius, color, intensity=0.3):
    """Draw a glowing effect."""
    for i in range(radius, 0, -1):
        alpha = int(255 * intensity * (i / radius))
        r, g, b = color
        glow_color = (r, g, b)
        draw.ellipse(
            [pos[0] - i, pos[1] - i, pos[0] + i, pos[1] + i],
            fill=None,
            outline=glow_color,
            width=1
        )

def create_blueprint_image():
    """Create a blueprint-style technical infographic hero image."""
    
    # Create image with dark background
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fallback to default
    try:
        # Try common monospace fonts for technical look
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        code_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        code_font = ImageFont.load_default()
    
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
    title = "AI Agent Tool Calling"
    draw.text((WIDTH//2, 60), title, font=title_font, fill=CYAN_NEON, anchor="mt")
    
    # Subtitle
    subtitle = "From Function Calls to Intelligent Orchestration"
    draw.text((WIDTH//2, 130), subtitle, font=subtitle_font, fill=GRAY, anchor="mt")
    
    # Draw horizontal divider line
    draw.line([(100, 180), (WIDTH-100, 180)], fill=CYAN_NEON, width=2)
    
    # Left section - Workflow diagram
    workflow_x = 120
    workflow_y = 220
    
    draw.text((workflow_x, workflow_y), "TOOL CALLING WORKFLOW", font=label_font, fill=PURPLE_NEON)
    
    # Workflow steps
    steps = [
        ("1. DEFINE", "Tool Schema"),
        ("2. DECIDE", "Model Choice"),
        ("3. EXECUTE", "Run Tool"),
        ("4. INTEGRATE", "Return Result")
    ]
    
    step_width = 180
    for i, (step, desc) in enumerate(steps):
        x_pos = workflow_x + i * (step_width + 40)
        y_pos = workflow_y + 50
        
        # Draw box
        draw.rectangle(
            [(x_pos, y_pos), (x_pos + step_width, y_pos + 80)],
            outline=CYAN_NEON, width=2
        )
        
        # Draw step label
        draw.text((x_pos + step_width//2, y_pos + 20), step, font=label_font, fill=CYAN_NEON, anchor="mt")
        draw.text((x_pos + step_width//2, y_pos + 55), desc, font=small_font, fill=GRAY, anchor="mt")
        
        # Draw arrow to next step
        if i < len(steps) - 1:
            arrow_start = x_pos + step_width + 5
            arrow_end = arrow_start + 30
            arrow_y = y_pos + 40
            draw.line([(arrow_start, arrow_y), (arrow_end, arrow_y)], fill=TEAL_NEON, width=2)
            # Arrow head
            draw.polygon([
                (arrow_end - 8, arrow_y - 5),
                (arrow_end, arrow_y),
                (arrow_end - 8, arrow_y + 5)
            ], fill=TEAL_NEON)
    
    # Center section - Tool types
    tools_x = 120
    tools_y = 400
    
    draw.text((tools_x, tools_y), "TOOL TYPES", font=label_font, fill=PURPLE_NEON)
    
    tool_types = [
        ("Function", "Custom code execution", CYAN_NEON),
        ("Code Interpreter", "Sandboxed Python env", TEAL_NEON),
        ("File Search", "Document retrieval", PURPLE_NEON),
        ("Web Browser", "Internet access", ORANGE_NEON)
    ]
    
    for i, (name, desc, color) in enumerate(tool_types):
        y_pos = tools_y + 45 + i * 50
        
        # Draw icon box
        draw.rectangle([(tools_x, y_pos), (tools_x + 30, y_pos + 30)], outline=color, width=2)
        draw.text((tools_x + 8, y_pos + 5), str(i + 1), font=small_font, fill=color)
        
        # Draw name and description
        draw.text((tools_x + 45, y_pos + 2), name, font=label_font, fill=WHITE)
        draw.text((tools_x + 200, y_pos + 5), desc, font=small_font, fill=GRAY)
    
    # Right section - Code example
    code_x = 850
    code_y = 220
    
    draw.text((code_x, code_y), "TOOL DEFINITION EXAMPLE", font=label_font, fill=PURPLE_NEON)
    
    # Code block background
    code_block_x = code_x
    code_block_y = code_y + 40
    code_block_width = 950
    code_block_height = 200
    
    draw.rectangle(
        [(code_block_x, code_block_y), (code_block_x + code_block_width, code_block_y + code_block_height)],
        fill=(15, 20, 30), outline=CYAN_NEON, width=1
    )
    
    # Code content
    code_lines = [
        ('{', WHITE),
        ('  "name": "get_weather",', CYAN_NEON),
        ('  "description": "Get weather for a location",', GRAY),
        ('  "parameters": {', WHITE),
        ('    "type": "object",', TEAL_NEON),
        ('    "properties": {', WHITE),
        ('      "location": {', WHITE),
        ('        "type": "string",', TEAL_NEON),
        ('        "description": "City name"', GRAY),
        ('      }', WHITE),
        ('    },', WHITE),
        ('    "required": ["location"]', ORANGE_NEON),
        ('  }', WHITE),
        ('}', WHITE)
    ]
    
    line_height = 14
    for i, (line, color) in enumerate(code_lines):
        draw.text((code_block_x + 20, code_block_y + 15 + i * line_height), line, font=code_font, fill=color)
    
    # Bottom section - Orchestration patterns
    patterns_y = 480
    draw.line([(100, patterns_y - 20), (WIDTH-100, patterns_y - 20)], fill=TEAL_NEON, width=1)
    
    draw.text((WIDTH//2, patterns_y), "ORCHESTRATION PATTERNS", font=label_font, fill=PURPLE_NEON, anchor="mt")
    
    # Pattern boxes
    patterns = [
        ("CHAINED", "A → B → C → D", CYAN_NEON),
        ("PARALLEL", "A, B, C → merge", TEAL_NEON),
        ("CONDITIONAL", "if A then B else C", PURPLE_NEON),
        ("LOOP", "while !done: A", ORANGE_NEON)
    ]
    
    pattern_width = 400
    pattern_height = 100
    pattern_spacing = 50
    start_x = (WIDTH - (len(patterns) * pattern_width + (len(patterns) - 1) * pattern_spacing)) // 2
    
    for i, (name, desc, color) in enumerate(patterns):
        x_pos = start_x + i * (pattern_width + pattern_spacing)
        y_pos = patterns_y + 50
        
        # Draw pattern box
        draw.rectangle(
            [(x_pos, y_pos), (x_pos + pattern_width, y_pos + pattern_height)],
            outline=color, width=2
        )
        
        # Draw pattern name
        draw.text((x_pos + pattern_width//2, y_pos + 20), name, font=label_font, fill=color, anchor="mt")
        
        # Draw pattern description
        draw.text((x_pos + pattern_width//2, y_pos + 55), desc, font=small_font, fill=WHITE, anchor="mt")
    
    # Add corner decorations (blueprint style)
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
    
    # Add tech decorations
    # Circuit-like lines
    for i in range(3):
        x = 150 + i * 60
        draw.line([(x, HEIGHT - 80), (x, HEIGHT - 60)], fill=PURPLE_NEON, width=1)
        draw.line([(x, HEIGHT - 60), (x + 40, HEIGHT - 60)], fill=PURPLE_NEON, width=1)
        draw.ellipse([(x - 3, HEIGHT - 83), (x + 3, HEIGHT - 77)], fill=PURPLE_NEON)
    
    # Version info
    draw.text((WIDTH - 30, HEIGHT - 30), "v1.0", font=small_font, fill=GRAY, anchor="rb")
    
    # Save as WebP
    img.save(OUTPUT_PATH, 'WEBP', quality=95)
    print(f"Hero image saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_blueprint_image()