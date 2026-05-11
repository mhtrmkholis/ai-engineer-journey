"""Test summarizer — mock Claude API, no real call."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from week_01_python.models import Article
from week_01_python.summarizer import _calculate_cost, summarize_article


@pytest.fixture
def sample_article() -> Article:
    return Article(
        url="https://example.com/article",
        title="Test Article",
        text="This is a test article about AI engineering. " * 50,
        word_count=400,
    )


@pytest.fixture
def fake_claude_response():
    """Build fake Claude API response object."""
    tool_use = MagicMock()
    tool_use.type = "tool_use"
    tool_use.input = {
        "title": "AI Engineering",
        "tags": ["ai", "engineering", "test"],
        "summary": "Ringkasan tentang AI engineering. " * 10,
        "key_points": ["Poin satu.", "Poin dua.", "Poin tiga."],
    }
    response = MagicMock()
    response.content = [tool_use]
    response.usage.input_tokens = 100
    response.usage.output_tokens = 50
    return response


@pytest.mark.asyncio
async def test_summarize_returns_validated_result(
    sample_article, fake_claude_response, monkeypatch
):
    fake_client = MagicMock()
    fake_client.messages.create = AsyncMock(return_value=fake_claude_response)

    monkeypatch.setattr(
        "week_01_python.summarizer.AsyncAnthropic",
        lambda **kwargs: fake_client,
    )

    result = await summarize_article(sample_article)

    assert result.summary.title == "AI Engineering"
    assert len(result.summary.tags) == 3
    assert result.input_tokens == 100
    assert result.output_tokens == 50
    assert result.cost_usd > 0


@pytest.mark.asyncio
async def test_summarize_raises_when_no_tool_use(sample_article, monkeypatch):
    """Kalau Claude jawab text bukan tool_use, kode harus meledak."""
    text_block = MagicMock()
    text_block.type = "text"
    response = MagicMock()
    response.content = [text_block]

    fake_client = MagicMock()
    fake_client.messages.create = AsyncMock(return_value=response)
    monkeypatch.setattr(
        "week_01_python.summarizer.AsyncAnthropic",
        lambda **kwargs: fake_client,
    )

    with pytest.raises(RuntimeError, match="tool_use"):
        await summarize_article(sample_article)


def test_cost_calculation():
    # 1M input @ $3, 1M output @ $15 → $18 total
    cost = _calculate_cost(input_tokens=1_000_000, output_tokens=1_000_000)
    assert cost == pytest.approx(18.0)
