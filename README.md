<div align="center">

<!--
  COVER IMAGE — generate with this prompt, save as docs/cover.png, then uncomment below.

  Prompt (Midjourney / DALL-E 3 / Stable Diffusion XL):
  "A sleek dark terminal window showing a list of AI notebook entries glowing in soft blue,
  abstract network of interconnected nodes and pages in the background, Google color accents
  faintly visible, minimalist developer aesthetic, pure black background, cinematic banner,
  2:1 aspect ratio, no text overlay, no UI chrome"

  <img src="docs/cover.png" alt="notebooklm-cdp" width="100%">
-->

# notebooklm-cdp

Complete terminal toolkit for Google NotebookLM — Chrome-based auth via CDP, chat, source management, content generation, and Studio note access from the command line.

[![PyPI](https://img.shields.io/pypi/v/notebooklm-cdp?color=0ea5e9&label=PyPI)](https://pypi.org/project/notebooklm-cdp/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-0ea5e9.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-0ea5e9.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/nolan-vale/notebooklm-cdp?style=social)](https://github.com/nolan-vale/notebooklm-cdp)

</div>

---

## What it does

`notebooklm-cdp` is a complete terminal interface for Google NotebookLM. Install it and you get two CLI tools:

**`nlm`** — authenticates into NotebookLM using your already-open Chrome Beta browser. One command (`nlm login`) extracts your active Google session via the Chrome DevTools Protocol — no OAuth popup, no login flow, no stored passwords. `nlm` also provides convenient index-based access to Studio notes: list, read, and export them to Markdown without knowing their UUIDs.

**`notebooklm`** — the full NotebookLM API from the terminal: create and manage notebooks, add sources (URLs, PDFs, YouTube, Google Docs, audio, video), chat with your content, generate podcasts, videos, quizzes, flashcards, slide decks, infographics, reports, and mind maps, then download the results. Complete Studio note CRUD. Multi-account profiles. Clean `--json` output for every command.

---

## Who it is for

- AI agent developers who need authenticated, programmatic NotebookLM access without interactive browser sessions
- Developers using Claude Code, Codex, Cursor, or Windsurf who want to give their agent full NotebookLM access
- Automation engineers who build NotebookLM workflows — research pipelines, podcast generation, document analysis — from the terminal
- NotebookLM power users who want to manage notebooks, sources, and notes without touching the web UI

---

## Features

- **CDP auth** — reads Google session cookies from your running Chrome Beta; auto-detects the active account from the open NotebookLM tab
- **Notebooks** — create, list, rename, delete; switch context with `notebooklm use`
- **Sources** — add URLs, PDFs, YouTube videos, Google Docs, audio, video, images; wait for processing; deep web research mode
- **Chat** — ask questions, get answers with source citations, continue conversations, save history as notes
- **Content generation** — podcasts, videos, quizzes, flashcards, slide decks (PDF/PPTX), infographics, reports, mind maps, data tables
- **Studio notes** — full CRUD via `notebooklm note`; convenient index-based access via `nlm note list/read/export`
- **Profiles** — multiple Google accounts, isolated environments for parallel agents
- **`--json` output** on every command for scripting and AI agent pipelines
- **CI/CD support** — inline auth via `NOTEBOOKLM_AUTH_JSON` environment variable, no filesystem writes needed

---

## Requirements

- Chrome Beta with remote debugging enabled (`--remote-debugging-port=9222`)
- NotebookLM open in a Chrome Beta tab
- Python 3.11+

---

## Install

```bash
uv tool install notebooklm-cdp
```

> No `uv`? Run `curl -LsSf https://astral.sh/uv/install.sh | sh`, or use `pip install notebooklm-cdp`.

---

## Quick start

```bash
# 1. Start Chrome Beta with remote debugging (once per session)
/Applications/Google\ Chrome\ Beta.app/Contents/MacOS/Google\ Chrome\ Beta \
  --remote-debugging-port=9222 --profile-directory=Default

# 2. Open https://notebooklm.google.com in Chrome Beta, then authenticate
nlm login

# 3. Use the full NotebookLM CLI
notebooklm list
notebooklm create "My Research"
notebooklm source add "https://example.com/paper.pdf"
notebooklm ask "What are the key findings?"
notebooklm generate audio "Focus on practical implications"

# 4. Manage Studio notes
nlm note list -n <notebook_id>
nlm note read 1 -n <notebook_id>
nlm note export -n <notebook_id> --output notes.md
```

---

## Commands

### Authentication

| Command | Description |
|---|---|
| `nlm login` | Extract Google session from Chrome Beta via CDP |
| `notebooklm login` | Interactive browser login (fallback) |
| `notebooklm auth check` | Diagnose auth status |
| `notebooklm status` | Show active account and notebook context |

### Notebooks & Sources

| Command | Description |
|---|---|
| `notebooklm list` | List all notebooks |
| `notebooklm create "Title"` | Create a notebook |
| `notebooklm use <id>` | Set active notebook context |
| `notebooklm source add <url\|file>` | Add a source (URL, PDF, YouTube, etc.) |
| `notebooklm source list` | List sources in active notebook |
| `notebooklm source add-research "query"` | Add web research results as sources |

### Chat

| Command | Description |
|---|---|
| `notebooklm ask "question"` | Chat with notebook content |
| `notebooklm ask "question" --json` | Chat with source citations |
| `notebooklm ask "question" --save-as-note` | Save answer as a Studio note |
| `notebooklm history` | Show conversation history |

### Content Generation

| Command | Description |
|---|---|
| `notebooklm generate audio "instructions"` | Generate a podcast (Deep Dive) |
| `notebooklm generate video "instructions"` | Generate a video explainer |
| `notebooklm generate quiz` | Generate a quiz |
| `notebooklm generate flashcards` | Generate flashcards |
| `notebooklm generate slide-deck` | Generate a slide deck (PDF/PPTX) |
| `notebooklm generate report --format briefing-doc` | Generate a report |
| `notebooklm generate mind-map` | Generate a mind map |
| `notebooklm download audio ./output.mp3` | Download generated audio |
| `notebooklm artifact list` | Check generation status |

### Studio Notes

| Command | Description |
|---|---|
| `nlm note list -n <id>` | List notes with sequential index and title |
| `nlm note read <n> -n <id>` | Read note by 1-based index or UUID |
| `nlm note export -n <id> --output file.md` | Export all notes to Markdown |
| `notebooklm note list -n <id>` | Full note list with IDs |
| `notebooklm note create -n <id> --title "T" "content"` | Create a note |
| `notebooklm note save <note_id> -n <id>` | Update note content |
| `notebooklm note delete <note_id> -n <id>` | Delete a note |

---

## How auth works

`nlm login` connects to Chrome Beta's CDP endpoint at `http://127.0.0.1:9222`, finds the open NotebookLM tab, reads the active Google session cookies, and saves them to `~/.notebooklm/profiles/default/storage_state.json`. The Google account index (`authuser`) is detected automatically from the tab URL and embedded in the session file.

No passwords or credentials are stored — only the session cookies already present in your browser. Re-run `nlm login` whenever cookies expire.

---

## License

MIT — Nolan Vale
