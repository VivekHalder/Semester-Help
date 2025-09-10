import tiktoken
_encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(_encoding.encode(text))

def pack_context(docs, max_tokens: int) -> str:
    out, total = [], 0
    for d in docs:
        n = count_tokens(d.page_content)
        if total + n > max_tokens: break
        out.append(d.page_content)
        total += n
    return "\n\n".join(out)
