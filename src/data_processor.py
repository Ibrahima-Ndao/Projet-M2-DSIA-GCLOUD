import pandas as pd
from datetime import datetime
from io import StringIO
from gcp_utils import GCPUtils
from config import *

class DataProcessor:
    def __init__(self):
        self.gcp = GCPUtils()

    def validate_data(self, df):
        """Valider le dataframe selon les exigences du schéma"""
        try:
            # Vérifier les colonnes requises
            required_columns = {field['name'] for field in SCHEMA if field['mode'] == 'REQUIRED'}
            
            print("Colonnes requises:", required_columns)
            print("Colonnes dans le fichier:", df.columns.tolist())
            
            missing_columns = required_columns - set(df.columns)
            if missing_columns:
                return False, f"Colonnes manquantes: {missing_columns}"

            # Créer une copie du dataframe pour éviter les modifications sur l'original
            df = df.copy()

            # Valider les types de données
            df['transaction_id'] = pd.to_numeric(df['transaction_id'], errors='raise')
            df['price'] = pd.to_numeric(df['price'], errors='raise')
            df['quantity'] = pd.to_numeric(df['quantity'], errors='raise')
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.date

            # Vérifier les valeurs nulles dans les champs requis
            if df[list(required_columns)].isnull().any().any():
                return False, "Valeurs nulles dans les champs obligatoires"

            return True, df
        except Exception as e:
            return False, str(e)

    def process_file(self, file_name):
        """Traiter un fichier depuis le dossier d'entrée"""
        try:
            print(f"\nTraitement du fichier: {file_name}")
            
            # Lire le fichier
            content = self.gcp.read_file(f"{INPUT_FOLDER}{file_name}")
            print(f"\nAperçu du contenu du fichier:")
            print(content[:500])
            
            # Lire le CSV avec séparateur point-virgule
            df = pd.read_csv(StringIO(content), sep=';')
            print("\nAperçu des données:")
            print(df.head())

            # Valider les données
            is_valid, result = self.validate_data(df)

            if is_valid:
                # D'abord sauvegarder dans le dossier clean
                self.gcp.save_to_folder(result, CLEAN_FOLDER, file_name)
                
                try:
                    # Essayer de charger vers BigQuery
                    self.gcp.upload_to_bigquery(result)
                    # Si réussi, déplacer vers le dossier done
                    self.gcp.move_blob(file_name, INPUT_FOLDER, DONE_FOLDER)
                    print(f"Traitement réussi pour {file_name}")
                except Exception as e:
                    # Si échec du chargement BigQuery, garder dans clean mais déplacer l'original vers error
                    print(f"Erreur lors du chargement vers BigQuery: {str(e)}")
                    self.gcp.move_blob(file_name, INPUT_FOLDER, ERROR_FOLDER)
            else:
                # Déplacer vers le dossier error si la validation échoue
                self.gcp.move_blob(file_name, INPUT_FOLDER, ERROR_FOLDER)
                print(f"Erreur de validation pour {file_name}: {result}")

        except Exception as e:
            print(f"Erreur lors du traitement de {file_name}: {str(e)}")
            self.gcp.move_blob(file_name, INPUT_FOLDER, ERROR_FOLDER) 