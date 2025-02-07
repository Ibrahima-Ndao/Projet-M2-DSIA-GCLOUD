import pandas as pd
from datetime import datetime
from io import StringIO
from gcp_utils import GCPUtils
from config import *

class DataProcessor:
    def __init__(self):
        self.gcp = GCPUtils()

    def validate_data(self, df):
        """Validate the dataframe according to schema requirements"""
        try:
            # Check for required columns
            required_columns = {field['name'] for field in SCHEMA if field['mode'] == 'REQUIRED'}
            
            # Print debugging information
            print("Required columns:", required_columns)
            print("Columns in file:", df.columns.tolist())
            
            missing_columns = required_columns - set(df.columns)
            if missing_columns:
                return False, f"Missing required columns: {missing_columns}"

            # Validate data types
            df['transaction_id'] = pd.to_numeric(df['transaction_id'], errors='raise')
            df['price'] = pd.to_numeric(df['price'], errors='raise')
            df['quantity'] = pd.to_numeric(df['quantity'], errors='raise')
            # Convert date from DD/MM/YYYY format
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.date

            # Check for null values in required fields
            if df[list(required_columns)].isnull().any().any():
                return False, "Null values in required fields"

            return True, df
        except Exception as e:
            return False, str(e)

    def process_file(self, file_name):
        """Process a single file from input folder"""
        try:
            # Read the file
            content = self.gcp.read_file(f"{INPUT_FOLDER}{file_name}")
            print(f"\nFirst few lines of the file content:")
            print(content[:500])
            
            # Read CSV with semicolon separator
            df = pd.read_csv(StringIO(content), sep=';')
            print("\nDataFrame head:")
            print(df.head())

            # Validate data
            is_valid, result = self.validate_data(df)

            if is_valid:
                # Upload to BigQuery
                self.gcp.upload_to_bigquery(result)
                # Move file to done folder
                self.gcp.move_blob(file_name, INPUT_FOLDER, DONE_FOLDER)
                print(f"Successfully processed {file_name}")
            else:
                # Move file to error folder
                self.gcp.move_blob(file_name, INPUT_FOLDER, ERROR_FOLDER)
                print(f"Error processing {file_name}: {result}")

        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
            self.gcp.move_blob(file_name, INPUT_FOLDER, ERROR_FOLDER) 