from google.cloud import storage
from google.cloud import bigquery
from config import *

class GCPUtils:
    def __init__(self):
        self.storage_client = storage.Client(project=PROJECT_ID)
        self.bigquery_client = bigquery.Client(project=PROJECT_ID)
        self.bucket = self.storage_client.bucket(BUCKET_NAME)

    def move_blob(self, blob_name, from_folder, to_folder):
        """Déplacer un fichier entre les dossiers du bucket"""
        source_blob = self.bucket.blob(f"{from_folder}{blob_name}")
        destination_blob = self.bucket.blob(f"{to_folder}{blob_name}")
        
        destination_blob.rewrite(source_blob)
        source_blob.delete()
        print(f"Fichier déplacé de {from_folder} vers {to_folder}: {blob_name}")

    def copy_blob(self, blob_name, from_folder, to_folder):
        """Copier un fichier entre les dossiers du bucket sans supprimer l'original"""
        source_blob = self.bucket.blob(f"{from_folder}{blob_name}")
        destination_blob = self.bucket.blob(f"{to_folder}{blob_name}")
        
        destination_blob.rewrite(source_blob)
        print(f"Fichier copié de {from_folder} vers {to_folder}: {blob_name}")

    def list_files(self, prefix):
        """Lister tous les fichiers dans un dossier spécifique"""
        return [blob.name for blob in self.bucket.list_blobs(prefix=prefix)]

    def read_file(self, blob_name):
        """Lire un fichier depuis Cloud Storage"""
        blob = self.bucket.blob(blob_name)
        return blob.download_as_text()

    def upload_to_bigquery(self, dataframe, job_config=None):
        """Charger un dataframe vers BigQuery"""
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
        job.result()  # Attendre la fin du chargement

    def save_to_folder(self, content, folder, filename):
        """Sauvegarder du contenu dans un dossier spécifique"""
        blob = self.bucket.blob(f"{folder}{filename}")
        if isinstance(content, str):
            blob.upload_from_string(content)
        else:
            # Si c'est un DataFrame, le convertir en CSV
            blob.upload_from_string(content.to_csv(index=False, sep=';'))
        print(f"Fichier sauvegardé dans {folder}: {filename}") 