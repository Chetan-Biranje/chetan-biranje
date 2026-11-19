#!/usr/bin/env python3
"""Fetch the contribution calendar and a few profile numbers into data/contributions.json.

Runs inside GitHub Actions, where GITHUB_TOKEN may call the GraphQL API.
"""
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

LOGIN = os.getenv("PROFILE_LOGIN", "Chetan-Biranje")
TOKEN = os.environ["GH_TOKEN"]
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

QUERY = """query($login:String!){user(login:$login){
  repositories(ownerAffiliations:OWNER,privacy:PUBLIC){totalCount}
  contributionsCollection{contributionCalendar{totalContributions
    weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""


def api(payload):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "profile-readme-renderer"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def rest(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "profile-readme-renderer"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


data = api({"query": QUERY, "variables": {"login": LOGIN}})
if data.get("errors"):
    raise SystemExit(data["errors"])
user = data["data"]["user"]
cal = user["contributionsCollection"]["contributionCalendar"]

weeks = [
    [{"date": d["date"], "count": d["contributionCount"], "level": LEVELS.get(d["contributionLevel"], 0)}
     for d in w["contributionDays"]]
    for w in cal["weeks"]
]
days = [d for w in weeks for d in w]
today = dt.date.today().isoformat()
days = [d for d in days if d["date"] <= today]  # drop future cells

monthly = {}
for d in days:
    monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
months = [{"label": k, "count": v} for k, v in sorted(monthly.items())[-12:]]

longest = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)

by_date = {d["date"]: d["count"] for d in days}
cursor = dt.date.today()
if not by_date.get(cursor.isoformat()):
    cursor -= dt.timedelta(days=1)  # today may not have activity yet
current = 0
while by_date.get(cursor.isoformat(), 0) > 0:
    current += 1
    cursor -= dt.timedelta(days=1)

weekday = {}
for d in days:
    if d["count"]:
        name = dt.date.fromisoformat(d["date"]).strftime("%A")
        weekday[name] = weekday.get(name, 0) + d["count"]

stars = 0
page = 1
while True:
    repos = rest(f"/users/{LOGIN}/repos?per_page=100&page={page}&type=owner")
    if not repos:
        break
    stars += sum(r["stargazers_count"] for r in repos)
    page += 1

out = {
    "total": cal["totalContributions"],
    "months": months,
    "weeks": weeks,
    "current_streak": current,
    "longest_streak": longest,
    "active_days": sum(1 for d in days if d["count"]),
    "busiest_day": max(weekday, key=weekday.get) if weekday else "-",
    "repos": user["repositories"]["totalCount"],
    "stars": stars,
}
Path("data").mkdir(exist_ok=True)
Path("data/contributions.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("wrote data/contributions.json", out["total"], "contributions")
