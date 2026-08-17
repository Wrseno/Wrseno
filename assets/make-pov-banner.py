"""Pixel-art banner: dev at their desk, seen from behind. Outputs GIF."""
from PIL import Image

W, H = 128, 48
SCALE = 6
N = 16

PAL = {
    "h": (16, 16, 26),     # hair
    "H": (40, 38, 66),     # hair highlight
    "f": (232, 201, 168),  # skin
    "C": (27, 27, 46),     # sweater dark
    "D": (44, 44, 74),     # sweater highlight
    "k": (34, 32, 54),     # chair / bezel / keyboard
    "K": (52, 50, 82),     # headphone band
    "s": (18, 20, 34),     # screen background
    "g": (120, 220, 160),  # code green
    "p": (139, 92, 246),   # code purple
    "c": (110, 190, 240),  # code cyan
    "y": (240, 200, 120),  # code yellow
    "m": (230, 226, 200),  # moon
    "u": (196, 120, 130),  # mug
    "S": (200, 200, 210),  # steam
    "G": (90, 160, 110),   # plant leaves
    "t": (140, 90, 70),    # plant pot
}

DESK_Y = 34


def rng(*seed):
    v = 2166136261
    for s in seed:
        v = (v ^ (s + 11)) * 16777619 % (2**32)
    return v


def put(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), color)


def rect(img, x0, y0, x1, y1, color):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(img, x, y, color)


def background(img, frame):
    rect(img, 0, 0, W - 1, H - 1, (13, 12, 22))
    # window on the left edge, moon + twinkling stars
    rect(img, 1, 2, 21, 26, (10, 10, 20))
    for x in range(1, 22):
        put(img, x, 2, (52, 48, 80)); put(img, x, 26, (52, 48, 80))
    for y in range(2, 27):
        put(img, 1, y, (52, 48, 80)); put(img, 21, y, (52, 48, 80))
        put(img, 11, y, (52, 48, 80))
    rect(img, 14, 6, 18, 10, PAL["m"])
    for cx, cy in ((14, 6), (18, 6), (14, 10), (18, 10)):
        put(img, cx, cy, (10, 10, 20))
    rect(img, 15, 7, 16, 8, (200, 196, 170))
    for i in range(7):
        x = 3 + rng(i, 1) % 17
        y = 5 + rng(i, 2) % 18
        if x != 11 and not (13 <= x <= 19 and 5 <= y <= 11):
            on = (i + frame // 2) % 3 != 0
            put(img, x, y, (170, 170, 200) if on else (70, 70, 100))
    # shelf with books, out to the right edge
    rect(img, 103, 9, 127, 10, (60, 52, 44))
    for i, col in enumerate(("p", "c", "y", "g", "p")):
        rect(img, 105 + i * 4, 3, 107 + i * 4, 8, PAL[col])


def desk(img, frame):
    rect(img, 0, DESK_Y, W - 1, DESK_Y + 1, (94, 78, 62))
    rect(img, 0, DESK_Y + 2, W - 1, DESK_Y + 2, (60, 52, 44))
    rect(img, 0, DESK_Y + 3, W - 1, H - 1, (20, 18, 32))  # under-desk shadow
    # monitor facing the camera
    rect(img, 34, 3, 93, 31, PAL["k"])
    rect(img, 36, 5, 91, 29, PAL["s"])
    # code lines type over the loop
    lines = [(1, 26, "p"), (4, 38, "c"), (4, 20, "g"), (7, 30, "y"),
        (4, 24, "c"), (1, 34, "g"), (4, 18, "p"), (1, 28, "c")]
    total = sum(ln for _, ln, _ in lines)
    prog = (frame + 1) * (total // (N - 2) + 1)
    sy = 7
    for li, (indent, ln, col) in enumerate(lines):
        take = max(0, min(ln, prog))
        prog -= ln
        if take:
            rect(img, 38 + indent, sy + li * 3, 38 + indent + take - 1,
                 sy + li * 3, PAL[col])
    if frame % 2 == 0:  # cursor blink
        put(img, 39, sy + min(7, max(0, (frame * 8) // N)) * 3 + 1,
            (220, 220, 230))
    # glow specks on the wall around the monitor
    for i in range(6):
        x = 28 + rng(i, frame, 3) % 72
        y = 2 + rng(i, frame, 4) % 30
        if not (34 <= x <= 93 and 3 <= y <= 31):
            put(img, x, y, (50, 46, 84))
    # plant on the left of the desk
    rect(img, 25, 31, 29, 33, PAL["t"])
    for dx, dy in ((0, -1), (-1, -2), (1, -3), (2, -2), (-2, -3), (0, -4)):
        put(img, 27 + dx, 31 + dy, PAL["G"])
    # mug with steam on the right
    rect(img, 100, 30, 103, 33, PAL["u"])
    put(img, 104, 31, PAL["u"])
    for k in range(3):
        sx = 101 + (rng(k, frame // 2, 7) % 3) - 1
        put(img, sx, 27 - k * 2 - (frame % 2), PAL["S"])
    # keyboard strip, mostly hidden behind the dev
    rect(img, 42, DESK_Y - 1, 86, DESK_Y - 1, PAL["k"])


def dev(img, frame):
    sway = (0, 0, 0, 1, 1, 1, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0)[frame % 16]
    ox = 64 + sway  # center of the dev
    # hair, seen from behind
    rect(img, ox - 6, 13, ox + 5, 22, PAL["h"])
    rect(img, ox - 5, 12, ox + 4, 12, PAL["h"])
    put(img, ox - 4, 14, PAL["H"]); put(img, ox - 4, 15, PAL["H"])
    put(img, ox - 6, 13, (13, 12, 22)); put(img, ox + 5, 13, (13, 12, 22))
    # headphones: band over the hair, cups on both sides
    rect(img, ox - 5, 11, ox + 4, 11, PAL["K"])
    put(img, ox - 6, 12, PAL["K"]); put(img, ox + 5, 12, PAL["K"])
    rect(img, ox - 8, 16, ox - 7, 20, PAL["K"])
    rect(img, ox + 6, 16, ox + 7, 20, PAL["K"])
    put(img, ox - 7, 17, PAL["p"]); put(img, ox + 6, 17, PAL["p"])
    # neck and shoulders widening into the torso
    rect(img, ox - 1, 23, ox + 1, 24, PAL["f"])
    rect(img, ox - 8, 25, ox + 7, 26, PAL["C"])
    rect(img, ox - 11, 27, ox + 10, 40, PAL["C"])
    rect(img, ox - 9, 27, ox + 8, 27, PAL["D"])
    # arms down to the desk, hands typing alternately
    rect(img, ox - 13, 28, ox - 12, 32, PAL["C"])
    rect(img, ox + 11, 28, ox + 12, 32, PAL["C"])
    lh = DESK_Y - 1 - (frame % 2)
    rh = DESK_Y - 1 - ((frame + 1) % 2)
    rect(img, ox - 14, lh, ox - 12, lh, PAL["f"])
    rect(img, ox + 11, rh, ox + 13, rh, PAL["f"])
    # chair backrest in front of the camera, bleeding off the bottom
    rect(img, ox - 9, 41, ox + 8, H - 1, PAL["k"])
    rect(img, ox - 7, 40, ox + 6, 40, PAL["k"])
    rect(img, ox - 5, 39, ox + 4, 39, PAL["K"])


frames = []
for i in range(N):
    img = Image.new("RGB", (W, H))
    background(img, i)
    desk(img, i)
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
sheet.resize((W * 4 * 3, H * 4 * 3), Image.NEAREST).save("/tmp/pixelgen/pov-sheet.png")
print("ok")
