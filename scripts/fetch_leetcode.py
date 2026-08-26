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

    # Calculate percentages for progress bars (max width 180)
    easy_pct = min(100, int((easy_solved / max(1, easy_total)) * 100)) if easy_total else 0
    med_pct = min(100, int((medium_solved / max(1, medium_total)) * 100)) if medium_total else 0
    hard_pct = min(100, int((hard_solved / max(1, hard_total)) * 100)) if hard_total else 0

    easy_bar_w = int(1.8 * easy_pct)
    med_bar_w = int(1.8 * med_pct)
    hard_bar_w = int(1.8 * hard_pct)

    svg = f"""<svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #FFA116; }}
    .subtext {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8b949e; }}
    .bold-stat {{ font: 700 22px 'Segoe UI', Ubuntu, Sans-Serif; fill: #f0f6fc; }}
    .stat-label {{ font: 500 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8b949e; }}
    .easy-text {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #00b8a3; }}
    .med-text {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffc01e; }}
    .hard-text {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ef4743; }}
    .count-text {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #c9d1d9; }}
    .card-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 10px; }}
    .inner-card {{ fill: #161b22; rx: 8px; }}
  </style>

  <rect width="495" height="195" class="card-bg" />

  <!-- Title & Icon -->
  <g transform="translate(25, 30)">
    <path d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.248 5.669 4.757a1.374 1.374 0 0 0-1.942 0l-3.3 3.3a1.374 1.374 0 0 0 0 1.942l4.271 4.271a1.374 1.374 0 0 0 1.942 0l7.306-7.306a1.374 1.374 0 0 0 0-1.942L14.444.438A1.374 1.374 0 0 0 13.483 0z" fill="#FFA116" transform="translate(0, -12) scale(1.1)"/>
    <text x="26" y="0" class="header">LeetCode Profile Stats</text>
    <text x="210" y="0" class="subtext">(@{username})</text>
  </g>

  <!-- Left Column: Streak & Ranking Card -->
  <g transform="translate(25, 52)">
    <rect width="180" height="120" class="inner-card" />
    
    <!-- Streak -->
    <g transform="translate(15, 32)">
      <text x="0" y="0" font-size="18">🔥</text>
      <text x="28" y="-2" class="bold-stat">{streak}</text>
      <text x="65" y="-3" class="stat-label">Day Streak</text>
    </g>

    <!-- Active Days -->
    <g transform="translate(15, 66)">
      <text x="0" y="0" font-size="16">📅</text>
      <text x="28" y="-2" class="bold-stat">{active_days}</text>
      <text x="75" y="-3" class="stat-label">Active Days</text>
    </g>

    <!-- Ranking -->
    <g transform="translate(15, 100)">
      <text x="0" y="0" font-size="16">🏆</text>
      <text x="28" y="-2" font-weight="700" font-size="14" fill="#58a6ff" font-family="'Segoe UI', Ubuntu, Sans-Serif">Rank {ranking_str}</text>
    </g>
  </g>

  <!-- Right Column: Problems Solved Breakdown -->
  <g transform="translate(225, 52)">
    <rect width="245" height="120" class="inner-card" />

    <!-- Total Solved Header -->
    <g transform="translate(15, 25)">
      <text x="0" y="0" class="stat-label">Solved Problems:</text>
      <text x="110" y="0" font-weight="700" font-size="16" fill="#f0f6fc" font-family="'Segoe UI', Ubuntu, Sans-Serif">{total_solved}</text>
      <text x="145" y="0" class="subtext">/ {total_questions}</text>
    </g>

    <!-- Easy -->
    <g transform="translate(15, 52)">
      <text x="0" y="0" class="easy-text">Easy</text>
      <text x="180" y="0" class="count-text" text-anchor="end">{easy_solved}<tspan fill="#8b949e">/{easy_total}</tspan></text>
      <rect x="0" y="6" width="180" height="5" fill="#21262d" rx="2.5" />
      <rect x="0" y="6" width="{easy_bar_w}" height="5" fill="#00b8a3" rx="2.5" />
    </g>

    <!-- Medium -->
    <g transform="translate(15, 79)">
      <text x="0" y="0" class="med-text">Med.</text>
      <text x="180" y="0" class="count-text" text-anchor="end">{medium_solved}<tspan fill="#8b949e">/{medium_total}</tspan></text>
      <rect x="0" y="6" width="180" height="5" fill="#21262d" rx="2.5" />
      <rect x="0" y="6" width="{med_bar_w}" height="5" fill="#ffc01e" rx="2.5" />
    </g>

    <!-- Hard -->
    <g transform="translate(15, 106)">
      <text x="0" y="0" class="hard-text">Hard</text>
      <text x="180" y="0" class="count-text" text-anchor="end">{hard_solved}<tspan fill="#8b949e">/{hard_total}</tspan></text>
      <rect x="0" y="6" width="180" height="5" fill="#21262d" rx="2.5" />
      <rect x="0" y="6" width="{hard_bar_w}" height="5" fill="#ef4743" rx="2.5" />
    </g>
  </g>
</svg>
"""
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

        print("Successfully generated assets/leetcode-stats.svg!")

    except Exception as e:
        print(f"Error fetching/generating stats: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
