from data_processor import DataProcessor
from gcp_utils import GCPUtils
from config import *
import time
from datetime import datetime

def print_separator():
    print("\n" + "="*80 + "\n")

def print_step(step_number, description):
    print_separator()
    print(f"ÉTAPE {step_number}: {description}")
    print_separator()

def main():
    try:
        # En-tête du programme
        print_separator()
        print("PIPELINE DE TRAITEMENT DE DONNÉES GCP")
        print(f"Démarrage: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Projet: {PROJECT_ID}")
        print(f"Bucket: {BUCKET_NAME}")
        print_separator()

        # Initialisation
        print_step(1, "INITIALISATION DES CLIENTS GCP")
        gcp = GCPUtils()
        processor = DataProcessor()
        print("✓ Clients GCP initialisés avec succès")

        # Vérification des dossiers
        print_step(2, "VÉRIFICATION DES DOSSIERS")
        folders = [INPUT_FOLDER, CLEAN_FOLDER, ERROR_FOLDER, DONE_FOLDER]
        for folder in folders:
            files = gcp.list_files(folder)
            print(f"Dossier {folder}: {len(files)} fichiers")

        # Liste des fichiers à traiter
        print_step(3, "ANALYSE DES FICHIERS À TRAITER")
        input_files = [f.split('/')[-1] for f in gcp.list_files(INPUT_FOLDER) if f.endswith('.csv')]
        
        if not input_files:
            print("⚠ Aucun fichier CSV trouvé dans le dossier input/")
            return
        
        print(f"Nombre de fichiers à traiter: {len(input_files)}")
        for i, file in enumerate(input_files, 1):
            print(f"{i}. {file}")

        # Traitement des fichiers
        print_step(4, "TRAITEMENT DES FICHIERS")
        for i, file_name in enumerate(input_files, 1):
            print(f"\nTraitement du fichier {i}/{len(input_files)}: {file_name}")
            print("-" * 50)
            
            start_time = time.time()
            processor.process_file(file_name)
            duration = time.time() - start_time
            
            print(f"Durée du traitement: {duration:.2f} secondes")

        # Résumé final
        print_step(5, "RÉSUMÉ DU TRAITEMENT")
        
        # Compter les fichiers dans chaque dossier après traitement
        clean_files = len(gcp.list_files(CLEAN_FOLDER))
        error_files = len(gcp.list_files(ERROR_FOLDER))
        done_files = len(gcp.list_files(DONE_FOLDER))
        
        print("Résultats du traitement:")
        print(f"- Fichiers traités: {len(input_files)}")
        print(f"- Fichiers nettoyés: {clean_files}")
        print(f"- Fichiers en erreur: {error_files}")
        print(f"- Fichiers chargés dans BigQuery: {done_files}")

        print_separator()
        print(f"Fin du traitement: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print_separator()

    except Exception as e:
        print_separator()
        print("❌ ERREUR CRITIQUE DU PROGRAMME")
        print(f"Nature de l'erreur: {str(e)}")
        print_separator()
        raise

if __name__ == "__main__":
    main() 