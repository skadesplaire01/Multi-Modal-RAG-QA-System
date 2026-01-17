def rrf_fusion(dense_results, keyword_results, k=60, top_k=5):
    scores = {}

    def add_results(results, weight=1.0):
        for rank, item in enumerate(results):
            doc_id = item["chunk_id"]
            scores[doc_id] = scores.get(doc_id, 0) + weight * (1 / (k + rank + 1))

    add_results(dense_results, weight=1.0)
    add_results(keyword_results, weight=0.7)

    merged = {}
    for r in dense_results + keyword_results:
        merged[r["chunk_id"]] = r

    fused = list(merged.values())
    for r in fused:
        r["rrf_score"] = scores.get(r["chunk_id"], 0)

    fused.sort(key=lambda x: x["rrf_score"], reverse=True)
    return fused[:top_k]
