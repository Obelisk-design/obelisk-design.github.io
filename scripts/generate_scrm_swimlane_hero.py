#!/usr/bin/env python3
"""Generate a neon-blueprint hero for the SCRM scene-1 swimlane post."""

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1920, 1080
BG = (10, 14, 23)
GRID = (20, 30, 50)
GRID_MAJOR = (30, 45, 70)
CYAN = (0, 255, 255)
PURPLE = (180, 100, 255)
TEAL = (64, 224, 208)
GREEN = (7, 193, 96)      # wechat green
BLUE = (59, 130, 246)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 110, 125)

OUT = "/home/ubuntu/obelisk-design.github.io/src/assets/scrm-scene1-swimlane-hero.webp"

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
d.text((WIDTH // 2, 74), "WeChat SCRM Sync Design", font=title_font, fill=CYAN, anchor="mt")
d.text((WIDTH // 2, 152), "个人微信 · 企业微信双向同步 · 场景一泳道图", font=sub_font, fill=PURPLE, anchor="mt")
d.line([(100, 214), (WIDTH - 100, 214)], fill=CYAN, width=2)


def arrow(p1, p2, color, width=3, dashed=False, head=12):
    x1, y1 = p1
    x2, y2 = p2
    if dashed:
        import math
        dist = math.hypot(x2 - x1, y2 - y1)
        n = max(int(dist // 22), 1)
        for i in range(n + 1):
            s = i / n
            e = min((i + 0.55) / n, 1)
            d.line([(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s),
                    (x1 + (x2 - x1) * e, y1 + (y2 - y1) * e)], fill=color, width=width)
    else:
        d.line([p1, p2], fill=color, width=width)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    for off in (2.6, -2.6):
        d.line([(x2, y2), (x2 - head * math.cos(ang - off), y2 - head * math.sin(ang - off))],
               fill=color, width=width)


def pill(x, y, text, border, fnt=node_font, pad=14):
    tw = d.textlength(text, font=fnt)
    h = 44
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + h], radius=10, fill=(16, 24, 38), outline=border, width=2)
    d.text((x + pad, y + h // 2), text, font=fnt, fill=WHITE, anchor="lm")
    return tw + pad * 2, h


# ---- swimlane sketch (4 lanes) ----
LX0, LX1 = 250, 1660
lanes = [
    ("客户 · 个人微信", GREEN, 262, ["① 扫码加好友", "② 发起咨询", "⑧ 下单成交"]),
    ("销售 · 个微+企微助手", BLUE, 412, ["③ 接待确认", "④ AI 话术", "⑥ 标签·跟进", "⑦ SOP 促单"]),
    ("系统服务 · 同步+LLM", TEAL, 562, ["LLM freellmapi", "同步引擎", "CRM 客户库"]),
    ("管理员 · 企业微信后台", PURPLE, 712, ["客户看板", "分配/回收", "SOP 配置"]),
]
LANE_H = 118
lane_boxes = []
for name, color, y, nodes in lanes:
    d.rounded_rectangle([LX0, y, LX1, y + LANE_H], radius=14, fill=(14, 20, 32), outline=color, width=3)
    d.text((LX0 + 22, y + LANE_H // 2), name, font=node_font_sm, fill=color, anchor="lm")
    lane_boxes.append((y, y + LANE_H, color))
    # nodes
    nx = LX0 + 360
    for t in nodes:
        w, _ = pill(nx, y + (LANE_H - 44) // 2, t, color, fnt=node_font_sm if len(t) > 8 else node_font)
        nx += w + 18

# main-flow arrows (solid gray, down the left side between lanes)
fx = LX0 + 60
for i in range(3):
    y1 = lane_boxes[i][1]
    y2 = lane_boxes[i + 1][0]
    arrow((fx, y1 + 2), (fx, y2 - 2), DARK_GRAY, 3)
d.text((fx + 12, (lane_boxes[0][1] + lane_boxes[1][0]) // 2), "好友", font=tiny_font, fill=DARK_GRAY, anchor="lm")
d.text((fx + 12, (lane_boxes[1][1] + lane_boxes[2][0]) // 2), "记录", font=tiny_font, fill=DARK_GRAY, anchor="lm")
d.text((fx + 12, (lane_boxes[2][1] + lane_boxes[3][0]) // 2), "数据", font=tiny_font, fill=DARK_GRAY, anchor="lm")

# sync arrows (purple dashed) — the story of the post
sx1, sx2 = 1050, 1330
arrow((sx1, lane_boxes[1][0] + 4), (sx1, lane_boxes[2][1] - 4), PURPLE, 4, dashed=True)   # 销售→系统
arrow((sx2, lane_boxes[2][1] - 4), (sx2, lane_boxes[1][0] + 4), PURPLE, 4, dashed=True)   # 系统→销售
arrow((900, lane_boxes[2][1] - 4), (900, lane_boxes[3][0] + 4), PURPLE, 4, dashed=True)   # 系统→管理员
arrow((1500, lane_boxes[3][0] + 4), (1500, lane_boxes[2][1] - 4), PURPLE, 4, dashed=True) # 管理员→系统
d.text((sx1 + 10, (lane_boxes[1][1] + lane_boxes[2][0]) // 2), "个微->企微", font=tiny_font, fill=PURPLE, anchor="lm")
d.text((sx2 - 10, (lane_boxes[1][1] + lane_boxes[2][0]) // 2), "企微->个微", font=tiny_font, fill=PURPLE, anchor="rm")

# zone brackets: 个微 vs 企微
d.line([(120, 262), (120, 530)], fill=GREEN, width=4)
d.text((96, 396), "个微", font=node_font, fill=GREEN, anchor="rm")
d.line([(120, 712), (120, 830)], fill=PURPLE, width=4)
d.text((96, 771), "企微", font=node_font, fill=PURPLE, anchor="rm")

# legend
ly = 880
d.line([(320, ly), (400, ly)], fill=DARK_GRAY, width=3)
d.text((415, ly), "业务操作流", font=small_font, fill=GRAY, anchor="lm")
import math
seg = 14
for i in range(5):
    d.line([(640 + i * 24, ly), (640 + i * 24 + seg, ly)], fill=PURPLE, width=4)
d.text((780, ly), "个微-企微 信息同步", font=small_font, fill=PURPLE, anchor="lm")
d.text((1160, ly), "紫虚线 = 双向同步路径（记录级）", font=small_font, fill=GRAY, anchor="lm")

# footer
d.line([(100, 970), (WIDTH - 100, 970)], fill=GRID_MAJOR, width=2)
d.text((100, 1006), "SCENE 1 · LEAD TO DEAL", font=label_font, fill=TEAL, anchor="lm")
d.text((WIDTH // 2, 1006), "标签同步 | SOP 下发 | 看板数据 | LLM 话术", font=small_font, fill=GRAY, anchor="mm")
d.text((WIDTH - 100, 1006), "2026", font=label_font, fill=DARK_GRAY, anchor="rm")

img.save(OUT, "WEBP", quality=92)
print("saved", OUT)
