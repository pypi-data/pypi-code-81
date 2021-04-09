# -*- coding: utf-8 -*-
# __init__.py


from addressformat.structures import AddrMap, Pca
from addressformat.structures import P,C,A
#from addressformat.regex_format import *
from addressformat.project_setting import project_root
import os
import jieba
import json

jieba.load_userdict(os.path.join(project_root, "resources/address_dict.csv"))
jieba.load_userdict(os.path.join(project_root, "resources/town_dict.csv"))

VERSION = (0, 4, 8)

__version__ = ".".join([str(x) for x in VERSION])

# 从乡镇反推省市区的map
xz_map = {}

def _data_from_csv() -> (AddrMap, AddrMap, AddrMap, dict, dict):
    # 区名及其简写 -> 相关pca元组
    area_map = AddrMap()
    # 城市名及其简写 -> 相关pca元组
    city_map = AddrMap()
    # (省名全称, 区名全称) -> 相关pca元组
    province_area_map = AddrMap()
    # 省名 -> 省全名
    province_map = {}
    # (省名, 市名, 区名) -> (纬度,经度)
    latlng = {}
    # 数据约定:国家直辖市的sheng字段为直辖市名称, 省直辖县的city字段为空
    from pkg_resources import resource_stream

    with resource_stream('addressformat.resources', 'pca.csv') as pca_stream:
        from io import TextIOWrapper
        import csv
        text = TextIOWrapper(pca_stream, encoding='utf8')
        pca_csv = csv.DictReader(text)
        for record_dict in pca_csv:
            latlng[(record_dict['sheng'], record_dict['shi'], record_dict['qu'])] = \
                (record_dict['lat'], record_dict['lng'])

            _fill_province_map(province_map, record_dict)
            _fill_area_map(area_map, record_dict)
            _fill_city_map(city_map, record_dict)
            _fill_province_area_map(province_area_map, record_dict)

    return area_map, city_map, province_area_map, province_map, latlng

def _xz_map_from_csv_() ->(dict):
    xm = {}

    from pkg_resources import resource_stream
    with resource_stream('addressformat.resources', 'sz.csv') as pca_stream:
        from io import TextIOWrapper
        import csv
        text = TextIOWrapper(pca_stream, encoding='utf8')
        pca_csv = csv.DictReader(text)
        for record_dict in pca_csv:
            if record_dict['xz'] not in xm:
                xm[record_dict['xz']] = []
            xm[record_dict['xz']].append({'sheng':record_dict['sheng'], 'shi':record_dict['shi'], 'qu':record_dict['qu']})

    return xm

def _fill_province_area_map(province_area_map: AddrMap, record_dict):
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'])
    key = (record_dict['sheng'], record_dict['qu'])
    # 第三个参数在此处没有意义, 随便给的
    province_area_map.append_relational_addr(key, pca_tuple, P)


def _fill_area_map(area_map: AddrMap, record_dict):
    area_name = record_dict['qu']
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'])
    area_map.append_relational_addr(area_name, pca_tuple, A)
    if area_name.endswith('city'):
        area_map.append_relational_addr(area_name[:-1], pca_tuple, A)


def _fill_city_map(city_map: AddrMap, record_dict):
    city_name = record_dict['shi']
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'])
    city_map.append_relational_addr(city_name, pca_tuple, C)
    if city_name.endswith('city'):
        city_map.append_relational_addr(city_name[:-1], pca_tuple, C)
    # 特别行政区
    # elif city_name == '香港特别行政区':
    #     city_map.append_relational_addr('香港', pca_tuple, C)
    # elif city_name == '澳门特别行政区':
    #     city_map.append_relational_addr('澳门', pca_tuple, C)
    

def _fill_province_map(province_map, record_dict):
    sheng = record_dict['sheng']
    if sheng not in province_map:
        province_map[sheng] = sheng
        # 处理省的简写情况
        # 普通省分 和 直辖市
        if sheng.endswith('province') or sheng.endswith('city'):
            province_map[sheng[:-1]] = sheng
        # 自治区
        elif sheng == '新疆维吾尔自治区':
            province_map['新疆'] = sheng
        elif sheng == '内蒙古自治区':
            province_map['内蒙古'] = sheng
        elif sheng == '广西壮族自治区':
            province_map['广西'] = sheng
            province_map['广西省'] = sheng
        elif sheng == '西藏自治区':
            province_map['西藏'] = sheng
        elif sheng == '宁夏回族自治区':
            province_map['宁夏'] = sheng
        # 特别行政区
        # elif sheng == '香港特别行政区':
        #     province_map['香港'] = sheng
        # elif sheng == '澳门特别行政区':
        #     province_map['澳门'] = sheng


area_map, city_map, province_area_map, province_map, latlng = _data_from_csv()
xz_map = _xz_map_from_csv_()

def getSSQFromXZ(xzStr,province="",city="",default_province="",default_city=""):
    find_item_list = []
    if xzStr in xz_map:
        for item in xz_map[xzStr]:
            if province:
                if item['sheng'] != province:
                    continue
            if city:
                if item['shi'] != city:
                    continue

            find_item_list.append(item)

    if  default_province:
        find_item_list = [item for item in find_item_list if item['sheng'] == default_province]

    if  default_city:
        find_item_list = [item for item in find_item_list if item['shi'] == default_city]

    # 如果还存在多个，查找共同的省市
    if len(find_item_list) >= 2:
        provinces = [item['sheng'] for item in find_item_list ]
        city = [item['shi'] for item in find_item_list ]
        out_item = {}
        out_item['qu'] = ""
        out_item['sheng'] = ""
        out_item['shi'] = ""
        if len(list(set(provinces))) == 1:
            out_item['sheng'] = provinces[0]
        if len(list(set(city))) == 1:
            out_item['shi'] = city[0]
        find_item_list = [out_item]


    if len(find_item_list) == 1:
        return  find_item_list[0]['sheng'],find_item_list[0]['shi'],find_item_list[0]['qu']
    else:
        return "","",""


# 直辖市
munis = {'北京市', '天津市', '上海市', '重庆市'}


def is_munis(city_full_name):
    return city_full_name in munis


myumap = {
    '南关区': '长春市',
    '南山区': '深圳市',
    '宝山区': '上海市',
    '市辖区': '东莞市',
    '普陀区': '上海市',
    '朝阳区': '北京市',
    '河东区': '天津市',
    '白云区': '广州市',
    '西湖区': '杭州市',
    '铁西区': '沈阳市'
}


def transform(location_strs, umap=myumap, index=[], cut=True, lookahead=8, pos_sensitive=False, open_warning=True):
    """将地址描述字符串转换以"province","city","county"信息为列的DataFrame表格
        Args:
            locations:地址描述字符集合,可以是list, Series等任意可以进行for in循环的集合
                      比如:["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            umap:自定义的区级到市级的映射,主要用于解决区重名问题,如果定义的映射在模块中已经存在，则会覆盖模块中自带的映射
            index:可以通过这个参数指定输出的DataFrame的index,默认情况下是range(len(data))
            cut:是否使用分词，默认使用，分词模式速度较快，但是准确率可能会有所下降
            lookahead:只有在cut为false的时候有效，表示最多允许向前看的字符的数量
                      默认值为8是为了能够发现"新疆维吾尔族自治区"这样的长地名
                      如果你的样本中都是短地名的话，可以考虑把这个数字调小一点以提高性能
            pos_sensitive:如果为True则会多返回三列，分别提取出的省市区在字符串中的位置，如果字符串中不存在的话则显示-1
            open_warning: 是否打开umap警告, 默认打开
        Returns:
            一个Pandas的DataFrame类型的表格，如下：
               |province    |city   |county    |地址                 |
               |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
               |福建省|泉州市|洛江区|万安塘西工业区        |
    """

    from collections.abc import Iterable

    if not isinstance(location_strs, Iterable):
        from .exceptions import InputTypeNotSuportException
        raise InputTypeNotSuportException(
            'location_strs参数必须为可迭代的类型(比如list, Series等实现了__iter__方法的对象)')

    import pandas as pd

    result = pd.DataFrame([_handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning) for addr in location_strs], index=index) \
             if index else pd.DataFrame([_handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning) for addr in location_strs])
    # 这句的唯一作用是让列的顺序好看一些
    if pos_sensitive:
        return result.loc[:, ('province', 'city', 'county', '地址', '省_pos', '市_pos', '区_pos')]
    else:
        return result.loc[:, ('province', 'city', 'county', '地址')]

def parseAddr(addr, umap=myumap, index=[], cut=False, lookahead=8, pos_sensitive=False, open_warning=True):
    result = _handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning)
    # 获取乡镇
    dz = result["地址"]
    if dz is not None and dz!="":
        xz,new_addr = parseXZ(dz)
        if xz!="":
            # 分词匹配乡镇信息
            result["乡镇"] = xz
            result["地址"] = new_addr
        else:
            # 乡镇库匹配 不修改地址信息 仅做参考乡镇
            if dz[:2]+"镇" in xz_map:
                result["乡镇"] = dz[:2]+"镇"
                # result["地址"] = result["地址"][2:]
            elif dz[:3]+"镇" in xz_map:
                result["乡镇"] = dz[:3]+"镇"
                # result["地址"] = result["地址"][3:]


    # 根据正则获取道路和道路号码
    road,road_num = GetRoadNumByRegex(result["地址"])
    if road!="" and road_num!="":
        # result["道路"] = road
        # result["道路号"] = road_num
        result["地址"] = road + road_num + result["地址"][len(road)+len(road_num):]

    # 根据正则获取组和组号
    zu,zu_num = GetZuAndNum(result["地址"])
    if zu!="" and zu_num!="":
        # result["组"] = zu
        # result["组号"] = zu_num
        result["地址"] = result["地址"][:len(result["地址"])-len(zu)-len(zu_num)]+zu+zu_num
        
    # 乡镇反推省市区
    if result["乡镇"]!="":
        sheng,shi,qu = getSSQFromXZ(result["乡镇"])
        if sheng!="" and shi!="" and qu!="":
            result["province"] = sheng
            result["city"] = shi
            result["county"] = qu

    # 本项目用于江苏苏州
    result["province"] = "江苏省"
    result["city"] = "苏州市"

    return result

def parseXZ(addr):
    seg_list = jieba.lcut(addr, cut_all=False)
    
    if len(seg_list)>0 and isXZ(seg_list[0]):
        return seg_list[0],addr[len(seg_list[0]):]
    return "",""

def isXZ(value):
    if value.endswith("镇") or value.endswith("乡") or value.endswith("旗"):
        return True
    return False

def _handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning):
    """处理一条记录"""
    src_addr = addr
    # 空记录
    if not isinstance(addr, str) or addr == '' or addr is None:
        empty = {'province': '', 'city': '', 'county': ''}
        if pos_sensitive:
            empty['省_pos'] = -1
            empty['市_pos'] = -1
            empty['区_pos'] = -1
        return empty

    # 地名提取
    pca, addr = _extract_addr(addr, cut, lookahead)

    _fill_city(pca, umap, open_warning,src_addr)

    _fill_province(pca)


    # 乡镇反推省市区
    if pca.town != "":
        sheng, shi, qu = getSSQFromXZ(pca.town,pca.province,pca.city)
        if sheng != "" and shi != "" and qu != "":
            pca.province = sheng
            pca.city = shi
            pca.area = qu


    result = pca.propertys_dict(pos_sensitive)
    result["乡镇"] = ""
    # result["道路"] = ""
    # result["道路号"] = ""
    result["地址"] = addr
    # result["组"] = ""
    # result["组号"] = ""
    
    # # 去除剩余地址中以省市区开头的部分
    # for x in range(1,10):
    #     x = 0
    #     if addr.startswith(result["province"]):
    #         addr = addr[len(result["province"]):]
    #         result["地址"] = addr
    #     elif addr.startswith(result["city"]):
    #         addr = addr[len(result["city"]):]
    #         result["地址"] = addr
    #     elif addr.startswith(result["county"]):
    #         addr = addr[len(result["county"]):]
    #         result["地址"] = addr
    #     else:
    #         break

    return result


def handle_one_record(addr, umap=myumap, index=[], cut=False, lookahead=8, pos_sensitive=False, open_warning=True,default_province ="",default_city=""):
    """处理一条记录"""
    src_addr = addr
    # 空记录
    if not isinstance(addr, str) or addr == '' or addr is None:
        empty = {'province': '', 'city': '', 'county': ''}
        if pos_sensitive:
            empty['省_pos'] = -1
            empty['市_pos'] = -1
            empty['区_pos'] = -1
        return empty

    # 地名提取
    pca, addr = _extract_addr(addr, cut, lookahead)

    _fill_city(pca, umap, open_warning, src_addr)
    # if default_city:
    #     if pca.weak_county and pca.city != default_city:
    #         pca.area = ""
    #         pca.area_pos = -1
    #         pca.city = ""
    #         pca.city_pos = -1


    _fill_province(pca)

    if default_province:
        if pca.weak_county and pca.province != default_province:
            pca.area = ""
            pca.area_pos = -1
            pca.city = ""
            pca.city_pos = -1
            pca.province = ""
            pca.province_pos = -1

    # 乡镇反推省市区
    if pca.town != "":
        sheng, shi, qu = getSSQFromXZ(pca,default_province=default_province,default_city=default_city)
        if sheng != "":
            pca.province = sheng
        if shi != "":
            pca.city = shi
        if qu != "":
            pca.area = qu

    result = pca.propertys_dict(pos_sensitive)
    result["乡镇"] = ""
    # result["道路"] = ""
    # result["道路号"] = ""
    result["地址"] = addr
    # result["组"] = ""
    # result["组号"] = ""

    # # 去除剩余地址中以省市区开头的部分
    # for x in range(1,10):
    #     x = 0
    #     if addr.startswith(result["province"]):
    #         addr = addr[len(result["province"]):]
    #         result["地址"] = addr
    #     elif addr.startswith(result["city"]):
    #         addr = addr[len(result["city"]):]
    #         result["地址"] = addr
    #     elif addr.startswith(result["county"]):
    #         addr = addr[len(result["county"]):]
    #         result["地址"] = addr
    #     else:
    #         break

    return result

def _fill_province(pca):
    """填充省"""
    if (not pca.province) and pca.city and (pca.city in city_map):
        pca.province = city_map.get_value(pca.city, P)


def _fill_city(pca, umap, open_warning,addr):
    if not pca.city and not pca.province and not pca.area:
        return
    """填充市"""
    if not pca.city:
        # 从 province,county 映射
        if pca.area and pca.province:
            newKey = (pca.province, pca.area)
            if newKey in province_area_map and province_area_map.is_unique_value(newKey):
                pca.city = province_area_map.get_value(newKey, C)
                return
            else:
                pca.area = ""
                pca.area_pos = -1

        # 从 county 映射
        elif pca.area:
            # 从umap中映射
            if umap.get(pca.area):
                pca.city = umap.get(pca.area)
                return
            if pca.area in area_map and area_map.is_unique_value(pca.area):
                pca.city = area_map.get_value(pca.area, C)
                return


def _extract_addr(addr, cut, lookahead):
    """提取地址中的省,city,区名称
       Args:
           addr:原始地址字符串
           cut: 是否分词
       Returns:
           [sheng, shi, qu, (sheng_pos, shi_pos, qu_pos)], addr
    """
    return _jieba_extract(addr) if cut else _full_text_extract(addr, lookahead)


def _jieba_extract(addr):
    """基于结巴分词进行提取"""
    result = Pca(address= addr)

    pos = 0
    truncate = 0

    def _set_pca(pca_property, name, full_name):
        """pca_property: 'province', 'city' or 'area'"""
        if not getattr(result, pca_property):
            setattr(result, pca_property, full_name)
            setattr(result, pca_property + "_pos", pos)
            if is_munis(full_name):
                setattr(result, "province_pos", pos)
            nonlocal truncate
            if pos == truncate:
                truncate += len(name)

    for word in jieba.cut(addr):
        # 优先提取低级别行政区 (主要是为直辖市和特别行政区考虑)
        if word in area_map:
            _set_pca('area', word, area_map.get_full_name(word))
        elif word in city_map:
            _set_pca('city', word, city_map.get_full_name(word))
        elif word in province_map:
            _set_pca('province', word, province_map[word])
        
        pos += len(word)

    return result, addr[truncate:]


from addressformat.instance import get_keywordTredTree_instance,get_mapping_dict
def _full_text_extract(addr, lookahead):
    """全文匹配进行提取"""

    result = Pca(address=addr,map_dict=get_mapping_dict())

    truncate = 0
    trieTree = get_keywordTredTree_instance()
    jieba_cuts = list(jieba.cut(addr))
    jieba_cuts_start_positions = [0]
    for word in jieba_cuts[:-1]:
        jieba_cuts_start_positions.append(jieba_cuts_start_positions[-1] + len(word))

    words_list, type_list, position_list = trieTree.process(addr,jieba_cuts_start_positions)



    for word,word_type,positon in zip(words_list,type_list,position_list):
        result.update_info(word,word_type,positon)
    result.check_address_valid()
    return result, addr