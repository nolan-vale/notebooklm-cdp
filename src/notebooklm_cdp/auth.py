"""CDP login: extract Google auth cookies from running Chrome Beta."""

import json
import re
import sys
from pathlib import Path

CDP_URL = "http://127.0.0.1:9222"
PROFILE_DIR = Path.home() / ".notebooklm/profiles/default"
STORAGE_PATH = PROFILE_DIR / "storage_state.json"
AUTHUSER_PATH = PROFILE_DIR / "authuser"
NOTEBOOKLM_HOST = "notebooklm.google.com"


def _is_google_domain(domain: str) -> bool:
    d = domain.lstrip(".")
    return d == "google.com" or d.endswith(".google.com")


def do_login() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run: uv tool install notebooklm-cdp")
        sys.exit(1)

    print(f"Connecting to Chrome Beta at {CDP_URL}...")

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(CDP_URL)
        except Exception as exc:
            print(f"Cannot connect to Chrome Beta: {exc}")
            print("Start Chrome Beta first:  cba")
            sys.exit(1)

        authuser = "0"
        notebooklm_page = None

        for context in browser.contexts:
            for page in context.pages:
                if NOTEBOOKLM_HOST in page.url:
                    notebooklm_page = page
                    match = re.search(r"[?&]authuser=(\d+)", page.url)
                    if match:
                        authuser = match.group(1)
                    print(f"Found NotebookLM tab: authuser={authuser}  ({page.url[:80]})")
                    break
            if notebooklm_page:
                break

        if not notebooklm_page:
            print(f"No NotebookLM tab found in Chrome Beta.")
            print(f"Open https://{NOTEBOOKLM_HOST} in Chrome Beta first.")
            browser.close()
            sys.exit(1)

        page_cookies = notebooklm_page.context.cookies()
        google_cookies = [
            {
                "name": c["name"],
                "value": c["value"],
                "domain": c["domain"],
                "path": c.get("path", "/"),
                "expires": c.get("expires", -1),
                "httpOnly": c.get("httpOnly", False),
                "secure": c.get("secure", False),
                "sameSite": c.get("sameSite", "None"),
            }
            for c in page_cookies
            if _is_google_domain(c.get("domain", ""))
        ]

        browser.close()

    if not any(c["name"] == "SID" for c in google_cookies):
        print("SID cookie not found — not logged into Google in Chrome Beta.")
        sys.exit(1)

    storage_state = {
        "cookies": google_cookies,
        "origins": [],
        "notebooklm": {"account": {"authuser": int(authuser)}},
    }
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    STORAGE_PATH.write_text(json.dumps(storage_state, indent=2, ensure_ascii=False), encoding="utf-8")
    STORAGE_PATH.chmod(0o600)
    PROFILE_DIR.chmod(0o700)
    AUTHUSER_PATH.write_text(authuser, encoding="utf-8")

    print(f"Saved {len(google_cookies)} Google cookies → {STORAGE_PATH}")
    print(f"authuser={authuser} → {AUTHUSER_PATH}")
    print("Run:  notebooklm status")
