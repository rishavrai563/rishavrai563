#!/usr/bin/env python3
"""
update_repos.py
───────────────
Fetches public, non-forked repositories for rishavrai563 from the GitHub API
and injects them as a formatted Markdown list between the <!-- REPOS:START -->
and <!-- REPOS:END --> comment markers in README.md.

Uses only Python standard libraries: urllib, json, re.
"""

import urllib.request
import json
import re
import os

# ── Configuration ──────────────────────────────────────────────────────────────
USERNAME = "rishavrai563"
API_URL = (
    f"https://api.github.com/users/{USERNAME}/repos"
    f"?type=owner&sort=updated&per_page=100"
)
README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")

# Regex pattern to match the block between REPOS:START and REPOS:END markers
MARKER_PATTERN = r"(<!-- REPOS:START -->).*?(<!-- REPOS:END -->)"


def fetch_repos():
    """Fetch public repositories from the GitHub API."""
    req = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "rishavrai563-profile-updater/1.0"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def build_repo_markdown(repos):
    """Build a Markdown list of non-forked repositories with descriptions."""
    lines = []
    for repo in repos:
        # Skip forked repositories and the profile config repo itself
        if repo.get("fork"):
            continue
        if repo["name"] == USERNAME:
            continue

        name = repo["name"]
        url = repo["html_url"]
        description = repo.get("description") or "No description provided."
        language = repo.get("language") or ""

        # Build the entry with an optional language badge
        entry = f"- **[{name}]({url})**"
        if language:
            entry += f" `{language}`"
        entry += f"<br/>{description}"

        lines.append(entry)

    return "\n".join(lines)


def inject_into_readme(repo_markdown):
    """Replace content between REPOS markers in README.md using regex."""
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Use re.DOTALL so '.' matches newlines between the markers
    replacement = rf"\1\n{repo_markdown}\n\2"
    updated_content = re.sub(
        MARKER_PATTERN,
        replacement,
        readme_content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)


def main():
    print(f"⏳ Fetching repos for @{USERNAME}...")
    repos = fetch_repos()

    repo_markdown = build_repo_markdown(repos)
    repo_count = repo_markdown.count("\n") + (1 if repo_markdown else 0)
    print(f"📦 Found {repo_count} original repositories.")

    inject_into_readme(repo_markdown)
    print("✅ README.md updated successfully.")


if __name__ == "__main__":
    main()
