""" Parse static calltree and create call tree as Cypher statement. """

import sys
import click


filter_types = [
    "java.lang.Object",
    "java.lang.String",
    "java.lang.Long",
    "java.lang.Integer",
    "java.lang.Double",
    "java.lang.Float",
    "org.apache.commons.logging",
]


def is_filtered(instance):
    for criterion in filter_types:
        if criterion in instance:
            return True
    return False


def strip_args(line):
    """Takes com.some.thing.Class.method(this.that.SomeThing) and removes arguments and parentheses."""
    method, _ = line.split("(")
    return method


def get_method_identifier(qualified_name):
    """Takes com.some.thing.Class:method and returns Class_method."""
    parts = qualified_name.split(".")
    method_identifier = parts[-1]
    return method_identifier.replace(":", "_")


def get_class_identifier(qualified_name):
    """Takes com.some.thing.Class and returns Class."""
    parts = qualified_name.split(".")
    return parts[-1]


def is_method(source):
    return source[0] == "M"


def generate_class_relations(class_tuples):
    skip_first = True
    print("WITH [")
    for source_class, target_class in class_tuples:
        if not skip_first:
            # append comma to following lines, but not to last one.
            print(",")
        skip_first = False
        print(
            f"['{source_class}', '{target_class}']",
            end="",
        )
    print("] AS nested")
    print("UNWIND nested AS row")
    print("MERGE (n:Class {name: row[0]})")
    print("MERGE (m:Class {name: row[1]})")
    print("MERGE (n)-[r:uses]->(m)")


def generate_method_relations(method_tuples):
    skip_first = True
    print("WITH [")
    for source_method, target_method in method_tuples:
        if not skip_first:
            # append comma to following lines, but not to last one.
            print(",")
        skip_first = False
        print(
            f"['{source_method}', '{target_method}']",
            end="",
        )
    print("] AS nested")
    print("UNWIND nested AS row")
    print("MERGE (n:Method {name: row[0]})")
    print("MERGE (m:Method {name: row[1]})")
    print("MERGE (n)-[r:calls]->(m)")


def generate_with_statement(file_name: str):
    with open(file_name, "r") as fd:
        class_tuples = []
        method_tuples = []
        for line in fd.readlines():
            try:
                line = line.strip()
                source, target = line.split(" ")
                if is_method(source):
                    source_name = strip_args(source[2:])
                    target_name = strip_args(target[3:])
                    if not is_filtered(target_name):
                        method_tuples.append((source_name, target_name))
                else:
                    source_name = source[2:]
                    target_name = target
                    if not is_filtered(target_name):
                        class_tuples.append((source_name, target_name))
            except ValueError as e:
                print(e)
                print(line)
        generate_class_relations(class_tuples)
        generate_method_relations(method_tuples)


@click.command()
@click.argument("file_name")
def main(file_name):
    generate_with_statement(file_name)


if __name__ == '__main__':
    sys.exit(main())  # pylint: disable=no-value-for-parameter
