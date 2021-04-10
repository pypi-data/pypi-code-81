import re
import os
import pandas as pd
import datetime
def jh():
    x = input('请输入桌面上要转换的文件名:')
    day=input('请输入接机日期:')
    data = pd.read_excel(x+ '.xlsx')
    col = ['姓名', '人数', '身份证', '酒店', '接站牌', '备注']
    data.columns = col
    data = data[3:-1]

    data['航班'] = data['备注'].str.extract(r'([a-zA-Z0-9]+[a-zA-Z]+[\d\,\*]+)')
    data['时间'] = data['备注'].str.extract(r'(\d\d[：:]\d\d)')
    data['时间'] = data['时间'].str.replace("：", ":")
    data['手机'] = data['接站牌'].str.extract(r'(\d{11})')
    data['线路'] = '接机'
    data['成人'] = data['人数'].str.split('+', expand=True)[0]
    data['儿童'] = data['人数'].str.split('+', expand=True)[1]
    data['标'] = data['酒店'].str.extract(r'(.(?=标))')
    data['单'] = data['酒店'].str.extract(r'(.(?=单))')
    data['三'] = data['酒店'].str.extract(r'(.(?=三))')
    data['加'] = data['酒店'].str.extract(r'(.(?=加))')
    data['培'] = data['酒店'].str.extract(r'(.(?=培))')
    data['序号'] = 1
    data['接机日期'] = day
    data.reset_index(drop=True, inplace=True)

    tdy = datetime.date.today()
    dqrq = datetime.date(2021, 4, 15)
    if tdy > dqrq:
        order = ['序号', '姓名', '身份证', '手机', '成人', '儿童', '线路', '时间', '标', '单', '三', '加', '培', '接站牌', '备注', '人数',
                 ]
    else:
        order = ['序号', '姓名', '身份证', '手机', '成人', '儿童', '航班', '接机日期', '线路', '时间', '标', '单', '三', '加', '培', '接站牌', '备注',
                 '人数',
                 '酒店']

    data = data[order]  # 更改列顺
    # 添加分组序号
    for i in range(1, len(data)):
        if pd.isnull(data.loc[i, '接站牌']):
            data.loc[i, '序号'] = data.loc[i - 1, '序号']
            data.loc[i, '接机日期'] = ""
            data.loc[i, '线路'] = ""
        else:
            data.loc[i, '序号'] = data.loc[i - 1, '序号'] + 1
    # 处理单组分开接的情况
    num = []  # 保存自接客人编号
    for i in range(0, len(data)):
        s = str(data.loc[i, '备注'])
        if '接机1' in s:
            b = r'(?<=接机1)([\u4e00-\u9fa5]*)'
            c = r'接机1.*?([A-Z0-9]+)'
            d = r'(\d\d[：:]\d\d)'
            time = re.findall(d, s)[0]
            name = re.findall(b, s)[0]
            flight = re.findall(c, s)[0]
            j = data[data['姓名'] == name].index.tolist()[0]
            data.loc[j, '航班'] = flight
            data.loc[j, '接机日期'] = day
            data.loc[j, '时间'] = time
            data.loc[j, '线路'] = "接机"
        if '接机2' in s:
            b = r'(?<=接机2)([\u4e00-\u9fa5]*)'
            c = r'接机2.*?([A-Z0-9]+)'
            d = r'(\d\d[：:]\d\d)'
            time = re.findall(d, s)[0]
            name = re.findall(b, s)[0]
            flight = re.findall(c, s)[0]
            j = data[data['姓名'] == name].index.tolist()[0]
            data.loc[j, '航班'] = flight
            data.loc[j, '接机日期'] = day
            data.loc[j, '时间'] = time
            data.loc[j, '线路'] = "接机"
        if '接机3' in s:
            b = r'(?<=接机3)([\u4e00-\u9fa5]*)'
            c = r'接机3.*?([A-Z0-9]+)'
            d = r'(\d\d[：:]\d\d)'
            time = re.findall(d, s)[0]
            name = re.findall(b, s)[0]
            flight = re.findall(c, s)[0]
            j = data[data['姓名'] == name].index.tolist()[0]
            data.loc[j, '航班'] = flight
            data.loc[j, '接机日期'] = day
            data.loc[j, '时间'] = time
            data.loc[j, '线路'] = "接机"
        if '接高铁1' in s:
            b = r'(?<=接高铁1)([\u4e00-\u9fa5]*)'
            c = r'接高铁1.*?([A-Z0-9]+)'
            d = r'(\d\d[：:]\d\d)'
            time = re.findall(d, s)[0]
            name = re.findall(b, s)[0]
            flight = re.findall(c, s)[0]
            j = data[data['姓名'] == name].index.tolist()[0]
            data.loc[j, '航班'] = flight
            data.loc[j, '接机日期'] = day
            data.loc[j, '时间'] = time
            data.loc[j, '线路'] = '接高铁'
        if '接高铁2' in s:
            b = r'(?<=接高铁2)([\u4e00-\u9fa5]*)'
            c = r'接高铁2.*?([A-Z0-9]+)'
            d = r'(\d\d[：:]\d\d)'
            time = re.findall(d, s)[0]
            name = re.findall(b, s)[0]
            flight = re.findall(c, s)[0]
            j = data[data['姓名'] == name].index.tolist()[0]
            data.loc[j, '航班'] = flight
            data.loc[j, '接机日期'] = day
            data.loc[j, '时间'] = time
            data.loc[j, '线路'] = '接高铁'
        if '接高铁3' in s:
            b = r'(?<=接高铁3)([\u4e00-\u9fa5]*)'
            c = r'接高铁3.*?([A-Z0-9]+)'
            d = r'(\d\d[：:]\d\d)'
            time = re.findall(d, s)[0]
            name = re.findall(b, s)[0]
            flight = re.findall(c, s)[0]
            j = data[data['姓名'] == name].index.tolist()[0]
            data.loc[j, '航班'] = flight
            data.loc[j, '接机日期'] = day
            data.loc[j, '时间'] = time
            data.loc[j, '线路'] = '接高铁'
        if '接高铁4' in s:
            b = r'(?<=接高铁4)([\u4e00-\u9fa5]*)'
            c = r'接高铁4.*?([A-Z0-9]+)'
            d = r'(\d\d[：:]\d\d)'
            time = re.findall(d, s)[0]
            name = re.findall(b, s)[0]
            flight = re.findall(c, s)[0]
            j = data[data['姓名'] == name].index.tolist()[0]
            data.loc[j, '航班'] = flight
            data.loc[j, '接机日期'] = day
            data.loc[j, '时间'] = time
            data.loc[j, '线路'] = '接高铁'
        if '自接' in s:
            j = data.loc[i, '序号']
            num.append(j)
    for i in num:
        data.drop(data[data.序号 == i].index, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data['时间'] = data['时间'].str.replace("：", ":")
    for i in range(1, len(data)):
        if pd.isnull(data.loc[i, '接站牌']):
            data.loc[i, '序号'] = data.loc[i - 1, '序号']
            #data.loc[i, '接机日期'] = ""
            #data.loc[i, '线路'] = ""
        else:
            data.loc[i, '序号'] = data.loc[i - 1, '序号'] + 1
    print('已完成,请在桌面打开"' + x + '-导入.xlsx"' + '检查无误后导入易途')
    return data.to_excel(x + '-导入' + '.xlsx')