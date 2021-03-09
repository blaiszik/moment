import pandas as pd
import jsonlines
import bibtexparser
import os
import requests
import json
from datetime import date, datetime
from ghapi.all import GhApi

config = {
    "projects": "../input/projects.jsonl",
    "statistics": "../output/statistics.jsonl",
    "leaderboard": "../output/leaderboard.jsonl",
    "articles": "../output/articles.jsonl",
    "article_summary": "../output/article_summary.jsonl",
    "moment_dir": "../.moment",
    "issues": "../output/issues.jsonl",
}


# def collect_credits(proj):
#     credits = {}
#     path = os.path.join(proj["link"], moment_dir, "statistics.json")
#     with jsonlines.open(path) as reader:
#         for obj in reader:
#             user = list(obj["credits"].keys())[0]
#             if credits.get(user):
#                 credits[user] = credits[user] + obj["credits"][user]
#             else:
#                 credits[user] = obj["credits"][user]
#     return credits


def make_link(
    proj,
    repo,
    link_type="github",
    path=".moment",
    branch="main",
    file="statistics.json",
):
    # TODO: query the default branch from the API?
    # ask users to specify default branch on registration?
    if link_type == "github":
        return f"https://raw.githubusercontent.com/{proj}/{repo}/{branch}/{path}/{file}"


def get_creds(proj, repo, path):
    print(make_link(proj=proj, repo=repo, path=path))
    f = requests.get(make_link(proj=proj, repo=repo, path=path))

    if f.ok:
        decoded = f.content.decode("utf-8").split("\n")
        credits = [json.loads(obj) for obj in decoded if obj != ""]
        credits = [obj["credits"] for obj in credits]
    else:
        credits = []

    today = datetime.now()
    proj = {
        "date": today.strftime("%Y/%m/%d, %H:%M:%S"),
        "project": proj,
        "repo": repo,
        "credits": credits,
    }
    return proj


def write_creds(input_file=config["projects"], output_file=config["statistics"]):
    with jsonlines.open(input_file, mode="r") as reader:
        with jsonlines.open(output_file, "a") as writer:
            for proj in reader:
                creds = get_creds(proj["project"], proj["repo"], proj["path"])
                writer.write(creds)


def sum_credits(data: []):
    credits = {}

    for entry in data:
        for cred in entry:
            for sub in cred:
                if sub in credits:
                    credits[sub] = credits[sub] + cred[sub]
                else:
                    credits[sub] = cred[sub]

    return credits


def make_leaderboard(
    input_file=config["statistics"], output_file=config["leaderboard"]
):
    # Create a new leaderboard entry with the current time and date
    today = datetime.now()
    leaderboard = {"date": today.strftime("%Y/%m/%d, %H:%M:%S"), "credits": {}}

    df = pd.read_json(input_file, lines=True)
    df["unique"] = df["project"] + "/" + df["repo"]
    df = df.sort_values(["date"], ascending=False)

    latest = []
    groups = df.groupby(["unique"])
    for u, data in groups:
        latest.append(data.iloc[0]["credits"])

    leaderboard["credits"] = sum_credits(latest)
    with jsonlines.open(output_file, "a") as writer:
        writer.write(leaderboard)
    return leaderboard

    # Read BibTeX formatted article list from a repo


def get_articles(proj, repo, path):
    link = make_link(proj=proj, repo=repo, path=path, file="articles.bib")
    f = requests.get(make_link(proj=proj, repo=repo, path=path, file="articles.bib"))
    f.content.decode("utf-8")
    bib_database = bibtexparser.loads(f.content.decode("utf-8"))
    bib_database.entries

    today = datetime.now()
    proj = {
        "date": today.strftime("%Y/%m/%d, %H:%M:%S"),
        "project": proj,
        "repo": repo,
        "articles": bib_database.entries,
    }
    return proj


def write_articles(input_file=config["projects"], output_file=config["articles"]):
    with jsonlines.open(input_file, mode="r") as reader:
        with jsonlines.open(output_file, "a") as writer:
            for proj in reader:
                creds = get_articles(proj["project"], proj["repo"], proj["path"])
                writer.write(creds)


def make_article_summary(
    input_file=config["articles"], output_file=config["article_summary"]
):
    today = datetime.now()

    df = pd.read_json(input_file, lines=True)
    df["unique"] = df["project"] + "/" + df["repo"]
    # df = df.sort_values(['date'], ascending=False)

    summary = []
    groups = df.groupby(["unique"])
    for u, data in groups:
        entry = {
            "date": today.strftime("%Y/%m/%d, %H:%M:%S"),
            "project": "",
            "articles": None,
            "count": 0,
        }
        entry["project"] = u
        entry["count"] = len(data.iloc[0]["articles"])
        entry["articles"] = data.iloc[0]["articles"]
        summary.append(entry)

    with jsonlines.open(output_file, "a") as writer:
        writer.write(summary)


def serialize_issue(issue):
    new_issue = {}
    new_issue["user"] = dict(issue["user"])
    new_issue["title"] = issue["title"]
    new_issue["html_url"] = issue["html_url"]
    new_issue["url"] = issue["url"]
    new_issue["state"] = issue["state"]
    new_issue["body"] = issue["body"]
    new_issue["created_at"] = issue["created_at"]
    new_issue["updated_at"] = issue["updated_at"]
    new_issue["closed_at"] = issue["closed_at"]
    new_issue["labels"] = [
        {"name": label["name"], "color": label["color"]} for label in issue["labels"]
    ]
    return dict(new_issue)


def write_issues(output_file=config["issues"]):
    issues = {}
    with jsonlines.open(config["projects"], mode="r") as reader:
        for proj in reader:
            api = GhApi()
            r = api.issues.list_for_repo(
                state="open", owner=proj["project"], repo=proj["repo"]
            )
            issues[f'{proj["project"]}/{proj["repo"]}'] = [
                serialize_issue(i) for i in r
            ]
    with jsonlines.open(output_file, "a") as writer:
        writer.write(issues)
    return issues


# def write_issues():
#     with jsonlines.open(config['projects'], mode="r") as reader:
#     with jsonlines.open(config['projects'], mode="r") as reader:


# # Temporary object to hold new credits
# credits = {}

# with jsonlines.open(input_file, mode="r") as reader:
#     for obj in reader:
#         for credit in obj.get("credits", []):
#             for k in credit:
#                 if leaderboard["credits"].get(k):
#                     leaderboard["credits"][k] = (
#                         leaderboard["credits"][k] + credit[k]
#                     )
#                 else:
#                     leaderboard["credits"][k] = credit[k]
# with jsonlines.open(output_file, "a") as writer:
#     writer.write(leaderboard)
# return leaderboard


write_creds()
write_articles()
make_leaderboard()
make_article_summary()
write_issues()
