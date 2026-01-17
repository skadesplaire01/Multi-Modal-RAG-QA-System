# 📄 Multi-Modal RAG QA System (Qatar Test Document)

A **Multi-Modal Retrieval-Augmented Generation (RAG)** system that answers user questions from a complex PDF document (Qatar IMF report).  
The pipeline supports **text + tables + OCR (images/charts)** ingestion and provides **page-level citations** with retrieved evidence.

---
## Live Demo - https://multi-modal-rag-app-system-fciqs3fypnankzbhsjn3nj.streamlit.app/

## Key Features

- ✅ **Multi-modal ingestion**
  - Text extraction from PDF pages
  - Table extraction and conversion to readable text
  - OCR extraction from images inside PDF using Tesseract
- ✅ **Chunking strategy** for better retrieval
- ✅ **Vector search using FAISS**
- ✅ **Top-K retrieval** to fetch relevant chunks
- ✅ **Reranker (Bonus)** using CrossEncoder for higher relevance
- ✅ **Streamlit UI** for interactive QA
- ✅ **Source attribution** (page citations + retrieved evidence)
- ✅ **Evaluation suite** with benchmark queries

---

## 📁 Project Structure

```text
multi_modal_rag_qatar/
│
├── data/
│   └── qatar_test_doc.pdf
│
├── src/
│   ├── ingestion/
│   │   ├── pdf_text.py
│   │   ├── pdf_tables.py
│   │   ├── pdf_images_ocr.py
│   │   └── ingest_pipeline.py
│   │
│   ├── processing/
│   │   ├── cleaning.py
│   │   └── chunking.py
│   │
│   ├── retrieval/
│   │   ├── embedder.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── hybrid_rrf.py
│   │
│   ├── llm/
│   │   └── answer_generator.py
│   │
│   ├── evaluation/
│   │   ├── eval_questions.json
│   │   └── run_eval.py
│   │
│   └── utils/
│       └── logger.py
│
├── app.py
├── requirements.txt
└── README.md

```

## ⚙️ Installation (Windows)

#### 1️⃣ Install Python packages
``` powershell
python -m pip install -r requirements.txt.
```

#### 2️⃣ Install Tesseract OCR (for OCR support)
```powershell
Make sure **Tesseract OCR** is installed and this path exists: C:\Program Files\Tesseract-OCR\tesseract.exe
```

#### ▶️ Run the Application
```powershell
python -m streamlit run app.py
```
#### open in browser : http://localhost:8501
---
### 🚀 First Time Setup

Click: ✅ Build / Rebuild Index

This will:

→ Ingest PDF (text + tables + OCR)
→ Chunk extracted content
→ Create embeddings
→ Build the FAISS vector index
→ After indexing, you can ask unlimited questions without rebuilding.

## 💬 Example Questions
🔹 Text-based - 
What does the report say about inflation trends in Qatar?
What are the major risks highlighted in the report?

🔹 Table-based -
What is the CPI inflation in 2022, 2023 and projected for 2024?
What are the values of Real GDP growth from 2021 to 2025?

🔹 Image/OCR-based - 
What does Figure 2 indicate about inflation and monetary policy?

## Output Format
The system provides:

- Final answer (evidence-based)
- Source pages (citations)
- Retrieved evidence chunks for transparency

---













