class cute_charts(object):
    def __init__(self,
                 width="1440px",
                 height="720px"):
        self.width = width
        self.height = height

    def line(self, name='line',
             x=["a", "b", "c", "d", "e", "f", "g"],
             y={"series-A": [57, 134, 137, 129, 145, 60, 49],
                "series-B": [114, 55, 27, 101, 125, 27, 105]},
             x_label="I'm xlabel",
             y_label="I'm ylabel",):
        from cutecharts.charts import Line
        chart = Line(title=name,
                     width=self.width,
                     height=self.height)
        chart.set_options(
            labels=x,
            x_label=x_label,
            y_label=y_label,
            legend_pos="upRight"
        )
        for i, j in y.items():
            chart.add_series(i, j)
        return chart

    def bar(self, name='bar',
            x=["a", "b", "c", "d", "e", "f", "g"],
            y={"series-A": [57, 134, 137, 129, 145, 60, 49],
               "series-B": [114, 55, 27, 101, 125, 27, 105]},
            x_label="I'm xlabel",
            y_label="I'm ylabel",):
        from cutecharts.charts import Bar
        chart = Bar(title=name,
                    width=self.width,
                    height=self.height)
        chart.set_options(
            labels=x,
            x_label=x_label,
            y_label=y_label,
        )
        for i, j in y.items():
            chart.add_series(i, j)
        return chart

    def pie(self, name='pie',
            weights={'A': 1, 'B': 2, 'C': 3}):
        from cutecharts.charts import Pie
        chart = Pie(title=name,
                    width=self.width,
                    height=self.height)
        chart.set_options(labels=list(weights.keys()))
        chart.add_series(list(weights.values()))
        return chart

    def scatter(self, name='scatter',
                data={"series-A": [(79, 123), (76, 128), (84, 125), ],
                      "series-B": [(112, 20), (119, 113), (76, 126), (30, 149), ]
                      },
                x_label="I'm xlabel",
                y_label="I'm ylabel",
                dot_size=1.5,  # 点大小
                x_tick_count=3,  # X 轴刻度分割段数
                y_tick_count=3,  # Y 轴刻度分割段数
                line=False  # 是否连线
                ):
        from cutecharts.charts import Scatter
        chart = Scatter(title=name,
                        width=self.width,
                        height=self.height)
        chart.set_options(dot_size=dot_size,
                          x_tick_count=x_tick_count, y_tick_count=y_tick_count,
                          is_show_line=line,
                          x_label=x_label, y_label=y_label)
        for i, j in data.items():
            chart.add_series(i, j)
        return chart

    def save(self, chart, path='render'):
        chart.render(path+'.html')


if __name__ == '__main__':
    cc = cute_charts()
    l = cc.line()
    cc.save(l)
