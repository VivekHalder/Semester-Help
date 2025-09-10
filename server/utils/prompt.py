BRIEF = """You are an expert... (brief template) ... FINAL ANSWER:"""
DETAILED = """You are an expert... (detailed template) ... FINAL ANSWER:"""

def select_prompt(question: str) -> tuple[str, bool]:
    q = question.lower()
    brief = any(w in q for w in ["brief","short","summarize","quick","concise","overview","gist"])
    return (BRIEF if brief else DETAILED, brief)
