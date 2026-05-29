#!/usr/bin/env python3
"""Generate a technical blueprint-style hero image for OpenSpec Spec-Driven Development."""

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
OUTPUT_PATH = "/root/obelisk-design.github.io/src/assets/openspec-spec-driven-development-hero.webp"

def create_blueprint_image():
    """Create a blueprint-style technical infographic hero image."""
    
    # Create image with dark background
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fallback to default
    try:
        # Try common monospace fonts for technical look
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
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
    title = "OpenSpec"
    draw.text((WIDTH//2, 70), title, font=title_font, fill=CYAN_NEON, anchor="mt")
    
    # Subtitle
    subtitle = "Spec-Driven Development for AI Era"
    draw.text((WIDTH//2, 150), subtitle, font=subtitle_font, fill=GRAY, anchor="mt")
    
    # Draw horizontal divider line
    draw.line([(100, 210), (WIDTH-100, 210)], fill=CYAN_NEON, width=2)
    
    # ==================== Left Section: Three Layers ====================
    layers_x = 100
    layers_y = 260
    
    draw.text((layers_x + 20, layers_y), "LAYERED APPROACH", font=label_font, fill=PURPLE_NEON)
    
    # Three boxes representing CLAUDE.md, Skills, OpenSpec
    layers = [
        ("CLAUDE.md", "Behavior & Style", "Code conventions & rules", CYAN_NEON),
        ("SKILLS", "Task Workflows", "Repeated process templates", TEAL_NEON),
        ("OPENSPEC", "Requirement Definition", "What, boundaries, done criteria", PURPLE_NEON),
    ]
    
    box_width = 340
    box_height = 90
    
    for i, (name, subtitle_text, desc, color) in enumerate(layers):
        y_pos = layers_y + 45 + i * 110
        
        # Draw box with glow effect
        for j in range(3, 0, -1):
            draw.rectangle(
                [(layers_x - j, y_pos - j), (layers_x + box_width + j, y_pos + box_height + j)],
                outline=(color[0]//4, color[1]//4, color[2]//4), width=1
            )
        draw.rectangle(
            [(layers_x, y_pos), (layers_x + box_width, y_pos + box_height)],
            outline=color, width=2
        )
        
        # Fill background semi-transparent effect
        draw.rectangle(
            [(layers_x + 1, y_pos + 1), (layers_x + box_width - 1, y_pos + box_height - 1)],
            fill=(15, 20, 30)
        )
        
        # Draw layer name
        draw.text((layers_x + 15, y_pos + 12), name, font=label_font, fill=color)
        # Draw subtitle
        draw.text((layers_x + 15, y_pos + 40), subtitle_text, font=small_font, fill=WHITE)
        # Draw description
        draw.text((layers_x + 15, y_pos + 62), desc, font=small_font, fill=GRAY)
    
    # ==================== Center Section: SDD Flow ====================
    flow_x = 480
    flow_y = 260
    
    draw.text((flow_x + 80, flow_y), "SDD WORKFLOW", font=label_font, fill=PURPLE_NEON)
    
    # Workflow steps
    steps = [
        ("1", "PROPOSAL", "Define requirements"),
        ("2", "REVIEW", "Validate with human"),
        ("3", "IMPLEMENT", "AI executes tasks"),
        ("4", "ARCHIVE", "Merge specs"),
    ]
    
    step_width = 220
    step_height = 70
    
    for i, (num, name, desc) in enumerate(steps):
        x_pos = flow_x
        y_pos = flow_y + 50 + i * 100
        
        # Draw step box
        for j in range(3, 0, -1):
            draw.rectangle(
                [(x_pos - j, y_pos - j), (x_pos + step_width + j, y_pos + step_height + j)],
                outline=(CYAN_NEON[0]//4, CYAN_NEON[1]//4, CYAN_NEON[2]//4), width=1
            )
        draw.rectangle(
            [(x_pos, y_pos), (x_pos + step_width, y_pos + step_height)],
            outline=CYAN_NEON, width=2
        )
        draw.rectangle(
            [(x_pos + 1, y_pos + 1), (x_pos + step_width - 1, y_pos + step_height - 1)],
            fill=(15, 20, 30)
        )
        
        # Step number in circle
        circle_x = x_pos + 30
        circle_y = y_pos + 20
        draw.ellipse(
            [(circle_x - 15, circle_y - 15), (circle_x + 15, circle_y + 15)],
            outline=PURPLE_NEON, width=2
        )
        draw.text((circle_x, circle_y), num, font=label_font, fill=PURPLE_NEON, anchor="mm")
        
        # Step name and description
        draw.text((x_pos + 60, y_pos + 12), name, font=label_font, fill=WHITE)
        draw.text((x_pos + 60, y_pos + 40), desc, font=small_font, fill=GRAY)
        
        # Draw arrow to next step
        if i < len(steps) - 1:
            arrow_y = y_pos + step_height + 15
            draw.line([(x_pos + 110, y_pos + step_height), (x_pos + 110, arrow_y + 5)], fill=TEAL_NEON, width=2)
            # Arrow head pointing down
            draw.polygon([
                (x_pos + 105, arrow_y),
                (x_pos + 115, arrow_y),
                (x_pos + 110, arrow_y + 10)
            ], fill=TEAL_NEON)
    
    # ==================== Right Section: Key Concept ====================
    concept_x = 750
    concept_y = 260
    
    draw.text((concept_x + 50, concept_y), "CORE PRINCIPLE", font=label_font, fill=PURPLE_NEON)
    
    # Human vs AI division
    box_w = 400
    box_h = 200
    
    for j in range(3, 0, -1):
        draw.rectangle(
            [(concept_x - j, concept_y + 50 - j), (concept_x + box_w + j, concept_y + 50 + box_h + j)],
            outline=(PURPLE_NEON[0]//4, PURPLE_NEON[1]//4, PURPLE_NEON[2]//4), width=1
        )
    draw.rectangle(
        [(concept_x, concept_y + 50), (concept_x + box_w, concept_y + 50 + box_h)],
        outline=PURPLE_NEON, width=2
    )
    draw.rectangle(
        [(concept_x + 1, concept_y + 51), (concept_x + box_w - 1, concept_y + 50 + box_h - 1)],
        fill=(15, 20, 30)
    )
    
    # Divider line in middle
    mid_y = concept_y + 50 + box_h // 2
    draw.line([(concept_x, mid_y), (concept_x + box_w, mid_y)], fill=GRAY, width=1)
    
    # Human section (top)
    draw.text((concept_x + 20, concept_y + 70), "HUMAN DEFINES", font=label_font, fill=CYAN_NEON)
    draw.text((concept_x + 20, concept_y + 100), "WHAT", font=title_font, fill=WHITE)
    draw.text((concept_x + 20, concept_y + 140), "Requirements • Boundaries • Done Criteria", font=small_font, fill=GRAY)
    
    # AI section (bottom)
    draw.text((concept_x + 20, mid_y + 20), "AI EXECUTES", font=label_font, fill=TEAL_NEON)
    draw.text((concept_x + 20, mid_y + 50), "HOW", font=title_font, fill=WHITE)
    draw.text((concept_x + 20, mid_y + 90), "Implementation • Testing • Integration", font=small_font, fill=GRAY)
    
    # ==================== Bottom: Key Benefits ====================
    benefits_y = HEIGHT - 180
    draw.line([(100, benefits_y - 20), (WIDTH-100, benefits_y - 20)], fill=TEAL_NEON, width=1)
    
    draw.text((WIDTH//2, benefits_y), "KEY BENEFITS", font=label_font, fill=PURPLE_NEON, anchor="mt")
    
    benefits = [
        "No More Guessing",
        "Audit Trail",
        "Spec Accumulation",
        "Team Alignment",
    ]
    
    benefit_width = (WIDTH - 200) // len(benefits)
    
    for i, benefit in enumerate(benefits):
        x_pos = 100 + i * benefit_width + benefit_width // 2
        y_pos = benefits_y + 50
        
        # Draw box
        draw.rectangle(
            [(x_pos - 80, y_pos), (x_pos + 80, y_pos + 50)],
            outline=CYAN_NEON, width=1
        )
        draw.rectangle(
            [(x_pos - 79, y_pos + 1), (x_pos + 79, y_pos + 49)],
            fill=(15, 20, 30)
        )
        draw.text((x_pos, y_pos + 15), benefit, font=small_font, fill=WHITE, anchor="mt")
    
    # ==================== File structure mini display ====================
    files_x = 1200
    files_y = 260
    
    draw.text((files_x, files_y), "PROJECT STRUCTURE", font=label_font, fill=PURPLE_NEON)
    
    # Mini file tree
    file_tree = [
        ("openspec/", True),
        ("├── project.md", False),
        ("├── AGENTS.md", False),
        ("├── specs/", True),
        ("│   └── spec.md", False),
        ("└── changes/", True),
        ("    ├── proposal.md", False),
        ("    ├── tasks.md", False),
        ("    └── specs/", True),
    ]
    
    for i, (line, is_dir) in enumerate(file_tree):
        color = TEAL_NEON if is_dir else WHITE
        draw.text((files_x, files_y + 35 + i * 26), line, font=label_font, fill=color)
    
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
    
    # Add version info
    draw.text((WIDTH - 30, HEIGHT - 30), "OpenSpec SDD", font=small_font, fill=GRAY, anchor="rb")
    
    # Save as WebP
    img.save(OUTPUT_PATH, 'WEBP', quality=95)
    print(f"Hero image saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_blueprint_image()