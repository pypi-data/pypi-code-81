import os

from zemfrog.scaffold import Scaffold
from zemfrog.helper import import_attr

def init_app(app: Scaffold):
    template_dir = os.path.join(app.root_path, app.template_folder)
    searchpath = app.jinja_loader.searchpath
    next_idx = searchpath.index(template_dir) + 1
    for theme in app.config.get("ZEMFROG_THEMES", []):
        theme = import_attr(f"{theme}.get_template")()
        if theme not in searchpath:
            searchpath.insert(next_idx, theme)
