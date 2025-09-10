from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_model: str = "gpt-4o-mini"
    openai_temp: float = 0.5
    default_max_context_tokens: int = 800
    default_max_output_tokens: int = 500
    brief_max_context_tokens: int = 600
    brief_max_output_tokens: int = 300
    detailed_max_context_tokens: int = 1000
    detailed_max_output_tokens: int = 600
    k_initial: int = 10
    top_after_rerank: int = 5
    vectorstores_base: str = "vectorstores"
    allow_dangerous_deser: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
