from google.cloud import bigquery
from google.oauth2 import service_account
from config.settings import settings

def get_client() -> bigquery.Client:
    cred_file = settings.full_credentials_path
    if cred_file.exists():
        credentials = service_account.Credentials.from_service_account_file(str(cred_file))
        return bigquery.Client(project=settings.PROJECT_ID, credentials=credentials, location=settings.REGION)
    return bigquery.Client(project=settings.PROJECT_ID, location=settings.REGION)

bq_client = get_client()

def get_table_schemas_context() -> str:
    """Extracts column definitions and data types for the Text-to-SQL prompt context."""
    query = f"""
    SELECT table_name, column_name, data_type
    FROM `{settings.PROJECT_ID}.{settings.DATASET_ID}.INFORMATION_SCHEMA.COLUMNS`
    ORDER BY table_name, ordinal_position;
    """
    df = bq_client.query(query).to_dataframe()
    
    schema_str = ""
    for table_name, group in df.groupby("table_name"):
        cols = [f"{row['column_name']} ({row['data_type']})" for _, row in group.iterrows()]
        schema_str += f"Table `{table_name}`: {', '.join(cols)}\n"
    return schema_str

def execute_safe_query(sql: str, max_rows: int = 50) -> list[dict]:
    """Executes a validated read-only SQL query against BigQuery."""
    # Ensure query is read-only
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER"]
    if any(keyword in sql.upper().split() for keyword in forbidden):
        raise ValueError("Unsafe SQL detected: Only SELECT statements are permitted.")
    
    query_job = bq_client.query(sql)
    results = query_job.result(max_results=max_rows)
    return [dict(row) for row in results]