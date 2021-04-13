"""
Description: 类，针对facex的客户端，可以发送请求返回应答，不同考虑请求格式
version:
Author: TianyuYuan
Date: 2021-02-07 11:54:35
LastEditors: TianyuYuan
LastEditTime: 2021-03-23 19:36:45
"""
import base64
import json
import os
import os.path as osp

import numpy as np
import requests


class FacexClient():
    """
    针对facex的客户端，可以发送请求返回应答，不用考虑请求格式
    """

    def __init__(self, ip, port, group_id='FacexClient-tyyuan'):
        """
        初始化一个facex的客户端
        - ip: 服务器的ip地址(ip可直接选择输入gpu205或gpu206)
        - port: facex的服务端口
        - group_id: 注册照片的组名
        """
        if ip == 'gpu205': ip = "172.16.10.5"
        if ip == 'gpu206': ip = "172.16.10.6"
        self.url = "http://{}:{}".format(ip, port)
        self.api_add = "/users/v1/add"
        self.api_compare_1v1 = "/face/v1/compare-two-image"
        self.api_compare_1vn = "/face/v1/compare-1vn"
        self.api_get_feature = "/face/v1/get-feature"
        self.api_process = '/face/v1/process'
        self.group_id = group_id

    @staticmethod
    def img2base64(img_address: str) -> str:
        """读取图片地址，并将图片编码为base64"""
        with open(img_address, "rb") as fp:
            encoded_string = base64.b64encode(fp.read()).decode('utf-8').replace("'", "")
        return encoded_string

    def add(self, img_address, user_id, check=False) -> dict:
        """注册服务
        - img_address: abs path of the img
        - check: the swith of quality check
        - user_id
        - return: response
        """
        img64 = self.img2base64(img_address)
        data = {"user": {"user_id": user_id, "image": img64}, "groups": [self.group_id], "check": check}
        data = json.dumps(data)
        r = requests.post(self.url + self.api_add, data=data)
        return r.json()

    def add_samples(self, sample: dict, to_register: str, to_id: str, check: bool) -> dict:
        """注册sample
        - sample: 样本字典
        - to_register: 注册request_images or register_images
        - to_id: 以什么为user_id: img_name(without .jpg) or group_name
        - check: the swith of quality check
        - return: the response dict
        """
        img_address = sample[to_register][0]
        if to_id == "name":
            user_id = os.path.basename(img_address)[:-4]
        else:
            print("Unsupported user_id!")
            exit()
        r = self.add(img_address, user_id, check)
        return r

    @staticmethod
    def open_dataset(dataset) -> dict:
        """打开数据集"""
        if os.path.exists(dataset):
            with open(dataset, 'r') as fp:
                data = json.load(fp)
        elif isinstance(dataset, dict):
            data = dataset
        else:
            print("Unsupported dataset type, please make sure the input type is path or dict")
            exit(1)
        return data

    def add_dataset(self, dataset, to_register="register_images", to_id="name", check=False, worker=10):
        """注册整个数据集，适用于注册一个n_samples.json or p_samples.json
        - dataset: 数据集的字典
        - to_register: 注册request_images or register_images
        - to_id: 以什么为user_id: img_name(without .jpg) or group_name
        - check: the swith of quality check
        - worker: 多线程的大小
        - return log_list: 返回注册记录列表
        """
        from functools import partial
        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=worker)
        data = self.open_dataset(dataset)
        sample_list = data['images']
        log_list = list(
            executor.map(partial(self.add_samples, to_register=to_register, to_id=to_id, check=check), sample_list))
        return log_list

    def compare_1v1(self, img1_address, img2_address, threshold=80, check=False) -> bool:
        """比对1v1
        - img1_address,img2_address: abs path of the imgs
        - threshold: 阈值，大于此阈值则返回True
        - check: the switch of quality check
        - return: True: the same person
        """
        img1 = self.img2base64(img1_address)
        img2 = self.img2base64(img2_address)
        data = {"image1": img1, "image2": img2, "check": check}
        data = json.dumps(data)
        r = requests.post(self.url + self.api_compare_1v1, data=data)
        if r.json()["data"]["score"] < threshold:
            return False
        else:
            return True

    def compare_1vn(self, img_address, top_n=1, check=False, op=31) -> dict:
        """比对1vn
        - img_address: abs path of the img
        - top_n: 返回的最相似的个数
        - check: the swith of quality check
        - return: response
        """
        img64 = self.img2base64(img_address)
        data = {"image": img64, "group_id": self.group_id, "top_n": top_n, "check": check, "face_info_op": op}
        data = json.dumps(data)
        r = requests.post(self.url + self.api_compare_1vn, data=data)
        # check
        if r.status_code != requests.codes.ok:
            return None
        r = r.json()
        if r['error_no'] != 0:
            return None
        return r

    def compare_1vn_samples(self, sample, to_compare, top_n, check) -> dict:
        """比对1vn 输入维度为sample
        - sample: 样本
        - to_compare: 拿样本里的什么进行比对：register_images/request_images
        - top_n: 返回前n个结果
        - check: the swith of quality check
        - return: {图片名：对比结果字典}
        """
        img_path = sample[to_compare][0]
        img = os.path.basename(img_path)
        r = self.compare_1vn(img_path, top_n, check)
        return {img: r}

    def compare_1vn_dataset(self, dataset: dict, to_compare="register_images", top_n=1, check=False, worker=10) -> list:
        """比对1vn 输入维度为sample
        - dataset:数据集
        - to_compare: 拿样本里的什么进行比对：register_images/request_images
        - top_n: 返回前n个结果
        - check: the switch of quality check
        - worker: 多线程的大小
        - return: 结果列表[{img_name1:r1},{img_name2:r2}.....]
        """
        from functools import partial
        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=worker)
        data = self.open_dataset(dataset)
        sample_list = data["images"]
        log_list = list(executor.map(partial(self.compare_1vn_samples, to_compare=to_compare, top_n=top_n, check=check),
                                     sample_list))
        return log_list

    @staticmethod
    def base64tondarray(feature):
        """将64编码的特征转换成512维的特征向量"""
        tmp = base64.b64decode(feature)
        tmp2 = np.frombuffer(tmp, np.float32)
        return tmp2

    def get_feature(self, img_address) -> np.ndarray:
        """抽取图片的特征向量"""
        img64 = self.img2base64(img_address)
        data = {'image': img64}
        r = requests.post(self.url + self.api_get_feature, data=data)
        feature = r.json()['data']['feature_matrix']
        feature_array = self.base64tondarray(feature)
        return feature_array

    @staticmethod
    def write_log(log_list: list, log_name="log"):
        """保存log记录，可用于
        compare_1vn_dataset
        add_dataset之后
        """
        with open(log_name) as fp:
            json.dump(log_list, fp, indent=4)

    def img_process(self, img_address: str, op=31) -> dict:
        """处理图片，获取face_info信息
        - img_address: abs path of the img
        - op: 返回那些信息
        - return: response
        """
        img64 = self.img2base64(img_address)
        data = {'image_base64': img64, 'op': op}
        data = json.dumps(data)
        r = requests.post(self.url + self.api_process, data=data)
        if r.status_code != requests.codes.ok:
            return None
        r = r.json()
        if r['error_no'] != 0:
            return None
        return r

    # -------------------------------- 用facex建立rgbir/rgbdir/rgbd112的数据集 -------------------------------- #
    def get_box(self, img_address: str, check=True) -> dict:
        """从img_process的response中提取检测框的信息
        - img_address: abs path of the img
        - return: a dict contains the info of the box
        """
        if check:
            r = self.compare_1vn(img_address, check=True, op=10)
        else:
            r = self.img_process(img_address, op=10)
        if not r:
            return None
        box = r['data']['face_info']['box']
        return box

    def get_box_txt(self, txt_address: str, img_type=1) -> dict:
        """以txt为单位的提取图片检测框信息
        - txt_address: the abs address of txt: line: rgb (d) (ir)
        - return: ans = {txt_name:{img:box,img:box,...},txt_name:{...},...}
        """
        txt_name = osp.basename(txt_address).split('.')[0]
        ans = {txt_name: {}}
        with open(txt_address, 'r') as fp:
            lines = fp.readlines()
        for line in lines:
            line_list = line.strip().split()
            rgb_path = line_list[img_type]
            box = self.get_box(rgb_path, check=True)
            if not box:
                continue
            ans[txt_name][rgb_path] = box
        return ans
