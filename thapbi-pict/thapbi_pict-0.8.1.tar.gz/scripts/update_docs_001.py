#!/usr/bin/env python
"""Scan RST documentation for console snippets to be updated."""

import os
import sys

SKIP = ["quick_start.rst", "commands.rst"]


def scan_rst(filename):
    with open(filename) as handle:
        lines = list(handle)
        while lines:
            line = lines.pop(0)
            if line == ".. code:: console\n":
                line = lines.pop(0)
                assert not line.strip()
                block = []
                while lines:
                    line = lines.pop(0)
                    if not line.strip("\n").strip():
                        break
                    if not block and line.startswith("     "):
                        # Over indented
                        sys.exit(
                            f"ERROR: Console entry not four space indented in {filename}:\n{line}"
                        )
                        break
                    elif not line.startswith("    "):
                        # Under indented
                        sys.exit(
                            f"ERROR: Console entry not four space indented in {filename}:\n{line}"
                        )
                        break
                    else:
                        block.append(line[4:])
                if not block[0].startswith("$ "):
                    sys.exit(
                        f"ERROR: Console entry does not start four space dollar space in {filename}:\n{block[0]}"
                    )
                assert "\n" not in block, block
                yield block
            elif ".. code:: console" in line:
                sys.exit(f"ERROR: {filename} has this line:\n{repr(line)}")


def remove_slash_continuation(block):
    for line in block:
        assert line.endswith("\n") and line.count("\n") == 1
    text = "".join(block)
    while " \\\n " in text:
        text = text.replace(" \\\n ", " \\\n")
    text = text.replace(" \\\n", " ")
    assert "\\\n" not in line, "Style issue - missing preceeding space"
    return [line + "\n" for line in text.rstrip("\n").split("\n")]


def run_commands(block):
    for line in block:
        if line.startswith("$ "):
            print(line.rstrip("\n"))
            cmd = line[2:].rstrip("\n")
            if "curl" in cmd or "wget" in cmd:
                continue
            rc = os.system(cmd)
            if rc:
                sys.exit(f"ERROR: Return code {rc}")
            print("^^^^^^^^^^^")
        else:
            print(line.rstrip("\n"))


example_root = os.path.abspath(
    os.path.join(os.path.split(__file__)[0], "..", "examples")
)
doc_root = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", "docs"))
cur_dir = os.path.abspath(os.curdir)
tmp_dir = "/tmp/"

for (dirpath, dirnames, filenames) in os.walk(doc_root):
    run_dir = os.path.relpath(dirpath, example_root)
    if run_dir.startswith("../docs/examples/"):
        run_dir = os.path.join(example_root, run_dir[len("../docs/examples/") :])
    else:
        run_dir = None
    for f in filenames:
        if not f.endswith(".rst"):
            continue
        os.chdir(cur_dir)
        filename = os.path.abspath(os.path.join(dirpath, f))
        if run_dir:
            print(f"{filename} in {run_dir}")
            os.chdir(run_dir)
        else:
            print(f"{filename} in no particular directory")
            os.chdir(tmp_dir)

        for block in scan_rst(filename):
            assert block[0].startswith("$ "), block
            block = remove_slash_continuation(block)
            if all((line.startswith("$ ") or line == "...\n") for line in block):
                # Boring all commands with no output shown
                continue

            if f in SKIP:
                print(f"{filename} - skipped")
                continue

            print()
            print(filename, run_dir)
            print("-" * len(filename))
            # for line in block:
            #      print(line[:-1])
            run_commands(block)
