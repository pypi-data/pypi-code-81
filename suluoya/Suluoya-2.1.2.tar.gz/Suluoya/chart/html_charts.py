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
        # 保存
        self.ToolBoxFeatureSaveAsImageOpts = self.opts.ToolBoxFeatureSaveAsImageOpts(type_="png",
                                                                                     name='Suluoya',
                                                                                     # 保存的图片背景色，默认使用 backgroundColor，如果backgroundColor不存在的话会取白色。
                                                                                     background_color="auto",
                                                                                     # 如果图表使用了 echarts.connect 对多个图表进行联动，则在导出图片时会导出这些联动的图表。该配置项决定了图表与图表之间间隙处的填充色。
                                                                                     connected_background_color="#fff",
                                                                                     # 保存为图片时忽略的组件列表，默认忽略工具栏。
                                                                                     exclude_components=None,
                                                                                     # 是否显示该工具。
                                                                                     is_show=True,
                                                                                     # 提示语
                                                                                     title="保存图片")
        # 还原
        self.ToolBoxFeatureRestoreOpts = self.opts.ToolBoxFeatureRestoreOpts(
            is_show=True,
            title='还原')
        # 数据视图
        self.ToolBoxFeatureDataViewOpts = self.opts.ToolBoxFeatureDataViewOpts(is_show=True,
                                                                               title="数据",
                                                                               is_read_only=False,
                                                                               background_color="#fff",
                                                                               text_area_color="#fff",
                                                                               text_area_border_color="#333",
                                                                               text_color="#000",
                                                                               button_color="#c23531",
                                                                               button_text_color="#fff",)
        # 缩放
        self.ToolBoxFeatureDataZoomOpts = self.opts.ToolBoxFeatureDataZoomOpts(
            is_show=False,
            zoom_title='区域缩放',
            back_title='区域缩放还原',
        )
        # 动态
        self.ToolBoxFeatureMagicTypeOpts = self.opts.ToolBoxFeatureMagicTypeOpts(
            is_show=True,
            type_=['line', 'bar', 'stack', 'tiled'])
        # 选框组件
        self.ToolBoxFeatureBrushOpts = self.opts.ToolBoxFeatureBrushOpts(
            type_='rect')
        # 工具配置
        self.ToolBoxFeatureOpts = self.opts.ToolBoxFeatureOpts(
            # 保存为图片
            save_as_image=self.ToolBoxFeatureSaveAsImageOpts.opts,
            # 配置项还原
            restore=self.ToolBoxFeatureRestoreOpts.opts,
            # 数据视图工具，可以展现当前图表所用的数据，编辑后可以动态更新
            data_view=self.ToolBoxFeatureDataViewOpts.opts,
            # 数据区域缩放。（目前只支持直角坐标系的缩放）
            data_zoom=self.ToolBoxFeatureDataZoomOpts.opts,
            # 动态类型切换。
            magic_type=self.ToolBoxFeatureMagicTypeOpts.opts,
            # 选框组件的控制按钮。
            brush=self.ToolBoxFeatureBrushOpts.opts,)
        self.toolbox_opts = self.opts.ToolboxOpts(is_show=True,
                                                  # 工具栏 icon 的布局朝向。可选：'horizontal', 'vertical'
                                                  orient="horizontal",
                                                  feature=self.ToolBoxFeatureOpts.opts,
                                                  )

        #区域缩放
        self.DataZoomOpts = self.opts.DataZoomOpts(
            is_show=True,
            type_="slider",
            is_realtime=True,
            orient='horizontal',
            is_zoom_lock=False,
            range_start=0,
            range_end=100
        )
        

    # 环图
    def pie(self, weights={'A': 1, 'B': 2, 'C': 3},label=True):
        from pyecharts.charts import Pie
        chart = Pie(init_opts=self.init_opts)
        chart.set_global_opts(toolbox_opts=self.toolbox_opts)
        chart.add(series_name='',
              data_pair=[list(z) for z in zip(
                  list(weights.keys()), list(weights.values()))],
              radius=['40%', '75%'],
              label_opts=self.opts.LabelOpts(is_show=label)
              )
        return chart

    # 条图
    def bar(self, x=["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], 
            y={"商家A": [5, 20, 36, 10, 75, 90], "商家B": [6, 18, 34, 12, 55, 96]},
            reverse=False,  # 坐标轴翻转
            pictorial=False,  # 象形柱状图
            label=True):
        if pictorial == True:
            from pyecharts.charts import PictorialBar
            chart = PictorialBar(init_opts=self.init_opts)
            chart.set_global_opts(toolbox_opts=self.toolbox_opts,datazoom_opts=self.DataZoomOpts,)
            chart.add_xaxis(x)
            for i, j in y.items():
                chart.add_yaxis(i, j,
                            symbol_repeat="fixed",
                            symbol_offset=[0, 0], is_symbol_clip=True, symbol_size=18,
                            symbol=self.SymbolType.ROUND_RECT,label_opts=self.opts.LabelOpts(is_show=label))
                break
        else:
            from pyecharts.charts import Bar
            chart = Bar(init_opts=self.init_opts)
            chart.set_global_opts(toolbox_opts=self.toolbox_opts,datazoom_opts=self.DataZoomOpts,)
            chart.add_xaxis(x)
            for i, j in y.items():
                chart.add_yaxis(i, j, label_opts=self.opts.LabelOpts(is_show=label))
        if reverse == True:
            chart.reversal_axis()
        return chart

    # 散点图
    def scatter(self, x=["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], 
                y={"商家A": [5, 20, 36, 10, 75, 90], "商家B": [6, 18, 34, 12, 55, 96]}, 
                data=None,label=False):
        from pyecharts.charts import Scatter
        chart = Scatter(init_opts=self.init_opts)
        chart.set_global_opts(toolbox_opts=self.toolbox_opts,datazoom_opts=self.DataZoomOpts,)
        if data != None:
            x = [i[0] for i in data]
            y = [i[1] for i in data]
            chart.add_xaxis(x)
            chart.add_yaxis('',y, label_opts=self.opts.LabelOpts(is_show=label))
        else:
            chart.add_xaxis(x)
            for i, j in y.items():
                chart.add_yaxis(i, j, label_opts=self.opts.LabelOpts(is_show=label))
        return chart

    # 涟漪散点图
    def effect_scatter(self, x=["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], 
                       y={"商家A": [5, 20, 36, 10, 75, 90], "商家B": [6, 18, 34, 12, 55, 96]},
                       label=False):
        from pyecharts.charts import EffectScatter
        chart = EffectScatter(init_opts=self.init_opts)
        chart.set_global_opts(toolbox_opts=self.toolbox_opts,datazoom_opts=self.DataZoomOpts,)
        chart.add_xaxis(x)
        for i, j in y.items():
            chart.add_yaxis(i, j,label_opts=self.opts.LabelOpts(is_show=label))
        return chart

    # 线图
    def line(self, x=["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], 
             y={"商家A": [5, 20, 36, 10, 75, 90], "商家B": [6, 18, 34, 12, 55, 96]},
             smooth=False,  # 曲线是否平滑
             step=False,  # 阶梯形状
             label=True):
        from pyecharts.charts import Line
        chart = Line(init_opts=self.init_opts,)
        chart.set_global_opts(toolbox_opts=self.toolbox_opts,datazoom_opts=self.DataZoomOpts,)
        chart.add_xaxis(x)
        for i, j in y.items():
            chart.add_yaxis(series_name=i,
                        y_axis=j,
                        is_smooth=smooth,
                        is_step=step,
                        label_opts=self.opts.LabelOpts(is_show=label),
                        
                        )
        return chart

    def barline(self, x=["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], 
                y_bar={"商家A": [5, 20, 36, 10, 75, 90], "商家B": [6, 18, 34, 12, 55, 96]}, 
                y_line={"商家C": [51, 2, 6, 40, 72, 40], "商家D": [16, 38, 14, 122, 45, 56]}):
        chart = self.bar(x=x, y=y_bar)
        chart = self.line(x=x, y=y_line)
        chart.overlap(chart)
        return chart

    def river(self, x=["DQ", "TY"], y=[["2015/11/08", 10, "DQ"], ["2015/11/09", 15, "DQ"], ["2015/11/10", 35, "DQ"], ["2015/11/08", 35, "TY"], ["2015/11/09", 36, "TY"], ["2015/11/10", 37, "TY"], ],):
        from pyecharts.charts import ThemeRiver
        chart = ThemeRiver(init_opts=self.init_opts)
        chart.set_global_opts(toolbox_opts=self.toolbox_opts,datazoom_opts=self.DataZoomOpts,)
        chart.add(series_name=x, data=y, singleaxis_opts=self.opts.SingleAxisOpts(
            pos_top="50", pos_bottom="50", type_="time",))
        chart.set_global_opts(tooltip_opts=self.opts.TooltipOpts(
            trigger="axis", axis_pointer_type="line"))
        return chart

    def save(self, chart, path='render'):
        chart.render(path+'.html')


if __name__ == '__main__':
    hc = html_charts()
    bl = hc.line()
    hc.save(bl)
