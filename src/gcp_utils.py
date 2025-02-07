from google.cloud import storage
from google.cloud import bigquery
from config import *

class GCPUtils:
    def __init__(self):
        self.storage_client = storage.Client(project=PROJECT_ID)
        self.bigquery_client = bigquery.Client(project=PROJECT_ID)
        self.bucket = self.storage_client.bucket(BUCKET_NAME)

    def move_blob(self, blob_name, from_folder, to_folder):
        """Move a file between folders in the bucket"""
        source_blob = self.bucket.blob(f"{from_folder}{blob_name}")
        destination_blob = self.bucket.blob(f"{to_folder}{blob_name}")
        
        destination_blob.rewrite(source_blob)
        source_blob.delete()

    def list_files(self, prefix):
        """List all files in a specific folder"""
        return [blob.name for blob in self.bucket.list_blobs(prefix=prefix)]

    def read_file(self, blob_name):
        """Read a file from Cloud Storage"""
        blob = self.bucket.blob(blob_name)
        return blob.download_as_text()

    def upload_to_bigquery(self, dataframe, job_config=None):
        """Upload a dataframe to BigQuery"""
        if job_config is None:
            job_config = bigquery.LoadJobConfig(
                schema=SCHEMA,
                write_disposition="WRITE_APPEND",
            )
        
        job = self.bigquery_client.load_table_from_dataframe(
            dataframe,
            TABLE_ID,
            job_config=job_config
        )
        job.result()  # Wait for the job to complete 