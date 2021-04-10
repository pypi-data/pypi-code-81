"""Generate Cypher code from JDepend output for analysis of Java package dependencies."""

import sys
import xml.etree.ElementTree as ET

import click


def extract_dependencies(dependency_file):
    """Parse JDepend XML and extract package dpendencies."""
    tree = ET.parse(dependency_file)
    root = tree.getroot()
    node_packages = root.find('Packages')
    package_dependencies = {}
    for pnode in node_packages.findall('Package'):
        package_name = pnode.get('name')
        node_dependends = pnode.find('DependsUpon')
        dependends = []
        if node_dependends is not None:
            for dnode in node_dependends.findall('Package'):
                dependends.append(dnode.text)
        package_dependencies[package_name] = dependends
    return package_dependencies


def prepare_packages(mapping):
    """Generate a node for each package.

    For dependend packages no node will be generated because this will happen when generating relations.
    Here we generate nodes only because packages without dependencies would get lost.
    """
    print("WITH [")
    skip_first = True
    for package in mapping.keys():
        if not skip_first:
            # append comma to following lines, but not to last one.
            print(",")
        skip_first = False
        print(
            f"  ['{package}']",
            end="",
        )
    print("\n] AS nested")
    print("UNWIND nested AS row")
    print("MERGE (n:Package {name: row[0]})")


def prepare_dependencies(mapping):
    """Generate nodes and relations for depencies."""
    print("WITH [")
    skip_first = True
    for package, dependencies in mapping.items():
        for dependency in dependencies:
            if not skip_first:
                # append comma to following lines, but not to last one.
                print(",")
            skip_first = False
            print(
                f"  ['{package}', '{dependency}']",
                end="",
            )
    print("\n] AS nested")
    print("UNWIND nested AS row")
    print("MERGE (n:Package {name: row[0]})")
    print("MERGE (m:Package {name: row[1]})")
    print("MERGE (n)-[r:depends_on]->(m)")


@click.command()
@click.argument("dependency_file")
def main(dependency_file):
    mapping = extract_dependencies(dependency_file)
    prepare_packages(mapping)
    prepare_dependencies(mapping)


if __name__ == '__main__':
    sys.exit(main())  # pylint: disable=no-value-for-parameter
