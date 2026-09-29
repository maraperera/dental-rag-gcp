# Dental Clinic BigQuery Data Pipeline & RAG System

A scalable synthetic data pipeline and analytics foundation designed for dental clinic operations. This service provisions a relational dental clinic schema on Google Cloud Platform (GCP) BigQuery and batches over 1.5 million realistic clinical, diagnostic, appointment, and billing records.

---

## Architecture & Schema Overview

The database consists of 11 relational tables structured for analytics and Retrieval-Augmented Generation (Text-to-SQL / Hybrid Semantic Search):

* **Entities**: `patients`, `dentists`, `staff`
* **Clinical Catalog**: `treatments` (ADA item codes, descriptions, standard fees)
* **Operations**: `appointments`, `appointment_treatments`
* **Medical & Dental Records**: `medical_history`, `dental_records`, `prescriptions`
* **Billing & Finance**: `invoices`, `payments`

Partitioning and clustering are configured across time-series and relational keys (`appointment_date`, `patient_id`, `invoice_date`) to optimize BigQuery scan costs and query latency.

---

## Directory Structure

```text
dental-rag-gcp/
├── config/
│   ├── __init__.py
│   └── settings.py              # Environment configuration loader via Pydantic
├── data_generation/
│   ├── __init__.py
│   ├── catalog.py               # Procedural dental catalogs, clinical notes, medications
│   └── generate_and_load.py     # Batch data generation and BigQuery streaming pipeline
├── sql/
│   ├── schema.sql               # BigQuery DDL definitions
│   └── truncate.sql             # Table reset scripts
├── service_account.json         # GCP IAM Service Account Key (Git-ignored)
├── .env                         # Local runtime environment variables (Git-ignored)
├── .env.example                 # Environment configuration template
├── .gitignore                   # Ignored files, credentials, and virtual environments
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies