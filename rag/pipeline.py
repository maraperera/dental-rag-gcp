import time
from google import genai
from config.settings import settings
from rag.prompts import (
    GUARDRAIL_CLASSIFIER_PROMPT,
    REJECTION_MESSAGE,
    INTENT_ROUTER_PROMPT,
    SYNTHESIS_PROMPT
)
from rag.sql_agent import generate_and_execute_sql

ai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_with_retry(prompt: str, max_retries: int = 3, delay: float = 2.0):
    for attempt in range(max_retries):
        try:
            return ai_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )
        except Exception as e:
            err_str = str(e)
            if ("503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str) and attempt < max_retries - 1:
                sleep_time = delay * (2 ** attempt)
                print(f"[Model busy, retrying in {sleep_time:.1f}s...]")
                time.sleep(sleep_time)
            else:
                raise e

def is_domain_allowed(query: str) -> bool:
    """Evaluates whether the question is within the dental clinic scope."""
    response = generate_with_retry(GUARDRAIL_CLASSIFIER_PROMPT.format(query=query))
    verdict = response.text.strip().upper()
    return "ALLOWED" in verdict

def route_query(query: str) -> str:
    response = generate_with_retry(INTENT_ROUTER_PROMPT.format(query=query))
    decision = response.text.strip().upper()
    return "SEMANTIC" if "SEMANTIC" in decision else "SQL"

def run_dental_rag(query: str) -> dict:
    # 1. Guardrail Check
    if not is_domain_allowed(query):
        return {
            "answer": REJECTION_MESSAGE,
            "metadata": {"type": "GUARDRAIL_BLOCKED", "sql": "N/A"},
            "raw_records": []
        }

    # 2. Query Routing & Execution
    intent = route_query(query)
    execution = generate_and_execute_sql(query)
    context_data = execution["results"]
    metadata = {"type": intent, "sql": execution["generated_sql"]}

    # 3. Response Synthesis
    synthesis_response = generate_with_retry(
        SYNTHESIS_PROMPT.format(context=str(context_data), query=query)
    )

    return {
        "answer": synthesis_response.text,
        "metadata": metadata,
        "raw_records": context_data
    }