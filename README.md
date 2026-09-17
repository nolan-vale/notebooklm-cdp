# notebooklm-cdp

**A small integration for document and knowledge workflows: Chrome-session authentication and convenient NotebookLM note access.**

[![PyPI](https://img.shields.io/pypi/v/notebooklm-cdp?color=334155)](https://pypi.org/project/notebooklm-cdp/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-334155.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-6B705C.svg)](LICENSE)

## Practical purpose

This project connects an authorized Chrome Beta session to NotebookLM workflows and makes Studio notes easier to list, read, and export as Markdown. It supports recurring document and research tasks without presenting the underlying Google product or its AI capabilities as a new system built here.

## Project contribution

Built with AI coding agents as part of [Nolan Vale's](https://github.com/nolan-vale) independent product and workflow-automation work. My contribution is defining the use case, directing implementation, checking the resulting workflow, and iterating.

This repository supplies the **`nlm` helper**. It uses Playwright for Chrome DevTools Protocol access and depends on **`notebooklm-py`** for NotebookLM operations. The separate **`notebooklm` command and its broader notebook, source, chat, and generation features come from that dependency**, not from an independently implemented NotebookLM platform in this repository. This is not an official Google integration.

## What this repository adds

- **`nlm login`** — reads Google session cookies from an already authenticated Chrome Beta session and saves a local session file for the companion library.
- **Account detection** — reads the `authuser` index from an open NotebookLM tab.
- **Studio note access** — lists notes with sequential indexes, reads a note by index or ID, and exports notes to Markdown.

The companion `notebooklm-py` package supplies the `notebooklm` CLI for notebook and source management, chat, generation, and other operations. Available commands depend on the installed upstream version; check its help before building a workflow around them.

## Requirements

- Python 3.11+
- Chrome Beta with remote debugging enabled on port 9222
- An authorized Google account already signed in, with NotebookLM open in that browser
- The companion `notebooklm` CLI available for examples that invoke it

## Install

```bash
uv tool install notebooklm-cdp
```

Alternatively, use `pip install notebooklm-cdp` in a suitable Python environment.

`nlm` is the entry point defined by this package. `notebooklm` belongs to the `notebooklm-py` dependency; depending on how tools are installed, its executable may need to be exposed separately. See the dependency's installation instructions and check `notebooklm --help`.

## Quick start

Use a dedicated browser profile for automation rather than your everyday personal profile. Sign in yourself and complete any login or multifactor checks manually.

```bash
# Authenticate from an authorized Chrome Beta session with NotebookLM open
nlm login

# These commands belong to the companion notebooklm-py CLI
notebooklm list
notebooklm create "My Research"
notebooklm source add "https://example.com/paper.pdf"
notebooklm ask "What are the key findings?"

# Note-access helpers provided by this repository
nlm note list -n <notebook_id>
nlm note read 1 -n <notebook_id>
nlm note export -n <notebook_id> --output notes.md
```

## Commands provided here

| Command | Purpose |
|---|---|
| `nlm login` | Save an authorized Chrome session for NotebookLM access |
| `nlm note list -n <id>` | List notes with sequential indexes and titles |
| `nlm note read <n> -n <id>` | Read a note by 1-based index or ID |
| `nlm note export -n <id> --output file.md` | Export notes to Markdown |

## Companion CLI examples

The following commands are provided by `notebooklm-py`, not implemented by this repository. Refer to the installed version's help for supported options.

| Workflow | Example |
|---|---|
| Check account and context | `notebooklm status` |
| Diagnose authentication | `notebooklm auth check` |
| Create or select a notebook | `notebooklm create "Title"` / `notebooklm use <id>` |
| Add and list sources | `notebooklm source add <url>` / `notebooklm source list` |
| Ask about source material | `notebooklm ask "question"` |
| Generate a briefing | `notebooklm generate report --format briefing-doc` |
| Inspect generated artifacts | `notebooklm artifact list` |
| Manage Studio notes | `notebooklm note --help` |

Google NotebookLM provides the underlying source analysis and content generation. Check generated material against its sources before using it in decisions or external communications.

## Authentication and data handling

`nlm login` connects to Chrome Beta at `http://127.0.0.1:9222`, finds an open NotebookLM tab, reads Google session cookies, and writes them to `~/.notebooklm/profiles/default/storage_state.json`. The account index is saved alongside the session state. The helper writes to the default local profile; it is not a separate multi-account management system.

**Session cookies are sensitive credentials.** This tool does not ask for your password, but the saved cookies can authorize account access. Do not commit, share, or log them. Keep the debugging endpoint local, protect the session files, and re-run login when the session expires. `nlm login` writes local files; it should not be described as a credential-free or no-filesystem-write workflow.

NotebookLM is an external service. Upload only material you are authorized to share with it. This helper is not an enterprise identity, access-control, or compliance layer.

## Development approach

Requirements and workflow design are human-directed; implementation is AI-assisted. Usability checks and iteration are part of that process. This README does not claim an independent security audit or guaranteed reliability of third-party services.

## License

MIT — Nolan Vale. Part of **Nolan Vale Tools**, the label for my independent public projects.
