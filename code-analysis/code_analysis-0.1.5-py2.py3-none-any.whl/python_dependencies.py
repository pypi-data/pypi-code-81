"""Determine package dependencies and generate Cypher statements for import into Neo4j."""

import sys
import ast
from pathlib import Path

import click


def get_dependencies(mod):
    """Extract dependencies."""
    with open(mod) as content:
        tree = ast.parse(content.read())
    return get_dependencies_from_ast(tree)


def get_dependencies_from_ast(tree):
    """Return list with imported modules found in tree."""
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)
        if isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    return imports


class Stack:
    """Simple stack class."""
    def __init__(self):
        self._stack = []

    def __len__(self):
        return len(self._stack)

    def is_empty(self):
        return len(self._stack) == 0

    def push(self, item):
        self._stack.append(item)

    def multi_push(self, items):
        for item in items:
            self.push(item)

    def pop(self):
        return self._stack.pop()

    def top(self):
        return '' if self.is_empty() else self._stack[-1]

    def __repr__(self):
        repr = ("Stack:\n")
        for item in self._stack[::-1]:
            repr += f" -- {item}\n"
        return repr


class PackageStack(Stack):
    """Package hierarchy."""
    def __init__(self):
        Stack.__init__(self)

    def package_hierarchy(self):
        return '.'.join(self._stack)


def is_package(folder: [Path]):
    """Check if folder is a Python package."""
    PACKAGE_MARKER = '__init__.py'
    return len(list(filter(lambda x: x.name == PACKAGE_MARKER, folder))) > 0


def get_package_name(path: Path):
    """Extract the base name of the path."""
    return path.stem


def build_source_name(package_name, source_base_name):
    return '.'.join((package_name, source_base_name))


def get_subfolders(folder: [Path]):
    """Return list of folders."""
    return list(filter(lambda x: x.is_dir(), folder))


def walk_hierarchy(path_to_package: Path):
    """Recursively walk package hierarchy and extract dependencies."""
    mapping = {}
    packages_stack = PackageStack()

    def process_node(path: Path):
        folder = list(path.glob('*'))
        if is_package(folder):
            packages_stack.push(get_package_name(path))
        sources = path.glob('*.py')
        for source in sources:
            source_name = build_source_name(packages_stack.package_hierarchy(), source.stem)
            dependencies = get_dependencies(source)
            mapping[source_name] = dependencies
        sub_folders = get_subfolders(folder)
        for folder in sub_folders:
            process_node(folder)
            if is_package(folder.glob('*')):
                packages_stack.pop()

    process_node(path_to_package)
    return mapping, packages_stack


def prepare_package_module_dependencies(mapping, package_name):
    modules = set()
    modules.update(mapping.keys())
    print("WITH [")
    skip_first = True
    for module in modules:
        if not skip_first:
            # append comma to following lines, but not to last one.
            print(",")
        skip_first = False
        print(
            f"  ['{package_name}', '{module}']",
            end="",
        )
    print("\n] AS nested")
    print("UNWIND nested AS row")
    print("MERGE (n:Package {name: row[0]})")
    print("MERGE (m:Module {name: row[1]})")
    print("MERGE (n)-[r:contains]->(m)")


def prepare_dependencies(mapping):
    print("WITH [")
    skip_first = True
    for module, dependencies in mapping.items():
        for dependency in dependencies:
            if not skip_first:
                # append comma to following lines, but not to last one.
                print(",")
            skip_first = False
            print(
                f"  ['{module}', '{dependency}']",
                end="",
            )
    print("\n] AS nested")
    print("UNWIND nested AS row")
    print("MERGE (n:Module {name: row[0]})")
    print("MERGE (m:Module {name: row[1]})")
    print("MERGE (n)-[r:uses]->(m)")


@click.command()
@click.argument("package_path")
def main(package_path):
    mapping, package_stack = walk_hierarchy(Path(package_path))
    prepare_package_module_dependencies(mapping, package_stack.top())
    prepare_dependencies(mapping)
    return 0


if __name__ == '__main__':
    sys.exit(main())  # pylint: disable=no-value-for-parameter
