import os
from src.ingestion.pdf_text import extract_text
from src.ingestion.pdf_tables import extract_tables
from src.ingestion.pdf_images_ocr import extract_ocr_from_images

def ingest_pdf(pdf_path: str):
    source_name = os.path.basename(pdf_path)

    all_docs = []
    all_docs.extend(extract_text(pdf_path))
    all_docs.extend(extract_tables(pdf_path))
    all_docs.extend(extract_ocr_from_images(pdf_path))

    for d in all_docs:
        d["source"] = source_name

    return all_docs
