"""Pixel-art banner: shadow-monarch character slashing a monster. Outputs GIF."""
from PIL import Image

W, H = 128, 48
SCALE = 6
GROUND = 42

PAL = {
    "h": (16, 16, 26),     # hair black
    "H": (40, 38, 66),     # hair highlight
    "f": (232, 201, 168),  # skin
    "e": (139, 92, 246),   # glowing purple eye
    "C": (27, 27, 46),     # coat dark
    "D": (44, 44, 74),     # coat highlight
    "b": (14, 14, 20),     # boots
    "s": (200, 190, 255),  # dagger blade
    "S": (255, 255, 255),  # blade core / slash
    "m": (58, 47, 63),     # monster body dark
    "M": (82, 65, 90),     # monster body light
    "r": (255, 51, 85),    # monster eye red
    "t": (235, 235, 225),  # teeth/claw
    "p": (139, 92, 246),   # purple fx
    "P": (167, 139, 250),  # light purple fx
    "w": (255, 255, 255),  # white spark
}

JW_STAND = """
...hhhh....
..hhhhhh...
..hHffff...
..hhfefe...
...ffff....
..CCCCC....
.CCCCCCC...
.CCDCCCC...
.fCCCCCCf..
..CCCCCC.s.
..CCCCCC.s.
..CCCCC....
...CC.CC...
...CC.CC...
...CC.CC...
..bbb.bbb..
"""

JW_DASH = """
....hhhh...
...hhhhhh..
...hHffff..
...hhfefe..
....ffff...
...CCCCCC..
..CCCCCCCC.
.fCCDCCCCf.
...CCCCCC.s
...CCCCCC.s
....CCCCC..
...CCC.CCC.
..CCC...CC.
.bbb.....bb
"""

JW_SLASH = """
...hhhh....
..hhhhhh...
..hHffff...
..hhfefe...
...ffff....
..CCCCCC...
.CCCCCCCCf.
.CCDCCCCC.s
.fCCCCCC..s
..CCCCCC...
..CCCCC....
..CCC.CC...
.CCC...CC..
.bb.....bb.
"""

MONSTER = """
..tt..............tt..
..Mtt....mmmm....ttM..
...MMmmmmMMMMmmmmMM...
....mmMMMMMMMMMMmm....
...mmMMMMMMMMMMMMmm...
..mmMMrrMMMMMMrrMMmm..
..mMMMMMMMMMMMMMMMMm..
..mMMhthtthhtthtMMMm..
..mMMMMMMMMMMMMMMMMm..
.mMm.mmMMMMMMMMmm.mMm.
mMm...mMMMMMMMMm...mMm
mm....mMMMMMMMMm....mm
tt....mMMMMMMMMm....tt
......mMMMMMMMMm......
.....mmMMMMMMMMmm.....
.....mMMm....mMMm.....
....mmMm......mMmm....
....mmm........mmm....
...tmm..........mmt...
"""

MONSTER_HIT = MONSTER.replace("M", "P")


def sprite_px(art):
    px = []
    for y, row in enumerate(art.strip("\n").split("\n")):
        for x, ch in enumerate(row):
            if ch != ".":
                px.append((x, y, ch))
    return px


def blit(canvas, art, ox, oy):
    for x, y, ch in sprite_px(art):
        color = PAL[ch]
        if 0 <= ox + x < W and 0 <= oy + y < H:
            canvas.putpixel((ox + x, oy + y), color)


def rng(*seed):
    v = 2166136261
    for s in seed:
        v = (v ^ (s + 11)) * 16777619 % (2**32)
    return v


def background(img, frame):
    for y in range(H):
        for x in range(W):
            img.putpixel((x, y), (13, 12, 22) if y < GROUND else (24, 22, 38))
    for x in range(W):  # ground top edge
        img.putpixel((x, GROUND), (38, 34, 60))
    for i in range(26):  # distant cave specks
        x, y = rng(i, 1) % W, rng(i, 2) % (GROUND - 8)
        img.putpixel((x, y), (30, 28, 52))
    for i in range(16):  # floating purple motes, drift upward
        x = (rng(i, 3) % W)
        y = (rng(i, 4) % GROUND + GROUND - frame * 2) % GROUND
        img.putpixel((x, y), PAL["p"] if i % 2 else PAL["P"])


def aura(img, ox, oy, frame, height=16):
    for i in range(7):
        x = ox + rng(i, frame, 5) % 14 - 2
        y = oy + rng(i, frame, 6) % height
        if 0 <= x < W and 0 <= y < H:
            img.putpixel((x, y), PAL["p"] if i % 2 else PAL["P"])


def slash_arc(img, cx, cy, step):
    arcs = {
        0: [(2, -8), (4, -7), (6, -5), (7, -3), (8, -1)],
        1: [(8, -1), (8, 1), (7, 3), (6, 5), (4, 6), (2, 7)],
    }
    for dx, dy in arcs[step]:
        for spread in (0, 1):
            x, y = cx + dx + spread, cy + dy
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), PAL["S"] if spread == 0 else PAL["s"])


def spark(img, cx, cy, big):
    pts = [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2)]
    if big:
        pts += [(3, 3), (-3, 3), (3, -3), (-3, -3), (5, 0), (0, 5), (0, -5)]
    for dx, dy in pts:
        x, y = cx + dx, cy + dy
        if 0 <= x < W and 0 <= y < H:
            img.putpixel((x, y), PAL["w"] if big else PAL["P"])


DIGITS = {
    "-": ["...", "...", "###", "...", "..."],
    "9": ["###", "#.#", "###", "..#", "###"],
}


def damage_text(img, ox, oy, text, color):
    for ch in text:
        for dy, row in enumerate(DIGITS[ch]):
            for dx, c in enumerate(row):
                if c == "#" and 0 <= ox + dx < W and 0 <= oy + dy < H:
                    img.putpixel((ox + dx, oy + dy), color)
        ox += 4


MX = 104  # monster x
FRAMES = [
    # (pose, jw_x, monster_art, monster_dx, slash, spark, dashlines)
    ("stand", 14, MONSTER, 0, None, None, False),
    ("stand", 14, MONSTER, 0, None, None, False),
    ("dash", 34, MONSTER, 0, None, None, True),
    ("dash", 58, MONSTER, 0, None, None, True),
    ("dash", 76, MONSTER, 0, None, None, True),
    ("slash", 82, MONSTER, 0, 0, None, False),
    ("slash", 82, MONSTER_HIT, 2, 1, "big", False),
    ("slash", 82, MONSTER, 3, None, "small", False),
    ("slash", 82, MONSTER, 1, None, None, False),
    ("dash", 48, MONSTER, 0, None, None, True),
    ("stand", 14, MONSTER, 0, None, None, False),
    ("stand", 14, MONSTER, 0, None, None, False),
]

POSES = {"stand": JW_STAND, "dash": JW_DASH, "slash": JW_SLASH}

frames = []
prev_jx = FRAMES[0][1]
for i, (pose, jx, mart, mdx, slash, sp, lines) in enumerate(FRAMES):
    img = Image.new("RGB", (W, H))
    background(img, i)
    art = POSES[pose]
    jh = len(art.strip("\n").split("\n"))
    jy = GROUND - jh + (1 if pose == "stand" and i % 2 else 0)  # idle bob
    mh = len(mart.strip("\n").split("\n"))
    mdy = 1 if i % 2 and mdx == 0 else 0  # monster breathing
    blit(img, mart, MX - 11 + mdx, GROUND - mh + mdy)
    if lines:
        trail = -1 if jx >= prev_jx else 1  # lines on the trailing side
        edge = jx if trail == -1 else jx + 11
        for k in range(3):
            y = jy + 4 + k * 4
            for dx in range(4, 10):
                x = edge + trail * dx
                if 0 <= x < W:
                    img.putpixel((x, y), (60, 56, 96))
    blit(img, art, jx, jy)
    aura(img, jx, jy, i, jh)
    if slash is not None:
        slash_arc(img, jx + 11, jy + 8, slash)
    if sp:
        spark(img, MX - 9, GROUND - mh + 8, sp == "big")
        rise = 0 if sp == "big" else 3  # number floats up after the hit
        damage_text(img, MX - 3, GROUND - mh - 7 - rise,
                    "-99", PAL["w"] if sp == "big" else PAL["P"])
    prev_jx = jx
    frames.append(img.resize((W * SCALE, H * SCALE), Image.NEAREST))

frames[0].save(
    "/tmp/pixelgen/jinwoo-pixel.gif",
    save_all=True, append_images=frames[1:], duration=130, loop=0,
)

# contact sheet for review
sheet = Image.new("RGB", (W * 4, H * 3))
for i, f in enumerate(frames):
    small = f.resize((W, H), Image.NEAREST)
    sheet.paste(small, ((i % 4) * W, (i // 4) * H))
sheet.resize((W * 4 * 3, H * 3 * 3), Image.NEAREST).save("/tmp/pixelgen/sheet.png")
print("ok")
