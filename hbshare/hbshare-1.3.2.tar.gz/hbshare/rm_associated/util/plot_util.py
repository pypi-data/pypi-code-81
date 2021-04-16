import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Bar, Line, HeatMap
from pyecharts.globals import ThemeType


def draw_summary_bar(df):
    colors = ['#5793f3', '#d14a61']

    x_data = df.index.tolist()
    factor_exposure = df['factor_exposure'].tolist()
    return_attr = df['return_attr'].tolist()

    exposure_limit = int(np.max(np.abs(factor_exposure)) + 1)
    return_limit = int(np.max(np.abs(return_attr)) / 5 + 1) * 5

    bar = (
        Bar(init_opts=opts.InitOpts(width='1200px', height='600px', theme=ThemeType.WESTEROS))
        .add_xaxis(
            xaxis_data=x_data)
        .add_yaxis(
            series_name='因子暴露',
            y_axis=factor_exposure,
            label_opts=opts.LabelOpts(is_show=False),
            color=colors[0])
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="收益贡献",
                type_="value",
                min_=-return_limit,
                max_=return_limit,
                split_number=6,
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                axistick_opts=opts.AxisTickOpts(is_show=True)))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="风格暴露及收益贡献"),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts={"interval": "0"},
                axistick_opts=opts.AxisTickOpts(is_show=True),
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow")),
            yaxis_opts=opts.AxisOpts(
                name="因子暴露",
                type_="value",
                min_=-exposure_limit,
                max_=exposure_limit,
                split_number=6,
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ))
    )

    bar2 = (
        Bar()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="收益贡献",
            yaxis_index=1,
            y_axis=return_attr,
            label_opts=opts.LabelOpts(is_show=False))
    )

    return bar.overlap(bar2)


def draw_summary_bar_style(df):
    colors = ['#5793f3', '#d14a61']

    x_data = df.index.tolist()
    factor_exposure = df['factor_exposure'].tolist()
    return_attr = df['return_attr'].tolist()

    exposure_limit = int(np.max(np.abs(factor_exposure)) + 1)
    return_limit = int(np.max(np.abs(return_attr)) / 5 + 1) * 5

    bar = (
        Bar(init_opts=opts.InitOpts(width='1200px', height='600px', theme=ThemeType.WESTEROS))
        .add_xaxis(
            xaxis_data=x_data)
        .add_yaxis(
            series_name='因子暴露',
            y_axis=factor_exposure,
            label_opts=opts.LabelOpts(is_show=False),
            color=colors[0])
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="收益贡献",
                type_="value",
                min_=-return_limit,
                max_=return_limit,
                split_number=6,
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                axistick_opts=opts.AxisTickOpts(is_show=True)))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="风格暴露及收益贡献"),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts={"interval": "0"},
                axistick_opts=opts.AxisTickOpts(is_show=True),
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow")),
            yaxis_opts=opts.AxisOpts(
                name="因子暴露",
                type_="value",
                min_=-exposure_limit,
                max_=exposure_limit,
                split_number=6,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ))
    )

    bar2 = (
        Bar()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="收益贡献",
            yaxis_index=1,
            y_axis=return_attr,
            label_opts=opts.LabelOpts(is_show=False))
    )

    return bar.overlap(bar2)


def draw_area_line(df, title):
    x_data = df.index.tolist()

    line = (
        Line(init_opts=opts.InitOpts(width='1200px', height='600px', theme=ThemeType.WESTEROS))
        .add_xaxis(
            xaxis_data=x_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom", legend_icon='rect'),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                max_=100,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,
                                     axistick_opts=opts.AxisTickOpts(is_show=True),),
        )
    )

    for style_factor in df.columns.tolist():
        line.add_yaxis(
            series_name=style_factor,
            stack="总量",
            y_axis=df[style_factor].tolist(),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )

    return line


def draw_area_bar(df, title):
    x_data = df.index.tolist()

    bar = (
        Bar(init_opts=opts.InitOpts(width='1200px', height='600px', theme=ThemeType.WESTEROS))
        .add_xaxis(
            xaxis_data=x_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", axistick_opts=opts.AxisTickOpts(is_show=True)),
        )
    )

    for style_factor in df.columns.tolist():
        bar.add_yaxis(
            series_name=style_factor,
            stack="stack1",
            y_axis=df[style_factor].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            bar_width="60%"
        )

    return bar


def draw_heatmap(df, title):
    value = [[i, j, df.values[i, j]] for i in range(df.shape[0]) for j in range(df.shape[1])]

    picture = (
        HeatMap(init_opts=opts.InitOpts(width='1200px', height='600px'))
        .add_xaxis(df.index.tolist())
        .add_yaxis(
            "风格暴露",
            df.columns.tolist(),
            value=value,
            label_opts=opts.LabelOpts(is_show=True, position='inside')
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(min_=-4, max_=4, orient="horizontal", pos_left="center")
        )
    )

    return picture
