#!/usr/bin/env python3
import json
import os
import sys
import urllib.request

USERNAME = os.environ.get("LEETCODE_USERNAME", "prasanth_57")

GRAPHQL_URL = "https://leetcode.com/graphql"
QUERY = """
query getUserDetails($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      ranking
      reputation
    }
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
    userCalendar {
      streak
      totalActiveDays
    }
  }
  allQuestionsCount {
    difficulty
    count
  }
}
"""

def fetch_leetcode_data(username):
    payload = {
        "query": QUERY,
        "variables": {"username": username}
    }
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data

def generate_svg(stats):
    username = stats.get("username", USERNAME)
    streak = stats.get("streak", 0)
    active_days = stats.get("active_days", 0)
    ranking = stats.get("ranking", "N/A")
    if isinstance(ranking, int):
        ranking_str = f"#{ranking:,}"
    else:
        ranking_str = str(ranking)

    total_solved = stats.get("total_solved", 0)
    total_questions = stats.get("total_questions", 3300)
    easy_solved = stats.get("easy_solved", 0)
    easy_total = stats.get("easy_total", 800)
    medium_solved = stats.get("medium_solved", 0)
    medium_total = stats.get("medium_total", 1700)
    hard_solved = stats.get("hard_solved", 0)
    hard_total = stats.get("hard_total", 800)

    # Calculate percentages for progress bars (max width 205)
    bar_max_w = 205
    easy_pct = (easy_solved / max(1, easy_total)) if easy_total else 0
    med_pct = (medium_solved / max(1, medium_total)) if medium_total else 0
    hard_pct = (hard_solved / max(1, hard_total)) if hard_total else 0

    easy_bar_w = max(4, int(bar_max_w * min(1.0, easy_pct))) if easy_solved > 0 else 0
    med_bar_w = max(4, int(bar_max_w * min(1.0, med_pct))) if medium_solved > 0 else 0
    hard_bar_w = max(4, int(bar_max_w * min(1.0, hard_pct))) if hard_solved > 0 else 0

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
    .easy-label {{ font: 600 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #73daca; }}
    .med-label {{ font: 600 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #e0af68; }}
    .hard-label {{ font: 600 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #f7768e; }}
    .diff-val {{ font: 600 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #c0caf5; }}
    .bar-bg {{ fill: #24283b; rx: 3px; }}
  </style>

  <!-- TokyoNight Background Card -->
  <rect x="0.5" y="0.5" rx="8" height="194" stroke="#414868" stroke-width="1" width="494" fill="#1a1b26"/>

  <!-- Header with LeetCode Logo -->
  <g transform="translate(25, 24)">
    <!-- LeetCode Logo -->
    <svg viewBox="0 0 24 24" width="20" height="20" x="0" y="0">
      <path d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.261 2.87 10.507a6.273 6.273 0 0 0 0 8.87 6.273 6.273 0 0 0 8.87 0l5.802-5.802a1.374 1.374 0 1 0-1.943-1.943L9.797 17.434a3.525 3.525 0 0 1-4.984 0 3.525 3.525 0 0 1 0-4.984l3.508-3.508 4.723-4.723A1.374 1.374 0 0 0 13.483 0z" fill="#7aa2f7"/>
      <path d="M9.838 10.924a1.374 1.374 0 0 0-.971.402l-2.07 2.07a1.374 1.374 0 1 0 1.943 1.943l2.07-2.07a1.374 1.374 0 0 0-.972-2.345z" fill="#FFA116"/>
      <path d="M23.107 10.898H11.205a1.374 1.374 0 0 0 0 2.748h11.902a1.374 1.374 0 1 0 0-2.748z" fill="#FFA116"/>
    </svg>
    <text x="28" y="16" class="header">LeetCode Stats ({username})</text>
  </g>

  <!-- Left Column: Streak, Active Days, Rank, Total Solved -->
  <g transform="translate(25, 52)">
    <!-- Streak -->
    <g transform="translate(0, 20)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#ff9e64" x="0" y="-12">
        <path d="M8.5 0C8.5 0 8.7 2.2 7.7 3.5C6.7 4.8 5.2 5.5 5.2 7.2C5.2 9.1 6.8 10.7 8.7 10.7C10.6 10.7 12.2 9.1 12.2 7.2C12.2 4.2 8.5 0 8.5 0ZM8.5 16C4.4 16 1 12.6 1 8.5C1 5.6 2.6 3.1 4.9 1.8C4.6 3.1 4.9 4.5 5.7 5.5C6.4 6.4 7.5 7 8.6 7C9.3 7 10 6.7 10.5 6.3C10.8 7 11 7.7 11 8.5C11 12.6 9.9 16 8.5 16Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Current Streak:</text>
      <text class="stat-val" x="145" y="0">{streak} Days</text>
    </g>

    <!-- Active Days -->
    <g transform="translate(0, 46)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#7aa2f7" x="0" y="-12">
        <path d="M4.75 0a.75.75 0 0 1 .75.75V2h5V.75a.75.75 0 0 1 1.5 0V2h1.25c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 13.25 16H2.75A1.75 1.75 0 0 1 1 14.25V3.75C1 2.784 1.784 2 2.75 2H4V.75A.75.75 0 0 1 4.75 0ZM2.5 7.5v6.75c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25V7.5H2.5Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Active Days:</text>
      <text class="stat-val" x="145" y="0">{active_days}</text>
    </g>

    <!-- Global Rank -->
    <g transform="translate(0, 72)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#e0af68" x="0" y="-12">
        <path d="M4 2.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 .5.5v2.75a3.75 3.75 0 0 1-3.25 3.715V10.5h1.5a1.75 1.75 0 0 1 1.75 1.75v1.25a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5v-1.25A1.75 1.75 0 0 1 5.75 10.5h1.5V8.965A3.75 3.75 0 0 1 4 5.25V2.5Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Global Ranking:</text>
      <text class="stat-val" x="145" y="0">{ranking_str}</text>
    </g>

    <!-- Total Solved -->
    <g transform="translate(0, 98)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#bb9af7" x="0" y="-12">
        <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm9.78-2.22a.75.75 0 0 0-1.06-1.06L6.75 8.19 5.28 6.72a.75.75 0 0 0-1.06 1.06l2 2a.75.75 0 0 0 1.06 0l4-4Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Solved:</text>
      <text class="stat-val" x="145" y="0">{total_solved} <tspan font-weight="400" fill="#565f89" font-size="11">/{total_questions}</tspan></text>
    </g>
  </g>

  <!-- Right Column: Problems Solved Progress Breakdown -->
  <g transform="translate(260, 52)">
    <!-- Easy -->
    <g transform="translate(0, 20)">
      <text class="easy-label" x="0" y="0">Easy</text>
      <text class="diff-val" x="205" y="0" text-anchor="end">{easy_solved} <tspan fill="#565f89" font-size="11">/{easy_total}</tspan></text>
      <rect class="bar-bg" x="0" y="8" width="205" height="6" />
      <rect x="0" y="8" width="{easy_bar_w}" height="6" fill="#73daca" rx="3px" />
    </g>

    <!-- Medium -->
    <g transform="translate(0, 59)">
      <text class="med-label" x="0" y="0">Medium</text>
      <text class="diff-val" x="205" y="0" text-anchor="end">{medium_solved} <tspan fill="#565f89" font-size="11">/{medium_total}</tspan></text>
      <rect class="bar-bg" x="0" y="8" width="205" height="6" />
      <rect x="0" y="8" width="{med_bar_w}" height="6" fill="#e0af68" rx="3px" />
    </g>

    <!-- Hard -->
    <g transform="translate(0, 98)">
      <text class="hard-label" x="0" y="0">Hard</text>
      <text class="diff-val" x="205" y="0" text-anchor="end">{hard_solved} <tspan fill="#565f89" font-size="11">/{hard_total}</tspan></text>
      <rect class="bar-bg" x="0" y="8" width="205" height="6" />
      <rect x="0" y="8" width="{hard_bar_w}" height="6" fill="#f7768e" rx="3px" />
    </g>
  </g>
</svg>"""
    return svg

def main():
    print(f"Fetching LeetCode stats for {USERNAME}...")
    try:
        raw_data = fetch_leetcode_data(USERNAME)
        user_data = raw_data.get("data", {}).get("matchedUser")
        if not user_data:
            print("Error: User data not found in response.")
            sys.exit(1)

        questions = raw_data.get("data", {}).get("allQuestionsCount") or []
        q_map = {q["difficulty"]: q["count"] for q in questions if "difficulty" in q and "count" in q}

        ac_submissions = user_data.get("submitStatsGlobal", {}).get("acSubmissionNum") or []
        ac_map = {s["difficulty"]: s["count"] for s in ac_submissions if "difficulty" in s and "count" in s}

        calendar = user_data.get("userCalendar") or {}
        profile = user_data.get("profile") or {}

        stats = {
            "username": USERNAME,
            "streak": calendar.get("streak", 0),
            "active_days": calendar.get("totalActiveDays", 0),
            "ranking": profile.get("ranking", "N/A"),
            "total_solved": ac_map.get("All", 0),
            "total_questions": q_map.get("All", 3300),
            "easy_solved": ac_map.get("Easy", 0),
            "easy_total": q_map.get("Easy", 800),
            "medium_solved": ac_map.get("Medium", 0),
            "medium_total": q_map.get("Medium", 1700),
            "hard_solved": ac_map.get("Hard", 0),
            "hard_total": q_map.get("Hard", 800),
        }

        print(f"Fetched stats: Streak={stats['streak']}, Solved={stats['total_solved']}, Rank={stats['ranking']}")

        os.makedirs("assets", exist_ok=True)
        svg_content = generate_svg(stats)
        with open("assets/leetcode-stats.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)

        print("Successfully generated assets/leetcode-stats.svg with TokyoNight theme matching GitHub stats card!")

    except Exception as e:
        print(f"Error fetching/generating stats: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
