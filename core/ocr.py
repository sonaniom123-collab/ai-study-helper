import os
import shutil

import pytesseract
from PIL import Image, ImageFilter, ImageOps, ImageStat

_WINDOWS_PATH = r"E:\Tesseract-OCR\tesseract.exe"
if os.path.exists(_WINDOWS_PATH):
    pytesseract.pytesseract.tesseract_cmd = _WINDOWS_PATH
else:
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract") or "tesseract"


def _clean(img):
    img = ImageOps.exif_transpose(img).convert("L")
    if ImageStat.Stat(img).mean[0] < 128:
        img = ImageOps.invert(img)
    return ImageOps.autocontrast(img)


def _widths(width):
    if width < 1000:
        return (1000, 700, 1200, 2400)
    return tuple(dict.fromkeys((min(width, 2400), 1600, 1000)))


def _resize(img, width):
    height = max(1, int(img.height * width / img.width))
    return img.resize((width, height), Image.LANCZOS)


def _variants(base):
    for width in _widths(base.width):
        sized = _resize(base, width)
        radius = max(1.0, width / 500)
        blurred = sized.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: 255 if v > 150 else 0)
        yield ImageOps.expand(blurred, border=40, fill=255)
        yield ImageOps.expand(sized, border=40, fill=255)


def candidate_texts(file):
    """Yield different readings of the photo, best guesses first."""
    base = _clean(Image.open(file))
    seen = set()
    for image in _variants(base):
        text = pytesseract.image_to_string(image, lang="eng", config="--psm 6").strip()
        if text and text not in seen:
            seen.add(text)
            yield text


def image_to_text(file):
    for text in candidate_texts(file):
        return text
    return ""