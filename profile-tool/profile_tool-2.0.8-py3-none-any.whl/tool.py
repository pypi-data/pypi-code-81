import argparse
import configparser
import logging
import os
import re
import sys

from .auth import assume_role_with_saml
from .centrify import cenauth, cenapp, uprest
from .config import environment


def get_cert_path():
    local_system_paths = sys.path
    for i in local_system_paths:
        if ".zip" in i:
            continue
        for root, dirs, files in os.walk(i):
            for file in files:
                file_path = os.path.join(root, file)
                if "eotss.my.crt" in file_path:
                    return file_path


def get_environment(args):
    tenant = args.tenant
    if "idaptive.app" not in tenant:
        tenant = tenant + ".idaptive.app"
    name = tenant.split(".")[0]
    tenant = "https://" + tenant
    cert = get_cert_path()
    debug = args.debug
    env = environment.Environment(name, tenant, cert, debug)
    return env


def login_instance(proxy, environment):
    user = input('Please enter your username : ')
    version = "1.0"
    session = cenauth.centrify_interactive_login(
        user, version, proxy, environment)
    return session, user


def set_logging():
    logging.basicConfig(handlers=[logging.FileHandler('idaptive-cli.log', 'w', 'utf-8')],
                        level=logging.INFO, format='%(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s')
    logging.info('Starting App..')
    print("Logfile - idaptive-cli.log")


def select_app(awsapps):
    print("Select the aws app to login. Type 'quit' or 'q' to exit")
    count = 1
    for app in awsapps:
        print(str(count) + " : " + app['DisplayName'] + " | " + app['AppKey'])
        count = count+1
    if len(awsapps) == 1:
        return "1"
    return input("Enter Number : ")


def read_proxy_config(path):
    """
    """
    proxy_config = {}

    if path is not None:
        reader = configparser.ConfigParser()
        try:
            reader.read(path)
            proxy_config = dict(reader['Proxy'])
        except:
            logging.warning("Proxy configuration file could not be read. "
                            "Continuing without proxy configuration")

    return proxy_config


def run():
    parser = argparse.ArgumentParser(
        description="Enter Centrify Credentials and choose AWS Role to create AWS Profile."
                    " Use this AWS Profile to run AWS commands.")

    parser.add_argument(
        "--tenant",
        "-t",
        help="Enter tenant url or name e.g. cloud.idaptive.com or cloud",
        default=os.environ.get("IDAPTIVE_TENANT", "cloud"),
    )

    parser.add_argument("--region", "-r", default="us-east-1",
                        help="Enter AWS region. Default is us-east-1")

    parser.add_argument("--proxy-config-path", "-p",
                        help="Enter the path to the proxy configuration file.")

    # parser.add_argument("-cert",
    # "-c",
    # help="Enter Cert file name. Default is cacerts_<tenant>.pem",
    # default="cacerts")

    parser.add_argument(
        "--debug",
        "-d",
        help="This will make debug on",
        action="store_true")

    args = parser.parse_args()

    set_logging()

    proxy = read_proxy_config(args.proxy_config_path)
    environment = get_environment(args)
    session, user = login_instance(proxy, environment)

    region = args.region

    response = uprest.get_applications(user, session, environment, proxy)
    result = response["Result"]
    logging.info("Result " + str(result))
    apps = result["Apps"]
    logging.info("Apps : " + str(apps))
    length = len(apps)
#    awsapps = [ apps[j] for j in range(length) if (("AWS" in apps[j]["TemplateName"] or "Amazon" in apps[j]["TemplateName"]) and apps[j]["WebAppType"] != 'UsernamePassword')]
    awsapps = []
    for j in range(0, length):
        try:
            appinfo = {}
            if (("AWS" in apps[j]["TemplateName"] or "Amazon" in apps[j]["TemplateName"])
                    and apps[j]["WebAppType"] != 'UsernamePassword'):
                appinfo = apps[j]
                logging.info(appinfo)
                awsapps.append(appinfo)
        except KeyError:
            continue

    logging.info("AWSapps : " + str(awsapps))

    if len(awsapps) == 0:
        print("No AWS Applications to select for the user " + user)
        return

    pattern = re.compile("[^0-9.]")
    count = 1
    profilecount = [0] * len(awsapps)
    while True:
        number = select_app(awsapps)
        if number == "":
            continue
        if re.match(pattern, number):
            print("Exiting..")
            break
        if int(number) - 1 >= len(awsapps):
            continue

        appkey = awsapps[int(number)-1]['AppKey']
        display_name = awsapps[int(number)-1]['DisplayName']
        print("Calling app with key : " + appkey)
        encoded_saml = cenapp.call_app(
            session, appkey, "1.0", environment, proxy)
        while True:
            _quit, awsinputs = cenapp.choose_role(encoded_saml, appkey)
            if _quit == 'q':
                break
            count = profilecount[int(number)-1]
            assumed = assume_role_with_saml(
                awsinputs.role, awsinputs.provider, awsinputs.saml, count, display_name, region)
            if assumed:
                profilecount[int(number)-1] = count + 1
            if _quit == 'one_role_quit':
                break

        if len(awsapps) == 1:
            break

    logging.info("Done")
    logging.shutdown()
