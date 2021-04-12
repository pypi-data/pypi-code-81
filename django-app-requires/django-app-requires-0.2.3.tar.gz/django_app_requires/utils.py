from fastutils import listutils
from magic_import import import_from_string

def add_requires(apps, all_apps=None):
    all_apps = all_apps or set()
    applists = []
    for app in apps:
        if app in all_apps:
            continue
        all_apps.add(app)
        deps_path = app + ".app_requires"
        app_new_requires = import_from_string(deps_path)
        if app_new_requires:
            applists += add_requires(app_new_requires, all_apps)
        applists.append(app)
    return listutils.unique(applists)
