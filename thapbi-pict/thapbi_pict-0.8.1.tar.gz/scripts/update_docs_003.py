#!/usr/bin/env python
"""Scan RST documentation for console snippets to be updated."""

import os
import subprocess
import sys

SKIP = ["development_notes.rst", "installation.rst", "quick_start.rst", "commands.rst"]


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


def parse_block(block):
    block = list(block)  # copy
    assert block[0].startswith("$ ")
    while block:
        out = ""
        line = block.pop(0)
        assert line.startswith("$ "), line
        cmd = line[2:].lstrip().rstrip()
        while cmd.endswith("\\"):
            line = block.pop(0)
            assert not line.startswith("$ "), line
            cmd = cmd[:-1].strip() + " " + line.strip()
        while block and not block[0].startswith("$ "):
            out += block.pop(0)
        yield cmd, out


def fasta_wrap(text):
    new = []
    lines = text.split("\n")
    while lines:
        line = lines.pop(0)
        if line.startswith(">"):
            new.append(line)
            line = lines.pop(0)
            while len(line) > 80:
                new.append(line[:80])
                line = line[80:]
        new.append(line)
    return "\n".join(new)


assert (
    fasta_wrap(">Silly\n" + "ATCG" * 25) == ">Silly\n" + "ATCG" * 20 + "\n" + "ATCG" * 5
), fasta_wrap(">Silly\n" + "ATCG" * 100)


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

        print("=" * len(filename))
        print(filename)
        if f in SKIP:
            print("will skip running commands")
        elif run_dir:
            print(f"in {run_dir}")
        else:
            print("in no particular directory")
        print("=" * len(filename))

        for block in scan_rst(filename):
            if f in SKIP:
                continue

            if run_dir:
                os.chdir(run_dir)
            else:
                os.chdir(tmp_dir)

            for cmd, old_out in parse_block(block):
                print("$ " + cmd)
                if cmd.startswith("cd "):
                    os.chdir(cmd[3:])
                    continue
                if cmd.startswith("thapbi_pict ... "):
                    continue
                (exitcode, new_out) = subprocess.getstatusoutput(cmd)
                if new_out and not new_out.endswith("\n"):
                    new_out += "\n"
                if new_out.startswith(">") or "\n>" in new_out:
                    new_out = fasta_wrap(new_out)
                if old_out == "...\n" or old_out == new_out:
                    pass
                    # print("OK")
                elif "\t" in new_out:
                    print("TODO - tabs")
                    pass
                else:
                    print("---- Old:")
                    print(old_out)
                    print("---- New:")
                    print(new_out)
                    print("---- End")
                if exitcode:
                    sys.exit(f"ERROR, cmd failed, exit code {exitcode}")
