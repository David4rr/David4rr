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
        "description": "Huawei watch companion for Android with local bio-sync",
        "stack": "Kotlin · BLE · Android",
        "status": "Active",
    },
    "dynamic-qris": {
        "title": "dynamic-qris",
        "description": "Dynamic QRIS EMVCo payload generator and parser",
        "stack": "TypeScript · Node.js",
        "status": "Maintained",
    },
    "nano-island": {
        "title": "nano-island",
        "description": "Android foreground service with interactive status overlay",
        "stack": "Kotlin · Jetpack",
        "status": "Active",
    },
    "fiBOnanci": {
        "title": "fiBOnanci",
        "stack": "Flutter · Dart · Kotlin",
        "status": "Stable",
        "description": "Finance tracking client with native platform channels",
    },
    "ksuli-bisindo": {
        "title": "ksuli-bisindo",
        "description": "Indonesian sign language BISINDO recognition ML",
        "stack": "JS · Machine Learning",
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


def generate_ascii_table(repos):
    repo_map = {r["name"]: r for r in repos if isinstance(r, dict) and "name" in r}

    widths = [14, 58, 24, 10]
    top = "┌" + "┬".join("─" * (w + 2) for w in widths) + "┐"
    mid = "├" + "┼".join("─" * (w + 2) for w in widths) + "┤"
    bot = "└" + "┴".join("─" * (w + 2) for w in widths) + "┘"
    headers = ["Project", "Scope & Architecture", "Primary Stack", "Status"]

    lines = ["<pre>", top]
    h_line = "│" + "│".join(f" {h:<{w}} " for h, w in zip(headers, widths)) + "│"
    lines.append(h_line)
    lines.append(mid)

    links_list = []
    for key in FEATURED_ORDER:
        meta = PROJECT_METADATA.get(key)
        if not meta:
            continue
        repo_info = repo_map.get(key)
        url = repo_info["html_url"] if repo_info else f"https://github.com/David4rr/{key}"
        proj_link = f'<a href="{url}">{meta["title"]}</a>'
        proj_pad = widths[0] - len(meta["title"])
        row = f'│ {proj_link}{" " * proj_pad} │ {meta["description"]:<{widths[1]}} │ {meta["stack"]:<{widths[2]}} │ {meta["status"]:<{widths[3]}} │'
        lines.append(row)
        links_list.append(f'[{meta["title"]}]({url})')

    lines.append(bot)
    lines.append("</pre>")
    lines.append("")
    lines.append("`Quick links:` " + " / ".join(links_list))
    return "\n".join(lines)


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
    table_md = generate_ascii_table(repos)
    replacement = f"{start_tag}\n{table_md}\n{end_tag}"

    new_content = pattern.sub(replacement, content)
    README_PATH.write_text(new_content, encoding="utf-8")
    print("README.md updated successfully with ASCII table.")


if __name__ == "__main__":
    update_readme()
