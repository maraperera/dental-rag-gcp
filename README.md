# Dental Clinic BigQuery Data Pipeline & RAG System

A scalable synthetic data pipeline, operational data warehouse, and Retrieval-Augmented Generation (RAG) assistant designed for **dental practice management and analytics**.

This platform provisions a relational data warehouse in **Google Cloud Platform (GCP) BigQuery**, loads **1.8M+ synthetic clinical, diagnostic, appointment, and billing records**, and provides a domain-restricted natural-language analytics assistant powered by **Gemini**.

The system combines:

* BigQuery relational analytics
* Gemini-powered Text-to-SQL
* Domain intent classification
* SQL validation and repair
* Clinical semantic retrieval
* RAG-based response synthesis
* Synthetic healthcare data generation
* GCP service-account authentication

> **Important:** All patient and clinical data used by this project is synthetic and generated for development, testing, demonstration, and RAG evaluation purposes.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       User / CLI        │
                         │      app.py             │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │    RAG Pipeline         │
                         │    pipeline.py          │
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
                 │   SQL Route     │      │ Clinical Vector  │
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
                         │ Gemini                  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     Final Answer        │
                         └─────────────────────────┘
```

---

# ✨ Key Features

## 1. Relational BigQuery Data Warehouse

The system uses a structured **11-table relational schema** designed for dental clinic operations.

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

---

## 2. Intent-Driven RAG Routing

The system analyzes each user question before deciding how to retrieve information.

Queries are routed into appropriate retrieval paths:

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

### SQL queries

Used for questions involving:

* Counts
* Sums
* Averages
* Revenue
* Appointment volumes
* Treatment frequency
* Patient statistics
* Operational metrics

Example:

> How many appointments were completed last month?

### Vector queries

Used for semantic clinical questions involving:

* Clinical notes
* Dental observations
* Symptoms
* Treatment descriptions
* Medical history
* Free-text clinical information

Example:

> Find patients whose clinical notes mention sensitivity after a filling.

### Hybrid queries

Used when both structured and semantic information is required.

Example:

> How many patients who received root canal treatment had clinical notes mentioning post-treatment sensitivity?

---

# 🛡️ Domain Guardrails

The application includes a domain guardrail that runs before downstream SQL generation or retrieval.

The purpose is to prevent unrelated questions from reaching the database or model pipeline.

### Allowed topics

The assistant is designed for questions related to:

* Dental patients
* Dentists
* Dental staff
* Appointments
* Treatments
* Dental records
* Medical history
* Prescriptions
* Invoices
* Payments
* Clinic operations
* Dental analytics

### Example allowed question

```text
How many root canal treatments were performed this year?
```

### Example blocked question

```text
How many moons does Jupiter have?
```

The second question should be rejected before database execution.

---

# 🧠 Text-to-SQL Pipeline

The SQL agent converts natural-language questions into BigQuery-compatible GoogleSQL.

The workflow is:

```text
Natural Language Question
          │
          ▼
Schema Context
          │
          ▼
Gemini SQL Generation
          │
          ▼
SQL Extraction
          │
          ▼
SQL Safety Validation
          │
          ▼
BigQuery Dry Run / Validation
          │
       ┌──┴──┐
       │     │
     Valid  Invalid
       │     │
       │     ▼
       │   Gemini SQL Repair
       │     │
       │     ▼
       │   Re-validation
       │
       ▼
BigQuery Execution
```

---

# 🔧 Self-Healing SQL Agent

The SQL agent includes an automated repair mechanism.

If the generated SQL contains a syntax error, the system can:

1. Capture the BigQuery error.
2. Provide the error message to Gemini.
3. Provide the original SQL.
4. Request a corrected query.
5. Validate the corrected SQL.
6. Execute the query if validation succeeds.

Example:

```text
User:
What are the top five treatments by revenue?

        ↓

Gemini

        ↓

Generated GoogleSQL

        ↓

BigQuery Validation

        ↓

Syntax Error

        ↓

Gemini SQL Repair

        ↓

Corrected GoogleSQL

        ↓

BigQuery Execution

        ↓

Results
```

This reduces failures caused by:

* Incorrect column names
* Invalid SQL syntax
* Incorrect table references
* BigQuery-specific SQL differences
* Reserved keyword collisions

---

# 🔐 SQL Safety

The application should only execute read-oriented analytical queries.

The SQL validation layer should reject destructive operations such as:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
MERGE
GRANT
REVOKE
```

The intended query pattern is:

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
ORDER BY ...
LIMIT ...
```

This provides an additional protection layer between Gemini-generated SQL and the BigQuery warehouse.

---

# 🗄️ BigQuery Database Schema

The warehouse contains 11 core relational tables.

## 1. `patients`

Stores synthetic patient demographic information.

Typical fields include:

```text
patient_id
first_name
last_name
date_of_birth
gender
phone
email
address
registration_date
```

---

## 2. `dentists`

Stores dentist information.

Typical fields include:

```text
dentist_id
first_name
last_name
specialization
license_number
phone
email
```

---

## 3. `staff`

Stores non-dentist clinic staff.

Typical roles include:

```text
Receptionist
Dental Assistant
Practice Manager
Dental Hygienist
Administrator
```

---

## 4. `treatments`

Stores the dental treatment catalog.

Typical fields include:

```text
treatment_id
ada_code
treatment_name
description
standard_fee
category
```

Examples include:

```text
Dental Cleaning
Dental Examination
Dental Filling
Root Canal
Tooth Extraction
Dental Crown
Dental Bridge
Dental Implant
Teeth Whitening
```

---

## 5. `appointments`

Stores patient appointments.

Typical fields include:

```text
appointment_id
patient_id
dentist_id
appointment_date
appointment_time
status
appointment_type
reason
```

Possible appointment statuses:

```text
Scheduled
Confirmed
Completed
Cancelled
No Show
Pending
```

---

## 6. `appointment_treatments`

Provides the relationship between appointments and treatments.

Typical fields:

```text
appointment_treatment_id
appointment_id
treatment_id
quantity
unit_price
total_price
```

This table allows a single appointment to contain multiple treatments.

---

## 7. `medical_history`

Stores synthetic patient medical history.

Typical fields include:

```text
medical_history_id
patient_id
condition
description
recorded_date
status
```

---

## 8. `dental_records`

Stores clinical dental observations.

Typical fields include:

```text
dental_record_id
patient_id
dentist_id
appointment_id
tooth_number
condition
clinical_notes
recorded_date
```

The `clinical_notes` field is particularly important for semantic/vector retrieval.

---

## 9. `prescriptions`

Stores medication prescriptions.

Typical fields include:

```text
prescription_id
patient_id
dentist_id
appointment_id
medication
dosage
frequency
duration
instructions
prescribed_date
```

---

## 10. `invoices`

Stores patient invoices.

Typical fields include:

```text
invoice_id
patient_id
appointment_id
invoice_date
subtotal
tax
discount
total_amount
status
```

---

## 11. `payments`

Stores invoice payments.

Typical fields include:

```text
payment_id
invoice_id
payment_date
amount
payment_method
status
```

---

# 📊 Data Warehouse Optimization

BigQuery storage and query performance are considered when designing the schema.

## Partitioning

Large time-series tables can be partitioned using appropriate date fields.

Examples:

```text
appointments
    └── appointment_date

medical_history
    └── recorded_date

dental_records
    └── recorded_date

invoices
    └── invoice_date

payments
    └── payment_date
```

Partitioning allows queries to scan only relevant date ranges where applicable.

---

## Clustering

Frequently filtered or joined columns can be used as clustering keys.

Potential clustering fields include:

```text
patient_id
dentist_id
treatment_id
appointment_id
status
```

The exact clustering strategy should be aligned with the application's actual query patterns.

---

# 🧬 Synthetic Data Generation

The project generates synthetic dental clinic data using Python.

The main generation process is located at:

```text
data_generation/generate_and_load.py
```

Static catalogs are maintained in:

```text
data_generation/catalog.py
```

The catalog can contain:

* Dental procedures
* ADA-style procedure codes
* Dental conditions
* Clinical note templates
* Medications
* Appointment types
* Patient statuses
* Payment methods
* Treatment categories

All generated patient and clinical information is synthetic.

---

# 📁 Project Structure

```text
dental-rag-gcp/
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data_generation/
│   ├── __init__.py
│   ├── catalog.py
│   └── generate_and_load.py
│
├── rag/
│   ├── __init__.py
│   ├── bq_client.py
│   ├── pipeline.py
│   ├── prompts.py
│   └── sql_agent.py
│
├── sql/
│   ├── schema.sql
│   └── truncate.sql
│
├── app.py
├── service_account.json
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# ⚙️ Prerequisites

Before running the project, install the following:

### Python

Recommended:

```text
Python 3.10+
```

### Google Cloud

A Google Cloud project with:

* BigQuery enabled
* Appropriate IAM permissions
* A BigQuery dataset
* Service account credentials

### Gemini

A Gemini API configuration compatible with the application.

---

# ☁️ GCP Configuration

Example configuration:

```env
GCP_PROJECT_ID=dental-clinic-rag
BIGQUERY_DATASET=dental_service
GCP_REGION=australia-southeast2
GOOGLE_APPLICATION_CREDENTIALS=service_account.json

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace placeholder values with the actual configuration for your environment.

> Model availability and naming can change. Use a model identifier that is currently available to your Gemini/Vertex AI configuration.

---

# 🔑 Service Account Setup

Create a GCP service account for the application.

The service account requires appropriate permissions to:

* Submit BigQuery jobs
* Read BigQuery data
* Create or manage the required dataset/tables when provisioning the environment

For a minimally scoped runtime account, prefer granting only the permissions actually required by the application.

The credentials file should be stored locally as:

```text
service_account.json
```

### ⚠️ Security

Never commit the service-account key to Git.

The `.gitignore` file should contain:

```text
service_account.json
.env
.venv/
__pycache__/
*.pyc
```

---

# 🐍 Python Environment Setup

From the project root:

```powershell
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

# 🔧 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
GCP_PROJECT_ID=dental-clinic-rag
BIGQUERY_DATASET=dental_service
GCP_REGION=australia-southeast2

GOOGLE_APPLICATION_CREDENTIALS=service_account.json

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

A template should also be maintained in:

```text
.env.example
```

Never place real API keys or service-account secrets inside `.env.example`.

---

# 🗃️ BigQuery Dataset

The project expects the BigQuery dataset:

```text
dental_service
```

The fully qualified table naming convention is:

```text
PROJECT_ID.dental_service.TABLE_NAME
```

For example:

```text
dental-clinic-rag.dental_service.patients
```

---

# 🚀 Initial Setup

After configuring GCP credentials and environment variables, generate and load the synthetic dataset:

```powershell
python -m data_generation.generate_and_load
```

The data generation process is responsible for:

1. Loading the dental catalogs.
2. Generating synthetic records.
3. Creating the required BigQuery tables.
4. Loading records into BigQuery.
5. Applying the required schema definitions.
6. Preparing the warehouse for RAG queries.

---

# 🏃 Running the Application

Once the BigQuery data has been provisioned, start the assistant:

```powershell
python app.py
```

The application provides an interactive conversational interface.

Example:

```text
==================================================
 Dental Clinic RAG Assistant
==================================================

Ask a question or type 'exit' to quit.

You:
```

---

# 💬 Example Queries

## Analytical Queries

```text
What are the five most common dental treatments?
```

```text
What is the total revenue generated from dental treatments?
```

```text
What is the average treatment cost?
```

```text
How many appointments were completed last month?
```

---

## Operational Queries

```text
How many pending appointments are scheduled this month?
```

```text
How many appointments does each dentist have?
```

```text
Which dentists performed the most treatments?
```

```text
How many cancelled appointments were recorded this year?
```

---

## Financial Queries

```text
What is the total amount of unpaid invoices?
```

```text
What was the total revenue last month?
```

```text
What are the most common payment methods?
```

```text
What is the average invoice value?
```

---

## Clinical Semantic Queries

```text
Find clinical notes mentioning tooth sensitivity.
```

```text
Find patients with notes mentioning post-treatment discomfort.
```

```text
Find dental records describing symptoms associated with gum inflammation.
```

These questions can be routed toward semantic retrieval when they depend primarily on free-text clinical information.

---

# 🚫 Example Blocked Query

An unrelated query such as:

```text
How many moons does Jupiter have?
```

should be identified by the domain guardrail and rejected.

The system should not send an unrelated question to the BigQuery SQL execution layer.

---

# 🔄 End-to-End Query Flow

The complete application workflow is:

```text
User Question
      │
      ▼
Domain Guardrail
      │
      ▼
Intent Classification
      │
      ├───────────────┐
      │               │
      ▼               ▼
     SQL            Vector
      │               │
      ▼               ▼
Text-to-SQL      Semantic Search
      │               │
      ▼               │
SQL Validation         │
      │               │
      ▼               │
BigQuery Query         │
      │               │
      └───────┬───────┘
              │
              ▼
       Retrieved Context
              │
              ▼
       Response Synthesis
              │
              ▼
         Final Answer
```

---

# 🧩 Project Components

## `config/settings.py`

Responsible for loading environment configuration.

Typical responsibilities include:

* GCP project configuration
* BigQuery dataset configuration
* Gemini configuration
* Authentication settings
* Runtime settings

---

## `data_generation/catalog.py`

Contains static domain-specific catalogs.

Examples:

```text
Treatments
Medications
Dental Conditions
Clinical Note Templates
Appointment Types
Payment Methods
```

---

## `data_generation/generate_and_load.py`

Responsible for:

* Synthetic record generation
* Data transformation
* BigQuery table creation
* Batch loading
* Dataset initialization

---

## `rag/bq_client.py`

Provides the BigQuery interface.

Responsibilities include:

* BigQuery client initialization
* SQL execution
* Schema discovery
* Metadata extraction
* Query validation
* Result conversion

---

## `rag/prompts.py`

Contains prompts used by the RAG pipeline.

Prompt categories include:

```text
Domain Guardrail
Intent Classification
SQL Generation
SQL Repair
Response Synthesis
```

Keeping prompts in a dedicated module makes the RAG system easier to maintain and evaluate.

---

## `rag/sql_agent.py`

Responsible for Text-to-SQL processing.

Main responsibilities:

```text
Question
   ↓
Schema Context
   ↓
Gemini
   ↓
GoogleSQL
   ↓
Validation
   ↓
Repair if necessary
   ↓
Execution
```

---

## `rag/pipeline.py`

Acts as the main RAG orchestrator.

It coordinates:

* Guardrails
* Intent routing
* SQL retrieval
* Semantic retrieval
* Hybrid retrieval
* Context construction
* Response generation

---

# 🧪 SQL Validation

Generated SQL should be validated before execution.

Recommended validation stages:

```text
1. Remove Markdown SQL fences
2. Normalize whitespace
3. Check query type
4. Reject destructive statements
5. Validate referenced tables
6. Perform BigQuery dry-run where appropriate
7. Execute only validated SQL
```

Example generated query:

```sql
SELECT
    treatment_name,
    COUNT(*) AS treatment_count
FROM `dental-clinic-rag.dental_service.appointment_treatments`
GROUP BY treatment_name
ORDER BY treatment_count DESC
LIMIT 5;
```

---

# 📈 BigQuery Cost Considerations

BigQuery charges based on data processed for applicable query operations.

The project therefore uses several techniques to reduce unnecessary scanning:

* Partitioned tables
* Clustered tables
* Targeted SQL generation
* Limited result sets
* Domain filtering
* Query validation
* Avoiding unnecessary `SELECT *`
* Date-range filtering where appropriate

For example, instead of:

```sql
SELECT *
FROM `project.dataset.appointments`;
```

the SQL agent should generate targeted queries such as:

```sql
SELECT
    dentist_id,
    COUNT(*) AS appointment_count
FROM `project.dataset.appointments`
WHERE appointment_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY dentist_id;
```

---

# 🔒 Data & Privacy

This project is designed around synthetic data.

It should not be populated with real patient information unless the system has been appropriately secured, governed, and reviewed for the applicable privacy and healthcare requirements.

The repository should never contain:

```text
Real patient names
Real addresses
Real medical records
Real prescriptions
Real patient identifiers
Production credentials
API keys
Service-account keys
```

---

# 🧹 Resetting the Dataset

The SQL reset script is located at:

```text
sql/truncate.sql
```

It can be used to clear generated records when rebuilding the development dataset.

Before executing reset operations, verify that the target project and dataset are correct.

---

# 🧪 Development Workflow

A typical development cycle is:

```text
1. Modify schema
       ↓
2. Update synthetic data generator
       ↓
3. Load test data
       ↓
4. Test BigQuery queries
       ↓
5. Update prompts
       ↓
6. Test SQL generation
       ↓
7. Test guardrails
       ↓
8. Test RAG routing
       ↓
9. Test response synthesis
       ↓
10. Run end-to-end application
```

---

# 🛠️ Troubleshooting

## Authentication Error

If BigQuery authentication fails, verify:

```text
GOOGLE_APPLICATION_CREDENTIALS
```

and confirm that the service-account file exists:

```text
service_account.json
```

---

## Dataset Not Found

Verify:

```env
GCP_PROJECT_ID=dental-clinic-rag
BIGQUERY_DATASET=dental_service
```

Also verify that the dataset exists in the selected GCP project.

---

## Gemini API Error

Check:

```env
GEMINI_API_KEY
GEMINI_MODEL
```

Also verify that the configured model is available to the API/service being used.

---

## SQL Generation Error

Check:

```text
rag/prompts.py
rag/sql_agent.py
rag/bq_client.py
```

The generated SQL should be checked for:

* Correct project ID
* Correct dataset
* Correct table names
* Correct column names
* BigQuery SQL syntax
* Appropriate date handling
* Appropriate aggregation

---

## PowerShell Virtual Environment Error

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# 📋 Example Complete Session

```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Generate and load synthetic data
python -m data_generation.generate_and_load

# Start the assistant
python app.py
```

Then:

```text
You: What are the most common treatments?

Assistant:
The most frequently recorded treatments are ...
```

---

# 🔐 Recommended `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]

# Virtual environment
.venv/
venv/

# Environment variables
.env

# GCP credentials
service_account.json

# IDE
.vscode/

# Logs
*.log

# OS files
.DS_Store
Thumbs.db
```

---

# 📦 Requirements

The project's Python dependencies are maintained in:

```text
requirements.txt
```

Typical dependency categories include:

```text
Google Cloud BigQuery
Google authentication
Gemini / Google AI SDK
Pydantic
python-dotenv
Pandas
NumPy
```

The exact package versions should be pinned in `requirements.txt` when reproducible deployments are required.

---

# 🗺️ Future Enhancements

Potential extensions include:

* Streamlit web interface
* BigQuery Vector Search integration
* Clinical note embeddings
* Hybrid SQL + vector retrieval
* Automated RAG evaluation
* Query latency monitoring
* BigQuery cost monitoring
* Conversation history
* Role-based access control
* Structured audit logging
* Automated test suite
* CI/CD deployment
* Cloud Run deployment
* Vertex AI integration
* Production-grade secret management

---

# 📌 Project Summary

The **Dental Clinic BigQuery Data Pipeline & RAG System** combines a synthetic dental practice data warehouse with a natural-language analytics interface.

The major components are:

```text
Python
   │
   ├── Synthetic Data Generation
   │
   ├── BigQuery
   │
   ├── Gemini
   │
   ├── Text-to-SQL
   │
   ├── SQL Validation
   │
   ├── Semantic Retrieval
   │
   └── RAG Pipeline
```

The resulting system provides a foundation for experimenting with:

* Large-scale structured healthcare data
* Natural-language database querying
* Domain-specific LLM applications
* Text-to-SQL systems
* Clinical semantic retrieval
* Hybrid RAG architectures
* BigQuery analytics
* Synthetic healthcare datasets

---

# 🏁 Quick Start

For a fresh environment:

```powershell
# Clone/open project
cd dental-rag-gcp

# Create virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt

# Configure environment
# Create .env and add GCP/Gemini configuration

# Add GCP service-account key
# service_account.json

# Generate and load data
python -m data_generation.generate_and_load

# Start the RAG assistant
python app.py
```

The system is then ready for natural-language dental clinic analytics against the synthetic BigQuery dataset.
