import requests
from pathlib import Path

pwd = Path(__file__).resolve().parent

def test_pdf_api_without_llm():
    url = "http://127.0.0.1:8765/api/v1/convert"
    file = pwd / 'test.pdf'
    files = {'file': open(file, 'rb')}
    data = {
        'parse_mode': 'auto',
        'langs': 'en',
        'first_page': 1,
        'last_page': 1,
        'use_cache': 'false'
    }
    response = requests.post(url, files=files, data=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == 'success'
    assert response_json['metadata'] != None
    assert response_json['raw'] != None


def test_docx_api_without_llm():
    url = "http://127.0.0.1:8765/api/v1/convert"
    file = pwd / 'test.docx'
    files = {'file': open(file, 'rb')}
    data = {
        'parse_mode': 'auto',
        'langs': 'en',
        'first_page': 1,
        'last_page': 1,
        'use_cache': 'false'
    }
    response = requests.post(url, files=files, data=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == 'success'
    assert response_json['metadata'] != None
    assert response_json['raw'] != None


def test_doc_api_without_llm():
    url = "http://127.0.0.1:8765/api/v1/convert"
    file = pwd / 'test.doc'
    files = {'file': open(file, 'rb')}
    data = {
        'parse_mode': 'auto',
        'langs': 'en',
        'first_page': 1,
        'last_page': 1,
        'use_cache': 'false'
    }
    response = requests.post(url, files=files, data=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == 'success'
    assert response_json['metadata'] != None
    assert response_json['raw'] != None