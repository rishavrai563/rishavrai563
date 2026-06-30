import urllib.request
import json
import re

USERNAME = "rishavrai563"
API_URL = f"https://api.github.com/users/{USERNAME}/repos?type=owner&sort=updated&per_page=100"

def fetch_repos():
    # Fetch repository data from GitHub API
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def update_readme(repo_list_markdown):
    # Read the current README
    with open("README.md", "r", encoding="utf-8") as file:
        readme = file.read()

    # Replace content between the start and end markers
    new_readme = re.sub(
        r"(\n).*?()",
        f"\\1{repo_list_markdown}\n\\2",
        readme,
        flags=re.DOTALL
    )

    # Write the updated README back to the file
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_readme)

if __name__ == "__main__":
    repos = fetch_repos()
    
    markdown = ""
    for repo in repos:
        # Ignore forked repositories to keep the profile focused on your original work
        if not repo['fork']:
            desc = repo['description'] or "No description provided."
            url = repo['html_url']
            name = repo['name']
            markdown += f"* **[{name}]({url})**<br/>{desc}\n\n"

    update_readme(markdown)
    print("README.md updated successfully with latest repositories.")
