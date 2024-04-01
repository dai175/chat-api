from pathlib import Path

from fastapi.templating import Jinja2Templates


def create_jinja_templates(directory_name):
    base_path = Path(__file__).resolve().parent.parent
    templates_path = str(base_path / directory_name)
    return Jinja2Templates(directory=templates_path)


templates = create_jinja_templates("views/templates")
