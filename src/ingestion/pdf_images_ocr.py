import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

# ✅ Update if your tesseract is installed in different path
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_ocr_from_images(pdf_path: str, max_images_per_page=3):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    docs = []
    pdf = fitz.open(pdf_path)

    for page_index in range(len(pdf)):
        page = pdf[page_index]

        images = page.get_images(full=True)
        if not images:
            continue

        images = images[:max_images_per_page]  # speed control

        for img_i, img in enumerate(images):
            try:
                xref = img[0]
                base = pdf.extract_image(xref)
                image_bytes = base["image"]

                pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                ocr_text = pytesseract.image_to_string(pil_img).strip()

                if ocr_text and len(ocr_text) > 30:
                    docs.append({
                        "content": f"[OCR IMAGE {img_i+1}]\n{ocr_text}",
                        "page": page_index + 1,
                        "type": "ocr"
                    })
            except:
                continue

    return docs
