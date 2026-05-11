import asyncio

import httpx
from bs4 import BeautifulSoup

from week_01_python.models import Article


async def fetch_article(url: str, timeout: float = 10.0) -> Article:
    """Fetch URL dan extract title + clean text body."""
    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 (compatible; AI-Engineer-Bot/0.1)"},
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
        html = response.text

    return _extract(url, html)


def _extract(url: str, html: str) -> Article:
    """Parse HTML, ambil title dan body text bersih."""
    soup = BeautifulSoup(html, "html.parser")

    # Title: prefer <title>, fallback ke <h1>
    title_tag = soup.find("title") or soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    # Buang elemen yang biasanya bukan content
    exclude_tags: list[str] = ["script", "style", "nav", "header", "footer", "aside"]
    for tag in soup(exclude_tags):
        tag.decompose()

    # Prioritas: <article>, <main>, atau <body>
    main_content = soup.find("article") or soup.find("main") or soup.body
    text = main_content.get_text(separator="\n", strip=True) if main_content else ""

    # Clean: hilangkan baris kosong berlebih
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    cleaned = "\n".join(lines)

    return Article(
        url=url,
        title=title,
        text=cleaned,
        word_count=len(cleaned.split()),
    )


# Quick manual test
async def _main():
    article = await fetch_article(
        "https://en.wikipedia.org/wiki/Artificial_intelligence"
    )
    print(f"Title: {article.title}")
    print(f"Words: {article.word_count}")
    print(f"First 300 chars:\n{article.text[:300]}...")


if __name__ == "__main__":
    asyncio.run(_main())
