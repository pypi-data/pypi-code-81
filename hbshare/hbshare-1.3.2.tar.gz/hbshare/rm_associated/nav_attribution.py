"""
净值归因模型
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from hbshare.rm_associated.util.verifier import verify_type
from hbshare.rm_associated.util.exception import InputParameterError, PreprocessError
from hbshare.rm_associated.util.logger import logger
from hbshare.rm_associated.util.data_loader import NavAttributionLoader
from hbshare.rm_associated.util.regressions import Regression
from hbshare.rm_associated.util.config import factor_map_dict
from hbshare.rm_associated.util.plot_util import draw_summary_bar, draw_summary_bar_style, \
    draw_area_line, draw_area_bar, draw_heatmap


class StyleAttributionOutputs:
    def __init__(self):
        self.attribution_df = None
        self.r_square_series = None
        self.exposure_series = None
        self.return_attr_series = None
        self.style_allo_bar = None
        self.style_allo_line = None


class StyleAttribution:
    def __init__(self, fund_id, fund_type, start_date, end_date, factor_type, benchmark_id, nav_frequency):
        """
        :param fund_id: 基金代码
        :param fund_type: 基金类型, mutual：公募; private: 私募
        :param start_date: 归因的起始时间
        :param end_date: 归因的结束时间
        :param factor_type: 因子类型：分为风格配置(style_allo)/风格(style)/板块(sector)三种
        :param benchmark_id: 基准ID
        :param nav_frequency: 基金的净值频率
        """
        self.fund_id = fund_id
        self.fund_type = fund_type
        self.start_date = start_date
        self.end_date = end_date
        self.factor_type = factor_type
        self.benchmark_id = benchmark_id
        self.nav_frequency = nav_frequency
        self._verify_input_param()
        self._load_data()
        self._init_style_attribution_data()

    def _verify_input_param(self):
        verify_type(self.fund_id, 'fund_id', str)
        verify_type(self.start_date, 'start_date', str)
        verify_type(self.end_date, 'end_date', str)
        verify_type(self.benchmark_id, 'benchmark_id', str)
        if self.fund_type not in ['mutual', 'private']:
            msg = "fund_type not in ['mutual', 'private'], check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.factor_type not in ['style_allo', 'style', 'sector']:
            msg = "factor_type not in ['style_allo', 'style', 'sector']"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.nav_frequency not in ['day', 'week']:
            msg = "nav_frequency not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)

    def _load_data(self):
        data = NavAttributionLoader(
            self.fund_id, self.fund_type, self.start_date, self.end_date, self.factor_type, self.benchmark_id).load()
        self.calendar_df = data['calendar_df']
        self.fund_nav_series = data['fund_nav_series']
        self.factor_data = data['factor_data']
        self.benchmark_series = data['benchmark_series']

    def get_trading_day_list(self, nav_frequency):
        if nav_frequency == 'day':
            trading_day_list = sorted(list(self.calendar_df[self.calendar_df['isOpen'] == 1]['calendarDate']))
        elif nav_frequency == 'week':
            trading_day_list = sorted(list(self.calendar_df[self.calendar_df['isWeekEnd'] == 1]['calendarDate']))
        elif nav_frequency == 'month':
            trading_day_list = sorted(list(self.calendar_df[self.calendar_df['isMonthEnd'] == 1]['calendarDate']))
        elif nav_frequency == 'quarter':
            trading_day_list = sorted(list(self.calendar_df[self.calendar_df['isQuarterEnd'] == 1]['calendarDate']))
        else:
            trading_day_list = []

        return trading_day_list

    def _init_style_attribution_data(self):
        quarter_end_list = self.get_trading_day_list('quarter')
        if len(quarter_end_list) < 2:
            msg = "There is no complete quarter interval during start_date and end_date, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)

        date_list = sorted(self.calendar_df['calendarDate'].unique())
        trading_day_list = self.get_trading_day_list(self.nav_frequency)

        preprocessed_data = dict()
        if not (self.fund_nav_series.empty or self.factor_data.empty or self.benchmark_series.empty):
            # portfolio
            portfolio_nav_series = self.fund_nav_series.reindex(date_list).interpolate().reindex(
                trading_day_list).dropna().sort_index()
            portfolio_nav_series = portfolio_nav_series / portfolio_nav_series.iloc[0]
            portfolio_return_series = portfolio_nav_series.pct_change().dropna()
            # factor
            factor_nav_df = self.factor_data / self.factor_data.iloc[0]
            factor_nav_df = factor_nav_df.reindex(trading_day_list).fillna(method='ffill')
            factor_return_df = factor_nav_df.pct_change().dropna().reindex(portfolio_return_series.index).fillna(0.)
            # benchmark
            benchmark_nav_series = self.benchmark_series.reindex(date_list).interpolate().reindex(
                trading_day_list).dropna().sort_index()
            benchmark_nav_series = benchmark_nav_series / benchmark_nav_series.iloc[0]
            benchmark_return_series = benchmark_nav_series.pct_change().dropna()

            assert(portfolio_return_series.shape[0] == factor_return_df.shape[0])
            assert(portfolio_return_series.shape[0] == benchmark_return_series.shape[0])

            if self.factor_type == 'style' and self.fund_type == 'private':  # 半衰加权, 需要半年度的数据
                for i in range(2, len(quarter_end_list)):
                    Q_start, Q_end = quarter_end_list[i - 2], quarter_end_list[i]
                    interval_data = dict()
                    # 数据密度判定
                    actual_point = self.fund_nav_series[
                        (self.fund_nav_series.index > Q_start) & (self.fund_nav_series.index <= Q_end)]
                    all_points = [x for x in trading_day_list if (x <= Q_end) and (x > Q_start)]
                    nav_density = actual_point.shape[0] / len(all_points)
                    if nav_density <= 0.7:
                        interval_data['portfolio_return_series'] = pd.Series()
                        interval_data['factor_return_df'] = pd.DataFrame()
                        interval_data['benchmark_return_series'] = pd.Series()
                        continue
                    else:
                        interval_data['portfolio_return_series'] = \
                            portfolio_return_series[
                                (portfolio_return_series.index > Q_start) & (portfolio_return_series.index <= Q_end)]
                        interval_data['factor_return_df'] = factor_return_df[
                            (factor_return_df.index > Q_start) & (factor_return_df.index <= Q_end)]
                        interval_data['benchmark_return_series'] = benchmark_return_series[
                            (benchmark_return_series.index > Q_start) & (benchmark_return_series.index <= Q_end)]

                    preprocessed_data[Q_end] = interval_data
            else:
                for i in range(1, len(quarter_end_list)):
                    Q_start, Q_end = quarter_end_list[i - 1], quarter_end_list[i]
                    interval_data = dict()
                    # 数据密度判定
                    actual_point = \
                        self.fund_nav_series[
                            (self.fund_nav_series.index > Q_start) & (self.fund_nav_series.index <= Q_end)]
                    all_points = [x for x in trading_day_list if (x <= Q_end) and (x > Q_start)]
                    nav_density = actual_point.shape[0] / len(all_points)
                    if nav_density <= 0.7:
                        interval_data['portfolio_return_series'] = pd.Series()
                        interval_data['factor_return_df'] = pd.DataFrame()
                        interval_data['benchmark_return_series'] = pd.Series()
                        continue
                    else:
                        interval_data['portfolio_return_series'] = \
                            portfolio_return_series[
                                (portfolio_return_series.index > Q_start) & (portfolio_return_series.index <= Q_end)]
                        interval_data['factor_return_df'] = factor_return_df[
                            (factor_return_df.index > Q_start) & (factor_return_df.index <= Q_end)]
                        interval_data['benchmark_return_series'] = benchmark_return_series[
                            (benchmark_return_series.index > Q_start) & (benchmark_return_series.index <= Q_end)]

                    preprocessed_data[Q_end] = interval_data

            self.preprocessed_data = preprocessed_data
        else:
            msg = "Data empty occurred, check your input"
            logger.error(msg)
            raise PreprocessError(message=msg)

    @staticmethod
    def _private_style_regression(x_data, y_data):
        n = x_data.shape[0]
        half_life = int(n / 2)
        weight = np.array([2 ** (-i / half_life) for i in range(n)])
        weight = (weight / weight.sum())[::-1]
        results = sm.WLS(y_data, sm.add_constant(x_data), weights=weight).fit()

        return results.params.drop('const'), results.rsquared

    @staticmethod
    def _perf_attr(date, account_return, factor_df, beta_series, bm_series):
        calc_df = factor_df[beta_series.index.tolist()]

        idx = account_return.index.intersection(calc_df.index)
        calc_df = calc_df.loc[idx]
        account_return = account_return[idx]

        factor_cum_return = calc_df.fillna(0.).add(1.0).prod().subtract(1.0)
        perf_attr = beta_series.multiply(factor_cum_return)
        perf_attr = pd.merge(beta_series.to_frame('factor_exposure'), perf_attr.to_frame('return_attr'),
                             left_index=True, right_index=True)

        dynamic_bm = calc_df.dot(beta_series)
        return_df = account_return.to_frame('portfolio').merge(
            bm_series, left_index=True, right_index=True).merge(
            dynamic_bm.to_frame('dynamic_style_bm'), left_index=True, right_index=True)

        return_attr = return_df.fillna(0.).add(1.0).prod().subtract(1.0)
        attr_df = return_attr.to_frame(date).T
        attr_df['selection'] = attr_df.eval('portfolio - dynamic_style_bm')
        attr_df['allocation'] = attr_df.eval('dynamic_style_bm - benchmark')
        attr_df = attr_df[['benchmark', 'allocation', 'selection']]

        return perf_attr, return_df, attr_df

    def _compute_style_attribution(self, date, df):
        if self.factor_type in ['style_allo', 'sector']:
            lower, upper = 0.0, 1.0
            strategy_method, attribution_effort = 'ols', 'hard'
        else:
            lower, upper = None, None
            strategy_method, attribution_effort = 'ols', 'weak'

        # add new branch
        if self.factor_type == 'style' and self.fund_type == 'private':
            factor_beta_series, r_square = self._private_style_regression(
                df['factor_return_df'], df['portfolio_return_series'])
        else:
            sr_obj = Regression(df['factor_return_df'], df['portfolio_return_series'],
                                upper=upper, lower=lower,
                                method=strategy_method, effort=attribution_effort)
            solve_dict = sr_obj.solve()
            factor_beta_series = solve_dict['solution']
            r_square = solve_dict['r_square']

        perf_attr, return_df, attr_df = self._perf_attr(
            date=date,
            account_return=df['portfolio_return_series'],
            factor_df=df['factor_return_df'],
            beta_series=factor_beta_series,
            bm_series=df['benchmark_return_series'])

        return perf_attr, r_square, attr_df, return_df

    def _style_analysis(self):
        perf_attr_list = []
        r_square_list = []
        attr_list = []
        return_series_attr = []
        for date, period_data in self.preprocessed_data.items():
            if period_data['portfolio_return_series'].empty:
                logger.warning("{}: portfolio_return_series is empty !".format(date))
                perf_attr = pd.DataFrame(
                    index=period_data['factor_return_df'].columns, columns=['factor_exposure', 'return_attr'])
                r_square = np.NaN
                attr_df = pd.DataFrame(index=[date], columns=['benchmark', 'allocation', 'selection'])
                return_df = pd.DataFrame(
                    index=period_data['factor_return_df'].index, columns=['portfolio', 'benchmark', 'dynamic_style_bm'])
            else:
                perf_attr, r_square, attr_df, return_df = self._compute_style_attribution(date, period_data)

            perf_attr['date'] = date
            perf_attr.index.name = 'style_factor'
            perf_attr.reset_index(inplace=True)
            perf_attr_list.append(perf_attr)
            r_square_list.append(r_square)
            attr_list.append(attr_df)
            return_series_attr.append(return_df)

        perf_attr_df = pd.concat(perf_attr_list)
        # 1.总体风格暴露及收益贡献
        exposure_summary = perf_attr_df.dropna().groupby('style_factor')['factor_exposure'].mean()
        return_attr_summary = perf_attr_df.dropna().groupby('style_factor')['return_attr'].sum()
        attr_summary = pd.merge(exposure_summary.reset_index(), return_attr_summary.reset_index(), on='style_factor')
        # 2.风格暴露&收益贡献的时间序列
        exposure_series = pd.pivot_table(
            perf_attr_df, index='date', columns='style_factor', values='factor_exposure').sort_index()
        return_attr_series = pd.pivot_table(
            perf_attr_df, index='date', columns='style_factor', values='return_attr').sort_index()
        # 3.R2序列
        r_square_series = pd.Series(index=self.preprocessed_data.keys(), data=r_square_list).sort_index()
        # 4.风格配置能力
        total_attr_df = pd.concat(attr_list)
        total_return_df = pd.concat(return_series_attr).fillna(0.).add(1.0).cumprod().subtract(1.)

        return attr_summary, r_square_series, exposure_series, return_attr_series, total_attr_df, total_return_df

    def get_all(self, isPlot=False):
        output = StyleAttributionOutputs()

        attr_summary, r_square_series, exposure_series, return_attr_series, total_attr_df, total_return_df = \
            self._style_analysis()

        output.attribution_df = attr_summary
        output.r_square_series = r_square_series
        output.exposure_series = exposure_series
        output.return_attr_series = return_attr_series
        output.style_allo_bar = total_attr_df
        output.style_allo_line = total_return_df

        if isPlot:
            if self.factor_type == 'style_allo':
                factor_order = ['大盘价值', '大盘成长', '中盘价值', '中盘成长', '小盘价值', '小盘成长', '中证全债']
                attribution_df = output.attribution_df.set_index('style_factor').reindex(factor_order)
                attribution_df = (attribution_df * 100).round(2)
                summary_bar = draw_summary_bar(attribution_df)
                summary_bar.render('D:\\kevin\\净值归因示例\\style_allo\\summary_bar.html')

                exposure_series = (output.exposure_series[factor_order] * 100).round(2)
                exposure_area_line = draw_area_line(exposure_series, title="风格暴露时序分析")
                exposure_area_line.render('D:\\kevin\\净值归因示例\\style_allo\\exposure_area_line.html')

                return_attr_series = (output.return_attr_series[factor_order] * 100).round(2)
                return_attr_stack_bar = draw_area_bar(return_attr_series, title="风格收益贡献时序分析")
                return_attr_stack_bar.render('D:\\kevin\\净值归因示例\\style_allo\\return_attr_stack_bar.html')
            elif self.factor_type == 'sector':
                factor_order = ['大金融', '消费', 'TMT', '周期', '制造', '中证全债']
                attribution_df = output.attribution_df.set_index('style_factor').reindex(factor_order)
                attribution_df = (attribution_df * 100).round(2)
                summary_bar = draw_summary_bar(attribution_df)
                summary_bar.render('D:\\kevin\\净值归因示例\\sector\\summary_bar.html')

                exposure_series = (output.exposure_series[factor_order] * 100).round(2)
                exposure_area_line = draw_area_line(exposure_series, title="风格暴露时序分析")
                exposure_area_line.render('D:\\kevin\\净值归因示例\\sector\\exposure_area_line.html')

                return_attr_series = (output.return_attr_series[factor_order] * 100).round(2)
                return_attr_stack_bar = draw_area_bar(return_attr_series, title="风格收益贡献时序分析")
                return_attr_stack_bar.render('D:\\kevin\\净值归因示例\\sector\\return_attr_stack_bar.html')
            else:
                factor_order = list(factor_map_dict.keys())
                attribution_df = output.attribution_df.set_index('style_factor').reindex(factor_order)
                attribution_df['factor_exposure'] = attribution_df['factor_exposure'].round(2)
                attribution_df['return_attr'] = (attribution_df['return_attr'] * 100).round(2)
                attribution_df.index = attribution_df.index.map(factor_map_dict)
                summary_bar = draw_summary_bar_style(attribution_df)
                summary_bar.render('D:\\kevin\\净值归因示例\\style\\summary_bar.html')

                exposure_series = output.exposure_series[factor_order].round(3)
                exposure_series.columns = [factor_map_dict[x] for x in exposure_series.columns]
                exposure_heatmap = draw_heatmap(exposure_series, title="因子暴露时序分析")
                exposure_heatmap.render('D:\\kevin\\净值归因示例\\style\\exposure_heatmap.html')

        return output


if __name__ == '__main__':
    # a = ['000311', '110011', '161005', '166002', '162605']

    # 公募样例：110011
    # res = StyleAttribution(fund_id='110011', fund_type='mutual', start_date='20181120', end_date='20210120',
    #                        factor_type='style_allo', benchmark_id='000300', nav_frequency='day').get_all(isPlot=True)

    # 私募样例
    res = StyleAttribution(fund_id='110011', fund_type='mutual', start_date='20190220', end_date='20210120',
                           factor_type='sector', benchmark_id='000300', nav_frequency='day').get_all(isPlot=True)
