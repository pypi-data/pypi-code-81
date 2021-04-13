import pygal
from pygal.style import DefaultStyle, LightColorizedStyle, DarkStyle
from xyw_utils.data import *
from xyw_utils.math import sind, cosd


def driving_resistance(gvw, vehicle_type='coach'):
    """
    根据车辆总质量和车型，按照GB/T 18386-2017附录A中表格估算车辆行驶阻力系数
    :param gvw: 车辆最大总质量(kg)
    :param vehicle_type: 车辆类型，公路客车或城市客车，coach or bus
    :return: F = A + B * V + C * V^2,F(N),V(km/h)
    """
    m = np.array([3500, 4500, 5500, 7000, 8500, 10500, 12500, 14500, 16500, 18000, 22000, 25000])
    a1 = np.array([450.9, 481.0, 511.0, 556.1, 601.1, 661.2, 721.3, 781.4, 841.5, 886.5, 1006.7, 1096.8])
    b1 = np.array([2.29, 2.66, 3.02, 3.57, 4.12, 4.85, 5.58, 6.32, 7.05, 7.60, 9.06, 10.16])
    c1 = np.array([0.115, 0.119, 0.123, 0.129, 0.134, 0.142, 0.150, 0.158, 0.165, 0.171, 0.187, 0.198])
    a2 = np.array([432.9, 473.2, 513.6, 574.1, 634.6, 715.2, 795.9, 876.6, 957.3, 1017.8, 1179.1, 1300.1])
    b2 = np.array([2.67, 2.79, 2.91, 3.10, 3.28, 3.53, 3.78, 4.02, 4.27, 4.46, 4.95, 5.32])
    c2 = np.array([0.113, 0.120, 0.127, 0.138, 0.148, 0.162, 0.176, 0.190, 0.204, 0.214, 0.242, 0.263])

    if vehicle_type == 'coach':  # 公路车
        f = interpolate.interp1d(m, a1, kind='linear')
        a = f(gvw)
        f = interpolate.interp1d(m, b1, kind='linear')
        b = f(gvw)
        f = interpolate.interp1d(m, c1, kind='linear')
        c = f(gvw)
    elif vehicle_type == 'bus':  # 城市客车，即公交车
        f = interpolate.interp1d(m, a2, kind='linear')
        a = f(gvw)
        f = interpolate.interp1d(m, b2, kind='linear')
        b = f(gvw)
        f = interpolate.interp1d(m, c2, kind='linear')
        c = f(gvw)
    else:
        raise ValueError('not support such vehicle type,coach and bus only')

    p = [c, b, a]
    p = np.poly1d(p)
    return p


@validate_df
def steady_static_circular_test(df, l, t, a_y, v_x, v_yaw, roll):
    """
    稳态回转试验数据处理，主要参考：
    《GB/T 6323-2014 汽车操纵稳定性试验方法》10.4
    :param df: 包含所需数据的df（已筛选）
    :param l: 轴距，单位m
    :param t: 时间列名称，单位s
    :param a_y: 侧向加速度列名称，单位m/s^2
    :param v_x: 前进速度列名称，单位km/h
    :param v_yaw: 横摆角速度列名称，单位°/s
    :param roll: 车身侧倾角列名称，单位°
    :return:
    """
    # 提取并重命名相关数据列
    df = df[[t, a_y, v_x, v_yaw, roll]]
    df = df.rename(columns={t: 't', a_y: 'a_y', v_x: 'v_x', v_yaw: 'v_yaw', roll: 'roll'})

    # 计算侧向加速度修正值与转弯半径
    g = 9.81
    df['a_y_true'] = (df.a_y - g * sind(df.roll)) / cosd(df.roll)
    df['r'] = 180 / math.pi * df.v_x / 3.6 / df.v_yaw

    # 计算初始半径
    p_r = get_linear_fitting(df[['a_y_true', 'r']], method=3)
    r0 = p_r(0)

    # 根据初始半径正负判断转弯方向
    if r0 < 0:
        df['r'] = np.abs(df.r)
        r0 = np.abs(r0)
        direction = 'left'
    else:
        direction = 'right'

    # 计算转弯半径比
    df['ratio_r'] = df.r / r0

    # 计算前后轴侧偏角差
    df['d_sideslip_angle'] = 180 / math.pi * l * (1 / r0 - 1 / df.r)

    # 计算侧向加速度与转弯半径比拟合曲线
    p_ratio = get_linear_fitting(df[['a_y_true', 'ratio_r']], method=3)
    # 计算侧向加速度与前后轴侧偏角差拟合曲线
    p_d = get_linear_fitting(df[['a_y_true', 'd_sideslip_angle']], method=6)
    # 计算侧向加速度与车身侧倾角拟合曲线
    # 此处考虑到车身有起始侧倾角，因此没有使用无常数项的二次拟合，而是使用普通二次拟合
    p_roll = get_linear_fitting(df[['a_y_true', 'roll']], method=2)

    # 计算中性转向点
    a_neutral = np.roots(p_d.deriv())
    a_neutral = -a_neutral if direction == 'left' else a_neutral
    # 计算不足转向度
    degree_understeer = p_d(-2 if direction == 'left' else 2) / 2
    # 计算车身侧倾度
    roll_rate_body = (p_roll(-2 if direction == 'left' else 2) - p_roll(0)) / 2

    # 绘图时标题中的后缀
    suffix = '（' + ('左转' if direction == 'left' else '右转') + '）'

    # 绘图时用到点的x坐标
    x_max = df.a_y_true.max()
    x_min = df.a_y_true.min()
    x_range = np.arange(0, x_max, 0.01) if x_max > 0 else np.arange(x_min, 0, 0.01)

    # 绘制转弯半径比特性曲线
    ratio_chart = pygal.XY(
        legend_at_bottom=True,
        legend_at_bottom_columns=2,
        style=DefaultStyle(font_family='SimHei'),
        x_title='侧向加速度 a_y(m/s²)',
        y_title='转弯半径比 R/R_0',
    )
    ratio_chart.title = '转弯半径比特性曲线' + suffix
    ratio_chart.add('实际数据点', list(zip(df.a_y_true, df.ratio_r)), stroke=False)
    ratio_chart.add(
        'y={0:.4g}x³+{1:.4g}x²+{2:.4g}x+{3:.4g}'.format(*tuple(p_ratio.c)).replace('+-', '-'),
        [(x, p_ratio(x)) for x in x_range],
        show_dots=False, stroke=True, stroke_style={'width': 3}
    )
    # ratio_chart.render_in_browser()

    # 绘制前后轴侧偏角差曲线
    d_chart = pygal.XY(
        legend_at_bottom=True,
        legend_at_bottom_columns=2,
        style=DefaultStyle(font_family='SimHei'),
        x_title='侧向加速度 a_y(m/s²)',
        y_title='前后轴侧偏角差 δ_1-δ_2(°)',
    )
    d_chart.title = '前后轴侧偏角差特性曲线' + suffix
    d_chart.add('实际数据点', list(zip(df.a_y_true, df.d_sideslip_angle)), stroke=False)
    d_chart.add(
        'y={0:.4g}x³+{1:.4g}x²+{2:.4g}x'.format(*tuple(p_d.c)).replace('+-', '-'),
        [(x, p_d(x)) for x in x_range],
        show_dots=False, stroke=True, stroke_style={'width': 3}
    )
    # d_chart.render_in_browser()

    # 绘制车身侧倾角曲线
    roll_chart = pygal.XY(
        legend_at_bottom=True,
        legend_at_bottom_columns=2,
        style=DefaultStyle(font_family='SimHei'),
        x_title='侧向加速度 a_y(m/s²)',
        y_title='前后轴侧偏角差 Ψ(°)',
    )
    roll_chart.title = '车身侧倾角特性曲线' + suffix
    roll_chart.add('实际数据点', list(zip(df.a_y_true, df.roll)), stroke=False)
    roll_chart.add(
        'y={0:.4g}x²+{1:.4g}x+{2:.4g}'.format(*tuple(p_roll.c)).replace('+-', '-'),
        [(x, p_roll(x)) for x in x_range],
        show_dots=False, stroke=True, stroke_style={'width': 3}
    )
    # roll_chart.render_in_browser()

    return {
        'df': df,
        'charts': (ratio_chart, d_chart, roll_chart),
        'curves': (p_ratio, p_d, p_roll),
        'results': (direction, r0, a_neutral, degree_understeer, roll_rate_body),
    }


@validate_df
def returnability_test(df, leave_time, t, v_yaw, angle, precision=0.1):
    """
    低速转向回正试验数据处理，主要参考：
    《GB/T 6323-2014 汽车操纵稳定性试验方法》8.4
    :param df: 包含所需数据的df
    :param leave_time: 松手时刻
    :param t: 时间列名称，单位s
    :param v_yaw: 横摆角速度列名称，单位°/s
    :param angle: 转向盘转角列名称，单位°
    :param precision: 筛选精度
    :return:
    """
    # 提取并重命名相关数据列
    df = df[[t, v_yaw, angle]]
    df = df.rename(columns={t: 't', v_yaw: 'v_yaw', angle: 'angle'})

    # 截取松手至三秒后时刻数据段
    df_true = df.loc[(df.t >= leave_time) & (df.t <= leave_time + 3)]
    if len(df_true) < 2:
        raise RuntimeError('leave time out of range')
    if abs(df_true.iloc[0].t - leave_time) > precision:
        raise RuntimeError('there is no leave time satisfying %f precision in the data' % precision)
    if abs(df_true.iloc[-1].t - leave_time - 3) > precision:
        raise RuntimeError('there is no time three seconds later than the leave time'
                           ' satisfying %f precision in the data' % precision)

    # 计算横摆角速度初始值和结束值
    start_yaw = df_true.iloc[0].v_yaw
    end_yaw = df_true.iloc[-1].v_yaw  # 残余横摆角速度

    # 根据起始横摆角速度判断转弯方向
    direction = 'left' if start_yaw < 0 else 'right'

    # 计算横摆角速度总方差
    variance = (((df_true.v_yaw / start_yaw) ** 2).sum() - 0.5) * 3 / len(df_true)

    # 绘图时标题中的后缀
    suffix = '（' + ('左转' if direction == 'left' else '右转') + '）'

    # 截取绘图所用数据
    df_chart = df.loc[(df.t > leave_time - 3) & (df.t < leave_time + 5)]
    init_time = df_chart.iloc[0].t
    df_chart = set_zero(df_chart)

    # 绘制低速转向回正横摆角速度时域曲线
    yaw_chart = pygal.XY(
        legend_at_bottom_columns=4,
        style=DefaultStyle(font_family='SimHei'),
        x_title='时间 t(s)',
        y_title='横摆角速度 Δr(°/s)',
    )
    yaw_chart.title = '低速转向回正横摆角速度时域曲线' + suffix
    yaw_chart.add('横摆角速度', list(zip(df_chart.t, df_chart.v_yaw)),
                  stroke=True, show_dots=False, stroke_style={'width': 3})
    yaw_chart.add('松手时刻', [(df_true.iloc[0].t - init_time, df_true.iloc[0].v_yaw)], dots_size=5)
    yaw_chart.add('3s时刻', [(df_true.iloc[-1].t - init_time, df_true.iloc[-1].v_yaw)], dots_size=5)
    # yaw_chart.render_in_browser()

    # 绘制低速转向回正转向盘转角时域曲线
    angle_chart = pygal.XY(
        legend_at_bottom_columns=4,
        style=DefaultStyle(font_family='SimHei'),
        x_title='时间 t(s)',
        y_title='转向盘转角 δ(°)',
    )
    angle_chart.title = '低速转向回正转向盘转角时域曲线' + suffix
    angle_chart.add('转向盘转角', list(zip(df_chart.t, df_chart.angle)),
                    stroke=True, show_dots=False, stroke_style={'width': 3})
    angle_chart.add('松手时刻', [(df_true.iloc[0].t - init_time, df_true.iloc[0].angle)], dots_size=5)
    angle_chart.add('3s时刻', [(df_true.iloc[-1].t - init_time, df_true.iloc[-1].angle)], dots_size=5)
    # angle_chart.render_in_browser()

    return {
        'charts': (yaw_chart, angle_chart),
        'results': (end_yaw, variance),
    }


def draw_lemniscate(radius, width=3.0):
    """
    绘制双纽线摆桩图，主要参考：
    《GB/T 6323-2014 汽车操纵稳定性试验方法》9.3.1
    :param radius: 试验汽车前外轮的最小转弯半径，单位m
    :param width: 车宽，单位m
    :return:
    """
    angle = np.arange(0, 361, 0.1)
    r_min = radius * 1.1  # 双纽线最小曲率半径
    d = r_min * 3  # x轴最大值

    # 计算绘制双纽线所需xy坐标点
    l = d * np.sqrt(np.array([0 if item < 0 else item for item in cosd(2 * angle)]))
    x = l * cosd(angle)
    y = l * sind(angle)

    # 计算双纽线y轴最高点坐标
    x_max = d * np.sqrt(cosd(30 * 2)) * cosd(30)
    y_max = d * np.sqrt(cosd(30 * 2)) * sind(30)

    # 计算摆桩的偏移量
    offset = width / 2 + 0.05  # 车宽的一半加50cm

    # 标桩点
    stakes = [
        (d-offset, 0), (d+offset, 0), (x_max, y_max-offset), (x_max, y_max+offset),
        (x_max, -y_max-offset), (x_max, -y_max+offset), (offset, 0)
    ]
    stakes.extend([(-(item[0]), item[1]) for item in stakes])
    stakes.extend([(0, -offset), (0, offset)])

    # 绘制摆桩示意图
    chart = pygal.XY(style=DefaultStyle(font_family='SimHei'))
    chart.title = '双纽线摆桩示意图（最小转弯半径{0}m，车宽{1}m）'.format(radius, width)
    chart.add('双纽线', list(zip(x, y)), show_dots=False)
    chart.add('标桩点', stakes, stroke=False, formatter=lambda item: '({0:.4f},{1:.4f})'.format(*item), dots_size=5)
    chart.add('x={0:.4f}'.format(offset), [(offset, y_max+offset), (offset, -y_max-offset)], show_dots=False)
    chart.add(
        'x={0:.4f}'.format(x_max),
        [(x_max, y_max + offset), (x_max, -y_max - offset)],
        show_dots=False,
    )
    chart.add(
        'x={0:.4f}'.format(d - offset),
        [(d - offset, y_max + offset), (d - offset, -y_max - offset)],
        show_dots=False,
    )
    chart.add(
        'x={0:.4f}'.format(d + offset),
        [(d + offset, y_max + offset), (d + offset, -y_max - offset)],
        show_dots=False,
    )
    chart.add(
        'y={0:.4f}'.format(offset),
        [(-d - offset, offset), (d + offset, offset)],
        show_dots=False,
    )
    chart.add(
        'y={0:.4f}'.format(y_max - offset),
        [(-d - offset, y_max - offset), (d + offset, y_max - offset)],
        show_dots=False,
    )
    chart.add(
        'y={0:.4f}'.format(y_max + offset),
        [(-d - offset, y_max + offset), (d + offset, y_max + offset)],
        show_dots=False,
    )
    # chart.render_in_browser()
    # chart.render_to_png('re.png')
    # chart.render_to_file('re.svg')

    return {
        'chart': chart,
        'results': (stakes, r_min, d, offset, x_max, y_max),
    }


if __name__ == '__main__':
    # p = driving_resistance(12500)
    # print(p)
    res = draw_lemniscate(6.23, width=3.15)
    print()
