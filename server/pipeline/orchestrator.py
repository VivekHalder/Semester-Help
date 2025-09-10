from ..memory.memory_service import get_chat_history, append_user_message, append_ai_message
from ..retrieval.vectorstore_loader import load_vectorstore
from ..retrieval.retriever import retrieve
from ..retrieval.reranker import rerank
from ..pipeline.query_optimizer import optimize_query
from ..media.image_service import get_images_by_doc_and_pages
from ..config.settings import settings

def get_chat_response(username: str, question: str, session_id: str, year: str, semester: str, subject: str,
                      embedding_model, cross_encoder, build_and_run_fn):
    chat_history_str = get_chat_history(username, session_id, year, semester, subject, max_tokens=400)

    optimized_query = optimize_query(question, chat_history_str)

    vectorstore = load_vectorstore(subject, semester, year, embedding_model)
    initial_docs = retrieve(vectorstore, optimized_query, k=settings.k_initial)
    if not initial_docs:
        append_user_message(username, session_id, year, semester, subject, question)
        append_ai_message(username, session_id, year, semester, subject, "I don't know based on the given context.")
        return {"answer": "I don't know based on the given context.", "images": []}

    top_docs = rerank(cross_encoder, optimized_query, initial_docs, settings.top_after_rerank)

    response = build_and_run_fn(chat_history_str, top_docs, optimized_query)

    append_user_message(username, session_id, year, semester, subject, question)
    append_ai_message(username, session_id, year, semester, subject, response)

    try:
        doc_filename = top_docs[0].metadata.get("source", "")
        page_numbers = [d.metadata["page"] for d in top_docs if "page" in d.metadata]
        images = get_images_by_doc_and_pages(doc_filename, page_numbers) if doc_filename else []
    except Exception:
        images = []

    return {"answer": response, "images": images}
