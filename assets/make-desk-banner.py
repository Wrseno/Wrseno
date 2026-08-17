"""Pixel-art banner: dev coding at a cozy desk at night. Outputs GIF."""
from PIL import Image

W, H = 128, 48
SCALE = 6
GROUND = 44
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

# sitting, facing right: straight back, thigh level with the seat,
# shin down to the floor, one arm reaching the keyboard
DEV = """
......hhhhh.........
.....hhhhhhh........
.....hhhhhff........
.....hhHffff........
.....hhhffef........
......hhffff........
.......ffff.........
.......CCC..........
......CCCCC.........
.....CCCCCCC........
.....CCDCCCC........
.....CCCCCCCC.......
.....CCCCC.CCCC.....
.....CCCCC..........
.....CCCCC..........
.....CCCCC..........
.....CCCCC..........
.....CCCCC..........
.....CCCCCC.........
.....CCCCCCCCC......
......CCCCCCCCC.....
..........CCCC......
...........CCC......
...........CCC......
...........CCC......
...........CCC......
...........CCC......
..........bbbb......
"""

DEV_OX, DEV_OY = 24, 16


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
    # window fills the left edge, moon + twinkling stars
    rect(img, 1, 2, 21, 26, (10, 10, 20))
    for x in range(1, 22):
        put(img, x, 2, (52, 48, 80)); put(img, x, 26, (52, 48, 80))
    for y in range(2, 27):
        put(img, 1, y, (52, 48, 80)); put(img, 21, y, (52, 48, 80))
        put(img, 11, y, (52, 48, 80))
    rect(img, 14, 6, 18, 10, PAL["m"])                   # moon
    for cx, cy in ((14, 6), (18, 6), (14, 10), (18, 10)):
        put(img, cx, cy, (10, 10, 20))
    rect(img, 15, 7, 16, 8, (200, 196, 170))
    for i in range(7):                                   # stars
        x = 3 + rng(i, 1) % 17
        y = 5 + rng(i, 2) % 18
        if x != 11 and not (13 <= x <= 19 and 5 <= y <= 11):
            on = (i + frame // 2) % 3 != 0
            put(img, x, y, (170, 170, 200) if on else (70, 70, 100))
    # shelf with books, runs to the right edge
    rect(img, 100, 9, 127, 10, (60, 52, 44))
    for i, col in enumerate(("p", "c", "y", "g", "p", "c")):
        rect(img, 102 + i * 4, 3, 104 + i * 4, 8, PAL[col])


def desk_scene(img, frame):
    # desk bleeds off the right edge
    rect(img, 40, 30, 127, 31, PAL["W"])
    rect(img, 40, 32, 127, 32, PAL["w"])
    rect(img, 42, 33, 43, GROUND - 1, PAL["w"])
    rect(img, 120, 33, 121, GROUND - 1, PAL["w"])
    # monitor: stand, base, frame, screen
    rect(img, 86, 27, 89, 29, PAL["k"])
    rect(img, 78, 28, 97, 29, PAL["k"])
    rect(img, 62, 3, 113, 26, PAL["k"])
    rect(img, 64, 5, 111, 24, PAL["s"])
    # typed code lines, progress loops over N frames
    lines = [(1, 16, "p"), (3, 22, "c"), (3, 12, "g"), (5, 18, "y"),
             (3, 15, "c"), (1, 20, "g"), (3, 10, "p")]
    total = sum(ln for _, ln, _ in lines)
    prog = (frame + 1) * (total // (N - 2) + 1)
    sy = 7
    for li, (indent, ln, col) in enumerate(lines):
        take = max(0, min(ln, prog))
        prog -= ln
        if take:
            rect(img, 66 + indent, sy + li * 2, 66 + indent + take - 1,
                 sy + li * 2, PAL[col])
    # cursor blink on the active line
    if frame % 2 == 0:
        put(img, 66 + 1, sy + min(6, max(0, (frame * 7) // N)) * 2 + 1,
            (220, 220, 230))
    # screen glow specks on the wall
    for i in range(6):
        x = 58 + rng(i, frame, 3) % 60
        y = 2 + rng(i, frame, 4) % 26
        if not (62 <= x <= 113 and 3 <= y <= 26):
            put(img, x, y, (50, 46, 84))
    # keyboard
    rect(img, 45, 29, 58, 29, PAL["k"])
    # mug with steam, right of the monitor
    rect(img, 123, 27, 126, 29, PAL["u"])
    put(img, 127, 28, PAL["u"])
    for k in range(3):
        sx = 124 + (rng(k, frame // 2, 7) % 3) - 1
        put(img, sx, 24 - k * 2 - (frame % 2), PAL["S"])


def dev(img, frame):
    # chair behind the body: backrest, seat, legs
    rect(img, 26, 22, 27, 37, PAL["k"])
    rect(img, 26, 38, 40, 39, PAL["k"])
    rect(img, 28, 40, 29, GROUND - 1, PAL["k"])
    rect(img, 37, 40, 38, GROUND - 1, PAL["k"])
    blit(img, DEV, DEV_OX, DEV_OY)
    # forearm + typing hand bobbing over the keyboard
    hy = 28 if frame % 2 else 29
    rect(img, DEV_OX + 15, hy, DEV_OX + 18, hy, PAL["C"])
    put(img, DEV_OX + 19, hy, PAL["f"])
    put(img, DEV_OX + 20, hy, PAL["f"])
    put(img, DEV_OX + 21, hy, PAL["f"])
    # face lit by the screen
    put(img, DEV_OX + 11, DEV_OY + 4, (255, 226, 190))


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
