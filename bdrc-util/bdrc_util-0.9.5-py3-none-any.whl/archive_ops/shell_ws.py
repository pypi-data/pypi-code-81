"""
Callable front-end to remote web service locators
"""
import argparse
import sys

from util_lib.version import bdrc_util_version

# These are the keys we expect back from a call to the service
# which does not specify a protocol
ENCODE_S3: str = "s3"
ENCODE_LAST_TWO: str = "last2"
ENCODE_NULL: str = "resolve_null"
# response dict key names
# When all mappings requested
RESPONSE_KEY: str = "names"
# when the default mapping is requested
DEFAULT_RESPONSE_KEY: str = "default_resolve"
ENCODE_DEFAULT = "default"

# Web service URL builders
work_resolution_server: str = "sattva.wal"
api: str = "/resolve/"
default_api = api + "default/"


def get_mappings(args: object) -> str:
    """
    Calls the service
    :param args: parsed args
    :return:
    """
    import http.client
    import json
    global api, default_api, RESPONSE_KEY, DEFAULT_RESPONSE_KEY

    mapping_result: str = ""

    # Are we asking for default case?
    connection = http.client.HTTPConnection(work_resolution_server)
    headers = {'Content-type': 'application/json'}

    # names is a required arg
    post_args = json.dumps(dict(names=[args.root, args.archive]))

    # set up request
    if args.default:
        api = default_api
    connection.request('POST', api, post_args, headers)

    response = connection.getresponse()

    howdwedo = response.getcode()
    content_type: str = response.getheader('Content-type')
    if howdwedo != 200 and content_type.startswith('text/html'):
        mapping_result = response.read().decode()

    if howdwedo == 200 and content_type.find('json') > 0:
        json_response: {} = json.loads(response.read().decode())
        if (args.default):
            mapping_result = json_response.get(DEFAULT_RESPONSE_KEY)
        else:
            if args.two:
                mapping_result = json_response.get(ENCODE_LAST_TWO)
            if args.s3:
                mapping_result = json_response.get(ENCODE_S3)
            if args.null:
                mapping_result = json_response.get(ENCODE_NULL)

    return mapping_result


def resolve_arguments(arg_obj: object):
    """
    Modfies internal arguments - if no default resolution mapping was requested, set resolution_type
    to default
    :param arg_obj: parseargs
    :return: modified arg_obj
    """

    # if they asked for default, use it, otherwise if they didn't ask for anything else
    # return the default
    if not arg_obj.default:
        arg_obj.default = not(arg_obj.two or arg_obj.s3 or arg_obj.null)


def locate_archive():
    parser = argparse.ArgumentParser(description="Provides mapping of archive names to paths")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-s", "--s3", action="store_true", help="Map to ENCODE_S3 storage (hexdigest[:2])")
    group.add_argument("-t", "--two", action="store_true",
                       help="Derive from last two characters of archive")
    group.add_argument("-n", "--null", action="store_true", help="No Derivation - return input as path")
    group.add_argument("-d", "--default", action="store_true", help="return Web Service default")
    parser.add_argument("root", type=str, help="parent of archive trees")
    parser.add_argument("archive", type=str, help="the name of the work")

    if "-v" in sys.argv or "--version" in sys.argv:
        print(bdrc_util_version())
        sys.exit(0)

    arg_obj: object = parser.parse_args()

    resolve_arguments(arg_obj)
    print(get_mappings(arg_obj))


if __name__ == '__main__':
    locate_archive()
