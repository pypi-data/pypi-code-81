"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
from web3.types import BlockIdentifier

from moneyonchain.contract import ContractBase


class RDOCUpgraderChanger(ContractBase):
    contract_name = 'RDOCUpgraderChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/UpgraderChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/UpgraderChanger.bin'))

    mode = 'RDOC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):
        config_network = network_manager.config_network
        if not contract_address:
            raise ValueError("You need to pass contract address")

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def new_implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.newImplementation(block_identifier=block_identifier)

        return result

    def proxy(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.proxy(block_identifier=block_identifier)

        return result

    def upgrade_delegator(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.upgradeDelegator(block_identifier=block_identifier)

        return result
