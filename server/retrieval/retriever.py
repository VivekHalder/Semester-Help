def retrieve(vectorstore, query: str, k: int):
    return vectorstore.similarity_search(query, k=k)
