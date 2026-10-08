"""C案のSVGからWindows用のICOとPNGを作る(ADR0043)。

画像生成で検討した形をSVGで実装。縮小専用のSVGを32px以下で使用する。
使い方: python mozc/tools/package_origami_icons.py <出力フォルダ>
必要: skia-python、Pillow。インストール先や既存Mozcアイコンは変更しない。
"""
import argparse
from pathlib import Path

import skia
from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parents[2] / "docs/design/2026-10-kotori/source"
ICON_SIZES = (16, 20, 24, 32, 48, 64, 128, 256)
PNG_SIZES = ICON_SIZES + (512, 1024)


def render_icon(size):
    source = ASSETS / ("kotori-origami-v3-small.svg" if size <= 32
                       else "kotori-origami-v3.svg")
    dom = skia.SVGDOM.MakeFromStream(skia.MemoryStream(source.read_bytes()))
    if dom is None:
        raise ValueError(f"SVGを読み込めない: {source}")
    surface = skia.Surface(size * 4, size * 4)
    canvas = surface.getCanvas()
    canvas.clear(skia.ColorTRANSPARENT)
    canvas.scale(size * 4 / 1024, size * 4 / 1024)
    dom.render(canvas)
    pixels = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
    return Image.fromarray(pixels).resize((size, size), Image.Resampling.LANCZOS)


def package(out):
    out.mkdir(parents=True, exist_ok=True)
    images = {size: render_icon(size) for size in PNG_SIZES}
    for size, image in images.items():
        image.save(out / f"kotori-origami-v3-{size}.png")
    # 古いrc.exeのRC2176を避けるため、全フレームをBMP形式で格納する。
    images[256].save(out / "kotori-origami-v3.ico", format="ICO",
                     sizes=[(n, n) for n in ICON_SIZES],
                     append_images=[images[n] for n in ICON_SIZES if n != 256],
                     bitmap_format="bmp")
    preview = Image.new("RGB", (760, 380))
    draw = ImageDraw.Draw(preview)
    for row, (bg, fg) in enumerate((("#F4F5F8", "#333A4C"),
                                    ("#20232B", "#E8ECF7"))):
        y = row * 190
        draw.rectangle((0, y, 760, y + 190), fill=bg)
        x = 24
        for size in (128, 64, 48, 32, 24, 20, 16):
            image = images[size]
            preview.paste(image, (x, y + 32), image)
            draw.text((x, y + 166), f"{size}px", fill=fg)
            x += max(size, 36) + 24
    preview.save(out / "icon-sizes.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    package(parser.parse_args().out)