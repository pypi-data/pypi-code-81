# pie_tree.py
# nick gerend

import pandas as pd
import numpy as np
from math import pi, cos, sin, sqrt

class point:
    def __init__(self, index, level, group, x, y, path, count): 
        self.index = index
        self.level = level
        self.group = group
        self.x = x
        self.y = y
        self.path = path
        self.count = count
    def to_dict(self):
        return {
            'index' : self.index,
            'level' : self.level,
            'group' : self.group,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'count' : self.count }

def dict_start_end(group, start, count):
    df_dict = group.size()
    df_dict = df_dict.to_dict()
    #start = 0
    end = 0
    count_ = 0
    for key in df_dict:
        count_ = df_dict[key]
        end = df_dict[key] + start
        df_dict[key] = []
        df_dict[key].append(end/count - start/count)
        df_dict[key].append(0.) # r1
        df_dict[key].append(0.) # r2
        df_dict[key].append(0.) # a1
        df_dict[key].append(0.) # a2
        df_dict[key].append(0.) # jump
        df_dict[key].append(count_) # count
        start = end
    return df_dict

def inner_rad(area, r1, f):
    num = area/f+pi*r1**2
    return sqrt(num/pi)

def inner_angle(area, r1, r2, fill_angle):
    num = area/(pi*r2**2-pi*r1**2)
    return num*fill_angle

def location(r1, r2, a1, a2, area, orientation='v', fill_angle=360.):
    area_o = pi*r2**2-pi*r1**2
    out = 0.
    if orientation == 'h':
        f = (a2-a1)/fill_angle
        r3 = sqrt(((area/(f))+pi*r1**2)/pi)
        out = r1, r3, a1, a2 
    else:
        a3 = (area*fill_angle)/(pi*r2**2-pi*r1**2)
        out = r1, r2, a1, a3
    return out

def pie_tree(df, groupers, r1, r2, start_angle, end_angle, points, default_sort = False, default_sort_override = True, default_sort_override_reversed = True, all_vertical = False):

    #region algorithm

    #region initialize
    list_group = []
    for i in range(len(groupers)):
        group_i = groupers[0:i+1]
        df_group = df.groupby(group_i, sort=default_sort)
        df_dict = dict_start_end(df_group, 0., len(df))
        if default_sort_override:
            df_dict = dict(sorted(df_dict.items(), key=lambda item: item[1][0], reverse=default_sort_override_reversed))
        list_group.append(df_dict)
    last = 0.
    for i in list_group[0]:
        list_group[0][i][1] = r1
        list_group[0][i][2] = r2
        list_group[0][i][3] = last * (end_angle-start_angle) + start_angle
        list_group[0][i][4] = (last + list_group[0][i][0]) * (end_angle-start_angle) + start_angle
        last += list_group[0][i][0]
    #endregion

    #region point grid
    area = (pi*r2**2-pi*r1**2)*((end_angle-start_angle)/360.)
    for i in range(1, len(groupers), 1):
        ri = 0
        ai = 0
        rc1, rc2, ac1, ac2 = 0., 0., 0., 0.
        for j in list_group[i]:
            # parent box
            key = j[0:i]
            if i == 1:
                key = key[0]
            # key = ','.join(key)
            rp1 = list_group[i-1][key][1]
            rp2 = list_group[i-1][key][2]
            ap1 = list_group[i-1][key][3]
            ap2 = list_group[i-1][key][4]
            jump = list_group[i-1][key][5]
            
            # child box
            areac = list_group[i][j][0]*area
            if i % 2 == 0 or all_vertical:
                rc1, rc2, ac1, ac2 = location(rp1, rp2, ap1, ap2, areac, 'v')
                if key == ('Individual', 'Fixed wing single engine'):
                    stop = 1
                list_group[i-1][key][5] += ac2
                ac1 += jump
                ac2 += ac1
            else:
                if jump == 0:
                    jump = rp1
                rc1, rc2, ac1, ac2 = location(jump, rp2, ap1, ap2, areac, 'h')
                if key == 'Non Citizen Co-Owned':
                    stop = 1
                list_group[i-1][key][5] = rc2
            list_group[i][j][1] = rc1
            list_group[i][j][2] = rc2
            list_group[i][j][3] = ac1
            list_group[i][j][4] = ac2
    #endregion

    #region draw
    ix = 0
    level = 1
    list_xy = []
    for i in range(len(groupers)):
        for j in list_group[i]:
            ad1 = list_group[i][j][3]
            ad2 = list_group[i][j][4]
            a1 = (ad1-90.)*pi/180.
            a2 = (ad2-90.)*pi/180.
            r_1 = list_group[i][j][1]
            r_2 = list_group[i][j][2]
            x1 = r_1*cos(a1)
            y1 = r_1*sin(a1)

            point_frac = (ad2-ad1)/365.
            points1 = int(point_frac*points)+5
            points2 = int(point_frac*points*r_1/r_2)+5
            angles1 = np.linspace(a1, a2, num=points1)
            angles2 = np.linspace(a2, a1, num=points2)

            count = list_group[i][j][6]

            list_xy.append(point(ix, level, j, x1, -y1, 0, count))
            for k in range(len(angles1)):
                list_xy.append(point(ix, level, j, r_2*cos(angles1[k]), -r_2*sin(angles1[k]), k+1, count))
            for k in range(len(angles2)):
                list_xy.append(point(ix, level, j, r_1*cos(angles2[k]), -r_1*sin(angles2[k]), len(angles1)+k+1, count))
            
        level += 1
    #endregion

    #endregion

    df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
    return df_out

# df = pd.read_csv(os.path.dirname(__file__) + '/file.csv', dtype=pd.StringDtype())
# groupers = ['column_1', 'column_2', 'column_n']
# df_pie_tree = pie_tree(df, groupers, 0.5, 2., 0., 90., 200, default_sort = False, default_sort_override = True, default_sort_override_reversed = False, all_vertical = False)