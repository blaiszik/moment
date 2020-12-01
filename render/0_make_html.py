import jsonlines
import json
from jinja2 import Template


def get_projects(input_file='../input/projects.jsonl'):
    projects = []
    with jsonlines.open(input_file, mode="r") as reader:
        for obj in reader:
            projects.append(obj)
    return projects

def get_leaderboard(input_file='../output/leaderboard.jsonl'):
    with open(input_file, 'r') as f:
        return json.loads(f.readlines()[-1])

def make_html(projects, leaderboard):
    with open('index.jinja', 'r') as f:
        tm = Template(f.read())
        text = tm.render(projects=projects, leaderboard=leaderboard)
        
    with open('index.html', 'w+') as f:
        f.write(text)

projects = get_projects()
leaderboard = get_leaderboard()

make_html(projects, leaderboard)
