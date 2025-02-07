from data_processor import DataProcessor
from gcp_utils import GCPUtils
from config import *

def main():
    gcp = GCPUtils()
    processor = DataProcessor()

    # List all files in input folder
    input_files = [f.split('/')[-1] for f in gcp.list_files(INPUT_FOLDER) if f.endswith('.csv')]
    
    print(f"Found {len(input_files)} files to process")
    
    # Process each file
    for file_name in input_files:
        processor.process_file(file_name)

if __name__ == "__main__":
    main() 