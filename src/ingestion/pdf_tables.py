import pdfplumber

def extract_tables(pdf_path: str):
    docs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            try:
                tables = page.extract_tables()
            except:
                tables = []

            if not tables:
                continue

            for t_idx, table in enumerate(tables):
                if not table:
                    continue

                lines = []
                for row in table:
                    row_clean = [str(cell).strip() if cell else "" for cell in row]
                    lines.append(" | ".join(row_clean))

                table_text = "\n".join(lines).strip()

                if table_text and len(table_text) > 20:
                    docs.append({
                        "content": f"[TABLE {t_idx+1}]\n{table_text}",
                        "page": page_index + 1,
                        "type": "table"
                    })

    return docs
