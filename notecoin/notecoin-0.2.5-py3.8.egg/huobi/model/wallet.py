
from notecoin.huobi.constant import *


class ChainDepositAddress:
    """
    The deposit address.

    :member
        currency: The crypto currency to deposit.
        address: Deposit address
        addressTag: Deposit address tag.
        chain: Block chain name.
    """

    def __init__(self):
        self.currency = ""
        self.address = ""
        self.addressTag = ""
        self.chain = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.address, format_data + "Address")
        PrintBasic.print_basic(self.addressTag, format_data + "addressTag")
        PrintBasic.print_basic(self.chain, format_data + "Chain")


class ChainWithdrawAddress:
    """
    The deposit address.

    :member
        currency: The crypto currency to deposit.
        address: Deposit address
        addressTag: Deposit address tag.
        chain: Block chain name.
    """

    def __init__(self):
        self.currency = ""
        self.address = ""
        self.addressTag = ""
        self.chain = ""
        self.note = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.address, format_data + "Address")
        PrintBasic.print_basic(self.addressTag, format_data + "addressTag")
        PrintBasic.print_basic(self.chain, format_data + "Chain")
        PrintBasic.print_basic(self.note, format_data + "Note")


class DepositHistoryItem:
    """
     The deposit history

     :member
         id: The transfer id.
         currency: The crypto currency to deposit.
         txHash: The on-chain transaction hash.
         amount: The number of crypto asset transferred in its minimum unit.
         address: The deposit source address.
         addressTag: The user defined address tag.
         deposit_state: The deposit state of this transfer.
         created_timestamp: The UNIX formatted timestamp in UTC for the transfer creation.
         updated_timestamp: The UNIX formatted timestamp in UTC for the transfer's latest update.
     """

    def __init__(self):
        self.id = 0
        self.currency = ""
        self.txHash = ""
        self.chain = ""
        self.amount = 0.0
        self.address = ""
        self.addressTag = ""
        self.deposit_state = WithdrawState.INVALID
        self.created_timestamp = 0
        self.updated_timestamp = 0

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "ID")
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.chain, format_data + "Chain")
        PrintBasic.print_basic(self.txHash, format_data + "Trade Hash")
        PrintBasic.print_basic(self.amount, format_data + "Amount")
        PrintBasic.print_basic(self.address, format_data + "Address")
        PrintBasic.print_basic(self.addressTag, format_data + "Address Tag")
        PrintBasic.print_basic(self.deposit_state, format_data + "Deposit State")
        PrintBasic.print_basic(self.created_timestamp, format_data + "Create Time")
        PrintBasic.print_basic(self.updated_timestamp, format_data + "Update Time")


class DepositHistory:
    """
    The deposit history

    :member
        nextId: next id.
        data: history list.
    """

    def __init__(self):
        self.data = list()
        self.nextId = 0

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.nextId, format_data + "NextId")
        if self.data and len(self.data):
            for item in self.data:
                item.print_object()
                PrintBasic.print_basic("", format_data + "")


class Deposit:
    """
    The latest status for deposits

    :member
        id: The transfer id.
        currency: The crypto currency to deposit.
        tx_hash: The on-chain transaction hash.
        amount: The number of crypto asset transferred in its minimum unit.
        address: The deposit source address.
        address_tag: The user defined address tag.
        fee: The amount of fee taken by Huobi in this crypto's minimum unit.
        created_at: The UNIX formatted timestamp in UTC for the transfer creation.
        updated_at: The UNIX formatted timestamp in UTC for the transfer's latest update.
        state: The deposit state of this transfer.
    """

    def __init__(self):
        self.id = 0
        self.type = DepositWithdraw.DEPOSIT
        self.currency = ""
        self.tx_hash = ""
        self.amount = 0.0
        self.chain = ""
        self.address = ""
        self.address_tag = ""
        self.fee = 0.0
        self.created_at = 0
        self.updated_at = 0
        self.state = DepositState.INVALID

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "ID")
        PrintBasic.print_basic(self.type, format_data + "Operate Type")
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.chain, format_data + "Chain")
        PrintBasic.print_basic(self.tx_hash, format_data + "Trade Hash")
        PrintBasic.print_basic(self.amount, format_data + "Amount")
        PrintBasic.print_basic(self.address, format_data + "Address")
        PrintBasic.print_basic(self.address_tag, format_data + "Address Tag")
        PrintBasic.print_basic(self.fee, format_data + "Fee")
        PrintBasic.print_basic(self.state, format_data + "Deposit State")
        PrintBasic.print_basic(self.created_at, format_data + "Create Time")
        PrintBasic.print_basic(self.updated_at, format_data + "Update Time")


class WithdrawQuota:
    """
    Withdraw Quota info.

    :member
        chain: Block chain name.
        maxWithdrawAmt: Maximum withdraw amount in each request.
        withdrawQuotaPerDay: Maximum withdraw amount in a day
        remainWithdrawQuotaPerDay: Remaining withdraw quota in the day
        withdrawQuotaPerYear: Maximum withdraw amount in a year
        remainWithdrawQuotaPerYear: Remaining withdraw quota in the year
        withdrawQuotaTotal: Maximum withdraw amount in total
        remainWithdrawQuotaTotal: Remaining withdraw quota in total
    """

    def __init__(self):
        self.chain = ""
        self.maxWithdrawAmt = ""
        self.withdrawQuotaPerDay = ""
        self.remainWithdrawQuotaPerDay = ""
        self.withdrawQuotaPerYear = ""
        self.remainWithdrawQuotaPerYear = ""
        self.withdrawQuotaTotal = ""
        self.remainWithdrawQuotaTotal = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.chain, format_data + "Chain")
        PrintBasic.print_basic(self.maxWithdrawAmt, format_data + "maxWithdrawAmt")
        PrintBasic.print_basic(self.withdrawQuotaPerDay, format_data + "withdrawQuotaPerDay")
        PrintBasic.print_basic(self.remainWithdrawQuotaPerDay, format_data + "remainWithdrawQuotaPerDay")
        PrintBasic.print_basic(self.withdrawQuotaPerYear, format_data + "withdrawQuotaPerYear")
        PrintBasic.print_basic(self.remainWithdrawQuotaPerYear, format_data + "remainWithdrawQuotaPerYear")
        PrintBasic.print_basic(self.withdrawQuotaTotal, format_data + "withdrawQuotaTotal")
        PrintBasic.print_basic(self.remainWithdrawQuotaTotal, format_data + "remainWithdrawQuotaTotal")


class Withdraw:
    """
    The latest status for withdraws.

    :member
        id: The transfer id.
        currency: The crypto currency to deposit.
        tx_hash: The on-chain transaction hash.
        amount: The number of crypto asset transferred in its minimum unit.
        address: The deposit source address.
        address_tag: The user defined address tag.
        fee: The amount of fee taken by Huobi in this crypto's minimum unit.
        created_at: The UNIX formatted timestamp in UTC for the transfer creation.
        updated_at: The UNIX formatted timestamp in UTC for the transfer's latest update.
        state: The withdraw state of this transfer.
    """

    def __init__(self):
        self.id = 0
        self.type = DepositWithdraw.WITHDRAW
        self.currency = ""
        self.chain = ""
        self.tx_hash = ""
        self.amount = 0.0
        self.address = ""
        self.address_tag = ""
        self.fee = 0.0
        self.created_at = 0
        self.updated_at = 0
        self.state = WithdrawState.INVALID

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "ID")
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.type, format_data + "Operator Type")
        PrintBasic.print_basic(self.chain, format_data + "Chain")
        PrintBasic.print_basic(self.tx_hash, format_data + "Trade Hash")
        PrintBasic.print_basic(self.amount, format_data + "Amount")
        PrintBasic.print_basic(self.address, format_data + "Address")
        PrintBasic.print_basic(self.address_tag, format_data + "Address Tag")
        PrintBasic.print_basic(self.fee, format_data + "Fee")
        PrintBasic.print_basic(self.state, format_data + "Withdraw State")
        PrintBasic.print_basic(self.created_at, format_data + "Create Time")
        PrintBasic.print_basic(self.updated_at, format_data + "Update Time")
