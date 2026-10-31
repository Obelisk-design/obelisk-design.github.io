#!/usr/bin/env python3
"""Generate neon-blueprint hero for the S2 hospital data-governance post."""

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
DARK_GRAY = (100, 110, 125)

OUT = "/home/ubuntu/obelisk-design.github.io/src/assets/s2-data-governance-hero.webp"
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
WQY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

title_font = font(DEJAVU + "DejaVuSans-Bold.ttf", 68)
sub_font = font(WQY, 38)
label_font = font(DEJAVU + "DejaVuSansMono.ttf", 24)
node_font = font(WQY, 26)
node_font_sm = font(WQY, 22)
small_font = font(WQY, 20)
tiny_font = font(WQY, 18)

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
d.text((WIDTH // 2, 74), "Hospital Data Governance", font=title_font, fill=CYAN, anchor="mt")
d.text((WIDTH // 2, 152), "医院 · S2 · 中心库 —— 三级汇聚与治理闭环", font=sub_font, fill=PURPLE, anchor="mt")
d.line([(100, 214), (WIDTH - 100, 214)], fill=CYAN, width=2)

import math
def arrow(p1, p2, color, width=3, dashed=False, head=12):
    width = max(1, round(width))
    x1, y1 = p1; x2, y2 = p2
    if dashed:
        dist = math.hypot(x2 - x1, y2 - y1)
        n = max(int(dist // 22), 1)
        for i in range(n + 1):
            s = i / n; e = min((i + 0.55) / n, 1)
            d.line([(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s),
                    (x1 + (x2 - x1) * e, y1 + (y2 - y1) * e)], fill=color, width=width)
    else:
        d.line([p1, p2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for off in (2.6, -2.6):
        d.line([(x2, y2), (x2 - head * math.cos(ang - off), y2 - head * math.sin(ang - off))],
               fill=color, width=width)

def pill(x, y, text, border, fnt=node_font, pad=14, h=44):
    tw = d.textlength(text, font=fnt)
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + h], radius=10, fill=(16, 24, 38), outline=border, width=2)
    d.text((x + pad, y + h // 2), text, font=fnt, fill=WHITE, anchor="lm")
    return tw + pad * 2, h

def band(label, color, y, fill, pills, penw=2):
    d.rounded_rectangle([170, y, WIDTH - 170, y + 130], radius=16, fill=fill, outline=color, width=penw)
    d.text((196, y + 24), label, font=node_font, fill=color, anchor="lm")
    nx = 196
    for t in pills:
        w, _ = pill(nx, y + 62, t, color, fnt=node_font_sm)
        nx += w + 16
    return y, y + 130

# three tiers
b1y, b1e = band("医院端 ×N（每院前置机）", GREEN, 268, (14, 32, 26),
                ["HIS·EMR·LIS·PACS", "CDC 采集", "FHIR 标准化", "脱敏加密"])
b2y, b2e = band("S2 区域平台（中心的中心 · 治理核心）", PURPLE, 468, (32, 24, 52),
                ["标准引擎", "数据质量稽核", "EMPI 主索引", "元数据血缘", "治理库"], penw=4)
b3y, b3e = band("中心库（集团 / 省级）", ORANGE, 668, (42, 33, 14),
                ["全量仓 贴源→标准→主题", "指标·资产·API", "AI 与监管"], penw=2)

# uplink arrows (green): 医院 -> S2 -> 中心库
for x in (560, 960, 1360):
    arrow((x, b1e + 2), (x, b2y - 2), GREEN, 4)
    arrow((x, b2e + 2), (x, b3y - 2), GREEN, 4)
d.text((975, (b1e + b2y) // 2), "增量 CDC + T+1 批量 · TLS 加密", font=tiny_font, fill=GREEN, anchor="lm")
d.text((975, (b2e + b3y) // 2), "全量 + 增量同步 · 对账校验 · 幂等写入", font=tiny_font, fill=GREEN, anchor="lm")

# governance loop (teal dashed, upward on the right side)
arrow((1600, b3y - 2), (1600, b2e + 2), TEAL, 3.5, dashed=True)
arrow((240, b2y - 2), (240, b1e + 2), TEAL, 3.5, dashed=True)
d.text((1616, (b2e + b3y) // 2), "质控规则下发", font=tiny_font, fill=TEAL, anchor="lm")
d.text((256, (b1e + b2y) // 2), "质量报告 · 整改工单", font=tiny_font, fill=TEAL, anchor="lm")

# legend
ly = 880
d.line([(320, ly), (400, ly)], fill=GREEN, width=4)
d.text((415, ly), "数据上行（医院→S2→中心库）", font=small_font, fill=GRAY, anchor="lm")
seg = 14
for i in range(5):
    d.line([(900 + i * 24, ly), (900 + i * 24 + seg, ly)], fill=TEAL, width=4)
d.text((1055, ly), "治理闭环（规则下发 / 质量回流）", font=small_font, fill=GRAY, anchor="lm")

# footer
d.line([(100, 970), (WIDTH - 100, 970)], fill=GRID_MAJOR, width=2)
d.text((100, 1006), "DATA GOVERNANCE PIPELINE", font=label_font, fill=TEAL, anchor="lm")
d.text((WIDTH // 2, 1006), "CDC+批量双轨 · EMPI · FHIR · 质控闭环", font=small_font, fill=GRAY, anchor="mm")
d.text((WIDTH - 100, 1006), "2026", font=label_font, fill=DARK_GRAY, anchor="rm")

img.save(OUT, "WEBP", quality=92)
print("saved", OUT)
