from notecoin.huobi.constant import *
from notecoin.huobi.model.account import Balance
from notecoin.huobi.utils import *
from notecoin.huobi.utils import default_parse_list_dict


class LoanInfo:
    """
    The margin rate define.

    :member
        currency: The currency name.
        interest_rate: all interest rate
        min_loan_amt: min loan amount.
        max_loan_amt: max loan amount.
        loanable_amt: loanable amount.
        actual_rate: rate after deduction.
    """

    def __init__(self):
        self.currency = ""
        self.interest_rate = ""
        self.min_loan_amt = ""
        self.max_loan_amt = ""
        self.loanable_amt = ""
        self.actual_rate = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.interest_rate, format_data + "Interest Rate")
        PrintBasic.print_basic(self.min_loan_amt, format_data + "Min Loan Amount")
        PrintBasic.print_basic(self.max_loan_amt, format_data + "Max Loan Amount")
        PrintBasic.print_basic(self.loanable_amt, format_data + "Loanable Amount")
        PrintBasic.print_basic(self.actual_rate, format_data + "Actual Rate")


class LoanOrder:
    """
    The margin order information.

    :member
        id: The order id.
        user_id: The user id.
        account_type: The account type which created the loan order.
        currency: The currency name.
        loan_amount: The amount of the origin loan.
        loan_balance: The amount of the loan left.
        interest_rate: The loan interest rate.
        interest_amount: The accumulated loan interest.
        interest_balance: The amount of loan interest left.
        state: The loan stats, possible values: created, accrual, cleared, invalid.
        created_at: The UNIX formatted timestamp in UTC when the order was created.
        accrued_at: The UNIX formatted timestamp in UTC when the last accrue happened.
    """

    def __init__(self):
        self.currency = ""
        self.deduct_rate = 0
        self.paid_point = 0.0
        self.deduct_currency = ""
        self.user_id = 0
        self.created_at = 0
        self.account_id = 0
        self.paid_coin = 0.0
        self.loan_amount = 0.0
        self.interest_amount = 0.0
        self.deduct_amount = 0.0
        self.loan_balance = 0.0
        self.interest_balance = 0.0
        self.updated_at = 0
        self.accrued_at = 0
        self.interest_rate = 0.0
        self.id = 0
        self.state = LoanOrderState.INVALID

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.deduct_rate, format_data + "Deduct Rate")
        PrintBasic.print_basic(self.paid_point, format_data + "Paid Point")
        PrintBasic.print_basic(self.deduct_currency, format_data + "Deduct Currency")
        PrintBasic.print_basic(self.user_id, format_data + "User Id")
        PrintBasic.print_basic(self.created_at, format_data + "Create Time")
        PrintBasic.print_basic(self.account_id, format_data + "Account Id")
        PrintBasic.print_basic(self.paid_coin, format_data + "Paid Coin")
        PrintBasic.print_basic(self.loan_amount, format_data + "Load Amount")
        PrintBasic.print_basic(self.interest_amount, format_data + "Interest Amount")
        PrintBasic.print_basic(self.deduct_amount, format_data + "Deduct Amount")
        PrintBasic.print_basic(self.loan_balance, format_data + "Loan Balance")
        PrintBasic.print_basic(self.interest_balance, format_data + "Interest Balance")
        PrintBasic.print_basic(self.updated_at, format_data + "Update Time")
        PrintBasic.print_basic(self.accrued_at, format_data + "Accrued Time")
        PrintBasic.print_basic(self.interest_rate, format_data + "Interest Rate")
        PrintBasic.print_basic(self.id, format_data + "ID")
        PrintBasic.print_basic(self.state, format_data + "Loan Order State")


class MarginAccountBalance:
    """
    The margin order information.

    :member
        id: Inner id.
        type: The account type.
        state: The account state.
        symbol: The symbol, like "btcusdt".
        fl_price: The trigger price.
        fl_type: The trigger type.
        risk_rate: The risk rate.
        list:Balance Object list
    """

    def __init__(self):
        self.id = 0
        self.type = AccountType.INVALID
        self.state = AccountState.INVALID
        self.symbol = ""
        self.fl_price = 0.0
        self.fl_type = 0.0
        self.risk_rate = 0.0
        self.list = []

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "ID")
        PrintBasic.print_basic(self.type, format_data + "Account Type")
        PrintBasic.print_basic(self.state, format_data + "Account State")
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.fl_price, format_data + "Trigger Price")
        PrintBasic.print_basic(self.fl_type, format_data + "Trigger Type")
        PrintBasic.print_basic(self.risk_rate, format_data + "Risk Rate")
        if self.list and len(self.list):
            for balance_obj in self.list:
                balance_obj.print_object("\t")
                print()


class MarginLoanInfo:
    """
    The margin loan info.

    :member
        symbol: symbol like "btcusdt"
        currencies: loan info for currency in symbol
    """

    def __init__(self):
        self.symbol = ""
        self.currencies = list()

    @staticmethod
    def json_parse(json_data):
        retList = []
        for idx, item in enumerate(json_data):
            margin_loan_obj = MarginLoanInfo()
            margin_loan_obj.symbol = item.get("symbol", "")

            currencies_json = item.get("currencies")
            result_list = default_parse_list_dict(currencies_json, LoanInfo, [])

            margin_loan_obj.currencies = result_list

            retList.append(margin_loan_obj)

        return retList

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        if self.currencies and len(self.currencies):
            for currency_item in self.currencies:
                currency_item.print_object("\t")
                print()


class CrossMarginAccountBalance:

    """
    The account information for spot account, margin account etc.

    :member
        id: The unique account id.
        type: The type of this account, possible value: spot, margin, otc, point.
        state: The account state, possible value: working, lock.
        list: The balance list of the specified currency. The content is Balance class
    """

    def __init__(self):
        self.id = 0
        self.type = AccountType.INVALID
        self.state = AccountState.INVALID
        self.risk_rate = 0
        self.acct_balance_sum = 0.0
        self.debt_balance_sum = 0.0
        self.list = list()

    @staticmethod
    def json_parse(data_json):
        balance_list_json = data_json.get("list", [])
        data_json.pop("list")

        account_balance = default_parse_list_dict(data_json, CrossMarginAccountBalance)
        account_balance.list = default_parse_list_dict(balance_list_json, Balance, [])

        return account_balance

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "Account ID")
        PrintBasic.print_basic(self.type, format_data + "Account Type")
        PrintBasic.print_basic(self.state, format_data + "Account State")
        PrintBasic.print_basic(self.risk_rate, format_data + "Risk Rate")
        PrintBasic.print_basic(self.acct_balance_sum, format_data + "Total Balance")
        PrintBasic.print_basic(self.debt_balance_sum, format_data + "Debt Balance")
        if self.list and len(self.list):
            for balance in self.list:
                balance.print_object("\t")
                print()


class CrossMarginLoanInfo(LoanInfo):
    def __init__(self):
        LoanInfo.__init__(self)

    def print_object(self, format_data=""):
        LoanInfo.print_object(self)


class GeneralRepayLoanRecord:
    """
    The general repay loan record information.

    :member
        repayId: repayment transaction ID.
        repayTime: repayment transaction time (unix time in millisecond).
        accountId: repayment account ID.
        currency: repayment currency, like "usdt".
        repaidAmount: repaid amount.
        transactIds: ID list of original loan transactions (arranged by order of repayment time).
        nextId: search the start ID in the next page (return only when there is data in the next page).
    """

    def __init__(self):
        self.repayId = None
        self.repayTime = None
        self.accountId = None
        self.currency = None
        self.repaidAmount = None
        self.transactIds = Transact()
        self.nextId = None

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.repayId, format_data + "repayId")
        PrintBasic.print_basic(self.repayTime, format_data + "repayTime")
        PrintBasic.print_basic(self.accountId, format_data + "accountId")
        PrintBasic.print_basic(self.currency, format_data + "currency")
        PrintBasic.print_basic(self.repaidAmount, format_data + "repaidAmount")
        PrintBasic.print_basic(self.transactIds, format_data + "transactIds")
        PrintBasic.print_basic(self.nextId, format_data + "nextId")

        print()


class Transact:

    """
    The general repay loan record information.

    :member
        transactId: original loan transaction ID.
        repaidPrincipal: principal repaid.
        repaidInterest: interest repaid.
        paidHt: HT paid.
        paidPoint: point paid.
    """

    def __init__(self):
        self.transactId = None
        self.repaidPrincipal = None
        self.repaidInterest = None
        self.paidHt = None
        self.paidPoint = None


class GeneralRepayLoanResult:
    """
    The margin order information.

    :member
        id: Inner id.
        type: The account type.
        state: The account state.
        symbol: The symbol, like "btcusdt".
        fl_price: The trigger price.
        fl_type: The trigger type.
        risk_rate: The risk rate.
        list:Balance Object list
    """

    def __init__(self):
        self.repayId = 0
        self.repayTime = 0

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.repayId, format_data + "repayId")
        PrintBasic.print_basic(self.repayTime, format_data + "repayTime")

        print()
