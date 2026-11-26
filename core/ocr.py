import os
import shutil

import pytesseract
from PIL import Image, ImageOps, ImageStat

_WINDOWS_PATH = r"E:\Tesseract-OCR\tesseract.exe"
if os.path.exists(_WINDOWS_PATH):
    pytesseract.pytesseract.tesseract_cmd = _WINDOWS_PATH
else:
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract") or "tesseract"


def _prepare(img):
    img = ImageOps.exif_transpose(img).convert("L")
    if ImageStat.Stat(img).mean[0] < 128:
        img = ImageOps.invert(img)
    img = ImageOps.autocontrast(img)
    if img.width < 1000:
        scale = 1000 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    return ImageOps.expand(img, border=30, fill=255)


def image_to_text(file):
    img = _prepare(Image.open(file))
    return pytesseract.image_to_string(img, lang="eng", config="--psm 6").strip()