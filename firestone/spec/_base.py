"""
Base functions for managing spec files
"""
import jinja2
import yaml

JINJA_ENV = jinja2.Environment(
    loader=jinja2.PackageLoader("firestone", package_path="schema"),
    autoescape=jinja2.select_autoescape(),
)


def yaml_pretty(data, indent=2):
    dump = yaml.dump(data, indent=2)
    res = ""
    for line in dump.split("\n"):
        res += " " * indent + line + "\n"
    return res


JINJA_ENV.filters["yaml_pretty"] = yaml_pretty
