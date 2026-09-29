import os
import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound

from config.settings import settings
from data_generation.catalog import (
    TREATMENTS_CATALOG,
    DENTAL_CONDITIONS,
    MEDICAL_HISTORY_CONDITIONS,
    PRESCRIPTION_MEDICATIONS,
    APPOINTMENT_REASONS
)

# Initialize Faker with Australian locale
fake = Faker("en_AU")
Faker.seed(settings.RANDOM_SEED)
random.seed(settings.RANDOM_SEED)

def get_bq_client() -> bigquery.Client:
    """Instantiate authenticated BigQuery client."""
    cred_file = settings.full_credentials_path
    if cred_file.exists():
        credentials = service_account.Credentials.from_service_account_file(str(cred_file))
        return bigquery.Client(project=settings.PROJECT_ID, credentials=credentials, location=settings.REGION)
    print("Warning: service_account.json not found. Falling back to application-default login.")
    return bigquery.Client(project=settings.PROJECT_ID, location=settings.REGION)

client = get_bq_client()

def ensure_dataset_exists():
    """Verify or explicitly create the BigQuery dataset."""
    dataset_id = f"{settings.PROJECT_ID}.{settings.DATASET_ID}"
    try:
        dataset = client.get_dataset(dataset_id)
        print(f"Dataset exists: {dataset.full_dataset_id} in {dataset.location}")
    except NotFound:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = settings.REGION
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset: {dataset.full_dataset_id} in {dataset.location}")

def load_dataframe_to_bq(df: pd.DataFrame, table_name: str, write_mode: str = "WRITE_APPEND"):
    """Loads a pandas dataframe into BigQuery using Parquet format."""
    table_id = f"{settings.PROJECT_ID}.{settings.DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_mode,
        source_format=bigquery.SourceFormat.PARQUET,
    )
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"Loaded {len(df):,} rows into {table_name}")

def run_pipeline():
    ensure_dataset_exists()

    # 1. Treatments
    print("\n--- Populating treatments ---")
    df_treatments = pd.DataFrame(
        TREATMENTS_CATALOG,
        columns=["treatment_id", "treatment_name", "description", "standard_cost"]
    )
    df_treatments["standard_cost"] = df_treatments["standard_cost"].astype(float)
    load_dataframe_to_bq(df_treatments, "treatments", "WRITE_TRUNCATE")

    # 2. Dentists (100 clinicians)
    print("\n--- Populating dentists ---")
    specializations = ["General Dentist", "Endodontist", "Periodontist", "Oral Surgeon", "Orthodontist", "Pediatric Dentist"]
    dentists = [{
        "dentist_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "specialization": random.choice(specializations),
        "license_number": f"DEN-AU-{100000 + i}"
    } for i in range(1, 101)]
    df_dentists = pd.DataFrame(dentists)
    load_dataframe_to_bq(df_dentists, "dentists", "WRITE_TRUNCATE")

    # 3. Staff (150 clinic staff)
    print("\n--- Populating staff ---")
    roles = ["Dental Hygienist", "Senior Dental Assistant", "Practice Manager", "Receptionist", "Sterilization Technician"]
    staff = [{
        "staff_id": i,
        "name": fake.name(),
        "role": random.choice(roles),
        "phone": fake.phone_number(),
        "email": f"staff.{i}@dentalclinic.com.au"
    } for i in range(1, 151)]
    df_staff = pd.DataFrame(staff)
    load_dataframe_to_bq(df_staff, "staff", "WRITE_TRUNCATE")

    # 4. Patients (100,000 records loaded in chunks)
    print("\n--- Populating patients (100,000) ---")
    TOTAL_PATIENTS = 100000
    chunk_size = settings.BATCH_CHUNK_SIZE

    for start_idx in range(1, TOTAL_PATIENTS + 1, chunk_size):
        end_idx = min(start_idx + chunk_size, TOTAL_PATIENTS + 1)
        patients = [{
            "patient_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "dob": fake.date_of_birth(minimum_age=3, maximum_age=85),
            "phone": fake.phone_number(),
            "email": f"patient.{i}@domain.com.au",
            "address": fake.address().replace("\n", ", ")
        } for i in range(start_idx, end_idx)]
        
        df_patients = pd.DataFrame(patients)
        df_patients["dob"] = pd.to_datetime(df_patients["dob"]).dt.date
        mode = "WRITE_TRUNCATE" if start_idx == 1 else "WRITE_APPEND"
        load_dataframe_to_bq(df_patients, "patients", mode)

    # 5. Appointments & Appointment Treatments (400,000 records)
    print("\n--- Populating appointments & appointment_treatments (400,000) ---")
    TOTAL_APPTS = 400000
    appt_chunk = 100000
    base_date = datetime(2023, 1, 1)
    status_distribution = ["Completed", "Completed", "Completed", "Scheduled", "Cancelled", "No Show"]

    for start_idx in range(1, TOTAL_APPTS + 1, appt_chunk):
        end_idx = min(start_idx + appt_chunk, TOTAL_APPTS + 1)
        appts = []
        appt_treatments = []

        for i in range(start_idx, end_idx):
            appt_time = base_date + timedelta(
                days=random.randint(0, 1100),
                hours=random.randint(8, 17),
                minutes=random.choice([0, 15, 30, 45])
            )
            status = random.choice(status_distribution)
            p_id = random.randint(1, TOTAL_PATIENTS)
            d_id = random.randint(1, 100)

            appts.append({
                "appointment_id": i,
                "patient_id": p_id,
                "dentist_id": d_id,
                "appointment_date": appt_time,
                "status": status,
                "reason": random.choice(APPOINTMENT_REASONS)
            })

            if status in ["Completed", "Scheduled"]:
                chosen_treatment = random.choice(TREATMENTS_CATALOG)
                appt_treatments.append({
                    "appointment_id": i,
                    "treatment_id": chosen_treatment[0],
                    "quantity": 1,
                    "cost": float(chosen_treatment[3])
                })

        df_appts = pd.DataFrame(appts)
        df_appt_treatments = pd.DataFrame(appt_treatments)
        
        mode = "WRITE_TRUNCATE" if start_idx == 1 else "WRITE_APPEND"
        load_dataframe_to_bq(df_appts, "appointments", mode)
        load_dataframe_to_bq(df_appt_treatments, "appointment_treatments", mode)

    # 6. Medical History (120,000 records)
    print("\n--- Populating medical_history (120,000) ---")
    med_history = []
    for i in range(1, 120001):
        cond, notes = random.choice(MEDICAL_HISTORY_CONDITIONS)
        med_history.append({
            "history_id": i,
            "patient_id": random.randint(1, TOTAL_PATIENTS),
            "condition": cond,
            "notes": notes,
            "recorded_date": (datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1600))).date()
        })
    df_med = pd.DataFrame(med_history)
    df_med["recorded_date"] = pd.to_datetime(df_med["recorded_date"]).dt.date
    load_dataframe_to_bq(df_med, "medical_history", "WRITE_TRUNCATE")

    # 7. Dental Records (250,000 clinical records)
    print("\n--- Populating dental_records (250,000) ---")
    records = []
    for i in range(1, 250001):
        cond, notes = random.choice(DENTAL_CONDITIONS)
        records.append({
            "record_id": i,
            "patient_id": random.randint(1, TOTAL_PATIENTS),
            "dentist_id": random.randint(1, 100),
            "tooth_number": random.randint(1, 32),
            "condition": cond,
            "notes": notes
        })
    df_rec = pd.DataFrame(records)
    load_dataframe_to_bq(df_rec, "dental_records", "WRITE_TRUNCATE")

    # 8. Prescriptions (100,000 records)
    print("\n--- Populating prescriptions (100,000) ---")
    prescriptions = []
    for i in range(1, 100001):
        med, dose, inst = random.choice(PRESCRIPTION_MEDICATIONS)
        prescriptions.append({
            "prescription_id": i,
            "patient_id": random.randint(1, TOTAL_PATIENTS),
            "dentist_id": random.randint(1, 100),
            "appointment_id": random.randint(1, TOTAL_APPTS),
            "medication": med,
            "dosage": dose,
            "instructions": inst
        })
    df_rx = pd.DataFrame(prescriptions)
    load_dataframe_to_bq(df_rx, "prescriptions", "WRITE_TRUNCATE")

    # 9. Invoices & Payments (250,000 invoices / 200,000 payments)
    print("\n--- Populating invoices & payments ---")
    invoices = []
    payments = []
    pm_methods = ["Credit Card", "EFTPOS Debit", "HICAPS Direct Claim", "Private Health Insurance", "Direct Bank Deposit"]
    inv_statuses = ["Paid", "Paid", "Paid", "Partially Paid", "Unpaid"]

    for i in range(1, 250001):
        inv_dt = base_date + timedelta(days=random.randint(0, 1100), hours=random.randint(9, 18))
        total_amt = round(random.uniform(75.0, 1600.0), 2)
        st = random.choice(inv_statuses)

        invoices.append({
            "invoice_id": i,
            "patient_id": random.randint(1, TOTAL_PATIENTS),
            "appointment_id": i if i <= TOTAL_APPTS else None,
            "invoice_date": inv_dt,
            "total_amount": total_amt,
            "status": st
        })

        if st in ["Paid", "Partially Paid"] and len(payments) < 200000:
            paid_amount = total_amt if st == "Paid" else round(total_amt * 0.5, 2)
            payments.append({
                "payment_id": len(payments) + 1,
                "invoice_id": i,
                "payment_date": inv_dt + timedelta(hours=random.randint(1, 72)),
                "amount": paid_amount,
                "payment_method": random.choice(pm_methods)
            })

    df_invoices = pd.DataFrame(invoices)
    df_payments = pd.DataFrame(payments)
    load_dataframe_to_bq(df_invoices, "invoices", "WRITE_TRUNCATE")
    load_dataframe_to_bq(df_payments, "payments", "WRITE_TRUNCATE")

    print("\nPipeline execution complete. Over 1,500,000 rows loaded successfully into BigQuery.")

if __name__ == "__main__":
    run_pipeline()