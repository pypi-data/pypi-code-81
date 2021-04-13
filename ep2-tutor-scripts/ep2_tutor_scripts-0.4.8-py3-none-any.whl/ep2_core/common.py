# coding=utf-8
import configparser
import os
import shutil

import click
import git
import gitlab
from enum import Enum
import csv
from glob import glob

from result import Ok, Err, Result

KEY_STUDENT_ID = 'id'
KEY_STUDENT_NAME_FIRST = 'first_name'
KEY_STUDENT_NAME_LAST = 'last_name'
KEY_INVALID = 'invalid'
KEY_STUDENT_GENDER = 'gender'
KEY_STUDENT_EMAIL = 'email'

KEY_TEAM_MEMBER_1 = 'member1'
KEY_TEAM_MEMBER_2 = 'member2'
KEY_TEAM_MEMBER_3 = 'member3'
KEY_TEAM_NAME = 'name'
KEY_TEAM_PATH = 'path'

EX_TEST_COMMAND_NAME = 'ep2_ex_test'
UTIL_COMMAND_NAME = 'ep2_util'
EVAL_COMMAND_NAME = 'ep2_eval'

KEY_UE_NO = 'ue'
KEY_UE_TAG = 'tag'


def relative_path(basedir, filename):
    """Creates a path relative to base"""
    return os.path.join(basedir, filename)


def students_csv_fieldnames():
    return [KEY_STUDENT_ID, KEY_STUDENT_NAME_LAST, KEY_STUDENT_NAME_FIRST, KEY_STUDENT_GENDER, KEY_STUDENT_EMAIL]


def teams_csv_fieldnames():
    return ['member', 'team']


def escape_csv_string(string):
    s = string
    s = s.replace(';', u';')
    return s


def validate_headers(headers):
    return headers is not None and all({k is not None and headers[k] is not None and k.strip() == headers[k].strip(): headers[k] for k in headers})


def check_row(row):
    return not any({row[k] is None: row[k] for k in row})


class Subtask:
    name: str
    max_points: float
    half_points: float
    is_bonus: bool

    def __init__(self, name: str, max_points: float, is_bonus: bool):
        self.name = name
        self.max_points = max_points
        self.half_points = max_points / 2
        self.is_bonus = is_bonus


class Ep2Group:

    def __init__(self, ep2, name):
        self.ep2 = ep2
        self.name = name

    def tag_group_teams(self, tag):
        teams = self.ep2.teams_list(self.name)

        errors = []

        with click.progressbar(teams, label='Tagging teams') as bar:
            for team in bar:
                repo = self.ep2.team_repo(team[KEY_TEAM_PATH])
                # tag latest commit
                if not self.ep2.tag_project(repo, tag):
                    errors += [team]

        return teams

    def teams_list(self):
        csv_file = self.ep2.team_csv(self.name)
        teams = []

        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, teams_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % csv_file, fg='red')
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % csv_file, fg='red')
                    exit(1)

                teams += [row]
        return teams

    def student_info(self):
        stud_csv = self.students_csv()
        students = {}

        with open(stud_csv, 'r') as infile:
            reader = csv.DictReader(infile, students_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % stud_csv)
                exit(1)

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % stud_csv, fg='red')
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % stud_csv, fg='red')
                    exit(1)

                students[row[KEY_STUDENT_ID]] = row
        return students

    def tag_group(self, tag):
        students = self.student_list()

        errors = []

        with click.progressbar(students, label='Tagging projects') as bar:
            for student_id in bar:
                repo = self.ep2.ue_repo(student_id)
                # tag latest commit
                if not self.ep2.tag_project(repo, tag):
                    errors += [student_id]

        return students

    def student_list(self) -> [str]:
        stud_csv = self.students_csv()
        students = []

        with open(stud_csv, 'r') as infile:
            reader = csv.DictReader(infile, students_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % stud_csv)
                exit(1)

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % stud_csv, fg='red')
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % stud_csv, fg='red')
                    exit(1)

                students += [row[KEY_STUDENT_ID]]
        return students

    def exercise_test_csv(self, ue):
        """Creates the path to the adhoc submission CSV file for an exercise for a group"""
        return os.path.join(self.ep2.tutor_repo(), self.name, "ex_test_" + str(ue) + ".csv")

    def attendance_csv(self, ue: int):
        """Creates the path to the attendance CSV file for an exercise for a group"""
        return os.path.join(self.ep2.tutor_repo(), self.name, "exercise_%d.csv" % ue)

    def pre_eval_csv(self, ue: int):
        return os.path.join(self.ep2.tutor_repo(), self.name, "exercise_%d.csv" % ue)

    def students_csv(self):
        """Creates the path to the attendance CSV file for an exercise for a group"""
        return os.path.join(self.ep2.tutor_repo(), self.name, "students.csv")

    def statistics_file(self, ue: int):
        """Returns the path to the statistics file for a given exercise"""
        return os.path.join(self.ep2.tutor_repo(), self.name, "statistics_{}.txt".format(ue))

    def team_csv(self):
        """Creates the path to the attendance CSV file for an exercise for a group"""
        return os.path.join(self.ep2.tutor_repo(), self.name, "teams.csv")


class Ep2:

    def __init__(self, verbose: bool = False, config: configparser.ConfigParser = None, sudo: str = None):
        if config is None:
            self.config = create_config()
        else:
            self.config = config

        self.gitlab = create_gitlab(config=self.config)
        self.verbose = verbose
        self.sudo = sudo

        if self.sudo is not None:
            self.print_sudo_header()

    def tag_project(self, project, tag):
        """Tags the last commit of a given project with 'tag'."""
        try:  # search for project
            project = self.gitlab.projects.get(project)
        except gitlab.exceptions.GitlabGetError:  # project not found
            click.secho('No repository exists for project ' + project, fg='red')
            return False

        if self.verbose:
            print('[DEBUG] Found project ' + project.web_url)

        master = project.branches.get('master')  # get master branch
        if self.verbose:
            print('[DEBUG] Found master branch with commit ' + master.commit['short_id'])

        commit_id = master.commit['id']  # get the id of the commit

        # TODO check timing constraints? e.g. commit time can't be later than 5 minutes after hand-in?
        try:
            project.tags.create({'tag_name': tag, 'ref': commit_id}, sudo=self.sudo)  # create tag for commit
        except gitlab.exceptions.GitlabCreateError as err:  # tag already exists, fail gracefully
            click.secho('Error when tagging project: {}'.format(err), fg='red')
            return False

        if self.verbose:
            print('[DEBUG] Added tag successfully')

        return True

    def clone_or_update(self, repo_dir, project, tag) -> Result:
        """Clones or updates a repository into repo_dir"""

        try:
            project = self.gitlab.projects.get(project)  # find project on gitlab
        except gitlab.exceptions.GitlabGetError:
            click.secho('No repository exists for project ' + project, fg='red')  # no project has been found
            return Err('No repository exists for project ' + project)

        try:
            _ = project.tags.get(tag)  # look for tag in project, no need to check out untagged projects
        except gitlab.exceptions.GitlabGetError:
            if self.verbose:
                click.secho('No tag ' + tag + ' found in project ' + project.name_with_namespace.replace(' ', '')
                            + '. Trying for branch', fg='yellow')  # no tag has been found
            try:
                _ = project.branches.get(tag)
            except gitlab.exceptions.GitlabGetError:
                if self.verbose:
                    click.secho('No branch ' + tag + ' found! Aborting clone/pull', fg='red')
                return Err(
                    'no branch/tag ' + tag + ' found in repository %s' % project.name_with_namespace.replace(' ', ''))

        if os.path.exists(repo_dir):  # dir exists, no need to clone
            repo = git.Repo(repo_dir)
            origin = repo.remote("origin")
            if self.verbose:
                print('[DEBUG] dir exists, attempting pull')
            origin.fetch()  # fetch is enough, as checkout is performed later
        else:  # clone
            if self.verbose:
                print('[DEBUG] attempting clone')

            try:
                os.makedirs(repo_dir)
            except OSError:  # directory already exists
                pass

            if self.verbose:
                click.echo('[DEBUG] Cloning ' + project.ssh_url_to_repo + u' into ' + repo_dir)
            git.Git(repo_dir[:repo_dir.rindex(os.sep)]).clone(project.ssh_url_to_repo)  # clone repo

        try:
            git.Git(repo_dir).checkout(tag)  # checkout exercise tag
        except git.exc.GitCommandError as error:
            return Err('%s failed with status code: %d (stdout: %s) (stderr: %s)' % (error.command, error.status,
                                                                                     error.stdout, error.stderr))
        return Ok()

    def ue_repo(self, mat_no):
        """creates the path for a uebungs repository"""
        return os.path.join(self.config.get("Gitlab", "RepoPrefix"), 'uebung', mat_no).replace("\\", "/")

    def local_repo(self, mat_no):
        """Returns the local path of students uebungs repo"""
        return os.path.join(self.config.get('Local', 'GitHome'), 'uebung', mat_no)

    def tutor_repo(self):
        """Returns the path to the local tutor directory"""
        return self.config.get('Local', 'TutorRepo',
                               fallback=os.path.join(self.config.get('Local', 'GitHome'), 'org', 'tutorinnen'))

    def tutor_gender(self):
        """Returns the gender of a tutor"""
        try:
            return self.config.get('Personal', 'Gender')
        except configparser.NoSectionError:
            return 'diverse'

    def template_path(self, template):
        """Returns the path of the template file to be used"""
        template_file = os.path.join(self.tutor_repo(), 'templates', template)
        if os.path.exists(template_file):
            return template_file
        return None

    def team_repo(self, path):
        return os.path.join(self.config.get("Gitlab", "RepoPrefix"), 'team', path).replace("\\", "/")

    def group(self, group: str) -> Ep2Group:
        # TODO add caching
        return Ep2Group(self, group)

    def idea_checkout(self, project, group: str = None, ue: int = None, copy_pre_eval: bool = False, copy_tests: bool = False):
        src = self.local_repo(project)
        dst = self.config.get('Local', 'IdeaEvalDir')

        dst_src_dir = os.path.join(dst, 'src')
        dst_angabe_dir = os.path.join(dst, 'angabe')
        dst_test_dir = os.path.join(dst, 'test')

        src_src_dir = os.path.join(src, 'src')
        src_angabe_dir = os.path.join(src, 'angabe')

        if os.path.exists(dst):

            if os.path.exists(dst_src_dir):
                try:
                    os.unlink(dst_src_dir)
                except IsADirectoryError:
                    try:
                        os.rmdir(dst_src_dir)
                    except OSError:
                        shutil.rmtree(dst_src_dir)

            if os.path.exists(dst_angabe_dir):
                try:
                    os.unlink(dst_angabe_dir)
                except IsADirectoryError:
                    try:
                        os.rmdir(dst_angabe_dir)
                    except OSError:
                        shutil.rmtree(dst_angabe_dir)

            if os.path.exists(dst_test_dir):
                try:
                    os.unlink(dst_test_dir)
                except IsADirectoryError:
                    try:
                        os.rmdir(dst_test_dir)
                    except OSError:
                        shutil.rmtree(dst_test_dir)

            pre_eval_results = glob(os.path.join(dst, 'pre_eval_*.yml'))

            for pre_eval_result in pre_eval_results:
                os.unlink(pre_eval_result)      # should work the same for single files and symlinks

        else:
            os.makedirs(dst, exist_ok=True)

        try:
            os.symlink(src_src_dir, dst_src_dir, target_is_directory=True)
        except OSError as e:
            click.echo('User has no rights to create symlinks! See https://stackoverflow.com/a/65504258 to set proper '
                       'privileges under Windows 10.')
            click.echo('System error: {}'.format(e))
            exit(5)

        try:
            os.symlink(src_angabe_dir, dst_angabe_dir, target_is_directory=True)
        except OSError as e:
            click.echo('User has no rights to create symlinks! See https://stackoverflow.com/a/65504258 to set proper '
                       'privileges under Windows 10.')
            click.echo('System error: {}'.format(e))
            exit(5)

        if copy_pre_eval and ue is not None:
            src_pre_eval = os.path.join(self.tutor_repo(), group, project, 'pre_eval_{}.yml'.format(ue))
            dst_pre_eval = os.path.join(dst, 'pre_eval_{}.yml'.format(ue))

            try:
                os.symlink(src_pre_eval, dst_pre_eval)
            except OSError as e:
                click.echo(
                    'User has no rights to create symlinks! See https://stackoverflow.com/a/65504258 to set proper '
                    'privileges under Windows 10.')
                click.echo('System error: {}'.format(e))
                exit(5)

        if copy_tests and ue is not None:
            src_test_dir = os.path.join(self.tutor_repo(), 'unittests', str(ue))

            if os.path.exists(src_test_dir):
                try:
                    os.symlink(src_test_dir, dst_test_dir, target_is_directory=True)
                except OSError as e:
                    click.echo(
                        'User has no rights to create symlinks! See https://stackoverflow.com/a/65504258 to set proper '
                        'privileges under Windows 10.')
                    click.echo('System error: {}'.format(e))
                    exit(5)

    def local_team_repository(self, team: str):
        return os.path.join(self.uebung_dir(), team)

    def create_ex_test_symlink(self, project: str, team: str):
        local_team = self.local_team_repository(team)
        local_repo = self.local_repo(project)

        if os.path.exists(local_team):
            try:
                os.unlink(local_team)
            except IsADirectoryError:
                try:
                    os.rmdir(local_team)
                except OSError:
                    shutil.rmtree(local_team)

        try:
            os.symlink(local_repo, local_team)
        except OSError as e:
            click.echo(
                'User has no rights to create symlinks! See https://stackoverflow.com/a/65504258 to set proper '
                'privileges under Windows 10.')
            click.echo('System error: {}'.format(e))

    def test_info_csv(self) -> str:
        return os.path.join(self.tutor_repo(), "test_info.csv")

    def tests_for_exercise(self, ue: int) -> int:
        csv_file = self.test_info_csv()

        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, ['ex', 'test_groups'], KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            for row in reader:
                if int(row['ex']) == ue:
                    return int(row['test_groups'])

        raise Exception('no test info available for exercise %d' % ue)

    def uebung_dir(self):
        return os.path.join(self.config.get('Local', 'GitHome'), "uebung")

    def create_project_issue(self, project:str, title:str, descrition:str):
        proj = self.gitlab.projects.get(project, lazy=True)  # fetch project (gitlab) and add issue

        proj.issues.create({'title': title, 'description': descrition}, sudo=self.sudo,
                           headers={'content-type': 'application/json; charset=UTF-8'})

    def get_ue_tag(self, ue: int):
        csv_file = os.path.join(self.tutor_repo(), "tags.csv")

        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, [KEY_UE_NO, KEY_UE_TAG], KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            for row in reader:
                if int(row[KEY_UE_NO]) == ue:
                    return row[KEY_UE_TAG]

    def print_sudo_header(self):
        user = self.gitlab.users.list(username=self.sudo)[0]
        click.secho('*' * 60, fg='red', bold=True)
        click.secho('*' + ' ' * 27 + 'SUDO' + ' ' * 27 + '*', fg='red', bold=True)
        click.secho('*' + ' ' * 58 + '*', fg='red', bold=True)
        click.secho('* {:^56s} *'.format('Performing actions as {:s}'.format(user.name)), fg='red', bold=True)
        click.secho('*' * 60, fg='red', bold=True)

    def exercise_subtasks_csv(self, ex: int):
        return os.path.join(self.tutor_repo(), "ex_info", "ex_{}.csv".format(ex))

    def get_exercise_subtasks(self, ex: int) -> [Subtask]:
        csv_file = self.exercise_subtasks_csv(ex)

        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, ['subtask', 'max_points', 'bonus'], KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            subtasks: [Subtask] = []
            for row in reader:
                subtasks += [Subtask(row['subtask'], float(row['max_points']), row['bonus'] == 'true')]

            return subtasks

    def validate_grading(self, ex: int, grading: str) -> (bool, str):
        subtasks = self.get_exercise_subtasks(ex)

        if len(subtasks) != len(grading):
            return False, []

        return True, grading


def verify_and_normalize_student_id(student_id) -> Result:
    import re
    if re.match('\\d*', student_id) and len(student_id) <= 8:
        return Ok('0' * (8 - len(student_id)) + student_id)
    else:
        return Err('invalid student id: {}'.format(student_id))


def validate_student_id(ctx, param, value):
    if value is None:
        return None

    res = verify_and_normalize_student_id(value)
    if res.is_ok():
        return res.ok()
    else:
        raise click.BadParameter(res.err())


def create_gitlab(config):
    """Opens a gitlab instance with the supplied config.

    The environment variable EP2_GITLAB_KEY is the preferred source for the access token.
    If the variable is not provided, Gitlab.AccessToken from the configuration file is used"""
    access_token = os.environ.get("EP2_GITLAB_KEY")
    if access_token is None:
        access_token = config.get("Gitlab", "AccessToken")

    return gitlab.Gitlab(config.get("Gitlab", "URL"), private_token=access_token)


def create_config():
    """Loads the configuration file.

    Attempts to load the file from the EP2_CONF_FILE environment variable.
    If this variable is not present, it checks if the EP2_PATH environment variable is set.
    If it is set, $EP2_PATH/.ep2_gitlab is used as configuration file. If not, ~/.ep2_gitlab is used for config.
    """
    # Check for base path in env vars
    base = os.environ.get("EP2_PATH")
    if base is None:
        base = os.path.expanduser("~")

    # Load config file
    conf_file = os.environ.get("EP2_CONF_FILE")
    if conf_file is None:
        conf_file = relative_path(base, ".ep2_gitlab")

    config = configparser.ConfigParser()
    # file = open(conf_file, 'r')
    config.read(conf_file)
    return config


def ue_type(ue: int):
    if int(ue) == 7:
        return ExerciseType.Team
    return ExerciseType.Normal


def ex_test_type(ue: int):
    if ue == 4 or ue == 8:
        return ExTestType.Single
    return ExTestType.Team


class ExerciseType(Enum):
    Normal = 1
    Team = 2


class ExTestType(Enum):
    Single = 1
    Team = 2


class Action(Enum):
    ADD = 1
    DELETE = 2
    MODIFY = 3


class FileInfoFile:

    def __init__(self, path, action, push):
        self.path = path
        self.action = action
        self.push = push


class FileInformation:

    def __init__(self, name):
        self.name = name
        self.files = {}

    def add_file(self, file_path, action, push=False):
        """

        :type action: Action
        :type file_path: basestring
        :type push: bool
        """
        self.files[file_path] = FileInfoFile(file_path, action, push)

    def print_info(self,
                   print_info=lambda x: click.echo(x),
                   print_warn=lambda x: click.secho(x, fg='yellow', bold=True),
                   print_add=lambda x, push: click.secho('\tadd: %s%s' % (x, '*' if push else ''), fg='green'),
                   print_modify=lambda x, push: click.secho('\tmod: %s%s' % (x, '*' if push else ''), fg='blue'),
                   print_delete=lambda x, push: click.secho('\tdel: %s%s' % (x, '*' if push else ''), fg='red')):
        if len(self.files) == 0:
            return
        print_info('Change list [%s]' % self.name)
        lists = {}
        push = False
        for k in self.files:
            v = self.files[k]
            if v.action not in lists:
                lists[v.action] = []
            lists[v.action] += [v]
        for k in lists:
            v = lists[k]
            v.sort(key=lambda x: x.path)
            if k == Action.ADD:
                for f in v:
                    if f.push:
                        push = True
                    print_add(f.path, f.push)
            elif k == Action.MODIFY:
                for f in v:
                    if f.push:
                        push = True
                    print_modify(f.path, f.push)
            elif k == Action.DELETE:
                for f in v:
                    if f.push:
                        push = True
                    print_delete(f.path, f.push)
        if push:
            print_warn('*commit and push changes')

    def info_string(self):
        result = []
        self.print_info(
            print_info=(lambda x: result.append('%s' % x)),
            print_warn=(lambda x: result.append('%s' % x)),
            print_add=(lambda x, push: result.append('\t+ %s%s' % (x, '*' if push else ''))),
            print_modify=(lambda x, push: result.append('\t~ %s%s' % (x, '*' if push else ''))),
            print_delete=(lambda x, push: result.append('\t- %s%s' % (x, '*' if push else '')))
        )
        return '\n'.join(result)

    def open_write(self, file_path, push=False):
        if os.path.exists(file_path):
            self.add_file(file_path, Action.MODIFY, push)
        else:
            self.add_file(file_path, Action.ADD, push)

    def delete(self, file_path, push=False):
        if file_path in self.files and self.files[file_path].action == Action.ADD:
            del self.files[file_path]
        else:
            self.add_file(file_path, Action.DELETE, push)


class Ep2Team:
    students: [str]
    name: str

    def __init__(self, name: str):
        self.name = name
        self.students = []


class TeamIndex:
    marked: [str]
    team_index: {Ep2Team}
    teams: {Ep2Team}
    remaining_teams: [Ep2Team]

    def __init__(self, group: Ep2Group):
        self.students = group.student_list()
        csv_file = group.team_csv()
        self.marked = []
        self.team_index = {}
        self.teams = {}
        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, teams_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            for row in reader:
                member = row['member']
                team_name = row['team']

                if member not in self.students:
                    click.secho('[WARN] potential data inconsistency detected: student {} in team list but not in '
                                'student list!'.format(member), fg='yellow', bold=True)

                if team_name in self.teams:
                    team = self.teams[team_name]
                else:
                    team = Ep2Team(team_name)
                    self.teams[team_name] = team

                team.students += [member]
                self.team_index[member] = team

        self.remaining_teams = self.teams.values()

    def other_students(self, student: str) -> [str]:
        return list(filter(lambda x: x != student, self.team_index[student].students))

    def mark_done(self, student: str):
        self.marked += self.team_index[student].students

    def skip(self, student: str) -> bool:
        return student in self.marked

    def remaining(self) -> int:
        return len(self.students) - len(self.marked)

    def mark_team(self, team: str):
        self.remaining_teams = list(filter(lambda t: t.name != team, self.remaining_teams))

