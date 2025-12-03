#!/usr/bin/env python3
import os
import json
import urllib.request
from datetime import datetime, timezone

ORG = os.environ["ORG_NAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

API_URL = f"https://api.github.com/orgs/{ORG}/repos?per_page=5&sort=created&direction=desc"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def fetch_recent_repos():
    req = urllib.request.Request(API_URL, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode("utf-8")
    return json.loads(data)

def format_repo(repo):
    name = repo["name"]
    url = repo["html_url"]
    desc = repo["description"] or ""
    created = repo["created_at"]  # ISO8601
    created = created.replace("T", " ").replace("Z", " UTC")
    language = repo.get("language") or "—"
    return f"- [{name}]({url}) — {desc} _(язык: {language}, создан: {created})_"

def build_readme(repos):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append("# Организация IU5-14B\n")
    lines.append("Автоматически обновляемый профиль организации.\n")
    lines.append("## 📂 Последние созданные репозитории\n")

    if not repos:
        lines.append("_Пока нет репозиториев._\n")
    else:
        for r in repos:
            lines.append(format_repo(r))

    lines.append("\n---")
    lines.append(f"_Последнее обновление: {now}_")
    lines.append("\n")
    return "\n".join(lines)

def main():
    repos = fetch_recent_repos()
    content = build_readme(repos)

    os.makedirs("profile", exist_ok=True)
    readme_path = os.path.join("profile", "README.md")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README.md updated.")

if __name__ == "__main__":
    main()
