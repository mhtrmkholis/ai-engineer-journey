from pydantic import BaseModel, Field, HttpUrl


class Article(BaseModel):
    """Hasil scraping dari URL."""

    url: HttpUrl
    title: str
    text: str = Field(..., description="Teks artikel utama, sudah di-clean")
    word_count: int


class Summary(BaseModel):
    """Ringkasan terstruktur dari Claude."""

    title: str = Field(..., description="Judul artikel")
    tags: list[str] = Field(
        ..., min_length=3, max_length=5, description="3-5 tag relevan, lowercase"
    )
    summary: str = Field(
        ..., min_length=200, max_length=2000, description="Ringkasan 3-5 kalimat"
    )
    key_points: list[str] = Field(
        ...,
        min_length=3,
        max_length=5,
        description="3-5 poin utama, masing-masing 1 kalimat",
    )


class SummaryResult(BaseModel):
    """Output lengkap untuk display."""

    summary: Summary
    input_tokens: int
    output_tokens: int
    cost_usd: float
