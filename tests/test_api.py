import os
from dotenv import load_dotenv
import threading
import time
from typing import Iterator

import pytest
import requests
from uvicorn import Config, Server


BASE_URL = "http://127.0.0.1:8001"


def run_server() -> None:
    config = Config("api.main:app", host="127.0.0.1", port=8001, log_level="warning")
    server = Server(config)
    server.run()


@pytest.fixture(scope="session", autouse=True)
def start_api() -> Iterator[None]:
    # Load .env so DATABASE_URL is available locally
    load_dotenv()
    assert os.getenv("DATABASE_URL"), "DATABASE_URL must be set for tests (define it in .env)"
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    # wait for server
    for _ in range(60):
        try:
            r = requests.get(BASE_URL + "/docs", timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.2)
    yield


def test_docs() -> None:
    r = requests.get(BASE_URL + "/docs", timeout=5)
    assert r.status_code == 200


def test_search_messages_smoke() -> None:
    r = requests.get(BASE_URL + "/api/search/messages", params={"query": "medicine"}, timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_top_products_whitelist() -> None:
    r = requests.get(BASE_URL + "/api/reports/top-products", params={"strategy": "whitelist", "limit": 5}, timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_top_products_combined() -> None:
    r = requests.get(BASE_URL + "/api/reports/top-products", params={"strategy": "combined", "limit": 5}, timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


