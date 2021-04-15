'''
Description: 解析np_samples
version:
Author: TianyuYuan
Date: 2021-04-06 21:22:57
LastEditors: TianyuYuan
LastEditTime: 2021-04-15 15:08:46
'''
import json
import os.path as osp


class ParseNP:
    """
    ## 解析标注结果(np_samples.json)工具包
    """

    @staticmethod
    def read_json(json_path) -> dict:
        """读取json文件"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def get_ids2sample(data) -> dict:
        """
        描述：获取以ids为key，所对应sample为val的dict
        - data: 由json导入后的np_samples.json
        - return: ids2sample{'ids':sample}
        - ⚠️注意：key是ids，与图片名不通用
        """
        ids2sample = {}
        for sample in data['images']:
            for ids in sample['ids']:
                ids2sample[ids] = sample
        return ids2sample

    @staticmethod
    def get_request2sample(data) -> dict:
        """
        描述：获取以request为key，所对应sample为val的dict
        - data: 由json导入后的np_samples.json
        - return: request2sample={'request':sample}
        - ⚠️注意：key是图片名，带.jpg后缀
        """
        request2sample = {}
        for sample in data['images']:
            rqsts = sample['request_images']
            for rqst in rqsts:
                rqst = osp.basename(rqst)
                request2sample[rqst] = sample
        return request2sample

    @staticmethod
    def get_request2index(data:dict) -> dict:
        """
        描述：获取以request为key，所对应index为val的dict
        - data: 由json导入后的np_samples.json
        - return: request2index={'request':sample_index}
        - ⚠️注意：key是图片名，带.jpg后缀
        """
        request2index = {}
        for index, sample in enumerate(data['images']):
            requests = sample['request_images']
            for rqst in requests:
                rqst = osp.basename(rqst)
                request2index[rqst] = index
        return request2index

    @staticmethod
    def get_register2sample(data) -> dict:
        '''
        描述：获取以register为key，所对应sample为val的dict
        - data: 由json导入后的np_samples.json
        - return: register2sample{'register':sample}
        - ⚠️注意：key是图片名，带.jpg后缀
        '''
        register2sample = {}
        for sample in data['images']:
            registers = sample['register_images']
            for register in registers:
                register = osp.basename(register)
                register2sample[register] = sample
        return register2sample

    @staticmethod
    def get_register2index(data) -> dict:
        """从data中获得register和index的关系，方便后续用index直接修改p_data"""
        register2index = {}
        for index, sample in enumerate(data['images']):
            registers = sample['register_images']
            for register in registers:
                register = osp.basename(register)
                register2index[register] = index
        return register2index

    @staticmethod
    def get_ids2index(data: dict) -> dict:
        """从data中获得ids和index的关系，方便后续用index直接修改p_data"""
        ids_index = {}
        for index, sample in enumerate(data['images']):
            ids = sample['ids'][0]
            ids_index[ids] = index
            index += 1
        return ids_index
    
    @staticmethod
    def total_samples(data) -> int:
        """统计data中有多少个sample"""
        if not isinstance(data, dict):
            # not dict, is data's path?
            data = ParseNP.read_json(data)
        return len(data['images'])

    @staticmethod
    def total_requests(data) -> int:
        """
        描述：统计data中有多少的request_images
        - data: 由json导入后的np_samples.json
        - return: request_images的总数
        """
        if not isinstance(data, dict):
            # not dict, is data's path?
            data = ParseNP.read_json(data)
        total = 0
        for sample in data['images']:
            total += len(sample['request_images'])
        return total

    @staticmethod
    def total_registers(data) -> int:
        """
        描述：统计data中有多少的register_images
        - data: 由json导入后的np_samples.json
        - return: register_images的总数
        """
        if not isinstance(data, dict):
            # not dict, is data's path?
            data = ParseNP.read_json(data)
        total = 0
        for sample in data['images']:
            total += len(sample['register_images'])
        return total

    @staticmethod
    def show_info(data, np=""):
        """展示np_samples的主要信息"""
        if not isinstance(data, dict):
            data = ParseNP.read_json(data)
        total_samples = ParseNP.total_samples(data)
        total_registers = ParseNP.total_registers(data)
        total_requests = ParseNP.total_requests(data)
        if np == "p":
            print("p_samples的信息：")
        if np == "n":
            print("n_samples的信息")
        print("sample总数为：", total_samples)
        print("register总数为：", total_registers)
        print("request总数为：", total_requests)

if __name__ == "__main__":
    print(help(ParseNP))