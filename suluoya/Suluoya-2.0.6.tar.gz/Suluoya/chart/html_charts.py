class html_charts(object):
    def __init__(self,
                 width='1440px', height='720px',
                 page_title="Suluoya-charts",
                 theme='LIGHT'):
        '''theme:
        LIGHT,DARK,CHALK,ESSOS,INFOGRAPHIC,MACARONS,PURPLE_PASSION,ROMA,ROMANTIC,SHINE,VINTAGE,WALDEN,WESTEROS,WONDERLAND
        '''
        import pyecharts.options as opts
        from pyecharts.globals import ThemeType
        from pyecharts.globals import SymbolType
        self.opts = opts
        self.ThemeType = ThemeType
        self.SymbolType = SymbolType
        Theme = {'LIGHT': self.ThemeType.LIGHT,
                 'DARK': self.ThemeType.DARK,
                 'CHALK': self.ThemeType.CHALK,
                 'ESSOS': self.ThemeType.ESSOS,
                 'INFOGRAPHIC': self.ThemeType.INFOGRAPHIC,
                 'MACARONS': self.ThemeType.MACARONS,
                 'PURPLE_PASSION': self.ThemeType.PURPLE_PASSION,
                 'ROMA': self.ThemeType.ROMA,
                 'ROMANTIC': self.ThemeType.ROMANTIC,
                 'SHINE': self.ThemeType.SHINE,
                 'VINTAGE': self.ThemeType.VINTAGE,
                 'WALDEN': self.ThemeType.WALDEN,
                 'WESTEROS': self.ThemeType.WESTEROS,
                 'WONDERLAND': self.ThemeType.WONDERLAND,
                 }
        self.init_opts = self.opts.InitOpts(width=width,
                                            height=height,
                                            page_title=page_title,
                                            theme=Theme[theme])
    x = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    y = {"商家A": [5, 20, 36, 10, 75, 90], "商家B": [6, 18, 34, 12, 55, 96]}

    # 环图
    def pie(self, weights={'A': 1, 'B': 2, 'C': 3}):
        from pyecharts.charts import Pie
        p = Pie(init_opts=self.init_opts)
        p.add(series_name='',
              data_pair=[list(z) for z in zip(
                  list(weights.keys()), list(weights.values()))],
              radius=['40%', '75%'],
              )
        return p

    # 条图
    def bar(self, x=x, y=y,
            reverse=False,  # 坐标轴翻转
            pictorial=False,  # 象形柱状图
            ):
        if pictorial == True:
            from pyecharts.charts import PictorialBar
            b = PictorialBar(init_opts=self.init_opts)
            b.add_xaxis(x)
            for i, j in y.items():
                b.add_yaxis(i, j,
                            symbol_repeat="fixed",
                            symbol_offset=[0, 0], is_symbol_clip=True, symbol_size=18,
                            symbol=self.SymbolType.ROUND_RECT,)
                break
        else:
            from pyecharts.charts import Bar
            b = Bar(init_opts=self.init_opts)
            b.add_xaxis(x)
            for i, j in y.items():
                b.add_yaxis(i, j)
        if reverse == True:
            b.reversal_axis()
        return b

    # 散点图
    def scatter(self, x=x, y=y, data=None):
        from pyecharts.charts import Scatter
        s = Scatter(init_opts=self.init_opts)
        if data != None:
            x = [i[0] for i in data]
            y = [i[1] for i in data]
        s.add_xaxis(x)
        for i, j in y.items():
            s.add_yaxis(i, j, label_opts=self.opts.LabelOpts(is_show=False))
        return s

    # 涟漪散点图
    def effect_scatter(self, x=x, y=y,):
        from pyecharts.charts import EffectScatter
        es = EffectScatter(init_opts=self.init_opts)
        es.add_xaxis(x)
        for i, j in y.items():
            es.add_yaxis(i, j)
        return es

    # 线图
    def line(self, x=x, y=y,
             smooth=False,  # 曲线是否平滑
             step=False,  # 阶梯形状
             ):
        from pyecharts.charts import Line
        l = Line(init_opts=self.init_opts)
        l.add_xaxis(x)
        for i, j in y.items():
            l.add_yaxis(series_name=i,
                        y_axis=j,
                        is_smooth=smooth,
                        is_step=step,
                        )
        return l

    def barline(self, x=x, y_bar=y, y_line=y):
        bar = self.bar(x=x, y=y_bar)
        line = self.line(x=x, y=y_line)
        bar.overlap(line)
        return bar

    def river(self, x=["DQ", "TY"], y=[["2015/11/08", 10, "DQ"], ["2015/11/09", 15, "DQ"], ["2015/11/10", 35, "DQ"], ["2015/11/08", 35, "TY"], ["2015/11/09", 36, "TY"], ["2015/11/10", 37, "TY"], ]):
        from pyecharts.charts import ThemeRiver
        tr = ThemeRiver(init_opts=self.init_opts)
        tr.add(series_name=x, data=y, singleaxis_opts=self.opts.SingleAxisOpts(
            pos_top="50", pos_bottom="50", type_="time"))
        tr.set_global_opts(tooltip_opts=self.opts.TooltipOpts(
            trigger="axis", axis_pointer_type="line"))
        return tr

    def save(self, chart, path='render'):
        chart.render(path+'.html')


if __name__ == '__main__':
    hc = html_charts()
    bl = hc.scatter()
    hc.save(bl)
