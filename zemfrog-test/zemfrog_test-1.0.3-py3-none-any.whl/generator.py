from importlib import import_module
from flask import current_app
from .helper import copy_template, get_template, parse_args_to_spec, parse_paths
from zemfrog.helper import get_import_name, import_attr
from jinja2 import Template
import os


def g_init_test():
    import_name = current_app.import_name
    root_path = current_app.root_path
    tests_path = os.path.join(root_path, "tests")
    if os.path.isdir(tests_path):
        print("the 'tests' directory already exists")
        return

    print("Creating unittest... ", end="")
    copy_template("tests", tests_path)
    main_app = True if import_name == "wsgi" else False
    for root, _, files in os.walk(tests_path):
        for f in files:
            if not f.endswith(".py"):
                continue

            f = os.path.join(root, f)
            with open(f) as fp:
                data = fp.read()
                t = Template(data)
                new = t.render(import_name=import_name, main_app=main_app)

            with open(f, "w") as fp:
                fp.write(new)

    print("(done)")


def g_unit_test(name):
    specs = []
    output_dir = os.path.join(current_app.root_path, "tests")
    if not os.path.isdir(output_dir):
        print("Error: You must run 'flask test init' first")
        exit(1)

    import_name = get_import_name(current_app)
    if name in current_app.config["APIS"]:
        try:
            res = import_module(import_name + f"apis.{name}")
        except (ImportError, AttributeError):
            res = import_module(name)

        tag = res.tag
        routes = res.routes
        for detail in routes:
            url, view, methods = detail
            e = view.__name__
            spec = {
                "data": parse_args_to_spec(view),
                "method": methods[0],
                "name": tag,
                "func": e,
                "endpoint": f"{tag}.{e}",
                "paths": parse_paths(url),
            }
            specs.append(spec)
        output_dir = os.path.join(output_dir, "apis")

    elif name in current_app.config["BLUEPRINTS"]:
        try:
            bp = import_attr(import_name + f"{name}.routes.init_blueprint")()
            urls = import_module(import_name + f"{name}.urls")
        except (ImportError, AttributeError):
            bp = import_attr(f"{name}.routes.init_blueprint")()
            urls = import_module(f"{name}.urls")

        name = bp.name
        routes = urls.routes
        for detail in routes:
            url, view, methods = detail
            e = view.__name__
            spec = {
                "data": parse_args_to_spec(view),
                "method": methods[0],
                "name": name,
                "func": e,
                "endpoint": f"{name}.{e}",
                "paths": parse_paths(url),
            }
            specs.append(spec)
        output_dir = os.path.join(output_dir, "blueprints")

    else:
        print("Error: unknown resource %r" % name)
        exit(1)

    output_file = os.path.join(output_dir, f"test_{name}.py")
    if os.path.isfile(output_file):
        print("Error: The file already exists %r" % output_file)
        exit(1)

    tpl = get_template("unittest.py")
    with open(tpl) as fp:
        data = fp.read()

    print("Creating unit testing %r... " % name, end="")
    with open(output_file, "w") as fp:
        data = Template(data).render(name=name, specs=specs)
        fp.write(data)

    print("(done)")
