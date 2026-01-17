import json
import time
from src.retrieval.retriever import Retriever
from src.llm.answer_generator import generate_answer_offline

def run_eval(store_dir="vector_store", top_k=7):
    retriever = Retriever(store_dir=store_dir)

    with open("src/evaluation/eval_questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    print("\n✅ Running Evaluation...\n")

    for q in questions:
        start = time.time()
        retrieved = retriever.search(q["question"], top_k=top_k)
        answer = generate_answer_offline(q["question"], retrieved)
        latency = time.time() - start

        pages = sorted(list(set([r["page"] for r in retrieved])))
        print(f"Q{q['id']}: {q['question']}")
        print(f"Latency: {latency:.2f}s | Pages: {pages}")
        print(f"Answer Preview: {answer[:180]}...\n")

if __name__ == "__main__":
    run_eval()
