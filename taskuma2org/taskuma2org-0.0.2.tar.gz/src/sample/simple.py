import os
import click
import tempfile


MEMACS_ARGUMENT = 'memacs_csv \
--timestamp-field "start" \
--fieldnames "task, est, taskumaduration, start, end, rate, \
taskumaproj, section, map, memo, check, taskumatag, dummy" \
--delimiter "," \
--timestamp-format "%Y/%m/%d %H:%M" \
--output-format "{task}" \
--properties "taskumaduration,taskumaproj,section,memo,taskumatag" \
'


def return_input_file_name(infile, skip):
    return skip_first_two_lines(infile, skip)


def make_memacs_argument(infile, outfile=None):
    if outfile:
        return_value = MEMACS_ARGUMENT + " -f " + infile + " -o " + outfile
    else:
        return_value = MEMACS_ARGUMENT + " -f " + infile

    return return_value


def skip_first_two_lines(infile, skip):
    """return file name which is made from infile with removing first two lines"""
    fp = infile
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as tfp:
        i = 0
        for a_line in fp:
            if i < 2 and skip:
                i = i + 1
            else:
                tfp.write(a_line)
        tfp.close()
        return tfp.name


@click.command()
@click.argument("filename", type=click.File("r", encoding="utf-8"), default="-")
@click.option(
    "--output",
    type=click.Path(exists=True, writable=True, resolve_path=True),
    help="the path of org file output",
)
@click.option(
    "--skip/--no-skip",
    default=False,
    help="whether or not to skip the first two lines of the csv file.",
)
def wrapper(filename, output, skip):
    """convert taskuma log file to org-mode.
    taskuma log as csv file
    """
    try:
        inputfile = None
        inputfile = return_input_file_name(filename, skip)
        spec_arg = make_memacs_argument(inputfile, output)
        exit_status = os.system(spec_arg)
    finally:
        if inputfile is not None:
            os.remove(inputfile)
    exit(exit_status)
