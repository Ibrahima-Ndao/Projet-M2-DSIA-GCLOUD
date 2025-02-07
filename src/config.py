from pathlib import Path

# GCP Configuration
PROJECT_ID = "isi-group-m2-dsia"
BUCKET_NAME = "m2dsia-ndao-ibrahima-data"
DATASET_ID = f"{PROJECT_ID}.dataset_ndao_ibrahima"
TABLE_ID = f"{DATASET_ID}.transactions"

# Bucket folders
INPUT_FOLDER = "input/"
CLEAN_FOLDER = "clean/"
ERROR_FOLDER = "error/"
DONE_FOLDER = "done/"

# Schema for BigQuery table
SCHEMA = [
    {"name": "transaction_id", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "product_name", "type": "STRING", "mode": "REQUIRED"},
    {"name": "category", "type": "STRING", "mode": "REQUIRED"},
    {"name": "price", "type": "FLOAT", "mode": "REQUIRED"},
    {"name": "quantity", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "date", "type": "DATE", "mode": "REQUIRED"},
    {"name": "customer_name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "customer_email", "type": "STRING", "mode": "NULLABLE"}
] 