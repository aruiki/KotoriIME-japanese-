"""Published real-IME results, not a new benchmark. Requires Pillow and Windows fonts.

Run: python docs/images/gen_ime_comparison.py
Source: eval/imebench/README.md, measured 2026-10-01.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROWS = [("Kotori日本語入力", 88.4, "#ed653c"),
        ("Microsoft IME", 59.6, "#8190aa"),
        ("Google 日本語入力", 58.1, "#8190aa")]


def main():
    source = (ROOT / "eval/imebench/README.md").read_text(encoding="utf-8")
    for value in ("88.4%", "59.6%", "58.1%", "2026-10-01", "beta.8"):
        assert value in source, f"Published source changed: {value}"
    canvas = Image.new("RGB", (1760, 1020), "#f8f9fc")
    draw = ImageDraw.Draw(canvas)
    font_path = Path("C:/Windows/Fonts/YuGothM.ttc")
    bold_path = Path("C:/Windows/Fonts/YuGothB.ttc")

    def text(x, y, value, size=30, color="#242c5c", bold=False):
        font = ImageFont.truetype(str(bold_path if bold else font_path), size)
        draw.text((x, y), value, font=font, fill=color)

    text(72, 52, "同じ読みを、3つのIMEで実入力。", 62, bold=True)
    text(76, 147, "AJIMEE-Bench 198問 · Space 1回の第1候補の正解率", 32)
    left, width = 490, 1020
    for tick in range(0, 101, 20):
        x = left + width * tick / 100
        draw.line((x, 224, x, 602), fill="#dce1eb", width=2)
        text(x - 18, 614, str(tick), 25, "#5b6070")
    text(1540, 614, "%", 25, "#5b6070")
    for index, (name, value, color) in enumerate(ROWS):
        y = 244 + index * 122
        text(76, y + 15, name, 34, bold=index == 0)
        draw.rounded_rectangle((left, y, left + width * value / 100, y + 78), radius=10, fill=color)
        text(left + width * value / 100 + 22, y + 5, f"{value:.1f}%", 45, bold=True)
    text(76, 710, "+28.8ポイント", 57, "#c84623", True)
    text(925, 710, "+30.3ポイント", 57, "#c84623", True)
    text(76, 792, "Microsoft IMEとの差", 30)
    text(925, 792, "Google 日本語入力との差", 30)
    text(76, 876, "2026-10-01 / RTX 3060 / 全IMEで前の文なし", 28, "#5b6070")
    text(76, 925, "Kotori beta.8 (Unreal) / Windows 11 IME / Google 日本語入力 3.34.6260", 27, "#5b6070")
    canvas.save(HERE / "ime-comparison.png")


if __name__ == "__main__":
    main()
