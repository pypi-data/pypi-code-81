##!/usr/bin/env python3
# coding=utf-8
from __future__ import print_function

import random
import string

from ep2_core.common import *

from Cheetah.Template import Template

import csv

KEY_EX_TEST_ROLE = 'role'
KEY_EX_TEST_POINTS = 'points'
KEY_EX_TEST_LATE = 'late'
KEY_EX_TEST_TEAM = 'team'
KEY_EX_TEST_REMARKS = 'remarks'
KEY_EX_TEST_FEEDBACK = 'feedback'

TAG_NAME_EX_TEST = 'ex_test_%02d'
TAG_NAME_EX_TEST_LATE = 'ex_test_%02d_late'


def ex_test_csv_fieldnames():
    return [KEY_STUDENT_ID, KEY_EX_TEST_ROLE, KEY_EX_TEST_POINTS,
            KEY_EX_TEST_LATE, KEY_EX_TEST_TEAM , KEY_EX_TEST_REMARKS,
            KEY_EX_TEST_FEEDBACK]


class StudentIndex:

    def __init__(self, group: Ep2Group, ue: int, single: bool):
        current_ue_csv = group.exercise_test_csv(ue)

        self.students = group.student_list()
        self.group = group
        self.ue = ue
        self.single = single

        self.done = []
        try:
            with open(current_ue_csv, 'r') as infile:
                reader = csv.DictReader(infile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

                headers = next(reader, None)
                if not validate_headers(headers):
                    click.secho('Malformed file: %s. Invalid headers!' % current_ue_csv)
                    exit(1)

                for row in reader:
                    self.done += [row]
        except IOError:
            pass

        done_students = list(map(lambda x: x[KEY_STUDENT_ID], self.done))

        self.remaining = []
        for student_id in self.students:
            if student_id not in done_students:
                self.remaining += [student_id]

        self.teams = {}
        self.students_for_team = {}

        if single:
            return

        for row in self.done:
            student_id = row[KEY_STUDENT_ID]
            team = row[KEY_EX_TEST_TEAM % ue]
            if student_id == team:
                click.secho(('detected single exercise, if this is a mistake please delete %s/ex_test_%d.csv' % (group, ue)))
                self.single = True
                return
            self.teams[student_id] = team
            if team in self.students_for_team:
                self.students_for_team[team] += [student_id]
            else:
                self.students_for_team[team] = [student_id]

        if ue > 1:
            self.build_lookup_index(ue - 1)

    def build_lookup_index(self, prev_ue):
        previous_ue_csv = self.group.exercise_test_csv(prev_ue)

        done_students = map(lambda x: x[KEY_STUDENT_ID], self.done)
        previous = []
        try:
            with open(previous_ue_csv, 'r') as infile:
                reader = csv.DictReader(infile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

                headers = next(reader, None)
                if not validate_headers(headers):
                    click.secho('Malformed file: %s. Invalid headers!' % previous_ue_csv)
                    exit(1)

                for row in reader:
                    if row[KEY_EX_TEST_TEAM % prev_ue] == row[KEY_STUDENT_ID]:
                        click.secho('previous exercise was a single exercise, trying exercise before')
                        if prev_ue > 1:
                            self.teams = {}
                            self.build_lookup_index(prev_ue - 1)
                            return
                    if row[KEY_STUDENT_ID] not in done_students:
                        previous += [row]
        except IOError:
            pass

        for row in previous:
            student_id = row[KEY_STUDENT_ID]
            team = row[KEY_EX_TEST_TEAM % (prev_ue)]
            self.teams[student_id] = team
            if team in self.students_for_team:
                self.students_for_team[team] += [student_id]
            else:
                self.students_for_team[team] = [student_id]

    def team_members(self, student_id):
        if student_id not in self.teams:
            return []
        team = self.teams[student_id]
        colleagues = self.students_for_team[team]
        return list(filter(lambda x: x != student_id, colleagues))

    def mark_done(self, student_id):
        self.remaining.remove(student_id)
        self.done.append(student_id)

    def auto_fill_team(self, repo_owner):
        members = self.team_members(repo_owner)
        auto_fill_additionals: [str] = []

        for member in members:
            while member[0] == '0':
                member = member[1:]
                auto_fill_additionals += [member]

        return members + auto_fill_additionals

    def auto_fill_index(self):
        auto_fill_additionals: [str] = []

        for member in self.remaining:
            while member[0] == '0':
                member = member[1:]
                auto_fill_additionals += [member]

        return self.remaining + auto_fill_additionals


@click.group()
@click.option("--verbose/--silent", default=False, help='output extra information about the current steps')
@click.option("--sudo", required=False, default=None, help='Perform actions as a different user, ONLY usable by admins')
@click.pass_context
def cli(ctx, verbose, sudo):
    """Utility for ep2 tutors to keep track of submissions and grade ad-hoc exercises."""
    if verbose:
        click.echo("[DEBUG] Verbose output enabled!")

    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['SUDO'] = sudo


def team_name(members):
    return ''.join(sorted(members))


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.option("--late/--on-time", default=False, help='if submission was late')
@click.confirmation_option(prompt='This will tag all repositories with the adhoc tags. Continue?')
@click.pass_context
def tag(ctx, group, ue: int, late):
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    group.tag_group((TAG_NAME_EX_TEST % ue) if not late else (TAG_NAME_EX_TEST_LATE % ue))


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=int)
@click.option("--late/--on-time", default=False, help='if submission was late')
@click.option("--idea/--no-idea", default=False,
              help="load project into the folder, that is monitored by IntelliJ Idea")
@click.option("--grade/--no-grade", default=False, help="also add grading with submission")
@click.option("--single/--team", default=False, help="type of the exercise, default is team")
@click.pass_context
def submission(ctx, group, ue, late, idea, grade, single):
    """Adds submissions of teams for a specific exercise to the corresponding CSV files."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)
    f_info = FileInformation('Submission')

    curr_adhoc_type = ex_test_type(ue)
    if curr_adhoc_type != (ExTestType.Single if single else ExTestType.Team):
        click.confirm('You have chosen exercise type %s even tough ad hoc exercise %s is marked as %s. Continue?' %
                      ('Single' if single else 'Team', ue, curr_adhoc_type.name), abort=True)

    index = TeamIndex(group)

    csv_file = group.exercise_test_csv(ue)
    csv_path = csv_file[:csv_file.rindex(os.sep)]  # needed to create parent dir

    try:
        os.makedirs(csv_path)
    except OSError:  # directory already exists
        pass

    file_exists = os.path.exists(csv_file)

    f_info.open_write(csv_file, True)

    if not single:
        if file_exists:
            with open(csv_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

                headers = next(reader, None)
                if not validate_headers(headers):
                    click.secho('Malformed file: %s. Invalid headers!' % csv_path)
                    exit(1)

                old_rows = []

                for row in reader:
                    student_id = verify_and_normalize_student_id(row[KEY_STUDENT_ID])

                    if student_id.is_err():
                        click.secho(
                            "[ERROR] unrecoverable error in student id normalization: {}".format(student_id.err()),
                            fg='red', bold=True)
                        return
                    else:
                        student_id = student_id.ok()

                    row[KEY_STUDENT_ID] = student_id
                    old_rows += [row]

                    team = row[KEY_EX_TEST_TEAM]
                    index.mark_team(team)

        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ex_test_csv_fieldnames(), lineterminator='\n')

            writer.writeheader()

            if file_exists:
                for row in old_rows:
                    writer.writerow(row)

            if len(index.remaining_teams) == 0:
                click.echo('No teams left to add, use ' + click.style('ep2_ex_text man_submission', bold=True)
                           + ' to add a submission manually')

            for team in sorted(index.remaining_teams, key=lambda team: team.name):
                click.secho('Enter repository owner for team {}'.format(team.name))

                for i, member in enumerate(team.students):
                    click.secho('{}: {}'.format(i, member))

                repo_owner = prompt_manual("Repo Owner", suffix=': ', show_default=False, show_choices=True,
                                           type=click.Choice([str(i) for i in range(0, len(team.students))] + ['s']))

                if repo_owner.is_err():
                    break

                if repo_owner.ok() == 's':
                    click.secho('Skipping team {}'.format(team.name), color='yellow')
                    continue

                repo_owner = team.students[int(repo_owner.ok())]

                index.mark_done(repo_owner)

                if len(team.students) == 3:
                    other_students = index.other_students(repo_owner)
                    click.secho('Enter writer for team {}'.format(team.name))

                    for i, member in enumerate(other_students):
                        click.secho('{}: {}'.format(i, member))

                    editor = prompt_manual("Mat.No. Writer", type=click.Choice(str(i) for i in range(0, len(other_students))),
                                           show_default=False, suffix=': ')
                    if editor.is_err():
                        break

                    third = other_students[(int(editor.ok()) + 1) % 2]
                    editor = other_students[int(editor.ok())]
                elif len(team.students) == 2:
                    editor = index.other_students(repo_owner)[0]
                    third = None

                if third is not None and third != 'none':
                    members = [(repo_owner, 'o'), (editor, 'e'), (third, 't')]
                    index.mark_done(third)
                else:
                    members = [(repo_owner, 'o'), (editor, 'e')]

                if grade:
                    current_uebung = ep2.local_repo(repo_owner)

                    if ep2.clone_or_update(current_uebung, ep2.ue_repo(repo_owner), TAG_NAME_EX_TEST_LATE % ue).is_err():
                        clone_result = ep2.clone_or_update(current_uebung, ep2.ue_repo(repo_owner), TAG_NAME_EX_TEST % ue)
                        if clone_result.is_err():
                            click.secho("Could not checkout submission from {} for team {}, {}"
                                        .format(repo_owner, team.name, clone_result.value), fg='red')
                            f_info.print_info()
                            exit(1)
                        else:
                            if idea:
                                ep2.idea_checkout(repo_owner)
                                click.secho('Project %s loaded into IntelliJ Idea' % repo_owner, fg='green')
                    else:
                        if idea:
                            ep2.idea_checkout(repo_owner)
                            click.secho('Project %s loaded into IntelliJ Idea' % repo_owner, fg='green')

                    ep2.create_ex_test_symlink(repo_owner, team.name)

                    points = click.prompt("Points", type=click.IntRange(0, 4), show_choices=True)
                    remarks = click.prompt("Remarks", default='', show_default=True)
                    feedback = click.prompt("Feedback", default='', show_default=True)
                else:
                    points = '_'
                    remarks = ''
                    feedback = ''

                for member in members:
                    writer.writerow(
                        {KEY_STUDENT_ID: member[0], KEY_EX_TEST_ROLE: member[1], KEY_EX_TEST_POINTS: points,
                         KEY_EX_TEST_LATE: 1 if late else 0, KEY_EX_TEST_TEAM: team.name,
                         KEY_EX_TEST_REMARKS: remarks, KEY_EX_TEST_FEEDBACK: feedback})

                click.secho('submission ok', fg='green')

    else:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ex_test_csv_fieldnames(), lineterminator='\n')

            writer.writeheader()

            action = prompt_manual('Create submissions for: (all, check)', show_choices=True,
                                   show_default=True, default='a', type=click.Choice(['a', 'c']), suffix='> ')

            if action.is_ok():
                action = action.ok()

                if action == 'a':
                    for student in sorted(index.students):
                        if grade:
                            current_uebung = ep2.local_repo(student)

                            if ep2.clone_or_update(current_uebung, ep2.ue_repo(student),
                                                       TAG_NAME_EX_TEST_LATE % ue).is_err():
                                clone_result = ep2.clone_or_update(current_uebung, ep2.ue_repo(student),
                                                                   TAG_NAME_EX_TEST % ue)
                                if clone_result.is_err():
                                    click.secho("Could not checkout submission from {}, {}"
                                                .format(student, clone_result.value), fg='red')
                                else:
                                    if idea:
                                        ep2.idea_checkout(student)
                                        click.secho('Project %s loaded into IntelliJ Idea' % student, fg='green')
                            else:
                                if idea:
                                    ep2.idea_checkout(student)
                                    click.secho('Project %s loaded into IntelliJ Idea' % student, fg='green')

                            points = click.prompt("Points for {}".format(student), type=click.IntRange(0, 4),
                                                  show_choices=True)
                            remarks = click.prompt("Remarks", default='', show_default=True)
                            feedback = click.prompt("Feedback", default='', show_default=True)
                        else:
                            points = '_'
                            remarks = ''
                            feedback = ''

                        writer.writerow(
                            {KEY_STUDENT_ID: student, KEY_EX_TEST_ROLE: 'o', KEY_EX_TEST_POINTS: points,
                             KEY_EX_TEST_LATE: 1 if late else 0, KEY_EX_TEST_TEAM: student,
                             KEY_EX_TEST_REMARKS: remarks, KEY_EX_TEST_FEEDBACK: feedback})
                elif action == 'c':

                    for student in sorted(index.students):
                        if click.confirm('Add submission for student {}?'.format(student)):
                            if grade:
                                current_uebung = ep2.local_repo(student)

                                if ep2.clone_or_update(current_uebung, ep2.ue_repo(student),
                                                           TAG_NAME_EX_TEST_LATE % ue).is_err():
                                    clone_result = ep2.clone_or_update(current_uebung, ep2.ue_repo(student),
                                                                       TAG_NAME_EX_TEST % ue)
                                    if clone_result.is_err():
                                        click.secho("Could not checkout submission from {}, {}"
                                                    .format(student, clone_result.value), fg='red')
                                    else:
                                        if idea:
                                            ep2.idea_checkout(student)
                                            click.secho('Project %s loaded into IntelliJ Idea' % student, fg='green')
                                else:
                                    if idea:
                                        ep2.idea_checkout(student)
                                        click.secho('Project %s loaded into IntelliJ Idea' % student, fg='green')

                                points = click.prompt("Points", type=click.IntRange(0, 4), show_choices=True)
                                remarks = click.prompt("Remarks", default='', show_default=True)
                                feedback = click.prompt("Feedback", default='', show_default=True)
                            else:
                                points = '_'
                                remarks = ''
                                feedback = ''

                            writer.writerow(
                                {KEY_STUDENT_ID: student, KEY_EX_TEST_ROLE: 'o', KEY_EX_TEST_POINTS: points,
                                 KEY_EX_TEST_LATE: 1 if late else 0, KEY_EX_TEST_TEAM: student,
                                 KEY_EX_TEST_REMARKS: remarks, KEY_EX_TEST_FEEDBACK: feedback})

    f_info.print_info()
    if not idea:
        click.echo('To checkout the repositories run ' + click.style('%s checkout' % EX_TEST_COMMAND_NAME, bold=True) + '.')
    if not grade:
        click.echo('To grade the exercises run ' + click.style('%s grade' % EX_TEST_COMMAND_NAME, bold=True) + '.')
        click.echo('To load the projects into IntelliJ IDEA run ' + click.style('ep2_util idea', bold=True) + '.')

    click.echo('Submit your results using ' + click.style('ep2_ex_test submit', bold=True) + '.')


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=int)
@click.option("--student", required=True, prompt=True, help='student id of the student, that should be graded',
              callback=validate_student_id)
@click.option("--role", prompt=True, type=click.Choice(['o', 'e', 't']), help='the role of the student for this exercise test')
@click.option("--late/--on-time", default=False, help='if submission was late')
@click.option("--team", prompt=True, help='the name of the team to add (this will not be verified!)')
@click.pass_context
def man_submission(ctx, group: str, ue: int, student: str, late: bool, role: str, team: str):
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)
    f_info = FileInformation('Submission')

    csv_file = group.exercise_test_csv(ue)
    csv_path = csv_file[:csv_file.rindex(os.sep)]  # needed to create parent dir

    try:
        os.makedirs(csv_path)
    except OSError:  # directory already exists
        pass

    file_exists = os.path.exists(csv_file)

    f_info.open_write(csv_file, True)
    team_points = None
    team_feedback = None
    team_remarks = None

    if file_exists:
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_path)
                exit(1)

            old_rows = []

            for row in reader:
                student_id = verify_and_normalize_student_id(row[KEY_STUDENT_ID])

                if student_id.is_err():
                    click.secho(
                        "[ERROR] unrecoverable error in student id normalization: {}".format(student_id.err()),
                        fg='red', bold=True)
                    return
                else:
                    student_id = student_id.ok()

                if student_id == student:
                    click.secho('Student already in file, overwriting record!', fg='yellow')
                else:
                    row[KEY_STUDENT_ID] = student_id
                    old_rows += [row]

                if team == row[KEY_EX_TEST_TEAM]:
                    if row[KEY_EX_TEST_POINTS] != '_':
                        team_points = row[KEY_EX_TEST_POINTS]
                        team_feedback = row[KEY_EX_TEST_FEEDBACK]
                        team_remarks = row[KEY_EX_TEST_REMARKS]

    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ex_test_csv_fieldnames(), lineterminator='\n')

        writer.writeheader()

        if file_exists:
            for row in old_rows:
                writer.writerow(row)

        writer.writerow(
            {KEY_STUDENT_ID: student, KEY_EX_TEST_ROLE: role,
             KEY_EX_TEST_POINTS: team_points if team_points is not None else '_',
             KEY_EX_TEST_LATE: 1 if late else 0, KEY_EX_TEST_TEAM: team,
             KEY_EX_TEST_REMARKS: team_remarks if team_remarks is not None else '',
             KEY_EX_TEST_FEEDBACK: team_feedback if team_feedback is not None else ''})

        click.secho('submission ok', fg='green')

    f_info.print_info()

    click.echo('Submit your results using ' + click.style('ep2_ex_test submit', bold=True) + '.')


def prompt_manual(prompt:str, suffix:str, type:click.Choice, show_default: bool, default:str = None,
                  exit_condition=None, show_choices=False) -> Result[str, str]:
    if exit_condition is None:
        exit_condition = []
    prompt_result = click.prompt(prompt, prompt_suffix=suffix, show_default=show_default,
                         type=type, show_choices=show_choices, default=default)

    if prompt_result in exit_condition:
        return Err('exit condition reached')

    return Ok(prompt_result)


class ExTestCheckoutInfo:
    student_id: str
    team: str

    def __init__(self, student_id: str, team: str):
        self.student_id = student_id
        self.team = team


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.pass_context
def checkout(ctx, group, ue: int):
    """This command checks out all repositories of a group at the tag of the given exercise.

    To see the submissions, that have not yet been graded run:

        ep2_ex_test list ungraded --group <group> --ue <ue>
    """
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    git_path = ep2.config.get("Local", "GitHome")
    csv_path = group.exercise_test_csv(ue)
    uebung_path = os.path.join(git_path, "uebung")

    try:
        os.makedirs(uebung_path)
    except OSError:  # directory already exists
        pass

    if not os.path.exists(csv_path):
        click.secho("Could not find submissions file, please run 'submission' first or pull the tutor repo", fg='red')
        exit(1)

    teams: {str} = set()
    checkout_info: [ExTestCheckoutInfo] = []

    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

        headers = next(reader, None)
        if not validate_headers(headers):
            click.secho('Malformed file: %s. Invalid headers!' % csv_path)
            exit(1)

        for row in reader:
            if KEY_INVALID in row:
                click.secho('Malformed file: %s' % csv_path, fg='red')
                exit(1)

            if not check_row(row):
                click.secho('Malformed file: %s. Missing column(s)!' % csv_path, fg='red')
                exit(1)

            teams.add(row[KEY_EX_TEST_TEAM])

            if row[KEY_EX_TEST_ROLE] == 'o':
                student_id = verify_and_normalize_student_id(row[KEY_STUDENT_ID])

                if student_id.is_err():
                    click.secho("[ERROR] unrecoverable error in student id normalization: {}".format(student_id.err()),
                                fg='red', bold=True)
                    return
                else:
                    student_id = student_id.ok()

                checkout_info += [ExTestCheckoutInfo(student_id, row[KEY_EX_TEST_TEAM])]

    teams_without_repo = list(filter(lambda team: all(chkout.team != team for chkout in checkout_info), teams))
    if len(teams_without_repo) > 0:
        click.secho('There are teams with no repository configured (role `o`):', fg='red', bold=True)
        for team in teams_without_repo:
            click.secho('    {}'.format(team), fg='red', bold='True')
        exit(1)


    with click.progressbar(checkout_info, label='Check out', item_show_func=lambda chkout: chkout.team if chkout is not None else '') as bar:
        for chkout in bar:
            student_id = chkout.student_id
            team = chkout.team

            current_uebung = os.path.join(uebung_path, student_id)
            if ep2.clone_or_update(current_uebung, ep2.ue_repo(student_id), TAG_NAME_EX_TEST_LATE % ue).is_err():
                clone_result = ep2.clone_or_update(current_uebung, ep2.ue_repo(student_id), TAG_NAME_EX_TEST % ue)
                if clone_result.is_err():
                    click.echo()
                    click.secho("Could not checkout submission from {} for team {}, {}".format(student_id,
                                                                                               row[KEY_EX_TEST_TEAM],
                                                                                               clone_result.value),
                                fg='red')

            ep2.create_ex_test_symlink(student_id, team)

    click.echo('To grade the exercises run ' + click.style('%s grade' % EX_TEST_COMMAND_NAME, bold=True) + '.')
    click.echo('To load the projects into IntelliJ IDEA run ' + click.style('%s idea' % UTIL_COMMAND_NAME, bold=True) + '.')


@cli.command()
@click.option("--team", required=True, prompt=True, help='the name of the team or the student id of the student that '
                                                         'should be graded')
@click.option("--points", required=True, prompt=True, help='points graded for this exercise', type=click.IntRange(0, 4))
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero')
@click.option("--remarks", prompt=True, default='', help='optional remarks for the lecturer')
@click.option("--feedback", prompt=True, default='', help='feedback for the students')
@click.pass_context
def grade(ctx, team, points, ue, group, remarks, feedback):
    """This command grades a single submission by updating the submissions CSV entry and creating an
    issue for the project in which the ad-hoc exercise was written in."""
    f_info = FileInformation('Grade')
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    csv_file = group.exercise_test_csv(ue)
    tmp_file = csv_file + ".tmp"  # tmp file for editing

    f_info.open_write(tmp_file, True)
    matched = False

    with open(csv_file, 'r') as infile:
        with open(tmp_file, 'w') as outfile:
            reader = csv.DictReader(infile, fieldnames=ex_test_csv_fieldnames(), restkey=KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                f_info.print_info()
                exit(1)

            writer = csv.DictWriter(outfile, fieldnames=ex_test_csv_fieldnames(), lineterminator='\n')

            writer.writeheader()

            for row in reader:  # read and search for team members
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                student_id = verify_and_normalize_student_id(row[KEY_STUDENT_ID])

                if student_id.is_err():
                    click.secho("[ERROR] unrecoverable error in student id normalization: {}".format(student_id.err()),
                                fg='red', bold=True)
                    return
                else:
                    student_id = student_id.ok()

                row[KEY_STUDENT_ID] = student_id
                if row[KEY_EX_TEST_TEAM] == team:  # if team matches, update points
                    matched = True
                    row[KEY_EX_TEST_POINTS] = points
                    if remarks is not None and remarks != '':
                        row[KEY_EX_TEST_REMARKS] = escape_csv_string(remarks)
                    if feedback is not None and feedback != '':
                        row[KEY_EX_TEST_FEEDBACK] = escape_csv_string(feedback)
                writer.writerow(row)  # write row

    if not matched:
        click.secho('Warning: Did not find team {} in submission list! Check the team name and the submissions list.'
                    .format(team), fg='yellow', bold=True)

    f_info.open_write(csv_file, True)
    shutil.move(tmp_file, csv_file)  # replace old file with tmp file
    f_info.delete(tmp_file, True)

    f_info.print_info()
    click.echo('Submit your results using ' + click.style('%s submit' % EX_TEST_COMMAND_NAME, bold=True) + '.')
    click.echo('For a list of ungraded exercises run ' + click.style('%s list ungraded' % EX_TEST_COMMAND_NAME, bold=True) + '.')


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero')
@click.pass_context
def submit(ctx, group, ue):
    """Outputs all issues, that would be created, to verify them, before submission.

    To prevent accidental issue creation before validation, a challenge has to be entered, which is printed
    at the top of the output."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    f_info = FileInformation('Submit')

    challenge = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    click.secho('Challenge %s' % challenge, bold=True)
    click.echo('\n' + ('=' * 30) + '\n')

    ex_test_csv_file = group.exercise_test_csv(ue)
    ex_test_csv_file_tmp = ex_test_csv_file + '.tmp'

    students = group.student_list()
    student_details = group.student_info()

    issues = []

    template = Template(file=ep2.template_path('adhoc.tmpl'))

    template.tutor_gender = ep2.tutor_gender()
    template.group = group.name

    with open(ex_test_csv_file, 'r') as infile:
        f_info.open_write(ex_test_csv_file_tmp, True)
        with open(ex_test_csv_file_tmp, 'w') as outfile:
            reader = csv.DictReader(infile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % ex_test_csv_file)
                exit(1)

            writer = csv.DictWriter(outfile, ex_test_csv_fieldnames(), lineterminator='\n')

            writer.writeheader()

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % ex_test_csv_file)
                    f_info.print_info()
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % ex_test_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                student_id = verify_and_normalize_student_id(row[KEY_STUDENT_ID])

                if student_id.is_err():
                    click.secho("[ERROR] unrecoverable error in student id normalization: {}".format(student_id.err()),
                                fg='red', bold=True)
                    return
                else:
                    student_id = student_id.ok()

                row[KEY_STUDENT_ID] = student_id

                if row[KEY_EX_TEST_POINTS] == '_':
                    click.secho('%s has not been graded yet. aborting!' % student_id, fg='red')
                    f_info.print_info()
                    exit(1)

                row[KEY_EX_TEST_FEEDBACK] = escape_csv_string(row[KEY_EX_TEST_FEEDBACK])
                row[KEY_EX_TEST_REMARKS] = escape_csv_string(row[KEY_EX_TEST_REMARKS])

                details = student_details[student_id]

                template.points = row[KEY_EX_TEST_POINTS]
                template.student_feedback = row[KEY_EX_TEST_FEEDBACK]
                template.student_gender = details[KEY_STUDENT_GENDER]
                template.attended = True

                students.remove(student_id)

                issue = template.__str__()
                click.echo('Issue for student %s' % student_id, nl=True)
                click.echo(issue.replace('\n\n', '\n'), nl=True)
                click.echo(('=' * 30), nl=True)
                issues += [(student_id, issue)]

                writer.writerow(row)

    for student in students:
        details = student_details[student]

        template.attended = False
        template.student_feedback = None
        template.points = 0
        template.student_gender = details[KEY_STUDENT_GENDER]

        issue = template.__str__()
        click.echo('Issue for student %s' % student, nl=True)
        click.echo(issue.replace('\n\n', '\n'), nl=True)
        click.echo(('=' * 30), nl=True)
        issues += [(student, issue)]

    click.echo('Please enter the challenge, that has been printed at the beginning of the output.')
    c = click.prompt('Challenge')
    while c != challenge:
        click.secho('invalid challenge', fg='yellow', nl=True)
        c = click.prompt('Challenge')
    click.secho('challenge accepted', fg='green', nl=True)

    exceptions = []

    with click.progressbar(issues, label='Creating issues') as bar:
        for student_id, issue in bar:
            student_project = ep2.ue_repo(student_id)  # get project
            try:
                ep2.create_project_issue(project=student_project, title='Übungstest %s' % ue, descrition=issue)
            except gitlab.GitlabCreateError as e:
                exceptions += [(e, student_project)]

    if len(exceptions) > 0:
        click.secho('with errors:', fg='red', nl=True)
        for project, e in exceptions:
            click.secho('\t%s: %s' % (e, project), fg='red', nl=True)
    else:
        click.secho('ok', nl=True, fg='green')

    f_info.open_write(ex_test_csv_file, True)
    shutil.move(ex_test_csv_file_tmp, ex_test_csv_file)
    f_info.delete(ex_test_csv_file_tmp, True)

    f_info.print_info()


@cli.group('list')
def list_grp():
    """Performs various (maybe in the future) list operations"""
    pass


@list_grp.command("ungraded")
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero')
@click.pass_context
def list_ungraded(ctx, ue, group):
    """This command lists all ungraded submission for a specific group and exercise."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    csv_file = group.exercise_test_csv(ue)
    ungraded_teams: [str] = []

    try:
        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, fieldnames=ex_test_csv_fieldnames(), strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % csv_file)
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % csv_file, fg='red')
                    exit(1)

                student_id = verify_and_normalize_student_id(row[KEY_STUDENT_ID])

                if student_id.is_err():
                    click.secho("[ERROR] unrecoverable error in student id normalization: {}".format(student_id.err()),
                                fg='red', bold=True)
                    return

                if row[KEY_EX_TEST_POINTS] == '_':
                    ungraded_teams += [row[KEY_EX_TEST_TEAM]]
    except IOError:
        click.secho('no submission for ' + group.name + ' ue ' + ue, fg='red')
        exit(1)

    if len(ungraded_teams) == 0:
        click.secho('all graded!', fg='green', bold=True)
    else:
        click.secho('Ungraded teams/students:', fg='yellow', bold='True')
        for team in ungraded_teams:
            import sys
            click.echo("    - {} (call: {})".format(team, click.style('{} --group {} --ue {} --team {}'
                                                                      .format(sys.argv[0], group.name, ue, team),
                                                                      bold=True)))


if __name__ == '__main__':
    cli(obj={})
