import datetime
import pandas as pd
import numpy as np
import scipy.optimize as sco
from numpy.linalg import inv

class ModelCalulator:

    STATS_DICT = {
        'ret':0,
        'std':1,
        'sharpe':2,
    }

    def __init__(self, risk_free:float=0.03, trading_day_per_year:int=242):
        """
        - ''risk_free'' - (float) risk free rate default 0.03
        - ''trading_day_per_year'' -(int) trading day each year 242 or 252
        """
        self.risk_free = risk_free
        self.trading_day_per_year = trading_day_per_year

    def _calc_statistics(self, weights, *args):    
        returns = args[0]
        if len(args) == 1:
            ret_mean = returns.mean()
            ret_cov = returns.cov()
        else:
            ret_mean = args[1]
            ret_cov = args[2]
            
        weights = list(weights)
        
        weights = np.array(weights)

        port_ret = np.sum(ret_mean * weights)*self.trading_day_per_year

        port_std = np.sqrt(np.dot(weights.T, np.dot(ret_cov*self.trading_day_per_year,weights)))

        return np.array([port_ret, port_std, (port_ret-self.risk_free)/port_std])

    def _cons_parse(self, returns:pd.DataFrame, asset_weight_cons:list=[], port_stats_cons:list=[]):
        asset_list = returns.columns.tolist() 
        # 默认权重合为1
        cons = ({'type':'eq','fun':lambda x: np.sum(x) - 1},)
        # 资产权重条件
        for asset_weight_con_i in asset_weight_cons:
            asset_id = asset_weight_con_i[0]
            method = asset_weight_con_i[1]
            num = asset_weight_con_i[2]
            asset_idx = asset_list.index(asset_id)
            print(asset_id, method, num, asset_idx)
            if method == '=':
                cons += ({'type':'eq','fun':lambda x: x[asset_idx] - num},)
            elif method == '>=':
                cons += ({'type':'ineq','fun':lambda x: x[asset_idx] - num},) 
            elif method == '<=':
                cons += ({'type':'ineq','fun':lambda x: -x[asset_idx] + num},) 
        # 组合指标条件
        for port_stats_con_i in port_stats_cons:
            stat_name = port_stats_con_i[0]
            method = port_stats_con_i[1]
            num = port_stats_con_i[2]
            idx = self.STATS_DICT[stat_name]
            print(stat_name, method, num, idx)
            if method == '=':
                cons += ({'type':'eq','fun':lambda x: self._calc_statistics(x,(returns))[idx] - num}, )
            elif method == '>=':
                cons += ({'type':'ineq','fun':lambda x: self._calc_statistics(x,(returns))[idx] - num}, )
            elif method == '<=':
                cons += ({'type':'ineq','fun':lambda x: -self._calc_statistics(x,(returns))[idx] + num}, )
        return cons

    def _view_parse(self, investor_views:list, returns:pd.DataFrame, market_weights:list):
        def _asset_weight_sum(assets, market_weights, asset_list):
            return sum(market_weights[asset_list.index(asset_id)] for asset_id in assets)
        
        asset_list = returns.columns.tolist()
        views = []
        pick_list = []
        view_confidences = []
        for view_i in investor_views:
            good_assets = view_i[0]
            bad_assets = view_i[1]
            ret = view_i[2]
            confidence = view_i[3]
            views.append(ret)
            view_confidences.append(confidence)
            pick_dict = {}
            good_asset_weights = _asset_weight_sum(good_assets, market_weights, asset_list)
            bad_asset_weights = _asset_weight_sum(bad_assets, market_weights, asset_list)
            for asset_id in good_assets:
                w = market_weights[asset_list.index(asset_id)]
                pick_dict[asset_id] = w / good_asset_weights
            for asset_id in bad_assets:
                w = market_weights[asset_list.index(asset_id)]
                pick_dict[asset_id] = - w/ bad_asset_weights
            pick_list.append(pick_dict)
        return views, pick_list, view_confidences    

    def _max_sharpe(self, weights, *args):   
        return -self._calc_statistics(weights, *args)[2]

    def _min_vol(self, weights, *args):
        return self._calc_statistics(weights, *args)[1]
        
    def _max_ret(self, weights, *args):
        return -self._calc_statistics(weights, *args)[0]

    def _get_opt_weight(self, opts, fund_list):
        return pd.DataFrame(np.reshape(opts.x.round(3), newshape=(1,len(opts.x))), columns=fund_list)

    def _get_port_stats(self, opts, returns):
        return pd.DataFrame(np.reshape(self._calc_statistics(opts.x,(returns)).round(3), newshape=(1,3)),columns=['年化收益','年化波动','夏普率'])

    def _calculate_risk(self, risk_method, returns, fund_nav, day_per_year):
        if risk_method == 'annual_vol':
            risk = returns.std(ddof=1)*np.sqrt(day_per_year)
        elif risk_method == 'mdd':
            risk = 1 - (fund_nav / fund_nav.cummax()).min()
        elif risk_method == 'var':
            risk = returns.quantile(0.05)
        elif risk_method == 'cvar':
            var = returns.quantile(0.05)
            risk = returns[returns < var].mean()
        risk = np.array(risk)
        return risk
        
    def _risk_budget_objective(self, x, *pars):
        risk_method = pars[0]           
        target_risk_weight = pars[1]         
        returns = pars[2] 
        fund_nav = pars[3]    
        day_per_year = pars[4]

        risk = self._calculate_risk_contribution(x, risk_method, returns, fund_nav, day_per_year)
        risk = risk * 100
        s2 = np.sum(target_risk_weight)
        target_risk_weight = target_risk_weight/s2*100
        s = np.square(risk-target_risk_weight.T)
        J = np.sum(np.diagonal(s))
        return J

    def _calculate_risk_contribution(self, x, risk_method, returns, fund_nav, day_per_year):
        risk = self._calculate_risk(risk_method, returns, fund_nav, day_per_year)
        risk = risk * np.array(x)
        risk.resize((risk.shape[0],1))
        risk = np.matrix(risk)
        s1 = np.sum(risk)
        risk = risk/s1
        return risk

    def _total_weight_constraint(self,x):
        return np.sum(x)-1.0

    def _long_only_constraint(self,x):
        return x

    def get_opt_weight(self):
        return self.weights
    
    def get_ports_stats(self):
        return self.port_stats

    def get_asset_risk(self):
        return self.port_asset_risk


class MeanVarianceModel(ModelCalulator):

    def __init__(self,risk_free:float=0.03, trading_day_per_year:int=242): 
        super().__init__(risk_free=risk_free, trading_day_per_year=trading_day_per_year)
        
    def process(self, returns:pd.DataFrame,opt_method:str,asset_weight_cons:list=[],port_stats_cons:list=[]):
        """
        均值方差模型

        - ''returns'' - (pd.DataFrame) columns name is asset name
        - ''opt_method'' str,  in ['max_sharpe', 'limit_std', 'limit_ret']
        - ''asset_weight_cons'' - (list of list) 某资产权重限制 
            每单元由三部分组成： [000001!0, '<=', 0.6]
                        1 资产id （str） 
                        2 大小方式（str） ’=’ ‘>=’ '<='
                        3 权重数  (float)    
        - ''port_stats_cons'' - (list of list) 组合指标限制
            每单元由三部分组成：['std', '<=', 0.2]
                        1 指标：['ret','std','sharpe']
                        2 大小方式（str） ’=’ ‘>=’ '<='
                        3 指标数  (float)                      
        """ 
        cons = self._cons_parse(returns, asset_weight_cons, port_stats_cons)
        # 增加资产cash
        returns.loc[:,'cash'] = 0
        asset_list = returns.columns.tolist()
        noa = len(asset_list)
        bnds = tuple((0,1) for x in range(noa)) # 权重限制在0,1之间 不允许做空
        if opt_method == 'max_sharpe':
            opt_func = self._max_sharpe
        elif opt_method == 'max_ret':
            opt_func = self._max_ret
        elif opt_method == 'min_std':
            opt_func = self._min_vol
        opts = sco.minimize(fun=opt_func, args=(returns), x0=noa*[1./noa,], method='SLSQP', bounds=bnds, constraints=cons)
        self.weights = self._get_opt_weight(opts, asset_list)
        self.port_stats = self._get_port_stats(opts, returns)

class BlackLittermanModel(ModelCalulator):

    def __init__(self,risk_free:float=0.03, trading_day_per_year:int=242): 
        super().__init__(risk_free=risk_free, trading_day_per_year=trading_day_per_year)

    def process(self,   returns:pd.DataFrame,
                        market_weights:list,
                        investor_views:list,
                        tau:float,
                        opt_method:str,
                        risk_aversion:float,
                        omega_method:str,
                        asset_weight_cons:list=[],
                        port_stats_cons:list=[]):
        """
        Black Litterman 模型             
        - ''returns'' - (pd.DataFrame) columns name is asset name
        - ''asset_list'' - (list) asset name
        - ''market_weights'' - (list) weight of asset [36, 8, 56] i.e. sum up to 100
        - ''investor_views'' - (list of list) investor view information list
        ‘’看好的资产‘’ 比 ‘’看衰的资产‘’ 收益高 ‘’观点内的收益‘’， 信心水平 ''信心水平'' 
            每单元由四部分组成：[[],[],float,float]
                        1. 看好的资产列表 list 
                        2. 看衰的资产列表 list 
                                            如果看衰的资产列表非空，表示观点是相对观点 As 好于 Bs
                                            如果看衰的资产列表为空，表示观点是绝对观点 As 好
                        3. 观点内的收益 float 
                        4. 信心水平    float
        - ''tau'' - (float) investor view parameter less than 0.05,
        - ''opt_method'' - (str), 'max_sharpe' 'max_ret' 'min_std'
        - ''risk_aversion'' - (float) risk aversion, expected measures of returns with one measure of risk
        - ''omega_method'' - (str) 'prior_variance' or 'user_confidences'
                            prior_variance: investor confidence calculated by market history
                            user_confidences: investor confidence provide by user
        - ''asset_weight_cons'' - (list of list) 某资产权重限制 
            每单元由三部分组成： [000001!0, '<=', 0.6]
                        1 资产id （str） 
                        2 大小方式（str） ’=’ ‘>=’ '<='
                        3 权重数  (float)    
        - ''port_stats_cons'' - (list of list) 组合指标限制
            每单元由三部分组成：['std', '<=', 0.2]
                        1 指标：['ret','std','sharpe']
                        2 大小方式（str） ’=’ ‘>=’ '<='
                        3 指标数  (float)       
        """
        investor_views, pick_list, view_confidences = self._view_parse(investor_views,returns,market_weights)
        cons = self._cons_parse(returns, asset_weight_cons, port_stats_cons)

        # step 0 data prepare
        returns.loc[:,'cash'] = 0
        asset_list = returns.columns.tolist()
        market_capitalised_weights = market_weights + [0]
        covariance = returns.cov()
        asset_names = returns.columns.tolist()
        noa = len(asset_list)
        bnds = tuple((0,1) for x in range(noa)) # 权重限制在0,1之间 不允许做空

        # step 1
        num_assets = len(market_capitalised_weights)
        num_views = len(view_confidences)
        if asset_names is None:
            if covariance is not None and isinstance(covariance, pd.DataFrame):
                asset_names = covariance.columns
            else:
                asset_names = list(map(str, range(num_assets)))

        # step 2 pre process inputs
        investor_views = np.array(np.reshape(investor_views, newshape=(len(investor_views), 1)))
        market_capitalised_weights = np.array(np.reshape(market_capitalised_weights, newshape=(len(market_capitalised_weights), 1)))
        if isinstance(covariance, pd.DataFrame):
            covariance = covariance.values

        # step 3 calculate implied equilbrium returns
        implied_equilibrium_returns = risk_aversion * covariance.dot(market_capitalised_weights)

        # step 4 create the pick matrix (P) from user specified assets involved in the views
        pick_matrix = np.zeros((num_views, num_assets))
        pick_matrix = pd.DataFrame(pick_matrix, columns=asset_names)
        for view_index, pick_dict in enumerate(pick_list):
            assets = list(pick_dict.keys()) 
            values = list(pick_dict.values())
            pick_matrix.loc[view_index, assets] = values
        pick_matrix = pick_matrix.values

        # step 5 build the covariance matrix of errors in investor views (omega)
        if omega_method == 'prior_variance':
            print('without view confidences')
            omega = pick_matrix.dot((tau * covariance).dot(pick_matrix.T))
        else:
            print('include detault view confidences ')
            view_confidences = np.array(np.reshape(view_confidences, (1, len(view_confidences))))
            alpha = (1 - view_confidences) / view_confidences
            omega = alpha * pick_matrix.dot(covariance).dot(pick_matrix.T)
        omega = np.diag(np.diag(omega))
        omega = np.array(np.reshape(omega, (num_views, num_views)))

        # step 6 BL expected returns
        posterior_expected_returns = implied_equilibrium_returns + (tau * covariance).dot(pick_matrix.T).\
            dot(inv(pick_matrix.dot(tau * covariance).dot(pick_matrix.T) + omega).dot(investor_views - pick_matrix.dot(implied_equilibrium_returns)))
        posterior_expected_returns = posterior_expected_returns.reshape(1, -1)

        # step 7 BL covariance
        posterior_covariance = covariance + (tau * covariance) - (tau * covariance).dot(pick_matrix.T).\
                    dot(inv(pick_matrix.dot(tau * covariance).dot(pick_matrix.T) + omega)).dot(pick_matrix).dot(tau * covariance)

        if opt_method == 'max_sharpe':
            opt_func = self._max_sharpe
        elif opt_method == 'max_ret':
            opt_func = self._max_ret
        elif opt_method == 'min_std':
            opt_func = self._min_vol
        opts = sco.minimize(fun=opt_func, args=(returns,posterior_expected_returns,posterior_covariance), x0=noa*[1./noa,], method='SLSQP', bounds=bnds, constraints=cons)
        self.weights = self._get_opt_weight(opts, asset_list)
        self.port_stats = self._get_port_stats(opts, returns)

class RiskBudgetModel(ModelCalulator):

    def __init__(self,risk_free:float=0.03, trading_day_per_year:int=242): 
        super().__init__(risk_free=risk_free, trading_day_per_year=trading_day_per_year)

    def process(self, risk_method:str, fund_nav:pd.DataFrame, targets:list=[]):
        """
        风险预算模型
        - ''risk_method'' - (str) risk measure: annual_vol, mdd, var, cvar
        - ''fund_nav'' - (pd.DataFrame) fund nav, columns is asset name
        - ''targets'' - (list) risk budget, if is None, turn into Risk Parity Model
        """
        returns = fund_nav.pct_change(1).iloc[1:]
        if targets == []:
            targets = returns.shape[1] * [1/returns.shape[1]]
        x_0 = returns.shape[1] * [1/returns.shape[1]]
        cons = ({'type': 'eq', 'fun': self._total_weight_constraint},
        {'type': 'ineq', 'fun': self._long_only_constraint})
        res= sco.minimize(fun=self._risk_budget_objective, x0=x_0, args=(risk_method,targets,returns,fund_nav,self.trading_day_per_year), method='SLSQP',constraints=cons, options={'disp': True})
        self.weights = list(res.x)
        port_asset_risk = self._calculate_risk_contribution(self.weights, risk_method, returns, fund_nav, self.trading_day_per_year)
        self.port_asset_risk = list(np.array(port_asset_risk).T[0])

def test_mv():
    # 均值方差模型
    from ..data.api.basic import BasicDataApi
    fund_list = ['000001!0','000006!0','000011!0']
    fund_nav_ori = BasicDataApi().get_fund_nav(fund_list=fund_list)
    fund_nav = fund_nav_ori.pivot_table(index='datetime',columns='fund_id',values='adjusted_net_value').dropna()
    returns = fund_nav.pct_change(1).iloc[1:]
    # 夏普最大 限制资产权重测试
    opt_method = 'max_sharpe'
    asset_weight_cons = [['000006!0','<=',0.6]]
    port_stats_cons = []
    self = MeanVarianceModel()
    self.process(returns, opt_method, asset_weight_cons,port_stats_cons)
    w = self.get_opt_weight()
    p_stats = self.get_ports_stats()
    print(w)
    print(p_stats)

    # 收益最大 限制波动率测试
    opt_method = 'max_ret'
    asset_weight_cons = []
    port_stats_cons = [['std', '<=', 0.2]]
    self = MeanVarianceModel()
    self.process(returns,opt_method,asset_weight_cons,port_stats_cons)
    w = self.get_opt_weight()
    p_stats = self.get_ports_stats()
    print(w)
    print(p_stats)

def test_bl():
    # black litterman 模型
    from ..data.api.basic import BasicDataApi
    fund_list = ['000001!0','000006!0','000011!0']
    fund_nav_ori = BasicDataApi().get_fund_nav(fund_list=fund_list)
    fund_nav = fund_nav_ori.pivot_table(index='datetime',columns='fund_id',values='adjusted_net_value').dropna()
    returns = fund_nav.pct_change(1).iloc[1:]
    # 测试用用户设定的信心水平
    market_weights = [36, 8, 56]
    investor_view = [[['000006!0'],['000011!0'],0.03,0.5]]
    tau = 0.0019
    opt_method = 'max_sharpe'
    risk_aversion = 5
    omega_method='user_confidences'#'prior_variance'
    asset_weight_cons = []
    port_stats_cons = []
    self = BlackLittermanModel()
    self.process(returns,market_weights,investor_view,tau,opt_method,risk_aversion,omega_method,asset_weight_cons,port_stats_cons)
    w = self.get_opt_weight()
    p_stats = self.get_ports_stats()
    print(w)
    print(p_stats)

    # 测试不用用户设定的信心水平
    market_weights = [36, 8, 56]
    investor_view = [[['000006!0'],['000011!0'],0.03,0.5]]
    tau = 0.0019
    opt_method = 'max_sharpe'
    risk_aversion = 5
    omega_method='user_confidences'#'prior_variance'
    asset_weight_cons = []
    port_stats_cons = []
    self = BlackLittermanModel()
    self.process(returns,market_weights,investor_view,tau,opt_method,risk_aversion,omega_method,asset_weight_cons,port_stats_cons)
    w = self.get_opt_weight()
    p_stats = self.get_ports_stats()
    print(w)
    print(p_stats)

def test_rp():
    # 风险平价模型
    from ..data.api.basic import BasicDataApi
    fund_list = ['000001!0','000006!0','000011!0']
    fund_nav_ori = BasicDataApi().get_fund_nav(fund_list=fund_list)
    fund_nav = fund_nav_ori.pivot_table(index='datetime',columns='fund_id',values='adjusted_net_value').dropna()
    risk_method = 'annual_vol'
    self = RiskBudgetModel()
    self.process(risk_method, fund_nav)
    w = self.get_opt_weight()
    asset_risk_contribution = self.get_asset_risk()
    print(w)
    print(asset_risk_contribution)

def test_rb():
    # 风险预算模型
    from ..data.api.basic import BasicDataApi
    fund_list = ['000001!0','000006!0','000011!0']
    fund_nav_ori = BasicDataApi().get_fund_nav(fund_list=fund_list)
    fund_nav = fund_nav_ori.pivot_table(index='datetime',columns='fund_id',values='adjusted_net_value').dropna()
    risk_method = 'annual_vol'
    targets = [0.5,0.25,0.25]
    self = RiskBudgetModel()
    self.process(risk_method, fund_nav, targets)
    w = self.get_opt_weight()
    asset_risk_contribution = self.get_asset_risk()
    print(w)
    print(asset_risk_contribution)