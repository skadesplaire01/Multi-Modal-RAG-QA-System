# 📄 Multi-Modal RAG QA System (Qatar Test Document)

A **Multi-Modal Retrieval-Augmented Generation (RAG)** system that answers user questions from a complex PDF document (Qatar IMF report).  
The pipeline supports **text + tables + OCR (images/charts)** ingestion and provides **page-level citations** with retrieved evidence.

---

## ✅ Key Features

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

⚙️ Installation (Windows)
1️⃣ Install Python packages
python -m pip install -r requirements.txt

2️⃣ Install Tesseract OCR (for image OCR)

Install Tesseract and ensure this path exists:

C:\Program Files\Tesseract-OCR\tesseract.exe


If needed, update in:

src/ingestion/pdf_images_ocr.py

▶️ Run the Application

Start Streamlit app:

python -m streamlit run app.py


Then open:

http://localhost:8501

✅ First Time Setup

Click:
✅ Build / Rebuild Index
This will ingest the PDF, chunk it, embed it, and build the FAISS index.

After the index is built, you can ask unlimited questions.

💬 Example Questions
Text-based

What does the report say about inflation trends in Qatar?

What are the major risks highlighted in the report?

Table-based

What is the CPI inflation in 2022, 2023 and projected for 2024?

What are the values of Real GDP growth from 2021 to 2025?

Image/OCR-based

What does Figure 2 indicate about inflation and monetary policy? 

✅ Outputs

The system provides:

- Final answer (based on retrieved context)
- Sources (page numbers)
- Retrieved evidence chunks for transparency

