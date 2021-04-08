#  Copyright © 2020 Hashmap, Inc
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# Copyright © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging.config
import warnings
from argparse import ArgumentParser, ArgumentTypeError

from providah.factories.package_factory import PackageFactory as providah_pkg_factory

from hdc.core.asset_mapper import AssetMapper
from hdc.core.cataloger import Cataloger
from hdc.core.exceptions.hdc_error import HdcError
from hdc.utils import file_utils

warnings.filterwarnings("ignore")


def build_parser():
    parser = ArgumentParser(prog="hdc")

    parser.add_argument("-r", "--run", type=str, required=True, choices=['catalog', 'map'], help="One of 'catalog' or "
                                                                                                 "'map'")
    parser.add_argument("-s", "--source", type=str, required=True,
                        help="Name of any one of sources configured in hdc.yml")
    parser.add_argument("-d", "--destination", type=str,
                        help="Name of any one of destinations configured in hdc.yml")
    parser.add_argument("-c", "--app_config", type=str,
                        help="Path to application config (YAML) file if other than default")
    parser.add_argument("-l", "--log_settings", type=str, help="Path to log settings (YAML) file if other than default")

    return parser


def validate_hdc_cli_args(args):
    if len(args) != 0:
        if args.get('run').lower() == 'map':
            if args.get('destination') is None:
                raise ArgumentTypeError("For 'map' operation, destination option needs to be provided")
    else:
        raise ArgumentTypeError('No arguments provided!')


def start_here():
    hdc_parser = build_parser()
    cli_args = hdc_parser.parse_args()

    try:
        validate_hdc_cli_args(vars(cli_args))

        app_config: dict = file_utils.get_app_config(cli_args.app_config)

        if cli_args.log_settings is not None:
            logging.config.dictConfig(file_utils.yaml_parser(yaml_file_path=cli_args.log_settings))
        else:
            logging.config.dictConfig(file_utils.yaml_parser(yaml_file_path=file_utils.get_default_log_config_path()))

        if app_config is not None:
            if cli_args.run.lower() == 'map':
                try:
                    asset_mapper: AssetMapper = providah_pkg_factory.create(key='AssetMapper',
                                                                            library='hdc',
                                                                            configuration={
                                                                                'source': cli_args.source,
                                                                                'destination': cli_args.destination,
                                                                                'app_config': cli_args.app_config
                                                                            })

                    if asset_mapper.map_assets():
                        print(
                            f"Successfully mapped the source '{cli_args.source}' to destination '{cli_args.destination}'")

                except HdcError as hde:
                    print(hde)

            elif cli_args.run.lower() == 'catalog':
                try:
                    cataloger: Cataloger = providah_pkg_factory.create(key='Cataloger',
                                                                       library='hdc',
                                                                       configuration={
                                                                           'source': cli_args.source,
                                                                           'app_config': cli_args.app_config})

                    df_catalog = cataloger.obtain_catalog()

                    cataloger.pretty_print(df_catalog)

                except HdcError as hde:
                    print(hde)
        else:
            raise HdcError(message=f"Could not find file {app_config}")

    except ArgumentTypeError as err:
        hdc_parser.print_usage()
        raise HdcError(message=err)

    except RuntimeError as err:
        raise HdcError(message=err)


if __name__ == '__main__':
    start_here()
