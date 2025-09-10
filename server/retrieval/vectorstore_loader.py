from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from ..config.settings import settings

def load_vectorstore(subject: str, semester: str, year: str, embedding_model: HuggingFaceEmbeddings):
    path = Path(settings.vectorstores_base) / f"{subject}_{year}_{semester}"
    if not path.exists():
        raise FileNotFoundError(f"Vectorstore not found: {path}")
    return FAISS.load_local(
        path,
        embeddings=embedding_model,
        allow_dangerous_deserialization=settings.allow_dangerous_deser,
    )
