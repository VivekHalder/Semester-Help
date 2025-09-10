from typing import List
from memory_handler import get_memory
from ..utils.token import count_tokens

def _history_to_str(history) -> str:
    return "\n".join(f"{m.type.upper()}: {m.content}" for m in history)

def _trim_history_by_tokens(history, max_tokens: int) -> str:
    s = _history_to_str(history)
    if count_tokens(s) <= max_tokens:
        return s
    # take the shortest suffix that fits
    lo, hi = 0, len(history)
    best = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        tail = history[-mid:] if mid else []
        s_tail = _history_to_str(tail)
        if count_tokens(s_tail) <= max_tokens:
            best = s_tail
            lo = mid + 1
        else:
            hi = mid - 1
    return best

def get_chat_history(username: str, session_id: str, year: str, semester: str, subject: str, max_tokens: int = 400) -> str:
    mem = get_memory(username, session_id, year, semester, subject)
    hist: List = mem.load_memory_variables({}).get("history", []) or []
    return _trim_history_by_tokens(hist, max_tokens)

def append_user_message(username: str, session_id: str, year: str, semester: str, subject: str, text: str) -> None:
    mem = get_memory(username, session_id, year, semester, subject)
    mem.chat_memory.add_user_message(text)

def append_ai_message(username: str, session_id: str, year: str, semester: str, subject: str, text: str) -> None:
    mem = get_memory(username, session_id, year, semester, subject)
    mem.chat_memory.add_ai_message(text)
