import fitz  # PyMuPDF

def extract_text(pdf_path: str):
    docs = []
    pdf = fitz.open(pdf_path)

    for i in range(len(pdf)):
        page = pdf[i]
        text = page.get_text("text").strip()

        if text:
            docs.append({
                "content": text,
                "page": i + 1,
                "type": "text"
            })

    return docs
