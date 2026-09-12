import os

import pytesseract
from pypdf import PdfReader
from pdf2image import convert_from_path


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

# Windows: use your installed Tesseract path.
# Linux/cloud: leave TESSERACT_PATH unset and use the system
# tesseract command.
TESSERACT_PATH = os.getenv(
    "TESSERACT_PATH",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ============================================================
# POPPLER CONFIGURATION
# ============================================================

# Windows: your current Poppler installation.
# Linux/cloud: leave POPPLER_PATH unset so pdf2image uses
# the system installation.
POPPLER_PATH = os.getenv(
    "POPPLER_PATH",
    r"C:\Users\shivam\AppData\Local\Microsoft\WinGet\Packages"
    r"\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\poppler-25.07.0\Library\bin"
)

if not os.path.exists(POPPLER_PATH):
    POPPLER_PATH = None


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    # --------------------------------------------------------
    # 1. Try normal PDF text extraction
    # --------------------------------------------------------
    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print("PDF TEXT EXTRACTION ERROR:", e)

    text = text.strip()

    # --------------------------------------------------------
    # 2. If normal extraction fails, use OCR
    # --------------------------------------------------------
    if len(text) < 50:

        try:
            print("Normal extraction failed. Starting OCR...")

            if POPPLER_PATH:
                images = convert_from_path(
                    file_path,
                    dpi=200,
                    poppler_path=POPPLER_PATH
                )
            else:
                images = convert_from_path(
                    file_path,
                    dpi=200
                )

            print("PDF pages converted:", len(images))

            ocr_text = ""

            for image in images:

                page_text = pytesseract.image_to_string(image)

                if page_text:
                    ocr_text += page_text + "\n"

            text = ocr_text.strip()

            print(
                "OCR extracted characters:",
                len(text)
            )

        except Exception as e:
            print("OCR ERROR:", e)
            return ""

    return text