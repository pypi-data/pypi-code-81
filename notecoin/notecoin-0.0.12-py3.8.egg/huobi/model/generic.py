from notecoin.huobi.constant import *


class Chain:
    """
    The Huobi Chain.

    :member
        chain: Chain name
        numOfConfirmations: Number of confirmations required for deposit success (trading & withdrawal allowed once reached)
        numOfFastConfirmations: Number of confirmations required for quick success (trading allowed but withdrawal disallowed once reached)
        minDepositAmt: Minimal deposit amount in each request
        depositStatus: Deposit status	allowed,prohibited
        minWithdrawAmt: Minimal withdraw amount in each request.
        maxWithdrawAmt : Maximum withdraw amount in each request
        withdrawQuotaPerDay : Maximum withdraw amount in a day
        withdrawQuotaPerYear : Maximum withdraw amount in a year
        withdrawQuotaTotal : Maximum withdraw amount in total
        withdrawPrecision : Withdraw amount precision
        withdrawFeeType : Type of withdraw fee (only one type can be applied to each currency)

        transactFeeWithdraw : Withdraw fee in each request (only applicable to withdrawFeeType = fixed)
        minTransactFeeWithdraw : Minimal withdraw fee in each request (only applicable to withdrawFeeType = circulated)
        maxTransactFeeWithdraw : Maximum withdraw fee in each request (only applicable to withdrawFeeType = circulated or ratio)
        transactFeeRateWithdraw : Withdraw fee in each request (only applicable to withdrawFeeType = ratio)
        withdrawStatus : Withdraw status
    """

    def __init__(self):
        self.chain = ""
        self.baseChain = ""
        self.baseChainProtocol = ""
        self.numOfConfirmations = 0
        self.numOfFastConfirmations = 0
        self.depositStatus = ChainDepositStatus.INVALID
        self.minDepositAmt = 0
        self.withdrawStatus = ChainWithdrawStatus.INVALID
        self.minWithdrawAmt = 0
        self.withdrawPrecision = 0
        self.maxWithdrawAmt = 0.0
        self.withdrawQuotaPerDay = 0.0
        self.withdrawQuotaPerYear = 0.0
        self.withdrawQuotaTotal = 0.0
        self.withdrawFeeType = ""
        self.transactFeeWithdraw = 0.0
        self.minTransactFeeWithdraw = 0.0
        self.maxTransactFeeWithdraw = 0.0
        self.transactFeeRateWithdraw = 0.0

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.chain, format_data + "Chain")
        PrintBasic.print_basic(self.baseChain, format_data + "Base Chain")
        PrintBasic.print_basic(self.baseChainProtocol, format_data + "Base Chain Protocol")
        PrintBasic.print_basic(self.numOfConfirmations, format_data + "numOfConfirmations")
        PrintBasic.print_basic(self.numOfFastConfirmations, format_data + "numOfFastConfirmations")
        PrintBasic.print_basic(self.depositStatus, format_data + "depositStatus")
        PrintBasic.print_basic(self.minDepositAmt, format_data + "minDepositAmount")
        PrintBasic.print_basic(self.withdrawStatus, format_data + "withdrawStatus")
        PrintBasic.print_basic(self.minWithdrawAmt, format_data + "minWithdrawAmount")
        PrintBasic.print_basic(self.withdrawPrecision, format_data + "withdrawPrecision")
        PrintBasic.print_basic(self.maxWithdrawAmt, format_data + "maxWithdrawAmount")
        PrintBasic.print_basic(self.withdrawQuotaPerDay, format_data + "withdrawQuotaPerDay")
        PrintBasic.print_basic(self.withdrawQuotaPerYear, format_data + "withdrawQuotaPerYear")
        PrintBasic.print_basic(self.withdrawQuotaTotal, format_data + "withdrawQuotaTotal")
        PrintBasic.print_basic(self.withdrawFeeType, format_data + "withdrawFeeType")
        PrintBasic.print_basic(self.transactFeeWithdraw, format_data + "transactFeeWithdraw")
        PrintBasic.print_basic(self.minTransactFeeWithdraw, format_data + "minTransactFeeWithdraw")
        PrintBasic.print_basic(self.maxTransactFeeWithdraw, format_data + "maxTransactFeeWithdraw")
        PrintBasic.print_basic(self.transactFeeRateWithdraw, format_data + "transactFeeRateWithdraw")


class ExchangeInfo:
    """
    The Huobi supported the symbols and currencies.

    :member
        symbol_list: The symbol list. The content is Symbol class.
        currencies: The currency list. The content is string value.
    """

    def __init__(self):
        self.symbol_list = list()
        self.currencies = list()


class MarketStatus:
    """
    The Huobi market status info.

    :member
        marketStatus: .
        haltStartTime: .
        haltEndTime: .
        haltReason:
        affectedSymbols:
    """

    def __init__(self):
        self.marketStatus = MarketStatus.NORMAL
        self.haltStartTime = -1
        self.haltEndTime = -1
        self.affectedSymbols = ""


class ReferenceCurrency:
    """
    The Huobi supported static reference information for each currency.

    :member
        currency: currency
        instStatus: Instrument status
        chains: chain list
    """

    def __init__(self):
        self.currency = ""
        self.instStatus = InstrumentStatus.INVALID
        self.chains = []

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.currency, format_data + "Currency")
        PrintBasic.print_basic(self.instStatus, format_data + "Instrument Status")
        if self.chains and len(self.chains):
            for chain_obj in self.chains:
                chain_obj.print_object("\t")
                print()


class Symbol:
    """
    The Huobi supported symbols.

    :member
        base_currency: The base currency in a trading symbol.
        quote_currency: The quote currency in a trading symbol.
        price_precision: The quote currency precision when quote price (decimal places).
        amount_precision: The base currency precision when quote amount (decimal places).
        symbol_partition: The trading section, possible values: [main，innovation，bifurcation].
        symbol: The symbol, like "btcusdt".
        state : trade status, maybe one in [online，offline,suspend]
        value_precision : value precision
        min_order_amt : minimum volume limit only used in limit-order and sell-market order
        max_order_amt : Maximum volume
        min_order_value : Minimum order amount
        leverage_ratio : Leverage ratio for symbol
        limit_order_min_order_amt: Minimum order amount of limit order in base currency (NEW)
        limit_order_max_order_amt: Max order amount of limit order in base currency (NEW)
        sell_market_min_order_amt: Minimum order amount of sell-market order in base currency (NEW)
        sell_market_max_order_amt: Max order amount of sell-market order in base currency (NEW)
        buy_market_max_order_amt: Max order value of buy-market order in quote currency (NEW)
        max_order_value: Max order value of limit order and buy-market order in usdt (NEW)

    """

    def __init__(self):
        self.base_currency = ""
        self.quote_currency = ""
        self.price_precision = 0
        self.amount_precision = 0
        self.symbol_partition = ""
        self.symbol = ""
        self.state = ""
        self.value_precision = 0
        self.min_order_amt = ""
        self.max_order_amt = ""
        self.min_order_value = ""
        self.leverage_ratio = 0
        self.limit_order_min_order_amt = 0
        self.limit_order_max_order_amt = 0
        self.sell_market_min_order_amt = 0
        self.sell_market_max_order_amt = 0
        self.buy_market_max_order_value = 0
        self.max_order_value = 0

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.base_currency, format_data + "Base Currency")
        PrintBasic.print_basic(self.quote_currency, format_data + "Quote Currency")
        PrintBasic.print_basic(self.price_precision, format_data + "Price Precision")
        PrintBasic.print_basic(self.amount_precision, format_data + "Amount Precision")
        PrintBasic.print_basic(self.symbol_partition, format_data + "Symbol Partition")
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.state, format_data + "State")
        PrintBasic.print_basic(self.value_precision, format_data + "Value Precision")
        PrintBasic.print_basic(self.min_order_amt, format_data + "Min Order Amount")
        PrintBasic.print_basic(self.max_order_amt, format_data + "Max Order Amount")
        PrintBasic.print_basic(self.min_order_value, format_data + "Min Order Value")
        PrintBasic.print_basic(self.leverage_ratio, format_data + "Leverage Ratio")
        PrintBasic.print_basic(self.limit_order_min_order_amt, format_data + "Minimum order amount (Limit Order)")
        PrintBasic.print_basic(self.limit_order_max_order_amt, format_data + "Max order amount (Limit Order)")
        PrintBasic.print_basic(self.sell_market_min_order_amt, format_data + "Min order amount (Sell Market Order)")
        PrintBasic.print_basic(self.sell_market_max_order_amt, format_data + "Max order amount (Sell Market Order)")
        PrintBasic.print_basic(self.buy_market_max_order_value, format_data + "Max order value (Buy Market Order)")
        PrintBasic.print_basic(self.max_order_value, format_data + "Max order value (In USDT)")
