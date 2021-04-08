import os


def check(params, errors):
    """
    Check if all of the parameters exist or not, and print the corresponding
    error if one is not passed through.

    :param params:
    :param errors:
    :return {NoneType}:
    """
    for index, param in enumerate(params):
        if not param:
            print(errors[index])
            exit(0)


def check_executable(ctx, exe):
    """
    Check that the system has a certain executable file command available to it
    before we try to start running commands that utilize it.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param exe {str}:
    """
    current = ""

    try:
        for cmd in exe:
            current = cmd
            ctx.run("whereis {} > /dev/null".format(cmd))
    except Exception as e:
        ctx.run('echo "Make sure that you have the following packages installed properly: {}"'.format(", ".join(exe)))
        ctx.run('echo "It looks like you may have had a problem with the command: {}."'.format(current))
        exit(1)


def check_packages(ctx):
    """
    Check and make sure that all dependencies are configured to run the project
    in general. These are not project specific dependencies. Not talking about
    Odoo dependencies.

    This checks that the user has the proper packages available to them such as
    pip3, invoke, git, etc.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    check_executable(
        ctx,
        [
            "git",
            "docker",
            "docker-compose",
            "docker",
            "invoke",
            "curl",
            "echo",
            "sed",
            "pip3",
            "tail",
            "pylint",
            "yapf",
        ],
    )


def check_project(ctx):
    """
    Check that the project is ready to run basically. We need to make sure we
    have a few different things:

    - At least an odoo core instance.
    - An odoo log created.
    - An odoo conf file.

    :param ctx {invoke.context.Context}: Invoke context variable
    """

    must_have_files = [".env", ".container/config/odoo.conf", ".container/log/odoo.log", ".container/core/LICENSE"]

    for rel_filepath in must_have_files:
        path = os.path.abspath(rel_filepath)
        if not os.path.isfile(path):
            ctx.run('echo "Make sure that you have the following files configured:"')
            ctx.run('echo "{}"'.format(", ".join(must_have_files)))
            ctx.run('echo "It looks like you are missing {}."'.format(rel_filepath))
            return False

    with open(".env", "r") as f:
        if "enterprise=1" in f.read().lower():
            if not os.path.isfile(".container/enterprise/LICENSE"):
                ctx.run(
                    'echo "It looks like you have enterprise enabled. Make sure you have the source files setup in '
                    '.container/enterprise."'
                )
                return False

    return True


def check_env(config, required):
    """
    Check and make sure that the config (.env file) is setup properly.

    :param config {config.configparser.ConfigParser}:
    :param required {bool}:
    :return {bool}:
    """
    if not config or not config.sections():
        print(
            "Make sure you have the .env file and the .container/env/odoo/odoo.env file setup and that they have the [options] header."
        )
        exit(1)
    for param in required:
        if not config.has_option("options", param):
            print("Make sure that you have all of these required values in your .env:")
            for print_param in required:
                print("    - {}".format(print_param))
            exit(1)
    return True


def check_dirs():
    """
    Check and make sure that the required directories are setup properly based
    on the mapping define in the docker compose file.

    TODO: This is going to be used to ensure that everything is setup properly
    when a user tries to run the project or build the project.

    :return {bool}:
    """
    pass


def can_run(ctx):
    """
    Check and make sure that the project has everything that it needs to run
    before we actually try to run the project. This is meant to help prevent any
    confusion when someone is setting up a new project and running into errors.

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {bool}:
    """
    return check_project(ctx)
