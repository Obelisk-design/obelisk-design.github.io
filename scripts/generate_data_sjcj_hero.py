#!/usr/bin/env python3
"""Generate neon-blueprint hero for the data-sjcj teardown post."""

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1920, 1080
BG = (10, 14, 23)
GRID = (20, 30, 50)
GRID_MAJOR = (30, 45, 70)
CYAN = (0, 255, 255)
PURPLE = (180, 100, 255)
TEAL = (64, 224, 208)
GREEN = (7, 193, 96)
ORANGE = (245, 158, 11)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

OUT = "/home/ubuntu/obelisk-design.github.io/src/assets/data-sjcj-first-principles-hero.webp"
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
WQY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


title_font = font(DEJAVU + "DejaVuSans-Bold.ttf", 66)
sub_font = font(WQY, 36)
label_font = font(DEJAVU + "DejaVuSansMono.ttf", 24)
mono_sm = font(DEJAVU + "DejaVuSansMono.ttf", 21)
node_font = font(WQY, 27)
node_font_sm = font(WQY, 22)
tiny_font = font(WQY, 19)

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
d = ImageDraw.Draw(img)

# grid
for x in range(0, WIDTH, 40):
    d.line([(x, 0), (x, HEIGHT)], fill=GRID, width=1)
for y in range(0, HEIGHT, 40):
    d.line([(0, y), (WIDTH, y)], fill=GRID, width=1)
for x in range(0, WIDTH, 160):
    d.line([(x, 0), (x, HEIGHT)], fill=GRID_MAJOR, width=2)
for y in range(0, HEIGHT, 160):
    d.line([(0, y), (WIDTH, y)], fill=GRID_MAJOR, width=2)

# corner brackets
arm, m, cw = 46, 34, 4
for cx, cy, dx, dy in [(m, m, 1, 1), (WIDTH - m, m, -1, 1), (m, HEIGHT - m, 1, -1), (WIDTH - m, HEIGHT - m, -1, -1)]:
    d.line([(cx, cy), (cx + dx * arm, cy)], fill=CYAN, width=cw)
    d.line([(cx, cy), (cx, cy + dy * arm)], fill=CYAN, width=cw)

# title / subtitle / divider
d.text((WIDTH // 2, 72), "Data Platform Teardown", font=title_font, fill=CYAN, anchor="mt")
d.text((WIDTH // 2, 150), "医疗数据采集服务 · 第一性原理 · 开源对照 · 现代化路线", font=sub_font, fill=PURPLE, anchor="mt")
d.line([(100, 212), (WIDTH - 100, 212)], fill=CYAN, width=2)

# ---- five-layer stack (left) + open-source callouts (right) ----
BX0, BX1 = 150, 1030
CX0 = 1150
bands = [
    ("接入层", "ACCESS", "17+ 异构数据源 · JDBC / CDC 采集", CYAN, "SeaTunnel / Airbyte"),
    ("任务层", "TASKS", "抽取 · 初始化 · 比对 · 推送 + 状态机与锁", CYAN, "DolphinScheduler"),
    ("执行层", "EXECUTION", "Flink Session Cluster · Kafka · OGG/Debezium", GREEN, "Flink CDC 3.x / Routine Load"),
    ("标准层", "STANDARD", "标准码表 · 对照关系 · 审核流 · 转码", PURPLE, "LLM Mapping + dbt models"),
    ("监控层", "MONITORING", "17 Controller · 5 类告警 · 80+ 告警项", ORANGE, "OpenLineage / OpenMetadata"),
]

bh, gap = 96, 26
y = 262
band_boxes = []
for name_cn, name_en, detail, color, oss in bands:
    x1 = BX1
    d.rounded_rectangle([BX0, y, x1, y + bh], radius=10, outline=color, width=3)
    # translucent-ish fill: dark tint
    d.rounded_rectangle([BX0 + 3, y + 3, x1 - 3, y + bh - 3], radius=8, fill=(14, 20, 34))
    # re-draw outline over fill
    d.rounded_rectangle([BX0, y, x1, y + bh], radius=10, outline=color, width=3)
    d.text((BX0 + 26, y + bh // 2), name_cn, font=node_font, fill=WHITE, anchor="lm")
    en_w = d.textlength(name_en, font=label_font)
    d.text((BX0 + 26 + d.textlength(name_cn, font=node_font) + 22, y + bh // 2), name_en, font=label_font, fill=color, anchor="lm")
    d.text((x1 - 24, y + bh // 2), detail, font=node_font_sm, fill=GRAY, anchor="rm")
    # connector to OSS callout
    mid = y + bh // 2
    for i in range(4):
        sx = x1 + 14 + i * 16
        d.line([(sx, mid), (sx + 9, mid)], fill=color, width=2)
    d.text((CX0, mid), oss, font=mono_sm, fill=color, anchor="lm")
    band_boxes.append((BX0, y, x1, y + bh, color, mid))
    y += bh + gap

# downward arrows between bands (drawn polygon heads)
for i in range(len(band_boxes) - 1):
    ax = (BX0 + BX1) // 2
    y_end = band_boxes[i][3]
    y_next = band_boxes[i + 1][1]
    col = band_boxes[i][4]
    d.line([(ax, y_end + 2), (ax, y_next - 12)], fill=col, width=3)
    d.polygon([(ax - 9, y_next - 14), (ax + 9, y_next - 14), (ax, y_next - 2)], fill=col)

# feedback loop: monitoring -> tasks (left edge, dashed teal)
fx = 96
_, _, _, y_mon, _, mid_mon = band_boxes[4]
_, _, _, y_task, _, mid_task = band_boxes[1]
d.line([(BX0 - 54, mid_mon), (fx, mid_mon)], fill=TEAL, width=2)
d.line([(fx, mid_mon), (fx, mid_task)], fill=TEAL, width=2)
for yy in range(mid_task, mid_mon, 22):
    d.line([(fx, yy), (fx, min(yy + 12, mid_mon))], fill=TEAL, width=2)
d.line([(fx, mid_task), (BX0 - 54, mid_task)], fill=TEAL, width=2)
d.polygon([(BX0 - 56, mid_task - 8), (BX0 - 56, mid_task + 8), (BX0 - 42, mid_task)], fill=TEAL)
# label rotated? keep horizontal small text near loop
d.text((fx + 8, (mid_task + mid_mon) // 2 - 14), "治理", font=tiny_font, fill=TEAL)
d.text((fx + 8, (mid_task + mid_mon) // 2 + 8), "闭环", font=tiny_font, fill=TEAL)

# stats ribbon
ry = HEIGHT - 78
d.line([(140, ry - 30), (WIDTH - 140, ry - 30)], fill=GRID_MAJOR, width=2)
stats = "60+ TABLES   ·   17+ DB TYPES   ·   80+ ALARM ITEMS   ·   3 SCHEDULERS   ·   StarRocks + Flink + Kafka"
d.text((WIDTH // 2, ry + 4), stats, font=label_font, fill=GRAY, anchor="mm")

img.save(OUT, "WEBP", quality=90)
print("saved", OUT)
