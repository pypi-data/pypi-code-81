from scipy import interpolate
import numpy as np


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


if __name__ == '__main__':
    print(driving_resistance(12500))
