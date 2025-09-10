from langchain_openai import ChatOpenAI

def make_llm(model: str, temperature: float, max_tokens: int, api_key: str | None):
    return ChatOpenAI(model=model, temperature=temperature, max_tokens=max_tokens, openai_api_key=api_key)
