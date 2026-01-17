def generate_answer_offline(query: str, results: list):
    if not results:
        return "I could not find relevant information in the document."

    pages = sorted(list(set([r["page"] for r in results])))
    preview = results[0]["content"][:900]

    answer = f"""
✅ **Question:** {query}

📌 **Answer (Evidence-based):**
{preview}...

**Sources :** Pages {", ".join(map(str, pages))}
""".strip()

    return answer
