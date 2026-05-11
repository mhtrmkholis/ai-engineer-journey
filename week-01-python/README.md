# Week 1 — URL Article Summarizer

CLI tool yang membaca artikel dari URL dan menghasilkan ringkasan terstruktur menggunakan Claude API.

Bagian dari [AI Engineer Journey](https://github.com/<username>/ai-engineer-journey) — Week 1 deliverable: belajar Python untuk AI workflow.

## Demo

```
$ uv run summarize https://en.wikipedia.org/wiki/Large_language_model

✓ Large language model - Wikipedia (17,335 words)

📄 Summary
   Large Language Model
   Tags: ai, nlp, machine-learning, transformer, deep-learning

📝 Ringkasan
   LLM adalah jaringan saraf tiruan berbasis transformer yang dilatih
   pada dataset teks masif untuk tugas NLP...

🔑 Key Points
  • LLM menggunakan arsitektur transformer (sejak 2017)
  • Training melibatkan tokenisasi, pretraining, dan fine-tuning
  • RLHF digunakan untuk alignment dengan preferensi manusia

📊 Stats
  Input tokens   8,408
  Output tokens    711
  Cost          $0.0359
```

## Tech Stack

- **Python 3.12** + **uv** (package management)
- **Pydantic v2** (data validation, structured LLM output via JSON schema)
- **Anthropic SDK** (Claude API, async client)
- **httpx** + **BeautifulSoup4** (async URL fetching, HTML parsing)
- **typer** + **rich** (CLI + pretty terminal output)
- **pytest** + **pytest-asyncio** (testing dengan mocked API)

## Pattern AI Engineering yang Digunakan

- **Structured output via tool use** — Pydantic schema → JSON schema → forced tool_choice ke Claude → typed result
- **Async I/O** — non-blocking URL fetch dan API call
- **Token & cost tracking** — observability dasar dari awal
- **Schema validation** — output Claude divalidasi Pydantic, garbage in = visible error

## Setup

```bash
git clone <repo-url>
cd week-01-python
uv sync
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Usage

```bash
uv run summarize <url>
uv run summarize --show-text <url>     # plus preview teks artikel
uv run summarize --help                 # show all options
```

## Run Tests

```bash
uv run pytest -v
```

## Project Structure

```
src/week_01_python/
├── cli.py          # typer CLI entry point
├── config.py       # env + settings (pydantic-settings)
├── models.py       # Pydantic models (Article, Summary, SummaryResult)
├── scraper.py      # httpx async fetcher + bs4 extractor
└── summarizer.py   # Claude API call + tool use parsing

tests/
├── test_scraper.py    # pure logic tests
└── test_summarizer.py # mocked API tests
```

## Apa yang Dipelajari di Week 1

- Python fundamentals untuk dev TS/JS background
- Modern stack: uv, Pydantic v2, type hints, ruff
- Async/await Python (vs Node intuition)
- Anthropic SDK + tool use untuk structured output
- src/ layout, pytest, mocking external API
- Cost & token awareness dari API LLM

---

Built as part of [AI Engineer Roadmap 2026](../README.md).