#!/usr/bin/env python3
import json
import re
import urllib.request
from pathlib import Path

README_PATH = Path(__file__).resolve().parent.parent.parent / "README.md"

# Curated architecture descriptions and stack for notable repositories
PROJECT_METADATA = {
    "niche": {
        "title": "niche",
        "description": "Native macOS Dynamic Island companion. Implemented synchronized live lyrics engine (LRCLIB), zero-allocation vDSP audio FFT, and multi-copy clipboard (merged upstream into `raihanadf/niche`).",
        "stack": "Swift · macOS",
    },
    "joyofit": {
        "title": "joyofit",
        "description": "Reverse-engineered Android companion for Huawei wearables. Implemented two-way wearable smart replies (`RemoteInput`), Service `0x25` media controls, native BLE scanner, and `.hwt` watchface decoder.",
        "stack": "Kotlin · BLE · Android",
    },
    "musicfy": {
        "title": "musicfy",
        "description": "Custom high-loudness Android music player. Engineered Media3 ExoPlayer audio DSP pipeline with dynamic range compression and peak limiting calibrated for broadcast standards.",
        "stack": "Kotlin · Jetpack Compose · Media3",
    },
    "portfolio-website": {
        "title": "portfolio-website",
        "description": "Editorial personal web platform with 2D/3D interactive canvas. Built with Cloudflare Pages SSR, Notion API CMS, 120fps Lenis parallax, and strict `< 300 LOC` modular architecture.",
        "stack": "Astro · TypeScript · Cloudflare Pages",
    },
    "dynamic-qris": {
        "title": "dynamic-qris",
        "description": "Specification-compliant merchant dynamic QRIS EMVCo payload generator and byte-level TLV parser featuring CRC16-CCITT checksum validation.",
        "stack": "TypeScript · Node.js",
    },
    "nano-island": {
        "title": "nano-island",
        "description": "Android foreground service managing interactive floating UI overlays with system-event reactive updates.",
        "stack": "Kotlin · Jetpack Lifecycle",
    },
}

# Order of preference for featured showcase
FEATURED_ORDER = ["niche", "joyofit", "musicfy", "portfolio-website", "dynamic-qris"]

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


def generate_markdown_list(repos):
    repo_map = {r["name"]: r for r in repos if isinstance(r, dict) and "name" in r}

    entries = []
    for key in FEATURED_ORDER:
        meta = PROJECT_METADATA.get(key)
        if not meta:
            continue
        repo_info = repo_map.get(key)
        url = repo_info["html_url"] if repo_info else f"https://github.com/David4rr/{key}"
        stack_pills = " · ".join(f"`{s.strip()}`" for s in meta["stack"].split("·"))
        entry = f"**[{meta['title']}]({url})** · {stack_pills}  \n{meta['description']}"
        entries.append(entry)

    return "\n\n".join(entries)


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
    projects_md = generate_markdown_list(repos)
    replacement = f"{start_tag}\n{projects_md}\n{end_tag}"

    new_content = pattern.sub(replacement, content)
    README_PATH.write_text(new_content, encoding="utf-8")
    print("README.md updated successfully with Selected Work.")

if __name__ == "__main__":
    update_readme()
