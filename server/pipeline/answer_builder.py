from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..utils.prompt import select_prompt
from ..utils.llm_factory import make_llm
from ..utils.token import pack_context
from ..config.settings import settings
import os

def decide_limits(question: str) -> tuple[int,int]:
    q = question.lower()
    if any(w in q for w in ["brief","short","summarize","quick","concise","overview","gist"]):
        return settings.brief_max_context_tokens, settings.brief_max_output_tokens
    if any(w in q for w in ["detailed","explain","elaborate","comprehensive","thorough","in-depth","complete","full"]):
        return settings.detailed_max_context_tokens, settings.detailed_max_output_tokens
    return settings.default_max_context_tokens, settings.default_max_output_tokens

def build_and_run(chat_history: str, docs, question: str):
    max_ctx, max_out = decide_limits(question)
    prompt_text, _ = select_prompt(question)
    prompt = PromptTemplate.from_template(prompt_text)

    llm = make_llm(
        model=settings.openai_model,
        temperature=settings.openai_temp,
        max_tokens=max_out,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    chain = prompt | llm | StrOutputParser()

    context = pack_context(docs, max_ctx)
    return chain.invoke({"chat_history": chat_history, "context": context, "question": question})
