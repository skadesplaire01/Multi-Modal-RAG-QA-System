import os
import time
import streamlit as st
import numpy as np
from tqdm import tqdm

from src.ingestion.ingest_pipeline import ingest_pdf
from src.processing.chunking import chunk_documents

from src.retrieval.embedder import Embedder
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import Retriever
from src.retrieval.reranker import Reranker

from src.llm.answer_generator import generate_answer_offline

PDF_PATH = "data/qatar_test_doc.pdf"
STORE_DIR = "vector_store"

# -------------------------
# Page Config + Styling
# -------------------------
st.set_page_config(page_title="Multi-Modal RAG QA", layout="wide")

st.markdown(
    """
    <style>
    /* App background */
     .stApp {
        background: linear-gradient(180deg, #f3f6ff 0%, #f7f7fb 60%, #ffffff 100%);
    }


    /* Make main container look like a card */
    section.main > div {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .big-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #6b7280;
        margin-top: 0px;
        font-size: 14px;
    }

    /* Chips */
    .chip {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 999px;
        border: 1px solid #e5e7eb;
        font-size: 12px;
        margin-right: 8px;
        margin-bottom: 8px;
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(6px);
    }

    /* Small card style */
    .soft-card {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 16px;
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(8px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Header
# -------------------------
st.markdown('<div class="big-title">📄 Multi-Modal RAG QA System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle"> A professional-grade document assistant. Ask questions grounded in your knowledge base with verifiable citations.</div>',
    unsafe_allow_html=True
)

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.title("⚙️ Settings")

top_k = st.sidebar.slider("Top-K Retrieval", 3, 10, 7)
use_rerank = st.sidebar.checkbox(" Use Reranker (Bonus)", value=True)

st.sidebar.markdown("---")

# Show system status
vs = VectorStore(store_dir=STORE_DIR)
index_ready = vs.exists()

st.sidebar.markdown("### 📌 System Status")
if index_ready:
    st.sidebar.success("Index Ready ✅")
else:
    st.sidebar.warning("Index Not Built ⚠️")

st.sidebar.markdown("---")

# Build / Rebuild Index Button
if st.sidebar.button("🚀 Build / Rebuild Index", use_container_width=True):
    if not os.path.exists(PDF_PATH):
        st.error("❌ PDF not found! Place it at: data/qatar_test_doc.pdf")
    else:
        start_time = time.time()

        st.info("📌 Step 1/3: Ingesting PDF (Text + Tables + OCR)...")
        docs = ingest_pdf(PDF_PATH)

        st.info("📌 Step 2/3: Chunking extracted content...")
        chunks = chunk_documents(docs, chunk_size=900, overlap=150)

        st.info("📌 Step 3/3: Embedding + Building FAISS Index...")
        embedder = Embedder()
        embeddings = []

        for c in tqdm(chunks, desc="Embedding chunks"):
            embeddings.append(embedder.embed(c["content"]))

        embeddings = np.array(embeddings).astype("float32")

        vs = VectorStore(store_dir=STORE_DIR)
        vs.build(embeddings, chunks)

        elapsed = time.time() - start_time
        st.success(f"✅ Index built successfully! Total chunks = {len(chunks)} | Time: {elapsed:.2f}s")
        st.rerun()

st.markdown("<div style='height:2px;background:linear-gradient(90deg,#c7d2fe,#e9d5ff,#fde68a);border-radius:999px;margin:10px 0;'></div>", unsafe_allow_html=True)
st.subheader("💬 Ask a Question")

st.markdown("Try these examples:")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Inflation trends", use_container_width=True):
        st.session_state["query"] = "What does the report say about inflation trends in Qatar?"

with c2:
    if st.button("GDP outlook", use_container_width=True):
        st.session_state["query"] = "What is Qatar’s growth outlook according to the report?"

with c3:
    if st.button("Major risks", use_container_width=True):
        st.session_state["query"] = "What are the major risks highlighted in the report?"

query = st.text_input(
    "Enter your question",
    key="query",
    placeholder="E.g., What is the inflation outlook in Qatar according to the report?"
)

ask_clicked = st.button("🔍 Ask", use_container_width=True)

# -------------------------
# Answer + Evidence
# -------------------------
if ask_clicked:
    vs = VectorStore(store_dir=STORE_DIR)
    if not vs.exists():
        st.warning("⚠️ Please build the index first from the sidebar.")
    elif not query.strip():
        st.warning("⚠️ Please type a question.")
    else:
        retriever = Retriever(store_dir=STORE_DIR)

        with st.spinner("🔍 Retrieving relevant context..."):
            retrieved = retriever.search(query, top_k=top_k)

        if use_rerank:
            with st.spinner("⭐ Reranking for better accuracy..."):
                reranker = Reranker()
                retrieved = reranker.rerank(query, retrieved, top_k=5)

        with st.spinner("🧠 Generating answer..."):
            answer = generate_answer_offline(query, retrieved)

        st.markdown("---")
        st.markdown("## ⭐ Answer")
        st.write(answer)

        # Sources chips
        pages = sorted(list(set([r["page"] for r in retrieved])))
        st.markdown("### 🔖 Sources")
        chips_html = "".join([f'<span class="chip">Page {p}</span>' for p in pages])
        st.markdown(chips_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 📌 Retrieved Evidence")
        st.caption("These are the chunks used to generate the answer (with citations).")

        for i, r in enumerate(retrieved, 1):
            score_val = r.get("rerank_score", r.get("score", 0.0))
            title = f"Result {i}  •  Page {r['page']}  •  Type: {r['type']}  •  Score: {score_val:.3f}"

            with st.expander(title, expanded=(i == 1)):
                st.write(r["content"])
