from pathlib import Path
import os

text_file = Path(os.getcwd()) / 'pdf_api' /'api_uploaded_files' / 'test.txt'

with open(text_file, 'rb') as f:
    output = f.read()