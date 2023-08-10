import os
current = os.path.dirname(os.path.realpath(__file__))
from jinja2 import Environment, FileSystemLoader


def get_jinja_template(path: str):
    current_path = os.path.dirname(current)
    loader = FileSystemLoader(current_path)
    env = Environment(loader=loader)
    template = env.get_template(path)
    return template
