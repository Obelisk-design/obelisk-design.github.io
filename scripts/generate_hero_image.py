#!/usr/bin/env python3
"""Generate a technical blueprint-style hero image for Intel Mac Erase Guide."""

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
OUTPUT_PATH = "/root/obelisk-design.github.io/src/assets/intel-mac-erase-guide-hero.webp"

def create_blueprint_image():
    """Create a blueprint-style technical infographic hero image."""
    
    # Create image with dark background
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fallback to default
    try:
        # Try common monospace fonts for technical look
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
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
    title = "Intel Mac Erase Guide"
    draw.text((WIDTH//2, 80), title, font=title_font, fill=CYAN_NEON, anchor="mt")
    
    # Subtitle
    subtitle = "Complete Technical Reference for Disk Utility & APFS"
    draw.text((WIDTH//2, 160), subtitle, font=subtitle_font, fill=GRAY, anchor="mt")
    
    # Draw horizontal divider line
    draw.line([(100, 220), (WIDTH-100, 220)], fill=CYAN_NEON, width=2)
    
    # Key concepts section - left side
    concepts_x = 120
    concepts_y = 280
    
    draw.text((concepts_x, concepts_y), "KEY CONCEPTS", font=label_font, fill=PURPLE_NEON)
    
    concepts = [
        ("Disk Utility", "Primary erase tool"),
        ("APFS", "Copy-on-Write file system"),
        ("Recovery Mode", "Command+R boot environment"),
        ("FileVault", "Native disk encryption"),
        ("T2 Chip", "Secure Enclave key management"),
    ]
    
    for i, (term, desc) in enumerate(concepts):
        y_pos = concepts_y + 50 + i * 45
        # Draw bullet point
        draw.ellipse([(concepts_x, y_pos+5), (concepts_x+10, y_pos+15)], fill=CYAN_NEON)
        # Draw term and description
        draw.text((concepts_x+25, y_pos), f"{term}:", font=label_font, fill=WHITE)
        draw.text((concepts_x+200, y_pos), desc, font=small_font, fill=GRAY)
    
    # Draw disk architecture diagram - center/right
    diagram_x = WIDTH - 650
    diagram_y = 280
    
    draw.text((diagram_x + 150, diagram_y), "DISK ARCHITECTURE", font=label_font, fill=PURPLE_NEON)
    
    # Draw layered disk structure
    layer_width = 400
    layer_height = 50
    layer_x = diagram_x - 50
    
    layers = [
        ("EFI Partition", "300 MB", CYAN_NEON),
        ("Recovery HD", "650 MB", TEAL_NEON),
        ("APFS Container", "Remaining Space", PURPLE_NEON),
    ]
    
    for i, (name, size, color) in enumerate(layers):
        y_pos = diagram_y + 50 + i * 80
        # Draw rectangle
        draw.rectangle(
            [(layer_x, y_pos), (layer_x + layer_width, y_pos + layer_height)],
            outline=color, width=2
        )
        # Draw fill gradient effect (semi-transparent)
        for j in range(3):
            draw.rectangle(
                [(layer_x + 3 + j, y_pos + 3 + j), 
                 (layer_x + layer_width - 3 - j, y_pos + layer_height - 3 - j)],
                outline=(color[0]//4, color[1]//4, color[2]//4), width=1
            )
        # Draw text
        draw.text((layer_x + 20, y_pos + 15), name, font=label_font, fill=color)
        draw.text((layer_x + layer_width - 100, y_pos + 15), size, font=small_font, fill=GRAY)
    
    # Draw APFS sub-volumes
    apfs_y = diagram_y + 50 + 2 * 80 + layer_height + 20
    draw.text((diagram_x + 100, apfs_y), "APFS Volumes:", font=small_font, fill=GRAY)
    
    volumes = ["macOS (System)", "Data", "Preboot", "Recovery"]
    for i, vol in enumerate(volumes):
        vol_x = diagram_x - 30 + i * 100
        vol_y = apfs_y + 30
        draw.rectangle(
            [(vol_x, vol_y), (vol_x + 90, vol_y + 30)],
            outline=PURPLE_NEON, width=1
        )
        draw.text((vol_x + 5, vol_y + 5), vol[:8], font=small_font, fill=PURPLE_NEON)
    
    # Bottom section - workflow
    workflow_y = HEIGHT - 200
    draw.line([(100, workflow_y - 20), (WIDTH-100, workflow_y - 20)], fill=TEAL_NEON, width=1)
    
    draw.text((WIDTH//2, workflow_y), "ERASE WORKFLOW", font=label_font, fill=PURPLE_NEON, anchor="mt")
    
    # Workflow steps
    steps = ["Backup", "Sign Out", "Recovery Mode", "Disk Utility", "Erase", "Reinstall"]
    step_width = (WIDTH - 200) // len(steps)
    
    for i, step in enumerate(steps):
        x_pos = 100 + i * step_width + step_width // 2
        y_pos = workflow_y + 50
        
        # Draw circle
        draw.ellipse([(x_pos - 25, y_pos), (x_pos + 25, y_pos + 50)], outline=CYAN_NEON, width=2)
        
        # Draw step number
        draw.text((x_pos, y_pos + 10), str(i + 1), font=label_font, fill=CYAN_NEON, anchor="mt")
        
        # Draw step name below
        draw.text((x_pos, y_pos + 60), step, font=small_font, fill=WHITE, anchor="mt")
        
        # Draw arrow to next step
        if i < len(steps) - 1:
            arrow_start = x_pos + 30
            arrow_end = x_pos + step_width - 30
            draw.line([(arrow_start, y_pos + 25), (arrow_end, y_pos + 25)], fill=TEAL_NEON, width=2)
            # Arrow head
            draw.polygon([
                (arrow_end - 10, y_pos + 20),
                (arrow_end, y_pos + 25),
                (arrow_end - 10, y_pos + 30)
            ], fill=TEAL_NEON)
    
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
    draw.text((WIDTH - 30, HEIGHT - 30), "v1.0", font=small_font, fill=GRAY, anchor="rb")
    
    # Save as WebP
    img.save(OUTPUT_PATH, 'WEBP', quality=95)
    print(f"Hero image saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_blueprint_image()