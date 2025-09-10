def rerank(cross_encoder, query: str, docs, top_n: int):
    pairs = [(query, d.page_content) for d in docs]
    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [d for d, _ in ranked[:top_n]]
