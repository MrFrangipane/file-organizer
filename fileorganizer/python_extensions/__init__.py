import os.path

_HERE = os.path.dirname(__file__)


def make_resource_filepath(filename):
    return os.path.join(os.path.dirname(_HERE), "resources", filename)


def sanitize(name: str) -> str:
    return name.lower().replace(" ", "-").replace("'", "").replace("/", "-").replace("\\", "-").replace('"', "")
