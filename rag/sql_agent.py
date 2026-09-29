import re
import time
from google import genai
from langsmith import wrappers, traceable
from config.settings import settings
from rag.bq_client import execute_safe_query, get_table_schemas_context
from rag.prompts import SQL_GENERATION_PROMPT, SQL_FIX_PROMPT

raw_client = genai.Client(api_key=settings.GEMINI_API_KEY)
ai_client = wrappers.wrap_gemini(
    raw_client,
    tracing_extra={"tags": ["sql-agent", "bigquery"]}
)

schema_cache = None

def clean_sql(text: str) -> str:
    clean = text.strip()
    clean = re.sub(r"^```sql\s*", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"^```\s*", "", clean)
    clean = re.sub(r"```$", "", clean)
    return clean.strip()

@traceable(name="gemini_generate_with_retry")
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
                time.sleep(sleep_time)
            else:
                raise e

@traceable(name="generate_and_execute_sql", run_type="chain")
def generate_and_execute_sql(query: str) -> dict:
    global schema_cache
    if not schema_cache:
        schema_cache = get_table_schemas_context()

    prompt = SQL_GENERATION_PROMPT.format(
        project_id=settings.PROJECT_ID,
        dataset_id=settings.DATASET_ID,
        schema_context=schema_cache,
        query=query
    )

    response = generate_with_retry(prompt)
    raw_sql = clean_sql(response.text)

    try:
        rows = execute_safe_query(raw_sql)
    except Exception as err:
        fix_prompt = SQL_FIX_PROMPT.format(
            failed_sql=raw_sql,
            error_message=str(err),
            schema_context=schema_cache
        )
        fix_response = generate_with_retry(fix_prompt)
        raw_sql = clean_sql(fix_response.text)
        rows = execute_safe_query(raw_sql)

    return {
        "generated_sql": raw_sql,
        "results": rows
    }