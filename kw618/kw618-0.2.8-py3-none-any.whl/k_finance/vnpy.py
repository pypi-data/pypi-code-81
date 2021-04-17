
from logging import INFO
import multiprocessing
import sys
from time import sleep
from datetime import datetime, time


# 这里的vnpy直接是导入site-packages里的python包. (而不是在我'量化'目录下的项目!!) (所以要修改的话, 去到源文件去改!!)
from vnpy.trader.setting import SETTINGS
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.engine import EmailEngine
from vnpy.trader.event import EVENT_TICK
from vnpy.trader.object import *
from vnpy.trader.constant import *

# 每个网关都内含REST和Websocket两个API. (网关是数据的来源, 只要导入网关就可以获取币安所有数据.)
# from vnpy.gateway.ctp import CtpGateway # ctp网关需要用到米匡, 暂时用不了
from vnpy.gateway.binance import BinanceGateway
from vnpy.gateway.binances import BinancesGateway

from vnpy.app.cta_strategy import CtaStrategyApp, CtaEngine
from vnpy.app.cta_strategy.base import EVENT_CTA_LOG

from kw618.k_finance.const import * # 导入币安api-key



# 实例化三个主要的引擎
event_engine = EventEngine()
main_engine = MainEngine(event_engine)
cta_engine = main_engine.add_engine(CtaEngine)  # (会返回一个cat实盘引擎) (你中有我, 我中有你)
oms = main_engine.engines.get("oms")
# binance_rest_api = main_engine.gateways.get("BINANCE").rest_api

# 添加网关实例, 并connect它 (即: ui中的连接选项)
cta_engine.main_engine.add_gateway(BinanceGateway) # 已经生成了网关实例, 下挂在main_engine下
cta_engine.main_engine.add_gateway(BinancesGateway)
main_engine.connect(setting=connect_settings_binance_wyh, gateway_name="BINANCE")  # 把这个settings参数传递给对应gateway_name的网关实例, 供其建立连接
main_engine.connect(setting=connect_settings_binances_wyh, gateway_name="BINANCES")
binance_gateway = main_engine.gateways.get("BINANCE")
binances_gateway = main_engine.gateways.get("BINANCES")
spot_rest_api = main_engine.gateways.get("BINANCE").rest_api
futures_rest_api = main_engine.gateways.get("BINANCES").rest_api
spot_trade_ws_api = main_engine.gateways.get("BINANCE").trade_ws_api
futures_trade_ws_api = main_engine.gateways.get("BINANCES").trade_ws_api
spot_market_ws_api = main_engine.gateways.get("BINANCE").market_ws_api
futures_market_ws_api = main_engine.gateways.get("BINANCES").market_ws_api
# 因为连接是异步的, 要确保连接完成后才能进行下面的步骤, 所以这里要睡10s.  等待主引擎连接网关
sleep(15) # 经过测试, 10s还不够connect两个网关, 需要15s才算较为足够...




# temp
# ===========================
# cta_engine.init_engine( )
# cta_engine.init_all_strategies() # 这时候才开始获取tick数据





class SpreadClient():

    def __init__(self, main_engine=main_engine):
        """

            args:
                symbol: 应该做到'大小写不敏感', 需要在函数内部实现'大小写逻辑控制' (一般传入小写的货币对即可)

        """
        self.main_engine = main_engine
        self.oms = main_engine.engines["oms"]
        self.spot_rest_api = main_engine.gateways.get("BINANCE").rest_api
        self.futures_rest_api = main_engine.gateways.get("BINANCES").rest_api
        self.spot_trade_ws_api = main_engine.gateways.get("BINANCE").trade_ws_api
        self.futures_trade_ws_api = main_engine.gateways.get("BINANCES").trade_ws_api
        self.spot_market_ws_api = main_engine.gateways.get("BINANCE").market_ws_api
        self.futures_market_ws_api = main_engine.gateways.get("BINANCES").market_ws_api
        self.record_dict = {} # 用于记录价差率相关数据
        self.pairs = {} # 套利币对 (允许有多个币对)
        self.oms.futures_account = {} # 存放合约账户相关的重要信息 (关键是"维持保证金率"!!)
        self.get_margin_rate()

    def get_margin_rate(self):
        """
        function: 重新计算最新的'维持保证金率'(margin_rate), 以此来判断该合约账户是否快要爆仓...
        notes:
            1. 合约账户里的usdt账户的balance, 是可以由 trade_ws_api 动态地在oms_engine中更新余额 (实时监听事件, 更新余额)
                - 只有usdt的钱包余额是会监听事件动态更新的, 其他相关数据都有可能存在误差...
                - 解决方案: 在监听到这个事件后的回调函数中, 调用 self.gateway.rest_api.query_account()访问最新的account数据...
                        (但是有个问题, 这样会导致频繁请求req, io密集阻塞?? 在套利策略中极度影响执行速度!!)
                        (算了, 还是先不请求吧, 这个数据的更新有点延迟也影响不大... 真的需要使用该数据的时候,重新用rest_api请求就可以了)
            2. 但是合约账户里的usdt的'维持保证金'和'保证金余额'并不会由 trade_ws_api监听, 这就意味着当前数据有可能旧数据, 需要用过rest_api再请求一遍
        """
        self.futures_rest_api.query_account()
        # 因为上面的请求是异步的, 而后面的处理都是基于上面的req返回的数据的, 所以必须要等待它请求完成才能继续
        print("睡眠2秒, 等待请求最新的合约账户数据...")
        time.sleep(2)
        usdt_account = self.oms.accounts["BINANCES.USDT"]
        self.oms.futures_account["usdt_balance"] = usdt_account.balance # 未实现浮动盈亏
        self.oms.futures_account["pnl"] = usdt_account.pnl # 未实现浮动盈亏
        self.oms.futures_account["marginBalance"] = usdt_account.marginBalance # 保证金余额
        self.oms.futures_account["maintMargin"] = usdt_account.maintMargin # 维持保证金
        self.oms.futures_account["availableBalance"] = usdt_account.availableBalance # 可用划转余额
        self.oms.futures_account["margin_rate"] = self.oms.futures_account["maintMargin"] / self.oms.futures_account["marginBalance"]
        return self.oms.futures_account.get("margin_rate")


    def check_pair_name(self, pair):
        """
            function: 鉴于我经常把这个symbol/exchange拼错, 导致的各种bug... 提前先在oms.contract中检查...
            return: "BINANCE", "ETHUSDT"
        """

        # 1. '交易所'检查
        pair = pair.upper()
        exchange_name, symbol = pair.split(".")
        for ex in Exchange:
            if exchange_name == ex.name:
                exchange = ex
        if not exchange:
            msg = f"没有该交易所, 请检查..."
            raise Exception(msg)

        # 2. '币种'检查
        contracts_lst = list(oms.contracts)
        success = False
        for contract in contracts_lst:
            _sy, _ex = contract.split(".") # contract: 'wbtceth.BINANCE'
            if symbol == _sy:
                success = True
        if not success:
            msg = f"oms.contract中不存在该symbol..."
            raise Exception(msg)
        return exchange_name, symbol, exchange

    def check_pair_pos(self, pair_dict):
        """
            function: 核对pair的'对冲账户是否数量匹配'
            args:
                - pair_dict: self.pairs[pair] 得到的那个dict
            notes: - 一般用在add_pair中, 不单独对外使用
        """
        symbol = pair_dict.get("symbol") # "ethusdt"
        gateway_name_spot = pair_dict.get("gateway_name_spot") # "BINANCE"
        gateway_name_futures = pair_dict.get("gateway_name_futures") # "BINANCES"
        exchange_name = pair_dict.get("exchange_name") # "BINANCE"
            # i. 该币种的现货余额
        symbol_account = self.oms.accounts.get(f"{gateway_name_spot}.{symbol.upper()[:-4]}") # 这里是ETH不是ETHUSDT, 所以把后面4个字符删掉
        if symbol_account:
            spot_balance = symbol_account.balance
        else:
            spot_balance = 0 # 如果oms中没有该account, 则为0
            # ii. 该币种的合约持仓
        symbol_position = self.oms.positions.get(f"{symbol.upper()}.{exchange_name}.空")
        if symbol_position:
            futures_volume = symbol_position.volume
        else:
            futures_volume = 0 # 如果oms中没有该position, 则为0
            # iii. 现货和合约的volume总和  (做空的合约的volume为负数)
        sum_volume = spot_balance + futures_volume
        pair_dict["sum_volume"] = sum_volume
        pair_dict["spot_balance"] = spot_balance
        pair_dict["futures_volume"] = futures_volume
        if sum_volume == 0:
            pair_dict["equal_volume"] = True
        else:
            pair_dict["equal_volume"] = False

    def check_all_pair_pos(self):
        """
            function: 核对self.pairs中的每个币种的'对冲账户是否数量匹配'
            return: 每个pair的sum_volume
                eg:
                    {'BINANCE.CHZUSDT/sum_volume': -10.0,
                     'BINANCE.aliceUSDT/sum_volume': 5.3865379000000075}
        """
        # 遍历self.pairs, 核对这些pair的期现volume是否相等
        for pair_name, pair_dict in self.pairs.items():
            self.check_pair_pos(pair_dict=pair_dict)
        d = {}
        for pair_name, pair_dict in self.pairs.items():
            d.update({f"{pair_name}/sum_volume" : pair_dict.get("sum_volume")})
        return d

    def subscribe(self, pair):
        """
            function: 同时订阅'现货'和'期货'的tick数据 (都包含了'最优挂单信息')
                (前提: 要先add_pair(), 不能单独执行)
            args:
                symbol: 大小写不敏感 (一般小写即可)   # "ethusdt"

        """

        # 1. 初始化
        main_engine = self.main_engine
        pair_dict = self.pairs.get(pair)
        gateway_name_spot = pair_dict.get("gateway_name_spot") # BINANCE
        gateway_name_futures = pair_dict.get("gateway_name_futures") # BINANCES
        symbol = pair_dict.get("symbol") # ethusdt
        exchange = pair_dict.get("exchange") # Exchange.BINANCE (对象)
        exchange_name = pair_dict.get("exchange_name") # "BINANCE"

        # 2. 订阅tick数据
        while True:
            # i. 如果oms.ticks中有该tick数据, 则不重复subscribe
                # 当oms.ticks中同时存在 '现货'和'合约'的tick数据后, 才证明该函数订阅成功!
            msg = f"当前已经订阅tick的pair:\n{list(self.oms.ticks)}"
            logger.log(10, msg)
            if f"{symbol.lower()}.{exchange_name}" in list(self.oms.ticks) and f"{symbol.upper()}.{exchange_name}" in list(self.oms.ticks):
                time.sleep(4) # tick数据有了, 但是可能没有'最优挂单'数据??? 所以睡眠久一些, 让请求有时间去完成整个订阅过程
                return
            # ii. 如果oms.ticks中没有该tick数据, 则开始执行subscribe
            else:
                print(f"等待订阅 pair : {pair} 的tick数据... (直到订阅成功才会睡醒...)")
                    # i. 订阅'现货'的tick数据
                req = SubscribeRequest(symbol=symbol.lower(), exchange=exchange)
                main_engine.subscribe(req, gateway_name=gateway_name_spot)
                    # ii. 订阅'合约'的tick数据
                time.sleep(2) # 多个请求不要同时发送, 否则会出现各种莫名其妙的bug.... 多个请求之间一般都要睡眠一段时间比较好...
                req = SubscribeRequest(symbol=symbol.upper(), exchange=exchange)
                main_engine.subscribe(req, gateway_name=gateway_name_futures)
                time.sleep(4)
        return

    def add_pair(self, pair="BINANCE.ETHUSDT", to_subscribe=False):
        """
            function: 添加pair, 同时订阅该pair的 '现货and合约' 的tick数据
            args:
                pair: # BINANCE.ETHUSDT
                to_subscribe: True/False # 是否需要订阅tick数据(最优挂单信息)
            notes:
                - # exchange_name一定是大写的. (而symbol可能大写, 可能小写)
        """
        # 1. 核对该'pair'输入无误!!
        exchange_name, symbol, exchange = self.check_pair_name(pair=pair)

        # 2. 初始化一些数据
        gateway_name_spot = exchange_name
        gateway_name_futures = exchange_name + "S"
        vt_symbol_spot = f"{symbol.lower()}.{exchange_name}"
        vt_symbol_futures = f"{symbol.upper()}.{exchange_name}"
        symbol_spot = symbol.lower()
        symbol_futures = symbol.upper()
        symbol = symbol.lower()
        self.pairs.update(
            {
                pair : {
                    "gateway_name_spot" : gateway_name_spot, # BINANCE
                    "gateway_name_futures" : gateway_name_futures, # BINANCES
                    "vt_symbol_spot" : vt_symbol_spot, # ethusdt.BINANCE
                    "vt_symbol_futures" : vt_symbol_futures, # ETHUSDT.BINANCE
                    "symbol_spot" : symbol_spot, # ethusdt; (同vt_symbol_spot前半段)
                    "symbol_futures" : symbol_futures, # ETHUSDT; (同vt_symbol_futures前半段)
                    "symbol" : symbol, # ethusdt; (用小写来作为symbol的一般通用形式)
                    "exchange" : exchange, # Exchange.BINANCE (是个对象)
                    "exchange_name" : exchange_name, # 'BINANCE' (是个字符串)
                    "trading" : False, # 用于判断是否需要开启实盘交易...
                    "equal_volume" : False, # 用于判断某个pair的'期现数量是否相等'
                    "sum_volume" : -999,
                }
            }
        )
        self.record_dict.update({pair:[]})

        # 3. 核对pair的 '期现volume是否匹配'
        self.check_pair_pos(pair_dict=self.pairs[pair])

        # 4. 订阅该'pair'的tick'最优挂单'数据 (现货和合约)
        if to_subscribe:
            self.subscribe(pair=pair) # 订阅该'套利对'的现货和期货的tick数据

    def print_spread_rate(
            self, pair="BINANCE.ETHUSDT", cycle_count=1000, sleep_time=0.1
        ):
        """
            function: 传入一个pair, 打印该symbol现货和合约的'开仓价差'和'平仓价差率'
            args:
                pair: # BINANCE.ETHUSDT
        """
        # 1. 初始化
        pair = pair.upper()
        pair_dict = self.pairs.get(pair)
        if not pair_dict: # 这只是用于'重新add_pair', 其实已经没啥用了... 待删...
            self.add_pair(pair=pair, to_subscribe=True)
            pair_dict = self.pairs.get(pair)
        symbol = pair_dict.get("symbol")
        exchange_name = pair_dict.get("exchange_name")
        if (f"{symbol.lower()}.{exchange_name}" not in list(self.oms.ticks)) or \
            (f"{symbol.upper()}.{exchange_name}" not in list(self.oms.ticks)):
            msg = f"tick数据还没订阅成功, 请通过add_pair函数订阅pair后, 再重试...."
            raise Exception(msg)

        # 2. 循环获取最新的盘口数据, 并捕捉合适的'价差率'
        for count in range(cycle_count):
            # 3. 通过pair, 计算价差率
            spread_open, spread_rate_open, spread_close, spread_rate_close = self.cal_spread_rate(pair=pair)

            # 4. 打印
            msg = f"'开仓价差率' : {round(spread_rate_open*100, 4)}%;    '平仓价差率' : {round(spread_rate_close*100, 4)}%;"
            logger.log(20, msg)
            time.sleep(sleep_time)

    def cal_spread_rate(self, pair):
        """
            function: 传入一个pair, 得到该symbol现货和合约的'最优挂单信息', 返回'价差率'相关信息
            args:
                pair: # BINANCE.ETHUSDT
            return: '开仓价差', '开仓价差率', '平仓价差', '平仓价差率'
        """
        # 1. 初始化
        oms = self.oms
        pair_dict = self.pairs.get(pair)
        vt_symbol_spot = pair_dict.get("vt_symbol_spot") # ethusdt.BINANCE
        vt_symbol_futures = pair_dict.get("vt_symbol_futures") # ETHUSDT.BINANCE

        # 2. 获取两个实时'挂单信息' (得到现货/合约的买一/卖一价, 总共4个价格)
        spot_live = oms.ticks[vt_symbol_spot].live # 获取到实时推送的'现货-最优挂单信息'
        futures_live = oms.ticks[vt_symbol_futures].live # 获取到实时推送的'合约-最优挂单信息'
        spot_buy1_price = spot_live.get("bid_price_1") # 现货买一价
        spot_sell1_price = spot_live.get("ask_price_1") # 现货卖一价
        futures_buy1_price = futures_live.get("bid_price_1") # 合约买一价
        futures_sell1_price = futures_live.get("ask_price_1") # 合约卖一价

        # 3. 计算'价差率'
            # i. 开仓的价差率
        spread_open = futures_buy1_price - spot_sell1_price
        spread_rate_open = spread_open / spot_sell1_price
            # ii. 平仓的价差率
        spread_close = futures_sell1_price - spot_buy1_price
        spread_rate_close = spread_close / spot_buy1_price
        return spread_open, spread_rate_open, spread_close, spread_rate_close

    def run(
            self, pair="BINANCE.ETHUSDT", trading=False, continue_count=1,
            offset="OPEN", volume=1, alert_spread_rate=0.005,
            cycle_count=1000, sleep_time=0.1, to_check_balance=True
        ):
        """
            function:
                - 计算该实例中币种的'价差率', 并在'捕捉到某个指定的价差率'时, 立即用'市价单'下单 (指定是开仓or平仓)
                        (现货/合约双向下单)
                - 每次执行run(), 只能跑一个pair (所以现货和合约的gateway_name是固定的)
            args:
                pair: # "BINANCE.ETHUSDT"
                    以下变量由pair在self.pairs中获取:
                        exchange: # Exchange.BINANCE (是个对象! 不是字符串)
                        symbol: # ethusdt
                offset:
                    'OPEN': '开仓'套利币对
                    'CLOSE': '平仓'套利币对
                count: 1
                to_check_balance: True/False
                        (因为check一次需要浪费1ms的时间, 而套利的机会是毫秒级别的!! 当资金量足够的时候, 其实完全没有必要去check啊...)
                        (或者在run之前就测算好最多能交易多少volume, 并把这个volume记录在某个变量中, run执行中只要满足这个volume, 就可以执行交易..)
                            - 但问题是, 如果同时执行多个run(), 每个run又是不同币种, 上面的方法就不适用了...
                                (我们未来一定是要实现多币种同时在run的..)

            usage:
                eg1:
                    # 开始套利
                    symbol = "dentusdt"
                    sc.run(
                        pair=f"BINANCE.{symbol}", trading=True, offset="OPEN", volume=10,
                        alert_spread_rate=0.002, cycle_count=1000000, sleep_time=0.1
                    )

            todo: (优化方向)
                1. 当达到目标价差率之后, 等待3次0.1秒后, 再正式下单...否则容易被忽悠...
                    (观察到一些现象, 就是在毫秒级别的挂撤单, 严重影响盘口价差的真实性.. 而它速度太快导致我一般捕捉不到那种'变态的挂撤单')
                2. 函数自己计算每次的开仓数量... 不要每次都要我去计算100u大概是几个币... 函数自己捕获最新价去计算
                3. 可以设置一些开仓金额/开仓次数, 当达到目标价差率后, 自动多次开仓.. 不要变成一次性的run.. 频繁复制粘贴也比较麻烦..没有必要..明明它自己能重新开的..
                    # 其实可以不用打印吧... 它自己跑就行了?
                    # 或者开个多进程让它去跑... (这样我可以在同一个终端中开多个run()函数)
                4. 最好是多进程执行多个run函数...
                    1. 或者手动开启?:
                        手动的话可控一些, 想kill哪个就kill那个
                        (但其实有进程id, 我也可以控制多进程啊...也可以随意杀死某个进程)
                    2. 多进程跑的好处:
                        可以设置不同的交易量:
                            低价差率(0.3%): 交易金额在 50-100u左右 (成交快)
                            中价差率(0.35%): 交易金额在 300u左右
                            高价差率(0.4%): 交易金额在 500u左右 (赚的多)
                            # 如果是刚交割完, 还有8小时时间, 那就更多地设置在高价差率, 如果是接近交割了, 就需要更多挂在低价差率
                            # 前期: 这些倾向性的控制可以是手动控制;   后期: 这些细微的调整也可以由函数自发性的来完成
                5. 测试一下 check_balance() 函数的执行时间.... 我的交易都是毫秒级别的, 万一它浪费了我0.1秒, 我都血亏啊....
                        目前实测是 1ms, 看看怎么能优化它, 达到微秒级别?
                            (想想怎么优化这个函数的性能)





        """

        # 1. 初始化
        x = None # 初始化一个x.(当作'锁'?)
        pair = pair.upper()
        pair_dict = self.pairs.get(pair)
        if not pair_dict:
            self.add_pair(pair=pair, to_subscribe=True)
            pair_dict = self.pairs.get(pair)
        record_lst = self.record_dict[pair]
        exchange = pair_dict.get("exchange") # Exchange.BINANCE
        pair_dict.update({"trading":trading})
        symbol = pair_dict.get("symbol") # ethusdt
        exchange_name = pair_dict.get("exchange_name")
        if (f"{symbol.lower()}.{exchange_name}" not in list(self.oms.ticks)) or \
            (f"{symbol.upper()}.{exchange_name}" not in list(self.oms.ticks)):
            msg = f"tick数据还没订阅成功, 请通过add_pair函数订阅pair后, 再重试...."
            raise Exception(msg)

        # 2. 循环获取最新的盘口数据, 并捕捉合适的'价差率'
        for count in range(cycle_count):
            # 3. 通过pair, 计算价差率
            spread_open, spread_rate_open, spread_close, spread_rate_close = self.cal_spread_rate(pair=pair)

            # 4. 处理'价差率'
            # msg = f"[开仓 - {symbol}]     价差:{round(spread, 6)},    价差率:{round(spread_rate*100, 4)}%"
            # logger.log(20, msg)
            if (spread_rate_open < 0.0023) and (spread_rate_close > 0):
                msg = '价差率在一个无聊的区间...'
                if x != '0':
                    logger.log(20, msg)
                    x = '0'
            elif (0.0023 <= spread_rate_open < 0.0025) or (-0.0002 < spread_rate_close <= 0.0000):
                if (0.0023 <= spread_rate_open < 0.0025):
                    msg = f"[{symbol}]   开仓 - 价差率区间: [0.23% 至 0.25%]   ({round(spread_rate_open*100, 4)}%)"
                if (-0.0002 < spread_rate_close <= 0.0000):
                    msg = f"[{symbol}]   平仓 - 价差率区间: [-0.02% 至 0.00%]   ({round(spread_rate_close*100, 4)}%)"
                if x != '1':
                    logger.log(20, msg)
                    x = '1'
            elif (0.0025 <= spread_rate_open < 0.0030) or (-0.0007 < spread_rate_close <= -0.0002):
                if (0.0025 <= spread_rate_open < 0.0030):
                    msg = f"[{symbol}]   开仓 - 价差率区间: [0.25% 至 0.30%]   ({round(spread_rate_open*100, 4)}%)"
                if (-0.0007 < spread_rate_close <= -0.0002):
                    msg = f"[{symbol}]   平仓 - 价差率区间: [-0.07% 至 -0.02%]   ({round(spread_rate_close*100, 4)}%)"
                if x != '2':
                    logger.log(20, msg)
                    x = '2'
            elif (0.0030 <= spread_rate_open < 0.0035) or (-0.0012 < spread_rate_close <= -0.0007):
                if (0.0030 <= spread_rate_open < 0.0035):
                    msg = f"[{symbol}]   开仓 - 价差率区间: [0.30% 至 0.35%]   ({round(spread_rate_open*100, 4)}%)"
                if (-0.0012 < spread_rate_close <= -0.0007):
                    msg = f"[{symbol}]   平仓 - 价差率区间: [-0.12% 至 -0.07%]   ({round(spread_rate_close*100, 4)}%)"
                if x != '3':
                    logger.log(20, msg)
                    x = '3'
            else:
                if (0.0035 <= spread_rate_open):
                    msg = f"[{symbol}]   开仓 - 价差率区间: >= 0.35%   ({round(spread_rate_open*100, 4)}%)"
                if (spread_rate_close <= -0.0012):
                    msg = f"[{symbol}]   平仓 - 价差率区间: <= -0.12%   ({round(spread_rate_close*100, 4)}%)"
                if x != '4':
                    logger.log(20, msg)
                    x = '4'

            # 5. 下单: (达到目标价差率)
            if (offset == 'OPEN') and (spread_rate_open >= alert_spread_rate):
                # 1. 开仓: 做空卖出合约, 买入现货;
                alert_msg = f"[提醒] =====>  当前'开仓'价差率: {round(spread_rate_open*100, 4)}, 大于{alert_spread_rate*100}%, 适合执行'开仓'操作....\n\n"
                logger.log(30, alert_msg)
                d = {
                    "spread_open" : spread_open, "spread_close" : spread_close,
                    "spread_rate_open" : spread_rate_open, "spread_rate_close" : spread_rate_close,
                    "offset" : offset, "alert_spread_rate" : alert_spread_rate,
                    }
                if pair_dict.get("trading"):
                    success = self.two_sides_send_order(pair=pair, offset="OPEN", volume=volume, to_check_balance=to_check_balance) # 双边下单
                    if not success:
                        return
                    msg = f"\n--------> 开仓成功~!\n"
                    logger.log(30, msg)
                    record_lst.append(d)
                    pair_dict.update({"trading":False}) # 成功交易一笔后, 就把trading设为False, 可以自行在控制台开启

                # break # 一旦达到'目标价差率'先break退出


            elif (offset == 'CLOSE') and (spread_rate_close <= alert_spread_rate):
                # 2. 平仓: 平空买入合约, 卖出现货;
                alert_msg = f"[提醒] =====>  当前'平仓'价差率: {round(spread_rate_close*100, 4)}, 小于{alert_spread_rate*100}%, 适合执行'平仓'操作....\n\n"
                logger.log(30, alert_msg)
                d = {
                    "spread_open" : spread_open, "spread_close" : spread_close,
                    "spread_rate_open" : spread_rate_open, "spread_rate_close" : spread_rate_close,
                    "offset" : offset, "alert_spread_rate" : alert_spread_rate,
                    }
                if pair_dict.get("trading"):
                    success = self.two_sides_send_order(pair=pair, offset="CLOSE", volume=volume, to_check_balance=to_check_balance) # 双边下单
                    if not success:
                        return
                    msg = f"\n--------> 平仓成功~!\n"
                    logger.log(30, msg)
                    record_lst.append(d)
                    pair_dict.update({"trading":False}) # 成功交易一笔后, 就把trading设为False, 可以自行在控制台开启

            # 休眠
            time.sleep(sleep_time)

    def check_balance(self, pair, volume, offset):
        """

            function: 核对本账户是否有足够的仓位.. (但是...合适的价差率转瞬即逝...你确定要在每次下单前还在先req一下position嘛....)
                    解决: 本地来管理这个pos, 这样不会浪费太多时间...
                    解决2: 压根不需要重新req呀.....我的trade_ws_api实时更新这个pos状态, 直接去oms.position取值就好了....
                    为了防止一边开仓, 另一边余额不够开不了仓的情况发生, 最好还是取值判断一下...

            args:
                - volume: 准备去交易的币种数量.. (本函数就是用于核对是否有足够的usdt来购买这些volume)
                - offset: "OPEN"/"CLOSE"  (开仓或者平仓的check方式不太一样, 所以一定要有这个参数...)
            notes:
                - **(volume是指币种数量, qty是指usdt数量)
                - 用volume形容合约的持仓, 用balance形容现货的余额

        """

        # 1. 查询当前余额
        pair = pair.upper()
        pair_dict = self.pairs.get(pair)
        if not pair_dict: # 这只是用于'重新add_pair', 其实已经没啥用了... 待删...
            self.add_pair(pair=pair, to_subscribe=True)
            pair_dict = self.pairs.get(pair)
        gateway_name_spot = pair_dict.get("gateway_name_spot") # "BINANCE"
        gateway_name_futures = pair_dict.get("gateway_name_futures") # "BINANCES"
        symbol = pair_dict.get("symbol") # "ethusdt"
        exchange_name = pair_dict.get("exchange_name") # "BINANCE"
        if (f"{symbol.lower()}.{exchange_name}" not in list(self.oms.ticks)) or \
            (f"{symbol.upper()}.{exchange_name}" not in list(self.oms.ticks)):
            msg = f"tick数据还没订阅成功, 请通过add_pair函数订阅pair后, 再重试...."
            raise Exception(msg)
            # i. 现货USDT余额
        usdt_balance_spot = self.oms.accounts[f"{gateway_name_spot}.USDT"].balance
            # ii. 合约USDT余额 (即: 钱包余额) (即: 最真实的保证金, 不考虑合约的浮盈浮亏!!)
        usdt_balance_futures = self.oms.accounts[f"{gateway_name_futures}.USDT"].balance

        # 2. 查询当前币种的最新价格
        last_price_spot = oms.ticks[f"{symbol.lower()}.{exchange_name}"].last_price
        last_price_futures = oms.ticks[f"{symbol.upper()}.{exchange_name}"].last_price

        # 3. 计算当前待开仓的qty **(volume是指币种数量, qty是指usdt数量)
        qty_spot = last_price_spot * volume
        qty_futures = last_price_futures * volume
        if (qty_spot <= 10) or (qty_futures <= 10):
            msg = f"[不满足最低交易额] 待交易现货qty : {qty_spot}; 待交易合约qty : {qty_futures}"
            raise Exception(msg)
            # logger.log(40, msg)
            # return False

        # 4. 计算当前账户能够支付的volume
        supported_volume_spot = usdt_balance_spot // (last_price_spot * 1.03) # 预留3%的余量..确保价格剧烈波动中也一定能买入!
        supported_volume_futures = usdt_balance_futures // (last_price_futures * 1.03) # 预留3%的余量..确保价格剧烈波动中也一定能买入!
        msg = f"现货USDT : {usdt_balance_spot}; 合约钱包余额USDT : {usdt_balance_futures}"
        logger.log(10, msg)
        msg = f"现货最大买入量: {supported_volume_spot}个币; 合约最大买入量: {supported_volume_futures}个币; 当前volume: {volume}"
        logger.log(10, msg)

        # 4. 判断是否能够买入
        if supported_volume_spot < volume:
            msg = f"############## 现货USDT不足!!!  [无法交易]\n"
            raise Exception(msg)
            # return False
        if supported_volume_futures < volume:
            msg = f"############## 合约钱包余额不足!!!  [无法交易]\n"
            raise Exception(msg)
            # return False
        msg = f"============== 余额检测通过!!  [允许交易]\n"
        logger.log(30, msg)
        return True

    def two_sides_send_order(self, pair, offset, volume, to_check_balance=True):
        """
            function:
                - 检查: 现货和期货的剩余资金是否足够下单
                - 下单:
                    1.先合约下单
                    2.后现货下单
        """

        # 1. 初始化
        pair = pair.upper()
        pair_dict = self.pairs.get(pair)
        if not pair_dict:
            self.add_pair(pair=pair, to_subscribe=True)
            pair_dict = self.pairs.get(pair)
        gateway_name_spot = pair_dict.get("gateway_name_spot") # BINANCE
        gateway_name_futures = pair_dict.get("gateway_name_futures") # BINANCES
        exchange = pair_dict.get("exchange") # Exchange.BINANCE (是对象不是str)
        symbol = pair_dict.get("symbol") # "ethusdt"
        exchange_name = pair_dict.get("exchange_name") # "BINANCE"
        if (f"{symbol.lower()}.{exchange_name}" not in list(self.oms.ticks)) or \
            (f"{symbol.upper()}.{exchange_name}" not in list(self.oms.ticks)):
            msg = f"tick数据还没订阅成功, 请通过add_pair函数订阅pair后, 再重试...."
            raise Exception(msg)

        # 开仓: 做空卖出合约, 买入现货;
        if offset == "OPEN":
            # 1. 核对仓位余额
            if to_check_balance == True:
                self.check_balance(pair=pair, volume=volume, offset=offset)
            # 2. 做空卖出合约
            req_futures = OrderRequest(
                exchange=exchange, symbol=symbol, offset=Offset.OPEN, direction=Direction.SHORT,
                type=OrderType.MARKET, price=None, volume=volume
            )
            vt_orderid_futures = main_engine.send_order(req_futures, gateway_name=gateway_name_futures)
            # 3. 买入现货
            req_spot = OrderRequest(
                exchange=exchange, symbol=symbol, offset=Offset.OPEN, direction=Direction.LONG,
                type=OrderType.MARKET, price=None, volume=volume
            )
            vt_orderid_spot = main_engine.send_order(req_spot, gateway_name=gateway_name_spot)

        # 平仓: 平空买入合约, 卖出现货;
        elif offset == "CLOSE":
            # 1. 核对仓位余额
            if to_check_balance == True:
                self.check_balance(pair=pair, volume=volume, offset=offset)
            # 2. 平空买入合约
            req_futures = OrderRequest(
                exchange=exchange, symbol=symbol, offset=Offset.CLOSE, direction=Direction.LONG,
                type=OrderType.MARKET, price=None, volume=volume
            )
            vt_orderid_futures = main_engine.send_order(req_futures, gateway_name=gateway_name_futures)
            # 3. 卖出现货
            req_spot = OrderRequest(
                exchange=exchange, symbol=symbol, offset=Offset.CLOSE, direction=Direction.SHORT,
                type=OrderType.MARKET, price=None, volume=volume
            )
            vt_orderid_spot = main_engine.send_order(req_spot, gateway_name=gateway_name_spot)

    def send_order(self, exchange, gateway_name, symbol, offset, direction, type, price=10, volume=1):
        """
            function: 封装后的send_order
            args:
                exchange:
                    Exchange.BINANCE (是个对象, 不是'BINANCE'字符串)
                gateway_name:
                    现货: 'BINANCE'
                    合约: 'BINANCES'
                symbol:
                    现货: 小写 # 'btcusdt'
                    合约: 大写 # 'BTCUSDT'
                offset:
                    开仓: "OPEN"   # 对应vnpy的 Offset.OPEN
                    平仓: "CLOSE"   # 对应vnpy的 Offset.CLOSE
                direction:
                    买入: "BUY"   # 对应vnpy的 Direction.LONG
                    卖出: "SELL"   # 对应vnpy的 Direction.SHORT
                type:
                    限价单: OrderType.LIMIT
                    市价单: OrderType.MARKET
            return:
                返回 该函数生成的req生成的order 下的 order.vt_orderid
                    # vt_orderid: "BINANCE.mUvoqJxFIILMdfAW5iGSOW"

            usage:
                eg1:
                    # 单独下单
                    symbol = "dentusdt"
                    sc.send_order(
                        exchange=Exchange.BINANCE, gateway_name="BINANCE",
                        symbol="chzusdt", offset='OPEN', direction='BUY', type="MARKET", price=15, volume=20
                    )

        """

        pair = f"{exchange.name}.{symbol.upper()}"
        self.check_balance(pair=pair, volume=volume, offset=offset)
        req = OrderRequest(
            exchange=exchange, symbol=symbol, offset=OFFSET_KW2VT[offset], direction=DIRECTION_KW2VT[direction],
            type=ORDERTYPE_KW2VT[type], price=price, volume=volume
        )
        # 发送请求 (即: 下单)
        vt_orderid = main_engine.send_order(req, gateway_name=gateway_name)
        msg = f"交易成功!!!\n"
        logger.log(20, msg)
        return vt_orderid

    def req_mytrade(self, pair="BINANCE.ETHUSDT", type="spot", df_type="3", query_date="today", direction=None):
        """
            function:
                - 请求历史成交记录, 复盘实际成交的价差率如何...
            args:
                - is_original: True/False  # 是否需要返回new_df, 还是过滤了不重要列的 _df
                - df_type: df的类型(根据df处理的顺序来决定):
                    - 1: 透视后的df
                    - 2: 透视表与原表联结的df (所有原字段)
                    - 3: 透视表与原表联结的df (挑选部分重要字段)
                - query_date: "today"/"2021-03-30"   # 选择某一天的数据生成df
                - direction: "BUY"/"SELL"/None    # 筛选不同买卖方向的df (None则不区分'买卖方向')

            usage:
                eg1:
                    symbol = "DENTUSDT"
                    s_df = sc.req_mytrade(symbol=symbol, type="spot", query_date="2021-03-30", is_original=False, direction="BUY")
                    f_df = sc.req_mytrade(symbol=symbol, type="futures", query_date="2021-03-30", is_original=False, direction="SELL")
                    sc.cal_avg_price(f_df) / sc.cal_avg_price(s_df)

        """

        # 1. 构造req对象, 并发送请求
        exchange_name, symbol = pair.split(".")
        req = MyTradesRequest(symbol=symbol.lower(), exchange=Exchange[exchange_name])
        if type == "spot":
            mytrade_dict = self.spot_rest_api.query_myTrades(req)
        elif type == "futures":
            mytrade_dict = self.futures_rest_api.query_myTrades(req)
        else:
            return
        # 2. 处理response数据, 转变成'目标df'
        df = pd.DataFrame(mytrade_dict)
        if len(df) == 0:
            msg = f"没有 {symbol} 的相关交易记录... 请检查是否有发生过交易.."
            raise Exception(msg)
            # df默认的时区是'naive'(即:没有时区)
            # 这里需要先定义当前的时间戳是哪个时区, 然后需要转换成哪个时区...
            # 目前df整列换时区唯一的解决办法:
        # df["time"] = pd.to_datetime(df["time"], unit="ms") + pd.to_timedelta("8h") # utc改成北京时间
        df["time"] = pd.to_datetime(df['time'], unit="ms").dt.tz_localize('UTC').dt.tz_convert('hongkong') # 转化成东八区的时间
        if type == "spot":
            df[['price', 'qty', 'quoteQty', 'commission']] = df[['price','qty', 'quoteQty', 'commission']].apply(pd.to_numeric)
            if direction == "BUY":
                df = df[df["isBuyer"]==True]
            elif direction == "SELL":
                df = df[df["isBuyer"]==False]
            # 如果direction不指定"BUY"or"SELL", 那么就不会进行筛选, 原df输出
        elif type == "futures":
            df[['price', 'qty', 'quoteQty', 'commission', 'realizedPnl']] = df[['price','qty', 'quoteQty', 'commission', 'realizedPnl']].apply(pd.to_numeric)
            if direction == "BUY":
                df = df[df["buyer"]==True]
            elif direction == "SELL":
                df = df[df["buyer"]==False]
            # 如果direction不指定"BUY"or"SELL", 那么就不会进行筛选, 原df输出
        else:
            raise Exception("没有此type...")
        df = df[df["time"] >= get_timestamp(query_date)]
        if len(df) == 0:
            msg = f"日期筛选后的 mytrade_df 为空...检查交易时间或者direction..."
            raise Exception(msg)
        tmp_df = df.pivot_table(index="orderId", aggfunc={"qty":"sum", "quoteQty":"sum"})
        tmp_df["avg_price"] = tmp_df["quoteQty"] / tmp_df["qty"]
        tmp_df.rename(columns={"qty":"order_qty", "quoteQty":"order_quoteQty", "avg_price":"order_avg_price"}, inplace=True)
        new_df = pd.merge(df, tmp_df, how="left", on="orderId")
        _df = new_df[["symbol", "orderId", "qty", "price", "quoteQty", "order_qty", "order_avg_price", "commission", "time"]]

        if df_type == "1":
            return tmp_df
        elif df_type == "2":
            return new_df
        else:
            # 不管是"3"或者其他任何数字, 都返回_df
            return _df

    def get_trade_spread_rate(self, pair="BINANCE.ETHUSDT", offset="OPEN", query_date="today"):

        # 1. 请求获得现货/合约的 trade_df (每笔交易数据)
        if offset == "OPEN":
                # i. 现货的'买入'trade
            s_df = sc.req_mytrade(pair=pair, type="spot", query_date="today", df_type="1", direction="BUY")
                # ii. 合约的'卖出'trade
            f_df = sc.req_mytrade(pair=pair, type="futures", query_date="today", df_type="1", direction="SELL")
        elif offset == "CLOSE":
                # i. 现货的'卖出'trade
            s_df = sc.req_mytrade(pair=pair, type="spot", query_date="today", df_type="1", direction="SELL")
                # ii. 合约的'买入'trade
            f_df = sc.req_mytrade(pair=pair, type="futures", query_date="today", df_type="1", direction="BUY")
        else:
            raise Exception("没有此offset...")

        # 2. 计算每笔trade的价差率
        spread_rate_arr = f_df["order_avg_price"].values / s_df["order_avg_price"].values
        qty_rate_arr = f_df["order_qty"].values / s_df["order_qty"].values
        order_qty_arr = f_df["order_qty"].values
        df = pd.DataFrame({"qty_rate":qty_rate_arr, "order_qty":order_qty_arr, "spread_rate":spread_rate_arr})
        return df

    def cal_avg_price(self, df):
        "计算这个df中交易数据的平均价格"
        avg_price = df["quoteQty"].sum() / df["qty"].sum()
        return avg_price




sc = SpreadClient(main_engine=main_engine)













#
