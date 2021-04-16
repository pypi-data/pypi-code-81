
from notecoin.huobi.constant import *
from notecoin.huobi.utils.json_parser import default_parse_list_dict, fill_obj


class BatchCancelCount:
    """
    The result of batch cancel operation.

    :member
        success_count: The number of cancel request sent successfully.
        failed_count: The number of cancel request failed.
        next_id:next open order id
    """

    def __init__(self):
        self.success_count = 0
        self.failed_count = 0
        self.next_id = -1

    def print_object(self, format_data=""):
        from huobi.utils import PrintBasic
        PrintBasic.print_basic(self.success_count, format_data + "Success Count")
        PrintBasic.print_basic(self.failed_count, format_data + "Failed Count")
        PrintBasic.print_basic(self.next_id, format_data + "Next Open Order ID")


class BatchCancelResult:
    """
    The result of batch cancel operation.

    :member
        success_count: The number of cancel request sent successfully.
        failed_count: The number of cancel request failed.

    """

    def __init__(self):
        self.success = []
        self.failed = []

    def print_object(self, format_data=""):
        print("Success Order Counts", len(self.success), " Success Order Ids : ", self.success)
        print("Fail Order Counts", len(self.failed), " Fail Order Ids : ", self.failed)


class BatchCreateOrder:
    """
    batch create order result

    :member
        order_id: The transfer id.
        client_order_id: The crypto currency to deposit.
        err_code: The on-chain transaction hash.
        err_msg: The number of crypto asset transferred in its minimum unit.

    """

    def __init__(self):
        self.order_id = 0
        self.client_order_id = ""
        self.err_code = ""
        self.err_msg = ""

    def print_object(self, format_data=""):
        from huobi.utils import PrintBasic
        PrintBasic.print_basic(self.order_id, format_data + "Order Id")
        PrintBasic.print_basic(self.client_order_id, format_data + "Client Order Id")
        PrintBasic.print_basic(self.err_code, format_data + "Error Code")
        PrintBasic.print_basic(self.err_msg, format_data + "Error Message")


class FeeRate:
    """
    The account information for spot account, margin account etc.

    :member
        symbol: The symbol, like "btcusdt".
        maker_fee: maker fee rate
        taker_fee: taker fee rate

    """

    def __init__(self):
        self.symbol = ""
        self.maker_fee = ""
        self.taker_fee = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.maker_fee, format_data + "Maker Fee")
        PrintBasic.print_basic(self.taker_fee, format_data + "Taker Fee")


class MatchResult:
    """
    The match result information.

    :member
        created_timestamp: The UNIX formatted timestamp in UTC when the match and fill is done.
        filled_amount: The amount which has been filled.
        filled_fees: The transaction fee paid so far.
        id: The internal id.
        match_id: The match id of this match.
        order_id: The order id of this order.
        price: The limit price of limit order.
        source: The source where the order was triggered, possible values: sys, web, api, app.
        symbol: The symbol, like "btcusdt".
        type: The order type, possible values are: buy-market, sell-market, buy-limit, sell-limit,
            buy-ioc, sell-ioc, buy-limit-maker, sell-limit-maker, buy-limit-fok, sell-limit-fok, buy-stop-limit-fok, sell-stop-limit-fok.
        filled_points: deduct points
        fee_deduct_currency: deduct type, it means deduct from HT/ HT points / or other currency
        fee_currency:
    """

    def __init__(self):
        self.created_at = 0
        self.filled_amount = 0.0
        self.filled_fees = 0.0
        self.id = 0
        self.match_id = 0
        self.order_id = 0
        self.price = 0.0
        self.source = OrderSource.INVALID
        self.symbol = ""
        self.type = OrderType.INVALID
        self.role = ""
        self.filled_points = ""
        self.fee_deduct_currency = ""
        self.fee_currency = ""
        self.fee_deduct_state = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "ID")
        PrintBasic.print_basic(self.created_at, format_data + "Create Time")
        PrintBasic.print_basic(self.filled_amount, format_data + "Fill Amount")
        PrintBasic.print_basic(self.filled_fees, format_data + "Fill Fee")
        PrintBasic.print_basic(self.filled_points, format_data + "Fill Points")
        PrintBasic.print_basic(self.match_id, format_data + "Match ID")
        PrintBasic.print_basic(self.order_id, format_data + "Order ID")
        PrintBasic.print_basic(self.price, format_data + "Price")
        PrintBasic.print_basic(self.source, format_data + "Source")
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.type, format_data + "Order Type")
        PrintBasic.print_basic(self.role, format_data + "Role")
        PrintBasic.print_basic(self.fee_deduct_currency, format_data + "Fee Deduct Currency")
        PrintBasic.print_basic(self.fee_currency, format_data + "Fee Currency")
        PrintBasic.print_basic(self.fee_deduct_state, format_data + "Fee Deduct State")


class OrderDetailReq:
    """
    The order update received by subscription of order update.

    :member
        symbol: The symbol you subscribed.
        timestamp: The UNIX formatted timestamp generated by server in UTC.
        topic : request topic
        client_req_id : client request id
        data: The order detail.

    """

    def __init__(self):
        self.ts = 0
        self.topic = ""
        self.cid = ""
        self.data = OrderListItem()

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.ts, format_data + "Timestamp")
        PrintBasic.print_basic(self.cid, format_data + "Client Req ID")
        PrintBasic.print_basic(self.topic, format_data + "Topic")
        self.data.print_object("\t")


class OrderListItem:
    """
    The order update received by request of order list.

    :member
        symbol: The symbol you subscribed.
        timestamp: The UNIX formatted timestamp generated by server in UTC.
        topic: request topic
        client_req_id: client request ID
        order_list : order list

    """

    def __init__(self):
        self.id = 0
        self.symbol = ""
        self.account_id = 0
        self.amount = 0.0
        self.price = 0.0
        self.created_at = 0
        self.type = OrderType.INVALID
        self.finished_at = 0
        self.source = OrderSource.INVALID
        self.state = OrderState.INVALID
        self.canceled_at = 0
        self.filled_amount = 0.0
        self.filled_cash_amount = 0.0
        self.filled_fees = 0.0
        self.stop_price = 0.0
        self.operator = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "ID")
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.account_id, format_data + "Account Id")
        PrintBasic.print_basic(self.amount, format_data + "Amount")
        PrintBasic.print_basic(self.price, format_data + "Price")
        PrintBasic.print_basic(self.created_at, format_data + "Create Time")
        PrintBasic.print_basic(self.type, format_data + "Order Type")
        PrintBasic.print_basic(self.finished_at, format_data + "Finish Time")
        PrintBasic.print_basic(self.source, format_data + "Order Source")
        PrintBasic.print_basic(self.state, format_data + "Order State")
        PrintBasic.print_basic(self.canceled_at, format_data + "Cancel Time")
        PrintBasic.print_basic(self.filled_amount, format_data + "Filled Amount")
        PrintBasic.print_basic(self.filled_cash_amount, format_data + "Filled Cash Amount")
        PrintBasic.print_basic(self.filled_fees, format_data + "Filled Fees")
        PrintBasic.print_basic(self.stop_price, format_data + "Stop Price")
        PrintBasic.print_basic(self.operator, format_data + "Operator")


class OrderListReq:
    """
    The order update received by request of order list.

    :member
        symbol: The symbol you subscribed.
        timestamp: The UNIX formatted timestamp generated by server in UTC.
        topic: request topic
        data : OrderListItem

    """

    def __init__(self):
        self.ts = 0
        self.topic = ""
        self.data = list()

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.ts, format_data + "Timestamp")
        PrintBasic.print_basic(self.topic, format_data + "Channel")
        print("Order List as below : count " + str(len(self.data)))
        if len(self.data):
            for orderlistitem_obj in self.data:
                orderlistitem_obj.print_object("\t ")
                print()


class OrderUpdateEvent:
    """
    The order update received by subscription of order update.

    :member
        ch: The symbol you subscribed.
        data: The order detail.

    """

    def __init__(self):
        self.ch = ""
        self.data = OrderUpdate()

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.ch, format_data + "Topic")

        orderupdate = self.data
        orderupdate.print_object()


class OrderUpdate:
    """
    The detail order information.

    :member
        orderId: The order id.
        tradePrice: trade price
        tradeVolume: trade volume
        tradeId: Id record for trade
        tradeTime: trade timestamp (ms)
        aggressor: true (taker), false (maker)
        remainAmt: Remaining amount (for buy-market order it's remaining value)
        orderStatus: Order status, valid value: partial-filled, filled
        clientOrderId: Client order ID (if any)
        eventType: Event type, valid value: trade
        symbol: The symbol, like "btcusdt".
        type: The order type, possible values are: buy-market, sell-market, buy-limit, sell-limit, buy-ioc, sell-ioc, buy-limit-maker, sell-limit-maker, buy-limit-fok, sell-limit-fok.
    """

    def __init__(self):
        self.orderId = 0
        self.tradePrice = ""
        self.tradeVolume = ""
        self.tradeId = 0
        self.tradeTime = 0
        self.aggressor = False
        self.remainAmt = ""
        self.orderStatus = OrderState.INVALID
        self.clientOrderId = ""
        self.eventType = ""
        self.symbol = ""
        self.type = OrderType.INVALID
        self.accountId = 0

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.orderId, format_data + "Order Id")
        PrintBasic.print_basic(self.tradePrice, format_data + "Trade Price")
        PrintBasic.print_basic(self.tradeVolume, format_data + "Trade Volume")
        PrintBasic.print_basic(self.tradeId, format_data + "Trade Id")
        PrintBasic.print_basic(self.tradeTime, format_data + "Trade Timestamp")
        PrintBasic.print_basic(self.aggressor, format_data + "is Taker")
        PrintBasic.print_basic(self.orderStatus, format_data + "Order State")
        PrintBasic.print_basic(self.clientOrderId, format_data + "Client Order Id")
        PrintBasic.print_basic(self.eventType, format_data + "Event Type")
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.type, format_data + "Order Type")
        PrintBasic.print_basic(self.accountId, format_data + "Account Id")


class Order:
    """
    The detail order information.

    :member
        amount: The amount of base currency in this order.
        price: The limit price of limit order.
        created_timestamp: The UNIX formatted timestamp in UTC when the order was created.
        canceled_timestamp: The UNIX formatted timestamp in UTC when the order was canceled, if not canceled then has value of 0.
        finished_timestamp: The UNIX formatted timestamp in UTC when the order was changed to a final state. This is not the time the order is matched.
        order_id: The order id.
        symbol: The symbol, like "btcusdt".
        order_type: The order type, possible values are: buy-market, sell-market, buy-limit, sell-limit, buy-ioc, sell-ioc, buy-limit-maker, sell-limit-maker, buy-limit-fok, sell-limit-fok, buy-stop-limit-fok, sell-stop-limit-fok.
        filled_amount: The amount which has been filled.
        filled_cash_amount: The filled total in quote currency.
        filled_fees: The transaction fee paid so far.
        source: The source where the order was triggered, possible values: sys, web, api, app.
        state: The order state: submitted, partial-filled, cancelling, filled, canceled.
        stop_price : stop price used for buy-stop-limit，sell-stop-limit
        operator : only [gte] and [lte] to trigger buy-stop-limit，sell-stop-limit
    """

    def __init__(self):
        self.id = 0
        self.symbol = ""
        self.account_id = 0
        self.amount = 0.0
        self.price = 0.0
        self.created_at = 0
        self.canceled_at = 0
        self.finished_at = 0
        self.type = OrderType.INVALID
        self.filled_amount = 0.0
        self.filled_cash_amount = 0.0
        self.filled_fees = 0.0
        self.source = OrderSource.INVALID
        self.state = OrderState.INVALID
        self.client_order_id = ""
        self.stop_price = ""
        self.next_time = 0
        self.operator = ""

    @staticmethod
    def json_parse(json_data):
        order = fill_obj(json_data, Order)
        order.filled_amount = json_data.get("filled-amount", json_data.get("field-amount", 0))
        order.filled_cash_amount = json_data.get("filled-cash-amount", json_data.get("field-cash-amount", 0))
        order.filled_fees = json_data.get("filled-fees", json_data.get("field-fees", 0))
        return order

    @staticmethod
    def json_parse_list(json_data):
        if json_data and len(json_data):
            order_list = list()
            for idx, row in enumerate(json_data):
                order_item = Order.json_parse(row)
                order_list.append(order_item)
            return order_list

        return list()

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.id, format_data + "Order Id")
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.price, format_data + "Price")
        PrintBasic.print_basic(self.amount, format_data + "Amount")
        PrintBasic.print_basic(self.created_at, format_data + "Create Time")
        PrintBasic.print_basic(self.canceled_at, format_data + "Cancel Time")
        PrintBasic.print_basic(self.finished_at, format_data + "Finish Time")
        PrintBasic.print_basic(self.type, format_data + "Order Type")
        PrintBasic.print_basic(self.filled_amount, format_data + "Filled Amount")
        PrintBasic.print_basic(self.filled_cash_amount, format_data + "Filled Cash Amount")
        PrintBasic.print_basic(self.filled_fees, format_data + "Filled Fees")
        #PrintBasic.print_basic(self.account_type, format_data + "Account Type")
        PrintBasic.print_basic(self.source, format_data + "Order Source")
        PrintBasic.print_basic(self.state, format_data + "Order State")
        PrintBasic.print_basic(self.client_order_id, format_data + "Client Order Id")
        PrintBasic.print_basic(self.stop_price, format_data + "Stop Price")
        PrintBasic.print_basic(self.operator, format_data + "Operator")
        PrintBasic.print_basic(self.next_time, format_data + "Next Time")


class TradeClearingEvent:
    """
    subscribe trading clearing information

    :member
        action: current is "sub" for subscribe
        ch: subscribe topic.
        data: data detail in TradeClearing.
    """

    def __init__(self):
        self.action = ""
        self.ch = ""
        self.seq = 0
        self.data = TradeClearing()

    @staticmethod
    def json_parse(data_json):
        event_obj = TradeClearingEvent()
        event_obj.action = data_json.get("action")
        event_obj.ch = data_json.get("ch")
        event_obj.seq = data_json.get("seq", 0)
        event_obj.data = TradeClearing.json_parse(data_json.get("data", {}))
        return event_obj

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.ch, format_data + "Channel")
        self.data.print_object()


class TradeClearing:
    """
    The detail order information.

    :member
        order_id: The order id.
        symbol: The symbol, like "btcusdt".
        tradePrice: trade price.
        tradeVolume: trade Volume.
        orderSide: order Side, more to see OrderSide
        orderType: order type, more to see OrderType
        aggressor: is aggressor, only true or false
        tradeId: trade ID.
        tradeTime: trade Time.
        transactFee: transact Fee.
        feeDeduct: Deduct Fee.
        feeDeductType: fee Deduct Type, current only support ht and point
    """

    def __init__(self):
        self.symbol = ""
        self.orderId = 0
        self.tradePrice = ""
        self.tradeVolume = ""
        self.orderSide = OrderSide.INVALID
        self.orderType = OrderType.INVALID
        self.aggressor = False
        self.tradeId = 0
        self.tradeTime = 0
        self.transactFee = ""
        self.feeDeduct = ""
        self.feeDeductType = FeeDeductType.INVALID

    @staticmethod
    def json_parse(json_data):
        if json_data.get("orderId", None):
            return default_parse_list_dict(json_data, TradeClearing)
        else:
            return TradeClearing()

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.orderId, format_data + "Order Id")
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.tradePrice, format_data + "Trade Price")
        PrintBasic.print_basic(self.tradeVolume, format_data + "Trade Volume")
        PrintBasic.print_basic(self.orderSide, format_data + "Order Side")
        PrintBasic.print_basic(self.orderType, format_data + "Order Type")
        PrintBasic.print_basic(self.aggressor, format_data + "is Taker")
        PrintBasic.print_basic(self.tradeId, format_data + "Trade Id")
        PrintBasic.print_basic(self.tradeTime, format_data + "Trade Time")
        PrintBasic.print_basic(self.transactFee, format_data + "Transact Fee")
        PrintBasic.print_basic(self.feeDeduct, format_data + "Fee Deduct")
        PrintBasic.print_basic(self.feeDeductType, format_data + "Fee Deduct Type")


class TransactFeeRate:
    """
    The transact fee rate.

    :member
        symbol: symbol like "btcusdt"
        makerFeeRate: maker fee rate
        takerFeeRate: taker fee rate
        actualMakerRate: actual maker fee rate
        actualTakerRate: actual taker fee rate
    """

    def __init__(self):
        self.symbol = ""
        self.makerFeeRate = ""
        self.takerFeeRate = ""
        self.actualMakerRate = ""
        self.actualTakerRate = ""

    def print_object(self, format_data=""):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.symbol, format_data + "Symbol")
        PrintBasic.print_basic(self.makerFeeRate, format_data + "makerFeeRate")
        PrintBasic.print_basic(self.takerFeeRate, format_data + "takerFeeRate")
        PrintBasic.print_basic(self.actualMakerRate, format_data + "actualMakerRate")
        PrintBasic.print_basic(self.actualTakerRate, format_data + "actualTakerRate")
