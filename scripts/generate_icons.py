from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT / 'www'
ANDROID = ROOT / 'android' / 'app' / 'src' / 'main' / 'res'

BG_TOP = (255, 181, 76)
BG_BOTTOM = (255, 151, 15)
PANEL = (255, 247, 239)
LINE = (242, 210, 173)
OUT = (42, 33, 30)
WHITE = (255, 255, 255)
PINK = (255, 176, 167)
TONGUE = (255, 112, 112)
YELLOW = (255, 190, 74)


def gradient_bg(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for y in range(size):
        ratio = y / max(size - 1, 1)
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    return img


def make_icon(size, rounded=False):
    img = gradient_bg(size)
    draw = ImageDraw.Draw(img)

    radius = size // 5 if not rounded else size // 2
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), radius=radius, fill=255)
    img.putalpha(mask)

    pad = int(size * 0.15)
    draw.rounded_rectangle((pad, pad, size - pad, size - pad), radius=int(size * 0.12), fill=PANEL, outline=LINE, width=max(2, size // 64))

    face_box = (int(size*0.24), int(size*0.21), int(size*0.76), int(size*0.72))
    draw.rounded_rectangle(face_box, radius=int(size*0.16), fill=WHITE, outline=OUT, width=max(4, size // 32))
    bump_box = (int(size*0.27), int(size*0.15), int(size*0.42), int(size*0.28))
    draw.pieslice(bump_box, start=180, end=360, fill=WHITE, outline=OUT, width=max(4, size // 32))

    eye_w = size * 0.035
    eye_h = size * 0.05
    draw.ellipse((size*0.38-eye_w, size*0.43-eye_h, size*0.38+eye_w, size*0.43+eye_h), fill=OUT)
    draw.line((size*0.57, size*0.44, size*0.63, size*0.41), fill=OUT, width=max(4, size // 40))

    draw.arc((size*0.42, size*0.45, size*0.58, size*0.60), start=10, end=170, fill=OUT, width=max(4, size // 40))
    draw.line((size*0.45, size*0.52, size*0.55, size*0.52), fill=OUT, width=max(4, size // 40))
    draw.rounded_rectangle((size*0.49, size*0.52, size*0.55, size*0.60), radius=int(size*0.02), fill=TONGUE, outline=OUT, width=max(2, size // 64))

    draw.ellipse((size*0.27, size*0.50, size*0.36, size*0.57), fill=PINK)
    draw.ellipse((size*0.64, size*0.50, size*0.73, size*0.57), fill=PINK)
    draw.ellipse((size*0.21, size*0.57, size*0.31, size*0.67), fill=WHITE, outline=OUT, width=max(4, size // 40))
    draw.ellipse((size*0.69, size*0.57, size*0.79, size*0.67), fill=WHITE, outline=OUT, width=max(4, size // 40))
    draw.rounded_rectangle((size*0.71, size*0.18, size*0.75, size*0.29), radius=int(size*0.01), fill=YELLOW)
    draw.rounded_rectangle((size*0.79, size*0.20, size*0.83, size*0.28), radius=int(size*0.01), fill=YELLOW)

    return img


def save_web_icons():
    WWW.mkdir(parents=True, exist_ok=True)
    make_icon(192).save(WWW / 'icon-192.png')
    make_icon(512).save(WWW / 'icon-512.png')


def save_android_icons():
    sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }
    for folder, size in sizes.items():
        target = ANDROID / folder
        target.mkdir(parents=True, exist_ok=True)
        make_icon(size).save(target / 'ic_launcher.png')
        make_icon(size, rounded=True).save(target / 'ic_launcher_round.png')


if __name__ == '__main__':
    save_web_icons()
    save_android_icons()
    print('Generated web and Android icons.')
