"""CLI entry point untuk URL summarizer."""

import asyncio

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from week_01_python.scraper import fetch_article
from week_01_python.summarizer import summarize_article

console = Console()


def main(
    url: str = typer.Argument(..., help="URL artikel yang mau diringkas"),
    show_text: bool = typer.Option(
        False, "--show-text", help="Tampilkan preview teks artikel mentah"
    ),
) -> None:
    """Fetch URL, ringkas pakai Claude, tampilkan hasil terstruktur."""
    asyncio.run(_run(url, show_text))


async def _run(url: str, show_text: bool) -> None:
    # 1. Fetch artikel
    with console.status(f"[cyan]Fetching {url}…"):
        try:
            article = await fetch_article(url)
        except Exception as e:
            console.print(f"[red]✗ Failed to fetch URL:[/red] {e}")
            raise typer.Exit(code=1)

    console.print(
        f"[green]✓[/green] [bold]{article.title}[/bold] "
        f"[dim]({article.word_count:,} words)[/dim]"
    )

    if show_text:
        preview = article.text[:1500] + ("..." if len(article.text) > 1500 else "")
        console.print(Panel(preview, title="📰 Article preview", border_style="dim"))

    # 2. Summarize
    with console.status("[cyan]Calling Claude…"):
        try:
            result = await summarize_article(article)
        except Exception as e:
            console.print(f"[red]✗ Failed to summarize:[/red] {e}")
            raise typer.Exit(code=1)

    # 3. Pretty print
    console.print()
    console.print(
        Panel(
            f"[bold cyan]{result.summary.title}[/bold cyan]\n\n"
            f"[yellow]Tags:[/yellow] {', '.join(result.summary.tags)}",
            title="📄 Summary",
            border_style="cyan",
        )
    )

    console.print("\n[bold]🔑 Key Points[/bold]")
    for kp in result.summary.key_points:
        console.print(f"  [green]•[/green] {kp}")

    table = Table(show_header=False, title="\n📊 Stats", title_style="bold")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white", justify="right")
    table.add_row("Input tokens", f"{result.input_tokens:,}")
    table.add_row("Output tokens", f"{result.output_tokens:,}")
    table.add_row("Cost", f"${result.cost_usd:.4f}")
    console.print(table)


def app() -> None:
    """Entry point untuk pyproject.toml [project.scripts]"""
    typer.run(main)


if __name__ == "__main__":
    app()
