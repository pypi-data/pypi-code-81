#!/usr/bin/env python
"""Scan RST documentation for console snippets to be updated."""

import os
import subprocess
import sys
import tempfile

SKIP = ["development_notes.rst", "installation.rst", "quick_start.rst"]


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


def run_cmd(cmd):
    child = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return child.stdout, child.stderr


def tsv_align(text):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as handle:
        handle.write(text)
        filename = handle.name
    output = subprocess.getoutput(f"xsv table -d '\t' {filename}")
    os.remove(filename)
    # Remove any trailing whitespace for RST readiness
    output = "\n".join(line.rstrip() for line in output.split("\n"))
    return output.rstrip("\n") + "\n"


def fasta_wrap(text):
    new = []
    lines = text.split("\n")
    while lines:
        line = lines.pop(0)
        if line.startswith(">"):
            while len(line) > 80 and " " in line:
                cut = line
                while len(cut) > 80 and " " in cut:
                    cut, rest = cut.rsplit(" ", 1)
                new.append(cut)
                line = line[len(cut) + 1 :].lstrip()
                del cut
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

assert (
    fasta_wrap(">Silly" + " blah" * 15 + "\n" + "ATCG")
    == ">Silly" + " blah" * 14 + "\nblah\nATCG"
), fasta_wrap(">Silly" + " blah" * 15 + "\n" + "ATCG")
assert (
    fasta_wrap(">Silly!" + " blah" * 15 + "\n" + "ATCG")
    == ">Silly!" + " blah" * 14 + "\nblah\nATCG"
), fasta_wrap(">Silly!" + " blah" * 15 + "\n" + "ATCG")
assert (
    fasta_wrap(">Silly!!" + " blah" * 15 + "\n" + "ATCG")
    == ">Silly!!" + " blah" * 14 + "\nblah\nATCG"
), fasta_wrap(">Silly!!" + " blah" * 15 + "\n" + "ATCG")
assert (
    fasta_wrap(">Silly!!?" + " blah" * 15 + "\n" + "ATCG")
    == ">Silly!!?" + " blah" * 14 + "\nblah\nATCG"
), fasta_wrap(">Silly!!?" + " blah" * 15 + "\n" + "ATCG")


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
                if cmd.startswith(("thapbi_pict ... ", "md5sum -c ", "curl ")):
                    continue
                if cmd.endswith("# Are you sure?"):
                    continue
                # (exitcode, new_out) = subprocess.getstatusoutput(cmd)
                new_out, err_out = run_cmd(cmd)
                if new_out and not new_out.endswith("\n"):
                    new_out += "\n"
                if new_out.startswith(">") or "\n>" in new_out:
                    new_out = fasta_wrap(new_out)
                elif "\t" in new_out:
                    new_out = tsv_align(new_out)
                if old_out == "...\n":
                    pass
                elif old_out == new_out:
                    if err_out:
                        # Warning?
                        print(err_out)
                    pass
                elif old_out == new_out + err_out or old_out == err_out + new_out:
                    pass
                elif old_out.startswith("...\n") and err_out.endswith(old_out[3:]):
                    pass
                elif (
                    old_out.startswith("...\n")
                    and old_out.endswith("...\n")
                    and (old_out[3:-4] in new_out or old_out[3:-4] in err_out)
                ):
                    pass
                else:
                    print("---- Old:")
                    print(old_out)
                    print("---- New:")
                    print(new_out)
                    print("---- Err:")
                    print(err_out)
                    print("---- End")
        print("Done")
        print()
