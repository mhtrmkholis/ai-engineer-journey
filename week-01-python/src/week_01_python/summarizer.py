import asyncio

from anthropic import AsyncAnthropic

from week_01_python.config import settings
from week_01_python.models import Article, Summary, SummaryResult

# Harga claude-sonnet-4-6 per April 2026 (USD per 1M tokens)
INPUT_COST_PER_M = 3.00
OUTPUT_COST_PER_M = 15.00

# Tool definition — schema otomatis dari Pydantic Summary
SUMMARY_TOOL = {
    "name": "save_summary",
    "description": "Simpan ringkasan artikel dalam format terstruktur.",
    "input_schema": Summary.model_json_schema(),
}

SYSTEM_PROMPT = """\
Kamu adalah asisten yang membaca artikel dan memberikan ringkasan terstruktur.
Selalu gunakan tool save_summary untuk output. Jangan berikan teks bebas.
Tulis title, summary, dan key_points dalam bahasa yang sama dengan artikel input.
Tags selalu lowercase, dipisah, dan relevan dengan topik utama.
"""


def _truncate(text: str, max_words: int = 5000) -> str:
    """Trim teks panjang biar hemat biaya API. ~5000 kata ≈ ~6.5k tokens."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "\n\n[... artikel dipotong ...]"


def _calculate_cost(input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens * INPUT_COST_PER_M / 1_000_000
        + output_tokens * OUTPUT_COST_PER_M / 1_000_000
    )


async def summarize_article(article: Article) -> SummaryResult:
    """Panggil Claude dengan tool use untuk dapat Summary terstruktur."""
    client = AsyncAnthropic(api_key=settings.anthropic_api_key.get_secret_value())

    user_message = (
        f"Buat ringkasan artikel berikut.\n\n"
        f"URL: {article.url}\n"
        f"Title: {article.title}\n\n"
        f"Konten:\n{_truncate(article.text)}"
    )

    response = await client.messages.create(
        model=settings.model,
        max_tokens=settings.max_tokens,
        system=SYSTEM_PROMPT,
        tools=[SUMMARY_TOOL],
        tool_choice={"type": "tool", "name": "save_summary"},
        messages=[{"role": "user", "content": user_message}],
    )

    # Extract tool_use block dari response
    tool_use_block = next(
        (block for block in response.content if block.type == "tool_use"),
        None,
    )
    if tool_use_block is None:
        raise RuntimeError("Claude tidak mengembalikan tool_use block.")

    # Validate output Claude lewat Pydantic — kalau Claude bandel, ValidationError
    summary = Summary.model_validate(tool_use_block.input)

    return SummaryResult(
        summary=summary,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        cost_usd=_calculate_cost(
            response.usage.input_tokens, response.usage.output_tokens
        ),
    )


async def _main():
    from week_01_python.scraper import fetch_article

    url = "https://en.wikipedia.org/wiki/Large_language_model"
    print(f"Fetching: {url}")
    article = await fetch_article(url)
    print(f"Got: {article.title} ({article.word_count} words)\n")

    print("Calling Claude...")
    result = await summarize_article(article)

    print(f"\n📄 Title:    {result.summary.title}")
    print(f"🏷️  Tags:     {', '.join(result.summary.tags)}")
    print(f"\n📝 Summary:\n{result.summary.summary}")
    print(f"\n🔑 Key points:")
    for kp in result.summary.key_points:
        print(f"   • {kp}")
    print(f"\n⏱️  Tokens: input={result.input_tokens}, output={result.output_tokens}")
    print(f"💰 Cost:   ${result.cost_usd:.4f}")


if __name__ == "__main__":
    asyncio.run(_main())
