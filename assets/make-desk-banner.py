"""Pixel-art banner: dev coding at a cozy desk at night. Outputs GIF."""
from PIL import Image

W, H = 128, 48
SCALE = 6
GROUND = 42
N = 16

PAL = {
    "h": (16, 16, 26),     # hair
    "H": (40, 38, 66),     # hair highlight
    "f": (232, 201, 168),  # skin
    "e": (139, 92, 246),   # eye
    "C": (27, 27, 46),     # sweater dark
    "D": (44, 44, 74),     # sweater highlight
    "b": (14, 14, 20),     # shoes
    "w": (60, 52, 44),     # desk wood dark
    "W": (94, 78, 62),     # desk wood light
    "k": (34, 32, 54),     # keyboard / chair
    "s": (18, 20, 34),     # screen background
    "g": (120, 220, 160),  # code green
    "p": (139, 92, 246),   # code purple
    "c": (110, 190, 240),  # code cyan
    "y": (240, 200, 120),  # code yellow
    "P": (167, 139, 250),  # glow light purple
    "m": (230, 226, 200),  # moon
    "u": (196, 120, 130),  # mug
    "S": (200, 200, 210),  # steam
}

DEV = """
..hhhh...
.hhhhhh..
.hhHfff..
.hhffef..
..hffff..
.CCCCC...
.CCCCCC..
.CCDCCCf.
.CCCCCC..
..CCCC...
..CCCCC..
..k.CCC..
..k..bb..
"""


def rng(*seed):
    v = 2166136261
    for s in seed:
        v = (v ^ (s + 11)) * 16777619 % (2**32)
    return v


def put(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), color)


def blit(img, art, ox, oy):
    for y, row in enumerate(art.strip("\n").split("\n")):
        for x, ch in enumerate(row):
            if ch != ".":
                put(img, ox + x, oy + y, PAL[ch])


def rect(img, x0, y0, x1, y1, color):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(img, x, y, color)


def background(img, frame):
    rect(img, 0, 0, W - 1, H - 1, (13, 12, 22))          # wall
    rect(img, 0, GROUND, W - 1, H - 1, (24, 22, 38))     # floor
    for x in range(W):
        put(img, x, GROUND, (38, 34, 60))
    # window, top-left, with moon and twinkling stars
    rect(img, 8, 6, 34, 24, (10, 10, 20))
    for x in range(8, 35):
        put(img, x, 6, (52, 48, 80)); put(img, x, 24, (52, 48, 80))
    for y in range(6, 25):
        put(img, 8, y, (52, 48, 80)); put(img, 34, y, (52, 48, 80))
        put(img, 21, y, (52, 48, 80))
    rect(img, 26, 9, 30, 13, PAL["m"])                    # moon
    for cx, cy in ((26, 9), (30, 9), (26, 13), (30, 13)):  # round the corners
        put(img, cx, cy, (10, 10, 20))
    rect(img, 27, 10, 28, 11, (200, 196, 170))
    for i in range(7):                                    # stars
        x = 10 + rng(i, 1) % 22
        y = 8 + rng(i, 2) % 14
        if x != 21 and not (25 <= x <= 31 and 8 <= y <= 14):
            on = (i + frame // 2) % 3 != 0
            put(img, x, y, (170, 170, 200) if on else (70, 70, 100))
    # shelf with books, top-right
    rect(img, 96, 10, 122, 11, (60, 52, 44))
    for i, col in enumerate(("p", "c", "y", "g", "p", "c")):
        rect(img, 98 + i * 4, 4, 100 + i * 4, 9, PAL[col])


def desk_scene(img, frame):
    # desk top and legs
    rect(img, 46, 30, 118, 31, PAL["W"])
    rect(img, 46, 32, 118, 32, PAL["w"])
    rect(img, 48, 33, 49, GROUND - 1, PAL["w"])
    rect(img, 115, 33, 116, GROUND - 1, PAL["w"])
    # monitor: stand, frame, screen
    rect(img, 88, 27, 91, 29, PAL["k"])
    rect(img, 78, 28, 101, 29, PAL["k"])
    rect(img, 72, 6, 107, 26, PAL["k"])
    rect(img, 74, 8, 105, 24, PAL["s"])
    # typed code lines, progress loops over N frames
    lines = [(1, 10, "p"), (3, 14, "c"), (3, 8, "g"), (5, 12, "y"),
             (3, 10, "c"), (1, 13, "g")]
    total = sum(ln for _, ln, _ in lines)
    prog = (frame + 1) * (total // (N - 2) + 1)
    sy = 9
    for li, (indent, ln, col) in enumerate(lines):
        take = max(0, min(ln, prog))
        prog -= ln
        if take:
            rect(img, 75 + indent, sy + li * 2, 75 + indent + take - 1,
                 sy + li * 2, PAL[col])
    # cursor blink on the active line
    if frame % 2 == 0:
        put(img, 75 + 1, sy + min(5, max(0, (frame * 6) // N)) * 2 + 1,
            (220, 220, 230))
    # screen glow specks
    for i in range(6):
        x = 70 + rng(i, frame, 3) % 42
        y = 4 + rng(i, frame, 4) % 26
        if not (72 <= x <= 107 and 6 <= y <= 26):
            put(img, x, y, (50, 46, 84))
    # keyboard
    rect(img, 62, 29, 74, 29, PAL["k"])
    # mug with steam, right of the monitor
    rect(img, 111, 27, 114, 29, PAL["u"])
    put(img, 115, 28, PAL["u"])
    for k in range(3):
        sx = 112 + (rng(k, frame // 2, 7) % 3) - 1
        put(img, sx, 24 - k * 2 - (frame % 2), PAL["S"])


def dev(img, frame):
    ox, oy = 52, 17
    blit(img, DEV, ox, oy)
    # chair
    rect(img, 50, 24, 51, 38, PAL["k"])
    rect(img, 50, 38, 60, 39, PAL["k"])
    rect(img, 52, 40, 53, GROUND - 1, PAL["k"])
    rect(img, 58, 40, 59, GROUND - 1, PAL["k"])
    # typing hand bobs between keyboard and up
    hy = 28 if frame % 2 else 27
    put(img, 62, hy, PAL["f"])
    put(img, 63, hy, PAL["f"])
    # face lit by screen
    put(img, 57, 20, (255, 226, 190))


frames = []
for i in range(N):
    img = Image.new("RGB", (W, H))
    background(img, i)
    desk_scene(img, i)
    dev(img, i)
    frames.append(img.resize((W * SCALE, H * SCALE), Image.NEAREST))

frames[0].save(
    "/tmp/pixelgen/dev-desk.gif",
    save_all=True, append_images=frames[1:], duration=160, loop=0,
)

sheet = Image.new("RGB", (W * 4, H * 4))
for i, f in enumerate(frames):
    small = f.resize((W, H), Image.NEAREST)
    sheet.paste(small, ((i % 4) * W, (i // 4) * H))
sheet.resize((W * 4 * 3, H * 4 * 3), Image.NEAREST).save("/tmp/pixelgen/desk-sheet.png")
print("ok")
