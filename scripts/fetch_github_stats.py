#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
from collections import defaultdict

USERNAME = os.environ.get("GITHUB_USERNAME", "Prasanth866")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/vnd.github.v3+json",
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

# Language colors (GitHub standard)
LANG_COLORS = {
    "Python": "#3572A5",
    "TypeScript": "#3178C6",
    "JavaScript": "#F1E05A",
    "Jupyter Notebook": "#DA5B0B",
    "C++": "#F34B7D",
    "C": "#555555",
    "Java": "#B07219",
    "HTML": "#E34C26",
    "CSS": "#563D7C",
    "Shell": "#89E051",
    "Go": "#00ADD8",
    "Rust": "#DEA584",
}

def make_request(url):
    print(f"Requesting {url}...")
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Warning: request to {url} failed: {e}")
        return None

def fetch_github_data(username):
    # User Profile
    user_data = make_request(f"https://api.github.com/users/{username}") or {}
    
    # Commits count
    commit_data = make_request(f"https://api.github.com/search/commits?q=author:{username}") or {}
    total_commits = commit_data.get("total_count", 0)

    # PRs count
    pr_data = make_request(f"https://api.github.com/search/issues?q=author:{username}+type:pr") or {}
    total_prs = pr_data.get("total_count", 0)

    # Issues count
    issue_data = make_request(f"https://api.github.com/search/issues?q=author:{username}+type:issue") or {}
    total_issues = issue_data.get("total_count", 0)

    # Repos and Languages
    repos_data = make_request(f"https://api.github.com/users/{username}/repos?per_page=100") or []
    
    total_stars = 0
    lang_counts = defaultdict(int)
    for r in repos_data:
        if isinstance(r, dict):
            total_stars += r.get("stargazers_count", 0)
            lang = r.get("language")
            if lang:
                lang_counts[lang] += 1

    # Sort languages by count
    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:4]
    total_lang_repos = sum(count for _, count in sorted_langs) or 1

    top_langs = [
        {
            "name": name,
            "count": count,
            "pct": (count / total_lang_repos) * 100,
            "color": LANG_COLORS.get(name, "#7aa2f7")
        }
        for name, count in sorted_langs
    ]

    return {
        "username": username,
        "public_repos": user_data.get("public_repos", len(repos_data)),
        "followers": user_data.get("followers", 0),
        "total_commits": total_commits,
        "total_prs": total_prs,
        "total_issues": total_issues,
        "total_stars": total_stars,
        "top_langs": top_langs,
    }

def generate_svg(stats):
    username = stats.get("username", USERNAME)
    commits = stats.get("total_commits", 0)
    prs = stats.get("total_prs", 0)
    issues = stats.get("total_issues", 0)
    stars = stats.get("total_stars", 0)
    repos = stats.get("public_repos", 0)
    top_langs = stats.get("top_langs", [])

    # Format numbers
    commits_str = f"{commits:,}" if isinstance(commits, int) else str(commits)
    prs_str = f"{prs:,}" if isinstance(prs, int) else str(prs)
    stars_str = f"{stars:,}" if isinstance(stars, int) else str(stars)
    repos_str = f"{repos:,}" if isinstance(repos, int) else str(repos)

    # Build Top Languages SVG Elements
    lang_elements = []
    y_positions = [20, 48, 76, 104]
    bar_max_w = 205

    for idx, lang in enumerate(top_langs[:4]):
        y = y_positions[idx]
        name = lang["name"]
        pct = lang["pct"]
        color = lang["color"]
        bar_w = max(6, int((pct / 100) * bar_max_w))

        lang_elements.append(f"""    <g transform="translate(0, {y})">
      <circle cx="4" cy="-4" r="4" fill="{color}" />
      <text class="lang-label" x="14" y="0">{name}</text>
      <text class="diff-val" x="{bar_max_w}" y="0" text-anchor="end">{pct:.1f}%</text>
      <rect class="bar-bg" x="0" y="6" width="{bar_max_w}" height="5" />
      <rect x="0" y="6" width="{bar_w}" height="5" fill="{color}" rx="2.5px" />
    </g>""")

    lang_svg_block = "\n".join(lang_elements) if lang_elements else """    <g transform="translate(0, 20)">
      <text class="stat-label" x="0" y="0">No public repositories yet</text>
    </g>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195" fill="none" role="img">
  <style>
    .header {{
      font: 700 16px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      fill: #7aa2f7;
    }}
    .stat-label {{
      font: 500 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      fill: #a9b1d6;
    }}
    .stat-val {{
      font: 700 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      fill: #c0caf5;
    }}
    .lang-label {{
      font: 600 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      fill: #c0caf5;
    }}
    .diff-val {{
      font: 600 11px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      fill: #a9b1d6;
    }}
    .bar-bg {{ fill: #24283b; rx: 2.5px; }}
  </style>

  <!-- TokyoNight Background Card -->
  <rect x="0.5" y="0.5" rx="8" height="194" stroke="#414868" stroke-width="1" width="494" fill="#1a1b26"/>

  <!-- Header with GitHub Logo -->
  <g transform="translate(25, 24)">
    <!-- GitHub Octocat Logo -->
    <svg viewBox="0 0 24 24" width="20" height="20" x="0" y="0" fill="#7aa2f7">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
    </svg>
    <text x="28" y="16" class="header">GitHub Stats ({username})</text>
  </g>

  <!-- Left Column: Total Commits, PRs, Stars, Repos -->
  <g transform="translate(25, 52)">
    <!-- Total Commits -->
    <g transform="translate(0, 20)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#73daca" x="0" y="-12">
        <path fill-rule="evenodd" d="M10.5 8a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm.75 0a3.25 3.25 0 00-6.5 0H1.75a.75.75 0 000 1.5h3a3.25 3.25 0 006.5 0h3a.75.75 0 000-1.5h-3z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Commits:</text>
      <text class="stat-val" x="145" y="0">{commits_str}</text>
    </g>

    <!-- Total PRs -->
    <g transform="translate(0, 46)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#bb9af7" x="0" y="-12">
        <path fill-rule="evenodd" d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total PRs:</text>
      <text class="stat-val" x="145" y="0">{prs_str}</text>
    </g>

    <!-- Total Stars Earned -->
    <g transform="translate(0, 72)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#e0af68" x="0" y="-12">
        <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Stars Earned:</text>
      <text class="stat-val" x="145" y="0">{stars_str}</text>
    </g>

    <!-- Public Repositories -->
    <g transform="translate(0, 98)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#7aa2f7" x="0" y="-12">
        <path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Public Repos:</text>
      <text class="stat-val" x="145" y="0">{repos_str}</text>
    </g>
  </g>

  <!-- Right Column: Top Languages Breakdown -->
  <g transform="translate(260, 48)">
{lang_svg_block}
  </g>
</svg>"""
    return svg

def main():
    print(f"Fetching GitHub stats for {USERNAME}...")
    try:
        stats = fetch_github_data(USERNAME)
        print(f"Fetched stats: Commits={stats['total_commits']}, PRs={stats['total_prs']}, Stars={stats['total_stars']}, Repos={stats['public_repos']}")

        os.makedirs("assets", exist_ok=True)
        svg_content = generate_svg(stats)
        with open("assets/github-stats.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)

        print("Successfully generated assets/github-stats.svg with TokyoNight theme!")

    except Exception as e:
        print(f"Error fetching/generating GitHub stats: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
