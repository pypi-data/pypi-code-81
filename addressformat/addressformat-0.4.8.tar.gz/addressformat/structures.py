# -*- coding: utf-8 -*-

from collections import defaultdict


P = 0
C = 1
A = 2


class AddrMap(defaultdict):
    """封装 '地名' -> [[相关地址列表], 地名全名]   这种映射结构"""

    def __init__(self):
        super().__init__(lambda: [[], None])

    def get_full_name(self, key):
        return self[key][1]

    def is_unique_value(self, key):
        """key所映射到的地址列表中的地址是否唯一"""
        if key not in self.keys():
            return False
        
        return len(self.get_relational_addrs(key)) == 1

    def get_relational_addrs(self, key):
        return self[key][0]

    def get_value(self, key, pos):
        """获得映射的第一个地址, 必须保证该key存在, 不然会出错"""
        return self.get_relational_addrs(key)[0][pos]

    def append_relational_addr(self, key, pca_tuple, full_name_pos):
        self[key][0].append(pca_tuple)
        if not self[key][1]:
            self[key][1] = pca_tuple[full_name_pos]


class Pca(object):

    def __init__(self,address="", province = '', city = '', area = '',town="", province_pos = -1, city_pos = -1, area_pos = -1,map_dict={}):
        self.address = address
        self.province = province
        self.city = city
        self.area = area
        self.town = town
        self.province_pos = province_pos
        self.town_pos = -1
        self.city_pos = city_pos
        self.area_pos = area_pos

        self.need_province = True
        self.need_city = True
        self.need_area = True
        self.need_town = True

        self.weak_county = False
        self.map_dict = map_dict

    def __str__(self):
        return self.province+","+self.city+","+self.area+","+self.town

    def propertys_dict(self, pos_sensitive):
        result = {
            "province": self.province,
            "city": self.city,
            "county": self.area,
            'town':self.town
        }

        if pos_sensitive:
            result["省_pos"] = self.province_pos
            result["市_pos"] = self.city_pos
            result["区_pos"] = self.area_pos
            result["镇_pos"] = self.area_pos

        return result


    def update_info(self,word,word_type,position):
        # reversed_addr_list = addr_list[::-1]


        if 'province' in word_type and self.need_province:
            self.need_province = False
            self.province = self.map_dict['province'][word]
            self.province_pos = position - len(word)
            return position
        elif 'city' in word_type and self.need_city:
            self.need_province = False
            self.need_city = False
            self.city = self.map_dict['city'][word]
            self.city_pos = position - len(word)
            return position
        elif 'county' in word_type and self.need_area:
            self.need_province = False
            self.need_city = False
            self.need_area = False
            self.area = self.map_dict['county'][word]
            self.area_pos = position - len(word)

            if self.area != word and self.city == "":
                '''没有city,而且不是完全命中'''
                self.weak_county = True
            return position
        elif 'town' in word_type and self.need_area:
            self.need_province = False
            self.need_city = False
            self.need_area = False


            self.town = self.map_dict['town'][word]
            self.town_pos = position - len(word)
            return position

        else:
            return -1










    def check_address_valid(self):
        '''
        1.假设提取到的信息，省市区，应该都集中在开头部分
        '''
        if self.province_pos != -1:
            if self.province_pos >=1:
                self.province_pos = -1
                self.province = ""
                self.city_pos = -1
                self.city = ""
                self.area_pos = -1
                self.area = ""
                self.town_pos = -1
                self.town = ""
        elif self.city_pos != -1:
            if self.city_pos >= 1:
                self.city_pos = -1
                self.city = ""
                self.area_pos = -1
                self.area = ""
                self.town_pos = -1
                self.town = ""
        elif self.area_pos != -1:
            if self.area_pos >= 1:
                self.area_pos = -1
                self.area = ""
                self.town_pos = -1
                self.town = ""
        elif self.town_pos != -1:
            if self.town_pos >= 1:
                self.town_pos = -1
                self.town = ""









