

class svg_charts(object):

    from pygal.style import BlueStyle, CleanStyle, DarkColorizedStyle, DarkGreenBlueStyle, DarkGreenStyle, DarkSolarizedStyle, DarkStyle, DarkenStyle, DefaultStyle, DesaturateStyle, LightColorizedStyle, LightGreenStyle, LightSolarizedStyle, LightStyle, LightenStyle, NeonStyle, ParametricStyleBase, RedBlueStyle, RotateStyle, SaturateStyle, SolidColorStyle, Style, TurquoiseStyle
    def __init__(self,
                 width=1440,
                 height=720,
                 spacing=30,
                 margin=50,
                 style=BlueStyle,
                 ):
        self.width = width
        self.height = height
        self.spacing = spacing
        self.margin = margin
        self.style = style

    def bar(self, x=[1, 2, 3, 4, 5, 6],
            data={'A': [0, 1, 1, 2, 3, 5], 'B': [3, 4, 5, 7, 9, 1]}):
        from pygal import Bar
        chart = Bar(
            width=self.width,
            height=self.height,
            spacing=self.spacing,
            margin=self.margin,
            style=self.style,
            title='Suluoya-svg',
            x_title="I'm xlabel",
            y_title="I'm ylabel",
            show_x_labels=True,
            show_x_guides=False,
            x_label_rotation=0,  # 倾斜x轴标签
            show_y_labels=True,
            show_y_guides=False,
            y_label_rotation=0,  # 倾斜y轴标签
            print_values=True,
            print_values_position='top',  # bottom,
            print_zeroes=False,
            show_legend=True,
            legend_at_bottom=False,
            include_x_axis=False,  # 包含x=0
            inverse_y_axis=False,
            value_formatter=lambda x: "%.2f" % x,
            human_readable=True,
            rounded_bars=False,
        )
        chart.x_labels = x
        for i, j in data.items():
            chart.add(i, j)
        return chart

    def horizontal_bar(self, x=[1, 2, 3, 4, 5, 6],
                       data={'A': [0, 1, 1, 2, 3, 5], 'B': [3, 4, 5, 7, 9, 1]}):
        from pygal import HorizontalBar
        chart = HorizontalBar(
            width=self.width,
            height=self.height,
            spacing=self.spacing,
            margin=self.margin,
            style=self.style,
            title='Suluoya-svg',
            x_title="I'm xlabel",
            y_title="I'm ylabel",
            show_x_labels=True,
            show_x_guides=False,
            x_label_rotation=0,  # 倾斜x轴标签
            show_y_labels=True,
            show_y_guides=False,
            y_label_rotation=0,  # 倾斜y轴标签
            print_values=True,
            print_values_position='top',  # bottom,
            print_zeroes=False,
            show_legend=True,
            legend_at_bottom=False,
            include_x_axis=False,  # 包含x=0
            inverse_y_axis=False,
            value_formatter=lambda x: "%.2f" % x,
            human_readable=True,
            rounded_bars=False,
        )
        chart.x_labels = x
        for i, j in data.items():
            chart.add(i, j)
        return chart

    def stacked_bar(self, x=[1, 2, 3, 4, 5, 6],
                    data={'A': [0, 1, 1, 2, 3, 5], 'B': [3, 4, 5, 7, 9, 1]}):
        from pygal import StackedBar
        chart = StackedBar(
            width=self.width,
            height=self.height,
            spacing=self.spacing,
            margin=self.margin,
            style=self.style,
            title='Suluoya-svg',
            x_title="I'm xlabel",
            y_title="I'm ylabel",
            show_x_labels=True,
            show_x_guides=False,
            x_label_rotation=0,  # 倾斜x轴标签
            show_y_labels=True,
            show_y_guides=False,
            y_label_rotation=0,  # 倾斜y轴标签
            print_values=True,
            print_values_position='top',  # bottom,
            print_zeroes=False,
            show_legend=True,
            legend_at_bottom=False,
            include_x_axis=False,  # 包含x=0
            inverse_y_axis=False,
            value_formatter=lambda x: "%.2f" % x,
            human_readable=True,
            rounded_bars=False,
        )
        chart.x_labels = x
        for i, j in data.items():
            chart.add(i, j)
        return chart

    def line(self, x=[1, 2, 3, 4, 5, 6],
            data={'A': [0, 1, 1, 2, 3, 5], 'B': [3, 4, 5, 7, 9, 1]},
            title='Suluoya-svg',
            x_title="I'm xlabel",
            y_title="I'm ylabel",
            show_x_labels=True,
            show_x_guide=False,
            x_label_rotation=0,  # 倾斜x轴标签
            show_y_labels=True,
            show_y_guides=False,
            y_label_rotation=0,  # 倾斜y轴标签
            print_values=True,
            print_zeroes=False,
            show_legend=True,
            legend_at_bottom=False,
            include_x_axis=False,  # 包含x=0
            inverse_y_axis=False,
            interpolation='cubic',  # 折线图平滑处理
            value_formatter=lambda x: "%.2f" % x,
            human_readable=True,
            fill=False):
        from pygal import Line
        chart = Line(
            width=self.width,
            height=self.height,
            spacing=self.spacing,
            margin=self.margin,
            style=self.style,
            title=title,
            x_title=x_title,
            y_title=y_title,
            show_x_labels=show_x_labels,
            show_x_guide=show_x_guide,
            x_label_rotation=x_label_rotation,  # 倾斜x轴标签
            show_y_labels=show_y_labels,
            show_y_guides=show_y_guides,
            y_label_rotation=y_label_rotation,  # 倾斜y轴标签
            print_values=print_values,
            print_zeroes=print_zeroes,
            show_legend=show_legend,
            legend_at_bottom=legend_at_bottom,
            include_x_axis=include_x_axis,  # 包含x=0
            inverse_y_axis=inverse_y_axis,
            interpolation=interpolation,  # 折线图平滑处理
            value_formatter=value_formatter,
            human_readable=human_readable,
            fill=fill,  # 面积图
        )
        chart.x_labels = x
        for i, j in data.items():
            chart.add(i, j)
        return chart

    def stacked_line(self, x=[1, 2, 3, 4, 5, 6],
                     data={'A': [0, 1, 1, 2, 3, 5], 'B': [3, 4, 5, 7, 9, 1]}):
        from pygal import StackedLine
        chart = StackedLine(
            width=self.width,
            height=self.height,
            spacing=self.spacing,
            margin=self.margin,
            style=self.style,
            title='Suluoya-svg',
            x_title="I'm xlabel",
            y_title="I'm ylabel",
            show_x_labels=True,
            show_x_guide=False,
            x_label_rotation=0,  # 倾斜x轴标签
            show_y_labels=True,
            show_y_guides=False,
            y_label_rotation=0,  # 倾斜y轴标签
            print_values=True,
            print_zeroes=False,
            show_legend=True,
            legend_at_bottom=False,
            value_formatter=lambda x: "%.2f" % x,
            human_readable=True,
            fill=True,
        )
        chart.x_labels = x
        for i, j in data.items():
            chart.add(i, j)
        return chart

    def pie(self, 
            weights={'A': 1, 'B': 2, 'C': 3},
            title='Suluoya-svg',
            print_values=True,
            show_legend=True,
            legend_at_bottom=False,
            value_formatter=lambda x: "%.2f" % x,
            human_readable=True,
            inner_radius=0.6,  # 环图
            half_pie=False):
        from pygal import Pie
        chart = Pie(
            width=self.width,
            height=self.height,
            spacing=self.spacing,
            margin=self.margin,
            style=self.style,
            title=title,
            print_values=print_values,
            show_legend=show_legend,
            legend_at_bottom=legend_at_bottom,
            value_formatter=value_formatter,
            human_readable=human_readable,
            inner_radius=inner_radius,  # 环图
            half_pie=half_pie,)
        for i, j in weights.items():
            chart.add(i, j)
        return chart

    def scatter(self, 
                data={'A': [(1, 2), (3, 4)], 'B': [(12, 24), (33, 44)], 'C': [(11, 2), (33, 44)]},
                title='Suluoya-scatter',
                x_title="I'm xlabel",
                y_title="I'm ylabel",
                show_x_labels=True,
                show_x_guide=False,
                show_y_labels=True,
                show_y_guides=False,
                print_values=False,
                print_zeroes=False,
                show_legend=True,
                legend_at_bottom=False,
                interpolation='cubic',  # 折线图平滑处理
                human_readable=True,
                stroke=False
                ):
        from pygal import XY
        chart = XY(
            width=self.width,
            height=self.height,
            spacing=self.spacing,
            margin=self.margin,
            style=self.style,
            title=title,
            x_title=x_title,
            y_title=y_title,
            show_x_labels=show_x_labels,
            show_x_guide=show_x_guide,
            show_y_labels=show_y_labels,
            show_y_guides=show_y_guides,
            print_values=print_values,
            print_zeroes=print_zeroes,
            show_legend=show_legend,
            legend_at_bottom=legend_at_bottom,
            interpolation=interpolation,  # 折线图平滑处理
            human_readable=human_readable,
            stroke=stroke,  # 不连线
        )
        for i, j in data.items():
            chart.add(i, j)
        return chart

    def save(self, chart, path='render'):
        chart.render_to_file(path+'.svg')


if __name__ == '__main__':
    s = svg_charts()
    b = s.scatter()
    s.save(chart=b)




