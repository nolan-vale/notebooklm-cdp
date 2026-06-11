"""Studio note reading via notebooklm-py v0.7+ API."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path


def _require_notebook(notebook: str | None) -> str:
    nb = notebook or os.environ.get("NOTEBOOKLM_NOTEBOOK")
    if not nb:
        print("Error: notebook ID required. Use -n <id> or set NOTEBOOKLM_NOTEBOOK.", file=sys.stderr)
        sys.exit(1)
    return nb


def _run(coro):
    return asyncio.run(coro)


def list_notes(notebook: str | None) -> None:
    from notebooklm.client import NotebookLMClient

    nb_id = _require_notebook(notebook)

    async def _fetch():
        async with NotebookLMClient.from_storage() as client:
            return await client.notes.list(nb_id)

    notes = _run(_fetch())

    if not notes:
        print("No notes found.")
        return

    col_w = 42
    print(f"{'#':<4}  {'Title':<{col_w}}  ID")
    print("-" * (4 + 2 + col_w + 2 + 36))
    for i, n in enumerate(notes, 1):
        title = (n.title[: col_w - 2] + "..") if len(n.title) > col_w else n.title
        print(f"{i:<4}  {title:<{col_w}}  {n.id}")


def read_note(notebook: str | None, ref: str) -> None:
    from notebooklm.client import NotebookLMClient

    nb_id = _require_notebook(notebook)

    async def _fetch():
        async with NotebookLMClient.from_storage() as client:
            if ref.isdigit():
                notes = await client.notes.list(nb_id)
                idx = int(ref) - 1
                if idx < 0 or idx >= len(notes):
                    print(f"Error: index {ref} out of range (1..{len(notes)}).", file=sys.stderr)
                    sys.exit(1)
                return notes[idx]
            note = await client.notes.get(nb_id, ref)
            if note is None:
                print(f"Error: note '{ref}' not found.", file=sys.stderr)
                sys.exit(1)
            return note

    note = _run(_fetch())
    print(f"# {note.title}\n")
    print(note.content)


def export_notes(notebook: str | None, output: str | None) -> None:
    from notebooklm.client import NotebookLMClient

    nb_id = _require_notebook(notebook)

    async def _fetch():
        async with NotebookLMClient.from_storage() as client:
            return await client.notes.list(nb_id)

    notes = _run(_fetch())

    if not notes:
        print("No notes found.")
        return

    parts = []
    for n in notes:
        parts.append(f"# {n.title}\n\n{n.content}")
    text = "\n\n---\n\n".join(parts) + "\n"

    if output:
        Path(output).write_text(text, encoding="utf-8")
        print(f"Exported {len(notes)} notes → {output}")
    else:
        print(text)
