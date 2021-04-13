#!/usr/bin/env python3
# coding=utf-8
import re
from statistics import mean

from ep2_tutors.ep2_eval import *
import result
import yaml
from terminaltables import AsciiTable, width_and_alignment
from ep2_tech.fails import *
from ep2_tech.test_index import *

DATA_FILE = "pre_eval_%d.yml"


@click.group()
@click.option("--verbose/--silent", default=False, help='output extra information about the current steps')
@click.pass_context
def cli(ctx, verbose):
    """Utility for ep2 tutors to perform pre evaluations of submitted exercises"""
    if verbose:
        click.echo("[DEBUG] Verbose output enabled!")

    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


@cli.group('tests')
def tests_group():
    pass


def create_eval_file(ep2: Ep2, group: Ep2Group, ue: int) -> result.Result:
    students_file = group.students_csv()

    errors: [str] = []

    with open(students_file, 'r') as infile:  # read students and create entries in attendance file
        reader = csv.DictReader(infile, students_csv_fieldnames(), KEY_INVALID, strict=True)

        headers = next(reader, None)
        if not validate_headers(headers):
            click.secho('Malformed file: %s. Invalid headers!' % students_file, fg='red')
            exit(1)

        for row in reader:
            if KEY_INVALID in row:
                click.secho('Malformed file: %s' % students_file, fg='red')
                exit(1)

            if not check_row(row):
                click.secho('Malformed file: %s. Missing column(s)!' % students_file, fg='red')
                exit(1)

        infile.seek(0)
        next(reader, None)  # skip header row

        curr_ue_type = ExerciseType.Team if ue == 7 else ExerciseType.Normal
        pre_eval_file = group.pre_eval_csv(ue)

        with open(pre_eval_file, 'w') as outfile:
            if curr_ue_type == ExerciseType.Normal:
                writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames(ep2, ue), lineterminator='\n')
            elif curr_ue_type == ExerciseType.Team:
                writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames_ta(), lineterminator='\n')
            else:
                click.secho('Unknown exercise type %s' % curr_ue_type, fg='red')
                exit(1)

            writer.writeheader()

            for row in reader:
                # no validation required, as file is the same

                student_id = row[KEY_STUDENT_ID]

                if curr_ue_type == ExerciseType.Normal:
                    sub_exercises = {KEY_UE_PRE_EVAL_EX % d: '0/0' for d in range(1, ep2.tests_for_exercise(ue) + 1)}
                    writer.writerow(
                        {KEY_STUDENT_ID: student_id, KEY_UE_GRADING: '_', KEY_UE_REMARKS: '', KEY_UE_FEEDBACK: '',
                         KEY_UE_ATTENDED: 0, **sub_exercises})
                elif curr_ue_type == ExerciseType.Team:
                    writer.writerow(
                        {KEY_STUDENT_ID: student_id, KEY_UE_TA_POINTS: '_', KEY_UE_REMARKS: '',
                         KEY_UE_FEEDBACK: '', KEY_UE_ATTENDED: 0})

    if not len(errors) == 0:
        return Err(errors)
    return Ok()


class TestGroup:

    def __init__(self, name: str, total: int, build_failed: int, test_build_failed: int, other_failure: int,
                 build_success: int, no_changes: int, results: {float}, build_failures: [str],
                 test_build_failures: [str], other_build_failures: [str], no_changes_failures: [str]):
        self.build_success = build_success
        self.results = results
        self.other_failure = other_failure
        self.test_build_failed = test_build_failed
        self.build_failed = build_failed
        self.total = total
        self.name = name
        self.no_changes = no_changes
        self.build_failures = build_failures
        self.test_build_failures = test_build_failures
        self.other_build_failures = other_build_failures
        self.no_changes_failures = no_changes_failures


def print_to_grid(texts: [str], length: int, fg: str = None, padding: int = 3, file: any = None):
    term_width = width_and_alignment.terminal_size()[0]
    current_pos = 0

    for text in texts:
        if current_pos + length > term_width:
            click.echo(nl=True, file=file)
            current_pos = 0

        if current_pos + length + padding <= term_width:
            click.secho(text + (" " * padding), fg=fg, nl=False, file=file)
        else:
            click.secho(text, fg=fg, nl=False, file=file)

        current_pos += length + padding
    click.echo(file=file)


@tests_group.command()
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.option("--rewrite-yml", required=False, default=False, help='rewrite YAML files while parsing them', type=click.BOOL)
@click.pass_context
def collect(ctx, ue: int, rewrite_yml: bool):
    """
    Tool to collect test results produced by automatic testing.
    The results are collected, written to the tutor evaluation files and a simple statistic is created.
    """
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"])

    tutor_repo = ep2.tutor_repo()

    groups_dirs = [f for f in os.listdir(tutor_repo) if re.match('(mo|do|fr|mi)(12|17|13|14|15|16|18)', f)]

    group_results: {TestGroup} = dict()

    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

    def repr_str(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
        return dumper.org_represent_str(data)

    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

    tests_for_exercise = ep2.tests_for_exercise(ue)

    fail_index = FailIndex()
    fail_regex = re.compile("org.opentest4j.AssertionFailedError:\\s*(typesys ([\\w(),.\\s]*)|assert (\\d+\\.\\d+\\.\\d+\\.\\d+(\\.\\d+)?)):([\\s\\w]*)\\s*(==>.*)?")
    test_index = TestIndex()

    click.echo("Loading data")
    with click.progressbar(groups_dirs, label='group') as bar:
        for group in bar:
            if group == 'keine':
                continue

            group = ep2.group(group)
            bar.label = group.name

            eval_file = group.pre_eval_csv(ue)

            if not os.path.exists(eval_file):
                res = create_eval_file(ep2, group, ue)
                if res.is_err():
                    click.secho(res.err(), fg='red')

            eval_file_tmp = eval_file + '.tmp'
            curr_ue_type = ue_type(ue)

            build_failed = 0
            test_build_failed = 0
            build_success = 0
            build_total = 0
            other_build_failure = 0
            no_changes = 0
            results: {[float]} = dict()
            build_failures: [str] = []
            test_build_failures: [str] = []
            other_build_failures: [str] = []
            no_changes_failures: [str] = []

            with open(eval_file, 'r') as infile:
                with open(eval_file_tmp, 'w') as outfile:

                    if curr_ue_type == ExerciseType.Normal:
                        reader = csv.DictReader(infile, fieldnames=pre_eval_csv_fieldnames(ep2, ue), strict=True,
                                                restkey=KEY_INVALID)

                        headers = next(reader, None)
                        if not validate_headers(headers):
                            click.secho('Malformed file: %s. Invalid headers!' % eval_file, fg='red')
                            exit(1)

                        writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames(ep2, ue),
                                                lineterminator='\n')
                    else:
                        reader = csv.DictReader(infile, fieldnames=pre_eval_csv_fieldnames_ta(), strict=True,
                                                restkey=KEY_INVALID)

                        headers = next(reader, None)
                        if not validate_headers(headers):
                            click.secho('Malformed file: %s. Invalid headers!' % eval_file, fg='red')
                            exit(1)

                        writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames_ta(), lineterminator='\n')

                    writer.writeheader()

                    for row in reader:
                        if KEY_INVALID in row:
                            click.secho('Malformed file: %s' % eval_file, fg='red')
                            exit(1)

                        if not check_row(row):
                            click.secho('Malformed file: %s. Missing column(s)!' % eval_file, fg='red')
                            exit(1)

                        if curr_ue_type == ExerciseType.Normal:
                            student_id = row[KEY_STUDENT_ID]
                            data_file = os.path.join(ep2.tutor_repo(), group.name, student_id, DATA_FILE % ue)

                            build_total += 1

                            with open(data_file) as data_file:
                                struct = yaml.load(data_file, Loader=yaml.FullLoader)

                                if rewrite_yml:
                                    yaml.dump(struct, Dumper=yaml.SafeDumper, stream=open(os.path.join(ep2.tutor_repo(),
                                                                                                       group.name,
                                                                                                       student_id,
                                                                                                       DATA_FILE % ue),
                                                                                          "w"))

                                if struct['build']:
                                    build_success += 1
                                    row[KEY_UE_BUILD_STATUS] = 'okay'

                                    for test_result in struct['results']:
                                        suite = int(test_result['suite'])
                                        total = int(test_result['total'])
                                        failed = int(test_result['failed']) + int(test_result['errors'])
                                        row[KEY_UE_PRE_EVAL_EX % suite] = "%d/%d" % (total - failed, total)
                                        if test_result['name'] in results:
                                            results[test_result['name']] += [(total - failed) / total]
                                        else:
                                            results[test_result['name']] = [(total - failed) / total]

                                        test_cnt = 1
                                        for test in test_result['tests']:
                                            test_obj = test_index.create_test(ue, suite, test_cnt, test['name'])
                                            test_obj.inc(group.name)
                                            test_cnt += 1

                                            if 'fail_msg' in test:  # failed test, analyze message
                                                test_obj.fail(group.name)
                                                match = fail_regex.match(test['fail_msg'])
                                                if match is not None:
                                                    if match.group(1).startswith("assert"):
                                                        fail_index.inc_assert(match.group(3), match.group(5).strip(), test['name'], group.name)
                                                    elif match.group(1).startswith("typesys"):
                                                        fail_index.inc_typesys(match.group(2).strip(), match.group(5).strip(), student_id, group.name)

                                else:
                                    build_log = struct['build_log'] if 'build_log' in struct else ''

                                    if not struct['changes']:
                                        no_changes += 1
                                        no_changes_failures += ["%s/%s" % (group.name, student_id)]
                                        row[KEY_UE_BUILD_STATUS] = 'no changes'
                                    else:
                                        test_failed = False
                                        main_failed = False
                                        row[KEY_UE_BUILD_STATUS] = 'build fail'

                                        for match in re.findall('src/(test|main)/java/(.*)\.java', build_log, re.DOTALL):
                                            dir = match[0]

                                            if dir == 'test':
                                                test_failed = True
                                            elif dir == 'main':
                                                main_failed = True

                                        if main_failed:
                                            build_failed += 1
                                            build_failures += ["%s/%s" % (group.name, student_id)]
                                        if test_failed:
                                            test_build_failed += 1
                                            test_build_failures += ["%s/%s" % (group.name, student_id)]

                                        if not main_failed and not test_failed:
                                            other_build_failures += ["%s/%s" % (group.name, student_id)]
                                            other_build_failure += 1

                                        for suite in range(1, tests_for_exercise + 1):
                                            row[KEY_UE_PRE_EVAL_EX % suite] = "0/0"

                            writer.writerow(row)
                        else:
                            writer.writerow(row)

            results = {k: mean(v) for k, v in results.items()}
            group_results[group.name] = TestGroup(group.name, build_total, build_failed, test_build_failed,
                                                  other_build_failure, build_success, no_changes, results,
                                                  build_failures, test_build_failures, other_build_failures,
                                                  no_changes_failures)
            shutil.move(eval_file_tmp, eval_file)  # replace old file with tmp file

    click.echo("Creating group statistics files")
    with click.progressbar(groups_dirs, label='group') as bar:
        for group in bar:
            file = click.open_file(ep2.group(group).statistics_file(ue), mode='w')
            print_results(file, test_index, fail_index, [group], group_results)

    print_results(None, test_index, fail_index, groups_dirs, group_results)


def print_results(file: any, test_index: TestIndex, fail_index: FailIndex, groups: [str], group_results: {TestGroup}):
    global_build_failed = 0
    global_build_success = 0
    global_build_total = 0
    global_no_changes = 0
    build_failures: [str] = []
    test_build_failures: [str] = []
    other_build_failures: [str] = []
    no_changes_failures: [str] = []

    click.secho("TESTS", bold=True, file=file)
    flat_tests = test_index.flat()
    for test in flat_tests:
        click.echo(test.flat_name(), file=file)
    click.echo(file=file)

    tests = [test.test_no() for test in flat_tests]
    headers = ['Group', 'Build Failed', 'No Changes', 'Successful Builds', 'Total'] + \
              [t + '*' for t in tests]

    table_data = [headers]

    for group in groups:
        if group == 'keine':
            continue

        global_build_total += group_results[group].total
        global_no_changes += group_results[group].no_changes
        global_build_failed += group_results[group].build_failed
        global_build_success += group_results[group].build_success

        build_failures += group_results[group].build_failures
        other_build_failures += group_results[group].other_build_failures
        test_build_failures += group_results[group].test_build_failures
        no_changes_failures += group_results[group].no_changes_failures

        group_result = group_results[group]
        test_results = ["%6.02f %%" % test.group_success(group) for test in flat_tests]
        table_data += [[group,
                        "%3d (%6.2f %%)" % (
                        group_result.build_failed, group_result.build_failed / group_result.total * 100),
                        "%3d (%6.2f %%)" % (
                        group_result.no_changes, group_result.no_changes / group_result.total * 100),
                        "%3d (%6.2f %%)" % (
                        group_result.build_success, group_result.build_success / group_result.total * 100),
                        group_result.total] + test_results]

    if len(groups) > 1:
        global_test_results = ["%6.02f %%" % test.global_success(groups) for test in flat_tests]
        table_data += [["TOTAL",
                        "%3d (%6.2f %%)" % (global_build_failed, global_build_failed / global_build_total * 100),
                        "%3d (%6.2f %%)" % (global_no_changes, global_no_changes / global_build_total * 100),
                        "%3d (%6.2f %%)" % (global_build_success, global_build_success / global_build_total * 100),
                        global_build_total] + global_test_results]

    table = AsciiTable(table_data)
    table.inner_footing_row_border = True
    click.echo(table.table, file=file)
    click.secho("*only successfully compiled exercises are included in the data", fg='white', file=file)
    click.echo(file=file)
    click.secho("BUILD FAILURES", bold=True, file=file)
    print_to_grid(build_failures, 14, fg='yellow', file=file)
    click.echo(file=file)
    if len(test_build_failures) > 0:
        click.secho("TEST BUILD FAILURES", bold=True, file=file)
        print_to_grid(test_build_failures, 14, fg='yellow', file=file)
        click.echo(file=file)
    if len(other_build_failures) > 0:
        click.secho("OTHER BUILD FAILURES", bold=True, file=file)
        print_to_grid(other_build_failures, 14, fg='yellow', file=file)
        click.echo(file=file)
    if len(no_changes_failures) > 0:
        click.secho("NO CHANGES", bold=True, file=file)
        print_to_grid(no_changes_failures, 14, fg='yellow', file=file)
        click.echo(file=file)

    click.secho("ASSERTION DETAILS", bold=True, file=file)

    curr_suite = -1
    curr_test = -1

    for index in sorted(fail_index.asserts):
        assert_obj = fail_index.asserts[index]
        count = assert_obj.count(groups)
        if count == 0:
            continue
        test = test_index.get_test(assert_obj.suite, assert_obj.test)
        if curr_suite != assert_obj.suite or curr_test != assert_obj.test:
            click.secho(test.flat_name(), bold=True, file=file)
            curr_suite = assert_obj.suite
            curr_test = assert_obj.test
        if test.fail_count(groups) == 0:
            click.echo("\t{} ({}): {} ({:3.2f}% of test failures)".format(index, assert_obj.message, count, 100), file=file)
        else:
            click.echo("\t{} ({}): {} ({:3.2f}% of test failures)".format(index, assert_obj.message, count, count / test.fail_count(groups) * 100), file=file)

    click.echo(file=file)
    click.secho("TYPESYSTEM FAILURES", bold=True, file=file)
    for identifier in sorted(fail_index.typesys):
        typesys = fail_index.typesys[identifier]
        click.echo("{} ({}): {}".format(identifier, typesys.message, typesys.count(groups)), file=file)


if __name__ == '__main__':
    cli(obj={})
