#!/usr/bin/env python3
"""Generate a technical blueprint-style hero image for AI Agent Workflow Orchestration."""

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
GREEN_NEON = (0, 255, 128)  # green neon
ORANGE_NEON = (255, 165, 0)  # orange neon
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Output path
OUTPUT_PATH = "/root/obelisk-design.github.io/src/assets/ai-agent-workflow-orchestration-hero.webp"

def create_blueprint_image():
    """Create a blueprint-style technical infographic hero image."""
    
    # Create image with dark background
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fallback to default
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        tiny_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
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
    title = "AI Agent Workflow Orchestration"
    draw.text((WIDTH//2, 70), title, font=title_font, fill=CYAN_NEON, anchor="mt")
    
    # Subtitle
    subtitle = "Building Intelligent Multi-Agent Systems"
    draw.text((WIDTH//2, 140), subtitle, font=subtitle_font, fill=GRAY, anchor="mt")
    
    # Draw horizontal divider line
    draw.line([(100, 200), (WIDTH-100, 200)], fill=CYAN_NEON, width=2)
    
    # === LEFT SECTION: Core Concepts ===
    concepts_x = 100
    concepts_y = 240
    
    draw.text((concepts_x, concepts_y), "CORE CONCEPTS", font=label_font, fill=PURPLE_NEON)
    
    concepts = [
        ("State Machine", "Finite state transitions"),
        ("DAG Model", "Directed Acyclic Graph"),
        ("Actor Model", "Message-passing agents"),
        ("Checkpointing", "State persistence & recovery"),
        ("Error Handling", "Retry, fallback, abort"),
    ]
    
    for i, (term, desc) in enumerate(concepts):
        y_pos = concepts_y + 45 + i * 42
        draw.ellipse([(concepts_x, y_pos+3), (concepts_x+8, y_pos+11)], fill=CYAN_NEON)
        draw.text((concepts_x+20, y_pos), f"{term}:", font=label_font, fill=WHITE)
        draw.text((concepts_x+200, y_pos+2), desc, font=small_font, fill=GRAY)
    
    # === CENTER SECTION: Workflow Diagram ===
    diagram_x = WIDTH // 2
    diagram_y = 280
    
    draw.text((diagram_x, diagram_y), "WORKFLOW ARCHITECTURE", font=label_font, fill=PURPLE_NEON, anchor="mt")
    
    # Draw orchestrator node (center top)
    orch_x = diagram_x
    orch_y = diagram_y + 60
    orch_radius = 45
    
    draw.ellipse(
        [(orch_x - orch_radius, orch_y - orch_radius), 
         (orch_x + orch_radius, orch_y + orch_radius)],
        outline=CYAN_NEON, width=3
    )
    draw.text((orch_x, orch_y - 10), "Orchestrator", font=small_font, fill=CYAN_NEON, anchor="mm")
    draw.text((orch_x, orch_y + 12), "Agent", font=tiny_font, fill=GRAY, anchor="mm")
    
    # Draw worker agents (below orchestrator)
    agents = [
        ("Research", TEAL_NEON),
        ("Analysis", PURPLE_NEON),
        ("Writing", GREEN_NEON),
        ("Review", ORANGE_NEON),
    ]
    
    agent_radius = 35
    agent_y = orch_y + 180
    agent_spacing = 220
    start_x = diagram_x - (len(agents) - 1) * agent_spacing // 2
    
    # Draw connections from orchestrator to agents
    for i, (agent_name, color) in enumerate(agents):
        agent_x = start_x + i * agent_spacing
        
        # Draw connection line
        draw.line([(orch_x, orch_y + orch_radius), (agent_x, agent_y - agent_radius)], 
                  fill=color, width=2)
        
        # Draw agent circle
        draw.ellipse(
            [(agent_x - agent_radius, agent_y - agent_radius),
             (agent_x + agent_radius, agent_y + agent_radius)],
            outline=color, width=2
        )
        draw.text((agent_x, agent_y - 8), agent_name, font=tiny_font, fill=color, anchor="mm")
        draw.text((agent_x, agent_y + 8), "Agent", font=tiny_font, fill=GRAY, anchor="mm")
    
    # Draw parallel execution indicator
    draw.line([(start_x - 50, agent_y), (start_x + (len(agents)-1) * agent_spacing + 50, agent_y)],
              fill=GRAY, width=1)
    draw.text((start_x - 70, agent_y), "parallel", font=tiny_font, fill=GRAY, anchor="rm")
    
    # Draw result aggregation
    result_y = agent_y + 120
    draw.line([(orch_x, agent_y + agent_radius), (orch_x, result_y - 30)], 
              fill=CYAN_NEON, width=2)
    
    draw.rectangle(
        [(orch_x - 80, result_y - 30), (orch_x + 80, result_y + 30)],
        outline=CYAN_NEON, width=2
    )
    draw.text((orch_x, result_y), "Final Output", font=small_font, fill=WHITE, anchor="mm")
    
    # === RIGHT SECTION: Framework Comparison ===
    compare_x = WIDTH - 480
    compare_y = 240
    
    draw.text((compare_x, compare_y), "FRAMEWORKS", font=label_font, fill=PURPLE_NEON)
    
    frameworks = [
        ("LangGraph", "State graph model"),
        ("CrewAI", "Role-based teams"),
        ("AutoGen", "Conversation flow"),
        ("Temporal", "Durable workflows"),
    ]
    
    for i, (name, desc) in enumerate(frameworks):
        y_pos = compare_y + 45 + i * 42
        # Draw box
        draw.rectangle(
            [(compare_x, y_pos), (compare_x + 100, y_pos + 30)],
            outline=TEAL_NEON, width=1
        )
        draw.text((compare_x + 50, y_pos + 15), name, font=small_font, fill=TEAL_NEON, anchor="mm")
        draw.text((compare_x + 115, y_pos + 6), desc, font=small_font, fill=GRAY)
    
    # === BOTTOM SECTION: Workflow Patterns ===
    pattern_y = HEIGHT - 220
    draw.line([(100, pattern_y - 20), (WIDTH-100, pattern_y - 20)], fill=TEAL_NEON, width=1)
    
    draw.text((WIDTH//2, pattern_y), "COLLABORATION PATTERNS", font=label_font, fill=PURPLE_NEON, anchor="mt")
    
    patterns = [
        ("Hierarchical", "Central coordination"),
        ("Peer-to-Peer", "Equal agents"),
        ("Debate", "Consensus via argument"),
        ("Competitive", "Best result wins"),
    ]
    
    pattern_width = (WIDTH - 200) // len(patterns)
    pattern_start_y = pattern_y + 50
    
    for i, (name, desc) in enumerate(patterns):
        x_center = 100 + i * pattern_width + pattern_width // 2
        
        # Draw pattern box
        box_width = 140
        box_height = 70
        draw.rectangle(
            [(x_center - box_width//2, pattern_start_y),
             (x_center + box_width//2, pattern_start_y + box_height)],
            outline=PURPLE_NEON, width=2
        )
        draw.text((x_center, pattern_start_y + 20), name, font=small_font, fill=WHITE, anchor="mm")
        draw.text((x_center, pattern_start_y + 45), desc, font=tiny_font, fill=GRAY, anchor="mm")
        
        # Draw arrow to next pattern
        if i < len(patterns) - 1:
            arrow_start = x_center + box_width//2 + 10
            arrow_end = x_center + pattern_width - box_width//2 - 10
            draw.line([(arrow_start, pattern_start_y + box_height//2), 
                      (arrow_end, pattern_start_y + box_height//2)], 
                      fill=TEAL_NEON, width=1)
    
    # === Add corner decorations ===
    corner_size = 25
    
    # Top-left
    draw.line([(20, 20), (20, 20 + corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(20, 20), (20 + corner_size, 20)], fill=CYAN_NEON, width=2)
    
    # Top-right
    draw.line([(WIDTH - 20, 20), (WIDTH - 20, 20 + corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(WIDTH - 20, 20), (WIDTH - 20 - corner_size, 20)], fill=CYAN_NEON, width=2)
    
    # Bottom-left
    draw.line([(20, HEIGHT - 20), (20, HEIGHT - 20 - corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(20, HEIGHT - 20), (20 + corner_size, HEIGHT - 20)], fill=CYAN_NEON, width=2)
    
    # Bottom-right
    draw.line([(WIDTH - 20, HEIGHT - 20), (WIDTH - 20, HEIGHT - 20 - corner_size)], fill=CYAN_NEON, width=2)
    draw.line([(WIDTH - 20, HEIGHT - 20), (WIDTH - 20 - corner_size, HEIGHT - 20)], fill=CYAN_NEON, width=2)
    
    # Add version and tech stack
    draw.text((WIDTH - 30, HEIGHT - 30), "2026", font=tiny_font, fill=GRAY, anchor="rb")
    draw.text((30, HEIGHT - 30), "AI Agent Architecture", font=tiny_font, fill=GRAY, anchor="lb")
    
    # Save as WebP
    img.save(OUTPUT_PATH, 'WEBP', quality=95)
    print(f"Hero image saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_blueprint_image()