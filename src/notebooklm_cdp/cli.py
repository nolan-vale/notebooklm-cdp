"""CLI entry point: nlm."""

import click
from notebooklm_cdp import __version__

_NOTEBOOK_OPTION = click.option(
    "-n", "--notebook",
    envvar="NOTEBOOKLM_NOTEBOOK",
    default=None,
    metavar="ID",
    help="Notebook ID (or set NOTEBOOKLM_NOTEBOOK env var).",
)


@click.group()
@click.version_option(__version__, prog_name="nlm")
def cli() -> None:
    """NotebookLM CLI — CDP auth + Studio note reading."""


@cli.command()
def login() -> None:
    """Extract Google auth cookies from running Chrome Beta via CDP."""
    from notebooklm_cdp.auth import do_login
    do_login()


@cli.group()
def note() -> None:
    """Read and export Studio notes from NotebookLM."""


@note.command("list")
@_NOTEBOOK_OPTION
def note_list(notebook: str | None) -> None:
    """List Studio notes with index, title and ID."""
    from notebooklm_cdp.notes import list_notes
    list_notes(notebook)


@note.command("read")
@click.argument("ref")
@_NOTEBOOK_OPTION
def note_read(ref: str, notebook: str | None) -> None:
    """Read a note by 1-based index or note ID."""
    from notebooklm_cdp.notes import read_note
    read_note(notebook, ref)


@note.command("export")
@_NOTEBOOK_OPTION
@click.option("--output", "-o", default=None, metavar="FILE", help="Output file (default: stdout).")
def note_export(notebook: str | None, output: str | None) -> None:
    """Export all Studio notes to a single Markdown file."""
    from notebooklm_cdp.notes import export_notes
    export_notes(notebook, output)
