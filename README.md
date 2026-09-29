# Dental Clinic BigQuery Data Pipeline & RAG System

A scalable synthetic data pipeline, operational data warehouse, and Retrieval-Augmented Generation (RAG) assistant designed for **dental practice management and analytics**.

This platform provisions a relational data warehouse in **Google Cloud Platform (GCP) BigQuery**, loads **1.8M+ synthetic clinical, diagnostic, appointment, and billing records**, and provides a domain-restricted natural-language analytics assistant powered by **Gemini**, with real-time observability and distributed tracing powered by **LangSmith**.

The system combines:

* BigQuery relational analytics
* Gemini-powered Text-to-SQL
* LangSmith observability and distributed tracing
* Domain intent classification and guardrails
* SQL validation and automated self-healing loops
* Clinical semantic retrieval
* RAG-based response synthesis
* Synthetic healthcare data generation
* GCP service-account authentication

> **Important:** All patient and clinical data used by this project is synthetic and generated exclusively for development, testing, demonstration, and RAG evaluation purposes.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       User / CLI        │
                         │        app.py           │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     RAG Pipeline        │
                         │     pipeline.py         │
                         └────────────┬────────────┘
                                      │
                                      │
                         ┌────────────▼────────────┐
                         │    LangSmith Tracing    │
                         │                         │
                         │  • Spans & Latency      │
                         │  • Token Usage & Cost   │
                         │  • Inputs / Outputs     │
                         │  • Error Tracking       │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   Domain Guardrail      │
                         │   Intent Classification │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
                 ┌─────────────────┐      ┌──────────────────┐
                 │    SQL Route    │      │ Clinical Vector  │
                 │                 │      │ Search Route     │
                 └────────┬────────┘      └────────┬─────────┘
                          │                        │
                          ▼                        ▼
                 ┌─────────────────┐      ┌──────────────────┐
                 │ Gemini Text-to- │      │ BigQuery Vector  │
                 │ SQL Agent       │      │ Search           │
                 └────────┬────────┘      └────────┬─────────┘
                          │                        │
                          ▼                        │
                 ┌─────────────────┐               │
                 │ SQL Validation  │               │
                 │ & Repair Loop   │               │
                 └────────┬────────┘               │
                          │                        │
                          ▼                        ▼
                 ┌──────────────────────────────────────┐
                 │             BigQuery                 │
                 │                                      │
                 │  11 Relational Tables                │
                 │  1.8M+ Synthetic Records             │
                 │  Partitioning + Clustering           │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────────┐
                         │ Response Synthesis      │
                         │        Gemini           │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      Final Answer       │
                         └─────────────────────────┘
```

---

# ✨ Key Features

## 1. Relational BigQuery Data Warehouse

The system uses a structured **11-table relational schema** designed around dental clinic operations.

The warehouse contains synthetic data covering:

* Patients
* Dentists
* Staff
* Treatments
* Appointments
* Appointment treatments
* Medical history
* Dental records
* Prescriptions
* Invoices
* Payments

The generated dataset contains **1.8M+ records** distributed across these tables.

BigQuery is used as the central analytical data warehouse, supporting:

* Large-scale SQL analytics
* Multi-table joins
* Aggregations
* Filtering
* Date-based analysis
* Financial analysis
* Operational reporting
* Clinical data retrieval

---

# 🔎 2. Real-Time Observability & Monitoring with LangSmith

The application integrates **LangSmith** for end-to-end execution tracing and observability.

Every RAG request can be monitored through a hierarchical trace structure.

### Trace Hierarchy

A typical request follows this structure:

```text
dental_rag_pipeline
│
├── guardrail_check
│
├── intent_router
│
├── generate_and_execute_sql
│   │
│   ├── sql_generation
│   ├── bigquery_execution
│   └── sql_repair
│
└── response_synthesis
```

LangSmith provides visibility into:

### Trace Hierarchies

Every query is recorded under a parent `dental_rag_pipeline` run with child execution spans such as:

* `guardrail_check`
* `intent_router`
* `generate_and_execute_sql`
* SQL generation
* BigQuery execution
* SQL repair/retry
* Response synthesis

### Latency Monitoring

The system can measure the execution time of individual pipeline stages.

For example:

```text
User Query
    │
    ├── Guardrail Check       → ~1.3s
    │
    ├── Intent Classification
    │
    ├── SQL Generation
    │
    ├── BigQuery Execution
    │
    └── Response Synthesis   → ~6–12s total
```

Actual latency depends on model response time, BigQuery execution time, network conditions, query complexity, and retry behaviour.

### Token & Cost Monitoring

LangSmith can be used to monitor:

* Input token usage
* Output token usage
* Total token usage
* Model calls
* Execution latency
* API-related costs where supported by the configured model/provider

This makes it easier to identify expensive prompts, unnecessary model calls, and inefficient pipeline stages.

### Debugging

Each trace can be inspected to understand:

* User input
* Intent classification
* Generated SQL
* SQL validation results
* BigQuery execution results
* SQL repair attempts
* Model responses
* Final response synthesis

This significantly simplifies debugging of Text-to-SQL and RAG workflows.

---

# 🧭 3. Intent-Driven RAG Routing

The system analyzes each user question before deciding how information should be retrieved.

Queries are routed into one of three retrieval paths:

```text
User Question
      │
      ▼
Intent Classification
      │
      ├── SQL
      │     └──► BigQuery GoogleSQL
      │
      ├── Vector
      │     └──► Clinical Semantic Search
      │
      └── Hybrid
            ├──► BigQuery SQL
            └──► Clinical Vector Search
```

---

## SQL Queries

SQL routing is intended for structured analytical and operational questions involving:

* Counts
* Sums
* Averages
* Revenue
* Appointment volumes
* Treatment frequency
* Patient statistics
* Dentist performance metrics
* Invoice information
* Payment information
* Date-based analysis

### Example

> **"What is the total revenue generated by each dentist, and how many unique appointments did they complete?"**

The system can translate this question into GoogleSQL, execute it against BigQuery, and use the results to construct a natural-language response.

---

## Vector Queries

Vector routing is intended for semantic clinical questions involving information such as:

* Clinical notes
* Dental observations
* Symptoms
* Treatment descriptions
* Medical history
* Free-text patient records

### Example

> **"Find patients whose clinical notes mention sensitivity after a filling."**

The semantic retrieval layer can identify relevant clinical records based on meaning rather than requiring an exact keyword match.

---

## Hybrid Queries

Hybrid routing is intended for questions that require both:

1. Structured relational information
2. Semantic clinical information

For example:

> **"Find patients with sensitivity after fillings and show the number of follow-up appointments they attended."**

The system can combine:

```text
Clinical Semantic Search
          +
BigQuery SQL
          │
          ▼
Combined Context
          │
          ▼
Gemini Response Synthesis
```

---

# 🛡️ 4. Domain Guardrails

The application includes a domain guardrail that executes before downstream SQL generation or semantic retrieval.

The guardrail helps ensure that the application remains focused on the dental-clinic domain.

## Allowed Queries

Queries related to areas such as:

* Patients
* Dentists
* Appointments
* Treatments
* Clinical records
* Medical history
* Prescriptions
* Invoices
* Payments
* Clinic operations
* Dental analytics

are passed to the appropriate downstream pipeline.

## Blocked Queries

Unrelated questions can be rejected before database execution or additional model processing.

For example:

> **"How many moons does Jupiter have, and which one is the largest?"**

The application can return a standardized domain disclaimer instead of executing an unnecessary database query.

This reduces:

* Unnecessary BigQuery execution
* Model token consumption
* Irrelevant SQL generation
* Unnecessary downstream processing

---

# 🧠 5. Text-to-SQL Pipeline & Self-Healing

The SQL agent converts natural-language questions into BigQuery-compatible GoogleSQL.

```text
Natural Language Question
          │
          ▼
Schema Context + Prompt Constraints
          │
          ▼
Gemini SQL Generation
          │
          ▼
BigQuery Execution
          │
       ┌──┴──┐
       │     │
    Success Error
       │     │
       │     ▼
       │   SQL Error Analysis
       │     │
       │     ▼
       │   Gemini SQL Repair
       │     │
       │     ▼
       │   Re-execution
       │
       ▼
Results & Context
```

## SQL Generation

The SQL agent receives relevant schema information and prompt constraints before generating GoogleSQL.

The prompt can include:

* Table names
* Column names
* Relationships
* Data types
* Join requirements
* Query restrictions
* BigQuery-specific syntax guidance
* Alias restrictions

---

## SQL Validation

Generated SQL is executed against BigQuery.

If execution succeeds:

```text
Generated SQL
     │
     ▼
BigQuery
     │
     ▼
Successful Results
```

If execution fails:

```text
Generated SQL
     │
     ▼
BigQuery
     │
     ▼
SQL Error
     │
     ▼
Gemini Repair
     │
     ▼
Corrected SQL
     │
     ▼
BigQuery
```

The repair loop helps the system recover from common SQL-generation errors.

---

# ⚠️ Keyword Conflict Safeguards

BigQuery reserves certain keywords that should not be used casually as table aliases.

For example, `AT` has special meaning in BigQuery time-travel syntax.

Therefore, the SQL-generation prompts include explicit aliasing constraints.

Instead of:

```sql
JOIN appointment_treatments AS at
```

the system can instruct Gemini to use:

```sql
JOIN appointment_treatments AS apt_treat
```

This reduces the probability of SQL parsing errors caused by reserved keywords.

---

# 🗄️ BigQuery Database Schema

The warehouse contains **11 core relational tables**.

| #  | Table                    | Description                                                  |
| -- | ------------------------ | ------------------------------------------------------------ |
| 1  | `patients`               | Synthetic patient demographic and registration details       |
| 2  | `dentists`               | Provider names, specializations, and license identifiers     |
| 3  | `staff`                  | Clinic receptionists, assistants, and practice managers      |
| 4  | `treatments`             | ADA procedure codes, treatment categories, and standard fees |
| 5  | `appointments`           | Patient scheduling, visit status, and appointment types      |
| 6  | `appointment_treatments` | Association table mapping procedures to appointments         |
| 7  | `medical_history`        | Systemic patient conditions and recorded dates               |
| 8  | `dental_records`         | Tooth-level observations and free-text clinical notes        |
| 9  | `prescriptions`          | Medications, dosage, frequency, and instructions             |
| 10 | `invoices`               | Billing subtotal, tax, discounts, and invoice status         |
| 11 | `payments`               | Payment dates, payment methods, and transaction totals       |

---

# 🔗 Relational Model

The core relationships can be represented conceptually as:

```text
patients
   │
   ├───────────────┐
   │               │
   ▼               ▼
appointments   medical_history
   │
   ├───────────────┐
   │               │
   ▼               ▼
dental_records  prescriptions
   │
   │
   ▼
appointment_treatments
   │
   ▼
treatments


appointments
   │
   ▼
invoices
   │
   ▼
payments


dentists
   │
   ▼
appointments


staff
   │
   ▼
appointments
```

This relational structure enables analytical queries across clinical, operational, and financial domains.

---

# 📊 Synthetic Dataset

The project uses synthetic data to simulate a realistic dental practice environment.

The generated data covers:

| Domain        | Example Data                                          |
| ------------- | ----------------------------------------------------- |
| Patients      | Demographics, registration dates, contact information |
| Dentists      | Names, specialties, license information               |
| Appointments  | Dates, times, status, appointment type                |
| Treatments    | Procedure codes, categories, fees                     |
| Clinical      | Tooth observations, clinical notes                    |
| Medical       | Conditions and medical history                        |
| Prescriptions | Medication, dosage, frequency                         |
| Billing       | Invoices, discounts, tax, totals                      |
| Payments      | Payment method, date, amount                          |

The complete generated dataset contains **1.8M+ synthetic records**.

> No real patient information is required for the project.

---

# 📁 Project Structure

```text
dental-rag-gcp/
│
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration & credentials
│
├── data_generation/
│   ├── __init__.py
│   ├── catalog.py               # Dental procedural catalogs and note templates
│   └── generate_and_load.py     # Synthetic data generator and BigQuery loader
│
├── rag/
│   ├── __init__.py
│   ├── bq_client.py             # BigQuery execution client and schema introspection
│   ├── prompts.py               # Guardrail, routing, SQL and repair prompts
│   ├── sql_agent.py             # Text-to-SQL agent and SQL repair loop
│   ├── vector_search.py         # Clinical semantic/vector retrieval
│   ├── router.py                # SQL / Vector / Hybrid routing
│   └── pipeline.py              # End-to-end RAG orchestration and tracing
│
├── sql/
│   ├── schema.sql               # BigQuery DDL definitions
│   ├── truncate.sql             # Table reset scripts
│   └── embeddings.sql           # Embedding/vector-search SQL
│
├── app.py                       # Interactive CLI entrypoint
├── service_account.json         # GCP service-account key (Git-ignored)
├── .env                         # Local runtime environment variables
├── .env.example                 # Environment configuration template
├── .gitignore                   # Git ignore rules
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
```

---

# ⚙️ Prerequisites & Setup

## 1. Required Software

Before running the project, install:

* Python 3.10+
* Google Cloud project
* BigQuery
* Gemini API access
* LangSmith account/API key
* Git
* VS Code or another Python-compatible IDE

---

# 🐍 2. Create the Python Environment

Open PowerShell from the project directory.

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade `pip`:

```powershell
python -m pip install --upgrade pip
```

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# ☁️ 3. Google Cloud Platform Configuration

Create or use a Google Cloud project for the application.

Example:

```text
Project ID:
dental-clinic-rag
```

Enable the required services, including BigQuery and the APIs required by the selected Gemini integration.

The exact APIs required may vary depending on whether Gemini is accessed through the Gemini API, Vertex AI, or another supported integration.

---

# 🔐 4. Service Account Configuration

Create a GCP service account for the application.

The service account should have only the permissions required by the project.

For a development environment, the account generally requires permissions to:

* Access BigQuery datasets
* Create/query BigQuery tables where required
* Load data into BigQuery
* Run BigQuery jobs

Download the service-account JSON key and place it in the project root:

```text
dental-rag-gcp/
│
└── service_account.json
```

> **Security:** Never commit `service_account.json` to Git.

The `.gitignore` should contain:

```gitignore
service_account.json
.env
.venv/
__pycache__/
*.pyc
```

---

# 🔑 5. Environment Configuration

Create a `.env` file in the project root.

```env
# GCP & BigQuery Settings
GCP_PROJECT_ID=project_name
BIGQUERY_DATASET=database_name
GCP_REGION=australia-southeast2
GOOGLE_APPLICATION_CREDENTIALS=service_account.json

# Gemini AI Settings
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite

# LangSmith Observability
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=project_name
```

> **Important:** Do not commit `.env` or API keys to a public repository.

---

# 🧪 6. Environment Template

A `.env.example` file can be committed to the repository as a template.

```env
GCP_PROJECT_ID=your_gcp_project_id
BIGQUERY_DATASET=databse_name
GCP_REGION=australia-southeast2
GOOGLE_APPLICATION_CREDENTIALS=service_account.json

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=project_name
```

---

# 📦 7. Install Dependencies

Install all dependencies from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

To verify the LangSmith installation:

```powershell
python -m pip show langsmith
```

To verify the installed packages:

```powershell
python -m pip list
```

---

# 🗃️ 8. BigQuery Dataset

Create the BigQuery dataset configured in `.env`.

For example:

```text
Project:
dental-rag

Dataset:
dental_service

Region:
australia-southeast2
```

The project can then create/load the required tables into:

```text
dental-rag.dental_service
```

---

# 🏭 9. Seed the Warehouse

After configuring GCP credentials and environment variables, run the synthetic data-generation pipeline:

```powershell
python -m data_generation.generate_and_load
```

The pipeline is responsible for generating and loading the synthetic dental-clinic records into BigQuery.

Depending on the implementation, this process may:

1. Generate synthetic patient data
2. Generate dentist and staff records
3. Generate treatment catalog data
4. Generate appointments
5. Generate treatment associations
6. Generate medical history
7. Generate dental records
8. Generate prescriptions
9. Generate invoices
10. Generate payments
11. Load the resulting data into BigQuery

---

# 🔄 10. Resetting the Warehouse

If the project includes table-reset SQL scripts, the tables can be cleared using:

```text
sql/truncate.sql
```

Use this carefully because truncation removes the existing table data.

---

# 🧮 11. Embeddings and Clinical Semantic Search

The project can use embeddings to support semantic retrieval over clinical text such as:

```text
dental_records.clinical_notes
```

The general flow is:

```text
Clinical Notes
      │
      ▼
Embedding Generation
      │
      ▼
Vector Representation
      │
      ▼
BigQuery Vector Storage
      │
      ▼
Semantic Similarity Search
```

The SQL used to support embedding/vector operations is maintained in:

```text
sql/embeddings.sql
```

---

# 🚀 Running the System

## 1. Seed the Warehouse

```powershell
python -m data_generation.generate_and_load
```

## 2. Start the Interactive Assistant

```powershell
python app.py
```

The application provides an interactive interface for submitting natural-language questions against the dental data warehouse and RAG system.

---

# 💬 Example Queries

## Analytical Query

```text
What are the top 5 most common dental treatments performed,
and what is the total revenue generated from each?
```

Expected routing:

```text
User Question
      │
      ▼
Guardrail
      │
      ▼
Intent Router
      │
      ▼
SQL
      │
      ▼
Gemini Text-to-SQL
      │
      ▼
BigQuery
```

---

## Multi-Table Join

```text
What is the total revenue generated by each dentist, and how many unique appointments did they complete?
```

This type of query requires information from multiple relational tables.

---

## Financial Query

```text
Which patients currently have overdue or unpaid invoices greater than $300, and what are their phone numbers?
```

This requires joining patient and invoice information and applying financial filters.

---

## Clinical Semantic Query

```text
Find patients whose clinical notes mention sensitivity after a filling.
```

This can be routed to semantic clinical retrieval.

---

## Hybrid Query

```text
Find patients with sensitivity after fillings and show the number of follow-up appointments they attended.
```

This can require:

```text
Clinical Vector Search
        +
BigQuery SQL
        │
        ▼
Combined Context
        │
        ▼
Gemini Response
```

---

## Blocked Guardrail Query

```text
How many moons does Jupiter have,and which one is the largest?
```

Expected behaviour:

```text
User Question
      │
      ▼
Domain Guardrail
      │
      ▼
Rejected
```

The application should reject unrelated questions without executing unnecessary database queries.

---

# 🔍 RAG Execution Flow

A complete request can be represented as:

```text
┌─────────────────────────┐
│      User Question      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    Domain Guardrail     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Intent Classification │
└────────────┬────────────┘
             │
       ┌─────┼─────┐
       │     │     │
       ▼     ▼     ▼
      SQL  Vector Hybrid
       │     │     │
       │     │     ├──────────────┐
       │     │     │              │
       ▼     ▼     ▼              ▼
   BigQuery Vector Search     BigQuery SQL
       │     │     │              │
       └─────┴─────┴──────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Context Assembly  │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Gemini Synthesis  │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │   Final Answer    │
          └───────────────────┘
```

---

# 📈 Observability Flow

LangSmith traces the major stages of the application.

```text
                    dental_rag_pipeline
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       guardrail_check  intent_router  retrieval
                                           │
                                  ┌────────┴────────┐
                                  │                 │
                                  ▼                 ▼
                              SQL Route       Vector Route
                                  │                 │
                                  ▼                 │
                           SQL Generation          │
                                  │                 │
                                  ▼                 ▼
                           BigQuery Query    Vector Search
                                  │                 │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  response_synthesis
```

This provides a single place to investigate the lifecycle of an individual request.

---

# 🧾 SQL Self-Healing Example

Suppose Gemini generates:

```sql
SELECT
    d.name,
    COUNT(DISTINCT a.appointment_id)
FROM appointments a
JOIN appointment_treatments at
    ON a.appointment_id = at.appointment_id
JOIN dentists d
    ON a.dentist_id = d.dentist_id
GROUP BY d.name;
```

If BigQuery reports an SQL parsing error because of the alias `at`, the repair process can identify the problem and regenerate the query using a safer alias:

```sql
SELECT
    d.name,
    COUNT(DISTINCT a.appointment_id)
FROM appointments a
JOIN appointment_treatments apt_treat
    ON a.appointment_id = apt_treat.appointment_id
JOIN dentists d
    ON a.dentist_id = d.dentist_id
GROUP BY d.name;
```

The corrected query can then be re-executed.

---

# 💰 BigQuery Cost Considerations

BigQuery charges can depend on the amount of data processed and the services/features being used.

To reduce unnecessary processing:

* Use partitioned tables where appropriate.
* Use clustering for frequently filtered columns.
* Avoid `SELECT *` when only a subset of columns is required.
* Apply filters as early as possible.
* Prevent unrelated queries from reaching BigQuery through domain guardrails.
* Validate generated SQL before execution where possible.
* Monitor query execution through BigQuery.
* Monitor model usage through LangSmith.
* Avoid unnecessary retry loops.

For large datasets, query design can have a significant impact on execution efficiency.

---

# 🔐 Security & Data Privacy

This project is designed around synthetic healthcare data.

### Security recommendations

Never commit:

```text
.env
service_account.json
```

to source control.

Recommended `.gitignore`:

```gitignore
# Python
.venv/
__pycache__/
*.pyc

# Environment variables
.env

# GCP credentials
service_account.json
*.json

# IDE
.vscode/
.idea/

# Logs
*.log

# OS files
.DS_Store
Thumbs.db
```

For production deployments, consider:

* Secret Manager
* Workload Identity
* Short-lived credentials
* IAM least privilege
* Separate development and production projects
* Dataset-level access controls
* Audit logging
* Key rotation

---

# 🧪 Testing Strategy

The RAG system can be tested across multiple query categories.

## Domain Guardrail Tests

```text
How many moons does Jupiter have?
```

Expected:

```text
Blocked
```

## SQL Tests

```text
How many appointments were completed last month?
```

Expected:

```text
SQL Route
```

## Financial Tests

```text
What is the total outstanding invoice balance?
```

Expected:

```text
SQL Route
```

## Clinical Tests

```text
Find clinical notes mentioning tooth sensitivity.
```

Expected:

```text
Vector Route
```

## Hybrid Tests

```text
Find patients with sensitivity after fillings
and count their follow-up appointments.
```

Expected:

```text
Hybrid Route
```

## SQL Repair Tests

Provide questions likely to produce complex joins and verify that:

1. SQL is generated.
2. BigQuery execution is attempted.
3. Errors are captured.
4. SQL repair is triggered where appropriate.
5. Corrected SQL is executed.
6. The final response is generated.

---

# 📊 Evaluation Areas

The project can be evaluated using the following dimensions.

| Area             | Evaluation                                  |
| ---------------- | ------------------------------------------- |
| Data Generation  | Volume, realism, referential integrity      |
| SQL Generation   | Syntax and semantic correctness             |
| SQL Execution    | BigQuery execution success                  |
| SQL Repair       | Recovery from generated SQL errors          |
| Routing          | Correct SQL/Vector/Hybrid classification    |
| Retrieval        | Relevance of retrieved clinical records     |
| Guardrails       | Correct handling of out-of-domain questions |
| Response Quality | Accuracy and contextual relevance           |
| Latency          | End-to-end response time                    |
| Observability    | Trace completeness and debugging visibility |
| Cost             | Model and BigQuery resource usage           |

---

# 🛠️ Troubleshooting

## BigQuery Authentication Error

Verify:

```env
GOOGLE_APPLICATION_CREDENTIALS=service_account.json
```

Also verify that the file exists:

```powershell
Test-Path .\service_account.json
```

Expected:

```text
True
```

---

## Environment Variables Not Loaded

Verify that `.env` exists:

```powershell
Test-Path .\.env
```

Check the required variables:

```env
GCP_PROJECT_ID=
BIGQUERY_DATASET=
GCP_REGION=
GEMINI_API_KEY=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
```

---

## LangSmith Traces Not Appearing

Verify:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=dental-clinic-rag
```

Also confirm that the application initializes LangSmith tracing before the RAG pipeline executes.

---

## BigQuery SQL Error

Inspect:

1. Generated SQL
2. BigQuery error message
3. Schema context
4. Join conditions
5. Column names
6. Alias names
7. SQL repair trace

LangSmith traces can be used to inspect the generated SQL and repair attempts.

---

## Gemini API Error

Check:

* API key
* Model name
* API availability
* Request limits
* Network connectivity
* Model configuration

If retry logic is implemented, the application should use controlled retry behaviour rather than continuously retrying failed requests.

---

# 📋 Example `.gitignore`

```gitignore
# Virtual environment
.venv/

# Python cache
__pycache__/
*.py[cod]

# Environment variables
.env

# Credentials
service_account.json

# IDE
.vscode/
.idea/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

---

# 📦 Requirements

The project dependencies are maintained in:

```text
requirements.txt
```

Install them using:

```powershell
python -m pip install -r requirements.txt
```

Typical dependencies include libraries for:

* Google Cloud BigQuery
* Gemini/Google AI integration
* LangChain components where used
* LangSmith observability
* Environment-variable management
* Synthetic data generation
* Vector/embedding workflows

The exact versions should be maintained in `requirements.txt` to provide reproducible environments.

---

# 🔭 Future Enhancements

Potential future improvements include:

### 1. BigQuery Vector Search

Expand semantic retrieval using native BigQuery vector capabilities.

### 2. Advanced Clinical RAG

Improve clinical-note retrieval using:

* Better embedding models
* Metadata filtering
* Hybrid keyword + vector retrieval
* Re-ranking

### 3. Automated Evaluation

Introduce automated evaluation for:

* SQL correctness
* Retrieval relevance
* Answer faithfulness
* Intent classification
* Guardrail accuracy

### 4. LangSmith Evaluation

Use LangSmith datasets and evaluation workflows to compare:

* Prompt versions
* SQL-generation strategies
* Retrieval strategies
* Model configurations

### 5. Production API

Expose the RAG pipeline through:

```text
FastAPI
    │
    ▼
RAG Pipeline
    │
    ├── SQL
    ├── Vector
    └── Hybrid
```

### 6. Web Interface

A future frontend could provide:

* Chat interface
* Query history
* SQL visibility
* Retrieved clinical context
* Trace links
* Analytics dashboards

### 7. Authentication

Implement application-level authentication and role-based access control for different clinic users.

---

# 📚 Project Objectives

The project demonstrates how modern cloud data and generative-AI technologies can be combined to build an analytical assistant for a structured healthcare domain.

The main objectives are:

1. Build a large-scale synthetic dental dataset.
2. Store structured data in BigQuery.
3. Develop a natural-language Text-to-SQL interface.
4. Implement domain-specific guardrails.
5. Route questions using SQL, Vector, and Hybrid retrieval strategies.
6. Implement SQL validation and automated repair.
7. Support semantic retrieval over clinical notes.
8. Generate natural-language responses using Gemini.
9. Monitor model and pipeline execution using LangSmith.
10. Demonstrate scalable cloud-based RAG architecture.

---

# 🧭 Quick Start

Clone or open the project:

```powershell
cd dental-rag-gcp
```

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Configure:

```text
.env
service_account.json
```

Seed BigQuery:

```powershell
python -m data_generation.generate_and_load
```

Start the assistant:

```powershell
python app.py
```

Then enter a natural-language dental analytics question.

---

# 🔗 LangSmith Dashboard

Traces, latency breakdowns, model usage, SQL-generation steps, errors, and other execution information can be inspected through the configured LangSmith project.

**LangSmith Dashboard:**

https://smith.langchain.com/

The project configured in `.env` is:

```env
LANGSMITH_PROJECT=dental-clinic-rag
```

---

# 📌 Important Notes

* The project uses **synthetic healthcare data**.
* `service_account.json` must never be committed to Git.
* `.env` must never expose API credentials publicly.
* BigQuery query costs should be monitored when working with large datasets.
* SQL generated by an LLM should always be validated before being trusted.
* Clinical retrieval should be treated as synthetic demonstration data in this project and not as medical advice.
* Production healthcare deployments require additional security, privacy, compliance, authentication, authorization, auditing, and governance controls.

---

# 📄 License

Add the appropriate license for the project before publishing the repository.

Example:

```text
MIT License
```

or use the license required by the organization, university, or project owner.

---

# 👤 Author

**Dental Clinic BigQuery Data Pipeline & RAG System**

Built as a demonstration of:

```text
Google Cloud
     +
BigQuery
     +
Gemini
     +
RAG
     +
Vector Search
     +
LangSmith
     +
Synthetic Healthcare Data
```

The project demonstrates an end-to-end architecture for combining structured data analytics, natural-language SQL generation, semantic retrieval, automated SQL repair, and LLM observability in a controlled dental-clinic domain.
