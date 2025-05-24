import builtins
from unittest.mock import Mock, patch

import pytest

from aozora_scraper import (
    extract_text_from_html,
    fetch_author_works,
    fetch_html,
    save_text_to_file,
)


def test_extract_text_from_html():
    html = "<div class='main_text'>Hello</div><div class='main_text'>World</div>"
    assert extract_text_from_html(html) == "Hello\nWorld"


def test_fetch_author_works():
    html = """
    <html><body>
        <a href='/cards/000148/files/1234_5678.html'>Work1</a>
        <a href='/other'>Other</a>
        <a href='/cards/000149/files/9999_8888.html'>Work2</a>
    </body></html>
    """
    mock_response = Mock()
    mock_response.content = html.encode("utf-8")
    mock_response.raise_for_status = Mock()
    with patch("aozora_scraper.requests.get", return_value=mock_response) as m:
        works = fetch_author_works("dummy")
        assert works == [
            "https://www.aozora.gr.jp/cards/000148/files/1234_5678.html",
            "https://www.aozora.gr.jp/cards/000149/files/9999_8888.html",
        ]
        m.assert_called_once_with("dummy")


def test_save_text_to_file(tmp_path):
    file_path = tmp_path / "out.txt"
    save_text_to_file(file_path, "Sample text")
    assert file_path.read_text(encoding="utf-8") == "Sample text"


def test_fetch_html():
    mock_response = Mock()
    mock_response.content = b"data"
    mock_response.raise_for_status = Mock()
    with patch("aozora_scraper.requests.get", return_value=mock_response) as m:
        assert fetch_html("https://example.com") == b"data"
        m.assert_called_once_with("https://example.com")
