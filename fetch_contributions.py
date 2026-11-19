
import json, os, urllib.request, datetime
from pathlib import Path

login = "Chetan-Biranje"
token = os.environ["GH_TOKEN"]
query = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
payload = json.dumps({"query": query, "variables": {"login": login}}).encode()
request = urllib.request.Request(
    "https://api.github.com/graphql", data=payload,
    headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "profile-readme"}
)
with urllib.request.urlopen(request) as response:
    result = json.load(response)
if result.get("errors"):
    raise RuntimeError(result["errors"])

calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = calendar["weeks"]
days = [day for week in weeks for day in week["contributionDays"]]
monthly = {}
for day in days:
    key = day["date"][:7]
    monthly[key] = monthly.get(key, 0) + day["contributionCount"]

active = [day for day in days if day["contributionCount"] > 0]
counts = {datetime.date.fromisoformat(day["date"]): day["contributionCount"] for day in days}
run = longest = 0
for day in sorted(counts):
    run = run + 1 if counts[day] else 0
    longest = max(longest, run)

today = datetime.date.today()
cursor = today if counts.get(today, 0) else today - datetime.timedelta(days=1)
current = 0
while counts.get(cursor, 0):
    current += 1
    cursor -= datetime.timedelta(days=1)

weekday_counts = {}
for day in active:
    weekday = datetime.date.fromisoformat(day["date"]).strftime("%A")
    weekday_counts[weekday] = weekday_counts.get(weekday, 0) + day["contributionCount"]

output = {
    "total": calendar["totalContributions"],
    "months": [{"label": key, "count": value} for key, value in sorted(monthly.items())[-12:]],
    "weeks": [week["contributionDays"] for week in weeks],
    "current_streak": current,
    "longest_streak": longest,
    "active_days": len(active),
    "busiest_day": max(weekday_counts, key=weekday_counts.get) if weekday_counts else "—"
}
Path("data/contributions.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
