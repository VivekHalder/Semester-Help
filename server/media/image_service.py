from typing import Iterable, List
from pathlib import Path
from image_retriever import get_images_by_doc_and_pages as _raw_get_images

def _normalize_pages(pages: Iterable[int]) -> List[int]:
    try:
        unique = sorted({int(p) for p in pages})
    except Exception:
        unique = []
    return unique

def get_images_by_doc_and_pages(doc_filename: str, page_numbers: Iterable[int]) -> List[str]:
    if not doc_filename:
        return []
    name = Path(doc_filename).name  # avoid path traversal
    pages = _normalize_pages(page_numbers)
    if not pages:
        return []
    try:
        images = _raw_get_images(name, pages)
        return images or []
    except Exception:
        return []
