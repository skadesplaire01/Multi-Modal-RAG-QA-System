from src.processing.cleaning import clean_text

def chunk_text(text: str, chunk_size=900, overlap=150):
    text = clean_text(text)
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start < 0:
            start = 0

    return chunks

def chunk_documents(docs, chunk_size=900, overlap=150):
    chunked = []

    for d in docs:
        pieces = chunk_text(d["content"], chunk_size=chunk_size, overlap=overlap)
        for i, p in enumerate(pieces):
            chunked.append({
                "chunk_id": f'{d["source"]}_p{d["page"]}_{d["type"]}_{i}',
                "content": p,
                "page": d["page"],
                "type": d["type"],
                "source": d["source"]
            })

    return chunked
