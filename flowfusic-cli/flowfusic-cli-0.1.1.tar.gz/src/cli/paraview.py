import os
import platform
import subprocess
from time import sleep

import click

# from yaspin import yaspin
from halo import Halo

from src.client.client_socket_proxy import ParaviewSocketClient
from src.client.cloud import CloudApiClient
from src.log import logger


@click.command()
@click.option("--paraview", "-p", "paraview_path", help="Path to paraview")
def paraview(paraview_path=False):
    """
    Run paraview in client-server configuration.

    Requires paraview client to be locally installed.
    """

    # Start paraview:
    # 1. Login user
    # 2. Check if paraview is available on $PATH
    # 2. Check version of paraview, should be 5.8.0
    # 3. Get token from cloud api
    # 4. Start server
    # 5. Start paraview

    # find paraview:
    spinner = Halo(text="Checking ParaView...")
    spinner.start()
    if paraview_path:
        if hasParaview(paraview_path):
            pass
        elif hasParaview(os.path.join(paraview_path, "paraview")):
            paraview_path = os.path.join(paraview_path, "paraview")
        else:
            # spinner.ok("❌ ")
            spinner.fail()
            logger.error("Paraview not found in %s", paraview_path)
            return None

    else:
        paraview_path = "paraview"
        if not hasParaview(paraview_path):
            spinner.fail()
            logger.error(
                "Paraview not found. Please use --paraview /path/to/paraview or make sure that paraview is in your PATH."
            )
            return None

    spinner.succeed()
    # Has paraview
    # check version

    spinner = Halo(text="Verifying ParaView version...")
    spinner.start()
    # check version of paraview:
    message = paraviewVersion(paraview_path)
    if message != True:
        spinner.fail()
        logger.info(message)
        logger.info(
            "Please make sure that paraview in your PATH is a supported version"
        )
        logger.info(
            " or use --paraview /path/to/paraview to a supported version of paraview."
        )
        logger.info("Find more information at www.flowfusic.com")
        return None

    spinner.succeed()
    spinner = Halo(text="Starting render server...")

    spinner.start()

    # get token:
    cloud_client = CloudApiClient()
    token = cloud_client.get_token()

    if not token:
        spinner.fail()
        return None

    # start pvserver in the backend rendering server:
    paraview_started = cloud_client.paraview_start()

    if not paraview_started:
        spinner.fail()
        logger.error("Problem with backend server. Try again later.")
        return None

    spinner.succeed()
    spinner = Halo(text="Checking connection...")
    spinner.start()

    paraview_ready = paraview_started == "ready"

    # MS: maybe don't run it forever?
    while not paraview_ready:
        paraview_ready = cloud_client.paraview_ready()
        sleep(0.5)

    spinner.succeed()

    logger.info("Running paraview client")

    # start local proxy client:
    socket_pv_client = ParaviewSocketClient(token)
    socket_pv_client.setup_server()

    # open paraview client window:
    subprocess.Popen(
        commandToOpenParaview(paraview_path, socket_pv_client),
        shell=True,
    )

    logger.info("Paraview client opened")

    # start server (close when paraview is closed):
    socket_pv_client.run_server()


def commandToOpenParaview(paraview_path, socket_pv_client):
    if platform.system() == "Windows":
        return '"{}" --server-url=cs://{}:{}'.format(
            paraview_path, socket_pv_client.address[0], socket_pv_client.address[1]
        )
    else:
        return "{} --server-url=cs://{}:{}".format(
            paraview_path, socket_pv_client.address[0], socket_pv_client.address[1]
        )


def hasParaview(paraview_path):
    return hasProg(paraview_path)


def pvpythonexePath(paraview_path):
    return os.path.join(os.path.dirname(paraview_path), "pvpython.exe")


def paraviewVersion(paraview_path):

    pvver = "paraview version"
    supported_version = "5.8.0"

    if platform.system() == "Windows":
        p = run([pvpythonexePath(paraview_path), "-V"], shell=False)
    else:
        p = run([paraview_path, "-V"], shell=False)

    # paraview sometimes prints to stderr
    line = [s for i, s in enumerate(p.stdout.split("\n")) if pvver in s]
    if len(line) > 0:
        pass
    else:
        line = [s for i, s in enumerate(p.stderr.split("\n")) if pvver in s]

    if len(line) == 0:
        return "Unable to determine version of paraview. Please check output of 'paraview -V' command."

    if "{} {}".format(pvver, supported_version) in line[0]:
        return True

    return "Unsupported: {}".format(line[0])


def run(command, shell=True):
    return subprocess.run(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=shell,
    )


def is_tool(name):
    """Check whether `name` is on PATH."""

    from distutils.spawn import find_executable

    return find_executable(name) is not None


def hasProg(prog):

    if platform.system() == "Windows":

        return is_tool(prog)

    else:

        return (
            subprocess.call(
                ["which", prog], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            == 0
        )
