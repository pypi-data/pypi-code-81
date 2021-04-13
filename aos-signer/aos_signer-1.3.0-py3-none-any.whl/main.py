#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import argparse
import sys

from colorama import Fore, Style

from aos_signer import __version__
from aos_signer.signer.bootstrapper import run_bootstrap
from aos_signer.signer.errors import SignerConfigError
from aos_signer.signer.signer import Signer, logger
from aos_signer.signer.uploader import run_upload
from aos_signer.service_config.service_configuration import ServiceConfiguration

_COMMAND_INIT = 'init'
_COMMAND_SIGN = 'sign'
_COMMAND_UPLOAD = 'upload'
_COMMAND_VALIDATE = 'validate'


def run_init_signer():
    print("{}Starting INIT process...{}".format(Fore.GREEN, Style.RESET_ALL))
    run_bootstrap()


def run_validate():
    print("{}Starting config validation process...{}".format(Fore.GREEN, Style.RESET_ALL))
    ServiceConfiguration('meta/config.yaml')
    print("{}Config is valid{}".format(Fore.GREEN, Style.RESET_ALL))


def run_upload_service():
    print("{}Starting SERVICE UPLOAD process...{}".format(Fore.GREEN, Style.RESET_ALL))
    try:
        run_upload()
        sys.exit(0)
    except OSError:
        print(Fore.RED + str(sys.exc_info()[1]))
        sys.exit(1)


def run_sign():
    print("{}Starting SERVICE SIGNING process...{}".format(Fore.GREEN, Style.RESET_ALL))
    try:
        logger.info("Validating config . . .")
        ServiceConfiguration('meta/config.yaml')
        s = Signer(src_folder='src', package_folder='.')
        s.process()
        print("{}Done!{}".format(Fore.GREEN, Style.RESET_ALL))
    except OSError:
        print(Fore.RED + str(sys.exc_info()[1]) + Style.RESET_ALL)


def main():
    from colorama import init
    init()
    parser = argparse.ArgumentParser(
        prog='Aos Signer Tool',
        description='This tool will help you to prepare, sign and upload service to Aos Cloud'
    )
    parser.add_argument('-V', '--version', action='store_true', help='Print aos-signer version number and exit')
    parser.set_defaults(which=None)

    sub_parser = parser.add_subparsers(title='Commands')

    init = sub_parser.add_parser(
        _COMMAND_INIT,
        help='Generate required folders and configuration file. If you don\'t know where to start type aos-signer init'
    )
    init.set_defaults(which=_COMMAND_INIT)

    validate = sub_parser.add_parser(
        _COMMAND_VALIDATE,
        help='Validate config file.'
    )
    validate.set_defaults(which=_COMMAND_VALIDATE)

    sign = sub_parser.add_parser(
        _COMMAND_SIGN,
        help='Sign Service. Read config and create signed archive ready to be uploaded.'
    )
    sign.set_defaults(which=_COMMAND_SIGN)

    upload = sub_parser.add_parser(
        _COMMAND_UPLOAD,
        help='Upload Service to the Cloud.'
             'Address, security credentials and service UID is taken from config.yaml in meta folder.'
    )
    upload.set_defaults(which=_COMMAND_UPLOAD)

    args = parser.parse_args()
    try:
        if args.version:
            print(__version__)
            sys.exit(0)

        if args.which is None:
            run_sign()

        if args.which == _COMMAND_INIT:
            print('__file__:{}'.format(__file__))
            run_init_signer()

        if args.which == _COMMAND_SIGN:
            run_sign()

        if args.which == _COMMAND_VALIDATE:
            run_validate()

        if args.which == _COMMAND_UPLOAD:
            run_upload_service()
    except SignerConfigError as sce:
        print(Fore.RED + 'Process failed with error: ')
        print(str(sce) + Style.RESET_ALL)
        sys.exit(1)
    except Exception as sce:
        print(Fore.RED + 'Process failed with error: ')
        print(str(sce) + Style.RESET_ALL)
        logger.exception(sce)
        sys.exit(1)


if __name__ == '__main__':
    main()
