import requests
from pathlib import Path
import os

url = "http://0.0.0.0:8000/"
# url = "http://167.172.34.189:8000/"

def get_list_of_files():
    response = requests.get(f'{url}/files')
    print(response.json())

def post_file(file):
    with open(file, 'rb') as fp:
        files = {'file': fp}
        response = requests.post(
            f'{url}', files=files
        )
    print(response.status_code)
    return response.json()


if __name__ == '__main__':
    CWD = Path(os.getcwd())
    file = CWD / 'pdf_api'/ 'test_data' / 'test.pdf'
    file = CWD / 'test_data' / 'test.pdf'
    #get_list_of_files()
    f = post_file(file)
    f['text']
    #get_list_of_files()