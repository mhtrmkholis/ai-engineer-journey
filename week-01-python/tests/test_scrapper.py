"""Test scraper — pure logic, no network."""

import pytest
from pydantic import ValidationError

from week_01_python.scraper import _extract

SAMPLE_HTML = """
<html>
<head><title>Test Article</title></head>
<body>
    <nav>Navigation menu yang harus dibuang</nav>
    <article>
        <h1>Main heading</h1>
        <p>First paragraph of the article.</p>
        <p>Second paragraph with more content.</p>
    </article>
    <footer>Footer content yang juga harus dibuang</footer>
</body>
</html>
"""


def test_extract_title():
    article = _extract("https://example.com", SAMPLE_HTML)
    assert article.title == "Test Article"


def test_extract_strips_nav_and_footer():
    article = _extract("https://example.com", SAMPLE_HTML)
    assert "Navigation menu" not in article.text
    assert "Footer content" not in article.text
    assert "First paragraph" in article.text


def test_extract_word_count_matches_text():
    article = _extract("https://example.com", SAMPLE_HTML)
    assert article.word_count == len(article.text.split())


def test_extract_with_no_title_falls_back_to_h1():
    html = "<html><body><h1>Fallback heading</h1><p>Body</p></body></html>"
    article = _extract("https://example.com", html)
    assert article.title == "Fallback heading"


def test_extract_invalid_url_raises():
    with pytest.raises(ValidationError):
        _extract("not-a-url", SAMPLE_HTML)
