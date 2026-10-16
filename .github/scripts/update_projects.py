#!/usr/bin/env python3
import json
import re
import urllib.request
from pathlib import Path

README_PATH = Path(__file__).resolve().parent.parent.parent / "README.md"

# Curated architecture descriptions and stack for notable repositories
PROJECT_METADATA = {
    "joyofit": {
        "title": "joyofit",
        "description": "Huawei watch companion for Android with local biometric sync",
        "stack": "`Kotlin` `Android SDK` `BLE`",
        "status": "Active",
    },
    "dynamic-qris": {
        "title": "dynamic-qris",
        "description": "EMVCo-compliant dynamic QRIS payload generator and parser",
        "stack": "`TypeScript` `Node.js`",
        "status": "Maintained",
    },
    "nano-island": {
        "title": "nano-island",
        "description": "Android foreground service with interactive status overlay",
        "stack": "`Kotlin` `Jetpack`",
        "status": "Active",
    },
    "fiBOnanci": {
        "title": "fiBOnanci",
        "description": "Finance tracking client built with native platform channels",
        "stack": "`Dart` `Flutter` `Kotlin`",
        "status": "Stable",
    },
    "ksuli-bisindo": {
        "title": "ksuli-bisindo",
        "description": "Indonesian sign language recognition experiment",
        "stack": "`JavaScript` `Machine Learning`",
        "status": "Research",
    },
}

# Order of preference for featured showcase
FEATURED_ORDER = ["joyofit", "dynamic-qris", "nano-island", "fiBOnanci", "ksuli-bisindo"]


def fetch_user_repos(username="David4rr"):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=50"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; GitHub-Readme-Updater/1.0)",
            "Accept": "application/vnd.github.v3+json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as err:
        print(f"Warning: Could not fetch from GitHub API ({err}). Using fallback cache.")
        return []


def generate_table_markdown(repos):
    repo_map = {r["name"]: r for r in repos if isinstance(r, dict) and "name" in r}

    rows = []
    rows.append("| Project | Description | Stack | Status |")
    rows.append("| :--- | :--- | :--- | :--- |")

    # Render featured curated repos first
    rendered_keys = set()
    for key in FEATURED_ORDER:
        meta = PROJECT_METADATA.get(key)
        if not meta:
            continue
        rendered_keys.add(key)
        repo_info = repo_map.get(key)
        url = repo_info["html_url"] if repo_info else f"https://github.com/David4rr/{key}"
        row = f"| **[{meta['title']}]({url})** | {meta['description']} | {meta['stack']} | {meta['status']} |"
        rows.append(row)

    return "\n".join(rows)


def update_readme():
    if not README_PATH.exists():
        print(f"README not found at {README_PATH}")
        return

    content = README_PATH.read_text(encoding="utf-8")
    start_tag = "<!-- PROJECTS:START -->"
    end_tag = "<!-- PROJECTS:END -->"

    pattern = re.compile(
        rf"({re.escape(start_tag)})(.*?)({re.escape(end_tag)})",
        re.DOTALL,
    )

    if not pattern.search(content):
        print(f"Markers {start_tag} ... {end_tag} not found in README.md")
        return

    repos = fetch_user_repos()
    table_md = generate_table_markdown(repos)
    replacement = f"{start_tag}\n{table_md}\n{end_tag}"

    new_content = pattern.sub(replacement, content)
    README_PATH.write_text(new_content, encoding="utf-8")
    print("README.md updated successfully.")


if __name__ == "__main__":
    update_readme()
