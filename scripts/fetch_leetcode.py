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

    # Calculate percentages for progress bars (width 210)
    easy_pct = (easy_solved / max(1, easy_total)) if easy_total else 0
    med_pct = (medium_solved / max(1, medium_total)) if medium_total else 0
    hard_pct = (hard_solved / max(1, hard_total)) if hard_total else 0

    easy_bar_w = max(4, int(210 * min(1.0, easy_pct)))
    med_bar_w = max(4, int(210 * min(1.0, med_pct)))
    hard_bar_w = max(4, int(210 * min(1.0, hard_pct)))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195" fill="none" role="img">
  <style>
    .header {{
      font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #70a5fd;
    }}
    .stat-label {{
      font: 400 13px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #38bdae;
    }}
    .stat-val {{
      font: 700 13px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #c0caf5;
    }}
    .easy-label {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #73daca; }}
    .med-label {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #e0af68; }}
    .hard-label {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #f7768e; }}
    .diff-val {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #a9b1d6; }}
    .bar-bg {{ fill: #24283b; rx: 3px; }}
  </style>

  <!-- TokyoNight Background Card -->
  <rect x="0.5" y="0.5" rx="4.5" height="99%" stroke="#e4e2e2" stroke-opacity="0" width="494" fill="#1a1b26"/>

  <!-- Title -->
  <g transform="translate(25, 35)">
    <text x="0" y="0" class="header">LeetCode Stats ({username})</text>
  </g>

  <!-- Left Column: Streak, Active Days, Rank, Total Solved -->
  <g transform="translate(25, 50)">
    <!-- Streak -->
    <g transform="translate(0, 20)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#ff9e64" x="0" y="-12">
        <path d="M8.5 0C8.5 0 8.7 2.2 7.7 3.5C6.7 4.8 5.2 5.5 5.2 7.2C5.2 9.1 6.8 10.7 8.7 10.7C10.6 10.7 12.2 9.1 12.2 7.2C12.2 4.2 8.5 0 8.5 0ZM8.5 16C4.4 16 1 12.6 1 8.5C1 5.6 2.6 3.1 4.9 1.8C4.6 3.1 4.9 4.5 5.7 5.5C6.4 6.4 7.5 7 8.6 7C9.3 7 10 6.7 10.5 6.3C10.8 7 11 7.7 11 8.5C11 12.6 9.9 16 8.5 16Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Current Streak:</text>
      <text class="stat-val" x="145" y="0">{streak} Days</text>
    </g>

    <!-- Active Days -->
    <g transform="translate(0, 45)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#7aa2f7" x="0" y="-12">
        <path d="M4.75 0a.75.75 0 0 1 .75.75V2h5V.75a.75.75 0 0 1 1.5 0V2h1.25c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 13.25 16H2.75A1.75 1.75 0 0 1 1 14.25V3.75C1 2.784 1.784 2 2.75 2H4V.75A.75.75 0 0 1 4.75 0ZM2.5 7.5v6.75c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25V7.5H2.5Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Active Days:</text>
      <text class="stat-val" x="145" y="0">{active_days}</text>
    </g>

    <!-- Global Rank -->
    <g transform="translate(0, 70)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#e0af68" x="0" y="-12">
        <path d="M4 2.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 .5.5v2.75a3.75 3.75 0 0 1-3.25 3.715V10.5h1.5a1.75 1.75 0 0 1 1.75 1.75v1.25a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5v-1.25A1.75 1.75 0 0 1 5.75 10.5h1.5V8.965A3.75 3.75 0 0 1 4 5.25V2.5Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Global Ranking:</text>
      <text class="stat-val" x="145" y="0">{ranking_str}</text>
    </g>

    <!-- Total Solved -->
    <g transform="translate(0, 95)">
      <svg viewBox="0 0 16 16" width="16" height="16" fill="#bf91f3" x="0" y="-12">
        <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm9.78-2.22a.75.75 0 0 0-1.06-1.06L6.75 8.19 5.28 6.72a.75.75 0 0 0-1.06 1.06l2 2a.75.75 0 0 0 1.06 0l4-4Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Solved:</text>
      <text class="stat-val" x="145" y="0">{total_solved} <tspan font-weight="400" fill="#565f89" font-size="11">/{total_questions}</tspan></text>
    </g>
  </g>

  <!-- Right Column: Problems Solved Progress Breakdown -->
  <g transform="translate(255, 50)">
    <!-- Easy -->
    <g transform="translate(0, 20)">
      <text class="easy-label" x="0" y="0">Easy</text>
      <text class="diff-val" x="210" y="0" text-anchor="end">{easy_solved} <tspan fill="#565f89" font-size="11">/{easy_total}</tspan></text>
      <rect class="bar-bg" x="0" y="7" width="210" height="6" />
      <rect x="0" y="7" width="{easy_bar_w}" height="6" fill="#73daca" rx="3px" />
    </g>

    <!-- Medium -->
    <g transform="translate(0, 58)">
      <text class="med-label" x="0" y="0">Medium</text>
      <text class="diff-val" x="210" y="0" text-anchor="end">{medium_solved} <tspan fill="#565f89" font-size="11">/{medium_total}</tspan></text>
      <rect class="bar-bg" x="0" y="7" width="210" height="6" />
      <rect x="0" y="7" width="{med_bar_w}" height="6" fill="#e0af68" rx="3px" />
    </g>

    <!-- Hard -->
    <g transform="translate(0, 96)">
      <text class="hard-label" x="0" y="0">Hard</text>
      <text class="diff-val" x="210" y="0" text-anchor="end">{hard_solved} <tspan fill="#565f89" font-size="11">/{hard_total}</tspan></text>
      <rect class="bar-bg" x="0" y="7" width="210" height="6" />
      <rect x="0" y="7" width="{hard_bar_w}" height="6" fill="#f7768e" rx="3px" />
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

        questions = raw_data.get("data", {}).get("allQuestionsCount", [])
        q_map = {q["difficulty"]: q["count"] for q in questions}

        ac_submissions = user_data.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
        ac_map = {s["difficulty"]: s["count"] for s in ac_submissions}

        calendar = user_data.get("userCalendar", {})
        profile = user_data.get("profile", {})

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
