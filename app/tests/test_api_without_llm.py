import requests
from pathlib import Path

pwd = Path(__file__).resolve().parent


def get_response(
    file: str, parse_mode: str, langs: str, first_page: int, last_page: int
):
    url = "http://127.0.0.1:8765/api/v1/convert"
    files = {"file": open(file, "rb")}
    data = {
        "parse_mode": parse_mode,
        "langs": langs,
        "first_page": first_page,
        "last_page": last_page,
        "use_cache": "false",
    }
    response = requests.post(url, files=files, data=data)
    return response


def test_api_ping():
    url = "http://127.0.0.1:8765/api/v1/ping"
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "You have successfully connected to the e2m API!"


def test_pdf_api_without_llm():
    file = pwd / "test.pdf"
    response = get_response(
        file=file,
        parse_mode="auto",
        langs="en",
        first_page=1,
        last_page=1,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["metadata"] is not None
    assert response_json["raw"] is not None


def test_docx_api_without_llm():
    file = pwd / "test.docx"
    response = get_response(
        file=file,
        parse_mode="auto",
        langs="en",
        first_page=1,
        last_page=1,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["metadata"] is not None
    assert response_json["raw"] is not None


def test_doc_api_without_llm():
    file = pwd / "test.doc"
    response = get_response(
        file=file,
        parse_mode="auto",
        langs="en",
        first_page=1,
        last_page=1,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["metadata"] is not None
    assert response_json["raw"] is not None


def test_pptx_api_without_llm():
    file = pwd / "test.pptx"
    response = get_response(
        file=file,
        parse_mode="auto",
        langs="en",
        first_page=1,
        last_page=1,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["metadata"] is not None
    assert response_json["raw"] is not None


def test_ppt_api_without_llm():
    file = pwd / "test.ppt"
    response = get_response(
        file=file,
        parse_mode="auto",
        langs="en",
        first_page=1,
        last_page=1,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["metadata"] is not None
    assert response_json["raw"] is not None


def test_html_api_without_llm():
    file = pwd / "test.html"
    response = get_response(
        file=file,
        parse_mode="auto",
        langs="en",
        first_page=1,
        last_page=1,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["metadata"] is not None
    assert response_json["raw"] is not None


def test_htm_api_without_llm():
    file = pwd / "test.htm"
    response = get_response(
        file=file,
        parse_mode="auto",
        langs="en",
        first_page=1,
        last_page=1,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["metadata"] is not None
    assert response_json["raw"] is not None
