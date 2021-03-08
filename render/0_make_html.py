import jsonlines
import json
from jinja2 import Template


def get_issues(input_file="../output/issues.jsonl"):
    with open(input_file, "r") as f:
        return json.loads(f.readlines()[-1])


def get_projects(input_file="../input/projects.jsonl"):
    issues = get_issues()
    for key, val in issues.items():
        print(key, len(val))

    projects = []
    with jsonlines.open(input_file, mode="r") as reader:
        for project in reader:
            slug = f"{project['project']}/{project['repo']}"
            print(slug)

            project["issues"] = issues[slug]
            print(project["issues"])
            labels = dict()
            for issue in project["issues"]:
                for label in issue["labels"]:
                    labels[label["name"]] = label["color"]

            project["labels"] = labels
            projects.append(project)

    return projects


def get_leaderboard(input_file="../output/leaderboard.jsonl"):
    with open(input_file, "r") as f:
        return json.loads(f.readlines()[-1])


def get_articles(input_file="../output/article_summary.jsonl"):
    with open(input_file, "r") as f:
        return json.loads(f.readlines()[-1])


def make_html(projects, leaderboard, articles):
    with open("index.jinja", "r") as f:
        tm = Template(f.read())
        text = tm.render(projects=projects, leaderboard=leaderboard, articles=articles)

    with open("index.html", "w+") as f:
        f.write(text)


projects = get_projects()
leaderboard = get_leaderboard()
articles = get_articles()

make_html(projects, leaderboard, articles)
