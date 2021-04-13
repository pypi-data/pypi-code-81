#!/usr/bin/env python3
# coding=utf-8
from gitlab.exceptions import GitlabAuthenticationError

from ep2_core.common import *


@click.group()
@click.option("--verbose/--silent", default=False, help='output extra information about the current steps')
@click.pass_context
def util_grp(ctx, verbose):
    """Utility commands"""
    if verbose:
        click.echo("[DEBUG] Verbose output enabled!")

    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


@util_grp.command('init')
@click.option('--semester', type=click.Choice(['2019s', '2020s', '2021s']), help='automatically provides values for gitlab-repo-prefix '
                                                               'and gitlab-url',
              required=False)
@click.option('--git-home', prompt=True, required=True, help='directory in which the repositories will be stored '
                                                             'locally')
@click.option('--gitlab-url', help='url of the gitlab instance')
@click.option('--gitlab-repo-prefix', help='prefix for uebungs repositories')
@click.option('--gitlab-access-token', prompt=True, default='', help='your personal gitlab access token, can be '
                                                                     'omitted in the configuration file, but needs to'
                                                                     ' be provided using EP2_GITLAB_KEY for all other '
                                                                     'calls')
@click.option("--gender", prompt=True, required=True, help='the gender you identify with, used for greeting lines in '
                                                           'issues', type=click.Choice(['male', 'female', 'diverse']))
@click.option('--idea-eval-dir', prompt=True, help='directory to copy projects to, so idea will display them correctly')
@click.option('--tutor-repo', required=False, help='path to the tutor repo if it is already cloned')
def util_init(semester, git_home, gitlab_url, gitlab_repo_prefix, gitlab_access_token, idea_eval_dir, gender, tutor_repo):
    """This command generates a config file that contains all necessary information to connect to the Gitlab instance
    and grade the ad-hoc exercises.

    To generate a simple configuration for this year call

        adhoc --semester ss2019 --git-home=/path/to/repositories

    The command will then prompt you for your Gitlab AccessToken.

    Location of the configuration file, can be controlled via the EP2_CONF_FILE environment variable. If EP2_CONF_FILE
    is not set, .ep_gitlab in EP2_PATH will be used. Default for EP2_PATH is ~/.
    """
    f_info = FileInformation('Configuration')

    # Check for base path in env vars
    base = os.environ.get("EP2_PATH")
    if base is None:
        base = os.path.expanduser("~")

    # Load config file
    conf_file = os.environ.get("EP2_CONF_FILE")
    if conf_file is None:
        conf_file = relative_path(base, ".ep2_gitlab")

    config = configparser.ConfigParser()

    config.add_section('Gitlab')
    config.add_section('Local')
    config.add_section('Personal')

    if gitlab_access_token is not None and not gitlab_access_token == '':  # do not store access token
        config.set('Gitlab', 'AccessToken', gitlab_access_token)

    config.set('Local', 'GitHome', os.path.expanduser(git_home))
    if idea_eval_dir is not None and idea_eval_dir != '':
        config.set('Local', 'IdeaEvalDir', os.path.expanduser(idea_eval_dir))
    if tutor_repo is not None:
        config.set('Local', 'TutorRepo', os.path.abspath(tutor_repo))

    if semester is not None:  # Use default settings for a specific semester
        if semester == '2019s':  # Semester 2019S
            config.set('Gitlab', 'URL', 'https://ep2.inflab.tuwien.ac.at/')
            config.set('Gitlab', 'RepoPrefix', 'ep2/2019s')
        if semester == '2020s':  # Semester 2020s
            config.set('Gitlab', 'URL', 'https://b3.complang.tuwien.ac.at/')
            config.set('Gitlab', 'RepoPrefix', 'ep2/2020s')
        if semester == '2021s':
            config.set('Gitlab', 'URL', 'https://b3.complang.tuwien.ac.at/')
            config.set('Gitlab', 'RepoPrefix', 'ep2/2021s')
        else:  # Should not be possible
            click.secho('unimplemented semester: ' + semester, fg='red')
            exit(1)
    else:  # Use info provided by options
        if (gitlab_url is None or gitlab_url == '') or (gitlab_repo_prefix is None or gitlab_repo_prefix == ''):
            click.secho('Please provide --gitlab-url and --gitlab-repo-prefix or --semester!')
            exit(1)

        config.set('Gitlab', 'URL', gitlab_url)
        config.set('Gitlab', 'RepoPrefix', gitlab_repo_prefix)

    config.set('Personal', 'Gender', gender)

    # Clone or update tutor repository
    ep2 = Ep2(verbose=True, config=config)
    clone_result = ep2.clone_or_update(ep2.tutor_repo(), os.path.join(config.get('Gitlab', 'RepoPrefix'), 'org', 'tutorinnen').replace("\\", "/"), 'master')
    if clone_result.is_err():
        click.secho('error while cloning student repository: {}', clone_result.is_err())

    if os.path.exists(conf_file):
        f_info.add_file(conf_file, Action.MODIFY)
    else:
        f_info.add_file(conf_file, Action.ADD)

    config.write(open(conf_file, 'w'))
    f_info.print_info()


@util_grp.command('test')
def util_test():
    """Attempts to perform an authentication request with the Gitlab instance. If the instance can be reached, the
    command will output 'ok'"""
    ep2 = Ep2()

    try:
        ep2.gitlab.auth()
        if ep2.gitlab.user is not None:
            click.secho('ok', fg='green', bold=True)
        else:
            click.secho('fail', fg='red', bold=True)
    except GitlabAuthenticationError:
        click.secho('fail', fg='red', bold=True)
        click.secho('Authentication error')

@util_grp.command('tag')
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--tag", required=True, prompt=True, help='name of the tag')
@click.option("--teams/--students", required=True, prompt=False, help='tag team repos', default=False) 
@click.confirmation_option(prompt='This will tag all repositories in the group. Continue?')
@click.pass_context
def util_tag(ctx, group, tag, teams):
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"])
    group = ep2.group(group)

    print(teams)

    if teams:
        group.tag_group_teams(tag)
    else:
        group.tag_group(tag)


@util_grp.command()
@click.option('--project', required=True, prompt=True, help='matriculation number of the student, whose project should '
                                                            'be copied')
@click.pass_context
def idea(ctx, project):
    """Copies a project to the a directory, that is monitored by IDEA, so it can be opened quickly"""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"])
    ep2.idea_checkout(project)


if __name__ == '__main__':
    util_grp(obj={})
