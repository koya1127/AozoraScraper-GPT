import json
from http.server import HTTPServer
from threading import Thread
from urllib.parse import urlencode
from unittest.mock import patch

import requests

from web_app import Handler


def run_server():
    server = HTTPServer(("localhost", 0), Handler)
    port = server.server_address[1]
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server, port, thread


def test_works_endpoint():
    with patch("web_app.fetch_author_works", return_value=["url1", "url2"]) as fetch:
        server, port, thread = run_server()
        resp = requests.get(f"http://localhost:{port}/works?" + urlencode({"author_url": "author"}))
        assert resp.status_code == 200
        assert resp.json() == {"works": ["url1", "url2"]}
        fetch.assert_called_once_with("author")
        server.shutdown()
        thread.join()


def test_work_endpoint():
    with patch("web_app.fetch_html", return_value=b"html") as f_html, patch(
        "web_app.extract_text_from_html", return_value="text"
    ) as extract:
        server, port, thread = run_server()
        resp = requests.get(f"http://localhost:{port}/work?" + urlencode({"url": "work"}))
        assert resp.status_code == 200
        assert resp.json() == {"text": "text"}
        f_html.assert_called_once_with("work")
        extract.assert_called_once_with(b"html")
        server.shutdown()
        thread.join()


def test_missing_params():
    server, port, thread = run_server()
    resp = requests.get(f"http://localhost:{port}/works")
    assert resp.status_code == 400
    resp = requests.get(f"http://localhost:{port}/work")
    assert resp.status_code == 400
    server.shutdown()
    thread.join()
