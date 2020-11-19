import jsonlines
import os
import requests
import json
from datetime import date, datetime

config = {
    "projects": "./data/input/projects.jsonl",
    "statistics": "./data/output/statistics.jsonl",
    "leaderboard": "./data/output/leaderboard.jsonl",
    "moment_dir":".moment"
}

def collect_credits(proj):
    credits = {}
    path = os.path.join(proj["link"], moment_dir, "statistics.json")
    with jsonlines.open(path) as reader:
        for obj in reader:
            user = list(obj["credits"].keys())[0]
            if credits.get(user):
                credits[user] = credits[user] + obj["credits"][user]
            else:
                credits[user] = obj["credits"][user]
    return credits


def make_link(
    proj,
    repo,
    link_type="github",
    path=".moment",
    branch="main",
    file="statistics.json",
):
    if link_type == "github":
        return f"https://raw.githubusercontent.com/{proj}/{repo}/{branch}/{path}/{file}"


def get_creds(proj, repo, path):
    print(make_link(proj=proj, repo=repo, path=path))
    f = requests.get(make_link(proj=proj, repo=repo, path=path))
    decoded = f.content.decode("utf-8").split("\n")
    credits = [json.loads(obj) for obj in decoded if obj != ""]
    credits = [obj["credits"] for obj in credits]
    proj = {"project": proj, "repo": repo, "credits": credits}
    return proj


def write_creds(input_file=config['projects'], output_file=config['statistics']):
    with jsonlines.open(input_file, mode="r") as reader:
        with jsonlines.open(output_file, "a") as writer:
            for proj in reader:
                creds = get_creds(proj["project"], proj["repo"], proj["path"])
                writer.write(creds)


def make_leaderboard(input_file=config['statistics'], output_file=config['leaderboard']):
    today = datetime.now()
    leaderboard = {"date": today.strftime("%Y/%m/%d, %H:%M:%S"), "credits": {}}
    credits = {}
    with jsonlines.open(input_file, mode="r") as reader:
        for obj in reader:
            for credit in obj.get("credits", []):
                for k in credit:
                    if leaderboard["credits"].get(k):
                        leaderboard["credits"][k] = (
                            leaderboard["credits"][k] + credit[k]
                        )
                    else:
                        leaderboard["credits"][k] = credit[k]
    with jsonlines.open(output_file, "a") as writer:
        writer.write(leaderboard)
    return leaderboard


write_creds()
make_leaderboard()
