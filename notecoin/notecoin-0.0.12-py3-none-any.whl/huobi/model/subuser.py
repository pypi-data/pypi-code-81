class SubuserApikeyGeneration:
    """
    The trade information with price and amount etc.

    :member
        accessKey:
        secretKey:
        note:
        permission: "trade,readOnly",
        ipAddresses":
    """

    def __init__(self):
        self.accessKey = ""
        self.secretKey = ""
        self.note = ""
        self.permission = ""
        self.ipAddresses = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.accessKey, format_data + "accessKey")
        PrintBasic.print_basic(self.secretKey, format_data + "secretKey")
        PrintBasic.print_basic(self.note, format_data + "note")
        PrintBasic.print_basic(self.permission, format_data + "permission")
        PrintBasic.print_basic(self.ipAddresses, format_data + "ipAddresses")


class SubuserApikeyModification:
    """
    The trade information with price and amount etc.

    :member
        note:
        permission: "trade,readOnly",
        ipAddresses":
    """

    def __init__(self):
        self.note = ""
        self.permission = ""
        self.ipAddresses = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.note, format_data + "note")
        PrintBasic.print_basic(self.permission, format_data + "permission")
        PrintBasic.print_basic(self.ipAddresses, format_data + "ipAddresses")


class SubuserCreation:
    """
    The trade information with price and amount etc.

    :member
        subUid: sub user ID.
        userState: sub user account state, states see SubUidState.
    """

    def __init__(self):
        self.user_name = ""
        self.note = ""
        self.uid = 0
        self.err_code = 0
        self.err_message = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.user_name, format_data + "userName")
        PrintBasic.print_basic(self.note, format_data + "note")
        PrintBasic.print_basic(self.uid, format_data + "uid")
        PrintBasic.print_basic(self.err_code, format_data + "errCode")
        PrintBasic.print_basic(self.err_message, format_data + "errMessage")


class SubuserTransferability:
    """
    The trade information with price and amount etc.

    :member
        subUid: sub user ID.
        userState: sub user account state, states see SubUidState.
    """

    def __init__(self):
        self.transferrable = ""
        self.accountType = ""
        self.subUid = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.subUid, format_data + "subUid")
        PrintBasic.print_basic(self.accountType, format_data + "accountType")
        PrintBasic.print_basic(self.transferrable, format_data + "transferrable")


class TradeMarket:
    """
    The trade information with price and amount etc.

    :member
        subUid: sub user ID.
        accountType:
        activation: sub user account state for given accountType.
    """

    def __init__(self):
        self.sub_uid = ""
        self.account_type = ""
        self.activation = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.sub_uid, format_data + "subUid")
        PrintBasic.print_basic(self.account_type, format_data + "accountType")
        PrintBasic.print_basic(self.activation, format_data + "activation")


class UserApikeyInfo:
    """
    The trade information with price and amount etc.

    :member
        accessKey: .
        createTime:
        ipAddresses: .
        note:
        permission:
        status:
        updateTime:
        validDays:

    """

    def __init__(self):
        self.accessKey = ""
        self.createTime = 0
        self.ipAddresses = ""
        self.note = ""
        self.permission = ""
        self.status = ""
        self.updateTime = 0
        self.validDays = -1

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic

        PrintBasic.print_basic(self.accessKey, format_data + "accessKey")
        PrintBasic.print_basic(self.createTime, format_data + "createTime")
        PrintBasic.print_basic(self.ipAddresses, format_data + "ipAddresses")
        PrintBasic.print_basic(self.note, format_data + "note")
        PrintBasic.print_basic(self.permission, format_data + "permission")
        PrintBasic.print_basic(self.status, format_data + "status")
        PrintBasic.print_basic(self.updateTime, format_data + "updateTime")
        PrintBasic.print_basic(self.validDays, format_data + "validDays")
