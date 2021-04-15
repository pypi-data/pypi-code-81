import random
import re
import os
import numpy as np
from .exif_read import ExifRead
from typing import Tuple

import requests
from io import BytesIO

from calculation.distance import Distance
from addict import Dict
import string


class Generator:

    @staticmethod
    def unique_matchId_generator(letter_count: int = 8, digit_count: int = 4) -> str:
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

        sam_list = list(str1)  # it converts the string to list.
        random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
        final_string = ''.join(sam_list)
        return final_string

    @staticmethod
    def path_url_creator(**kwargs) -> Tuple[str, str, str]:
        """

        :param gui:
        :param params.cfg:
        :param params.splitData:
        :param i:
        :param params.directory:
        :return:
        """
        params = Dict(kwargs)
        i = params.index
        host = params.cfgImage.ip_remote if params.cfgImage.Remote else params.cfgImage.ip_local
        if params.gui:
            ip_path = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            ip_check = bool(ip_path.match(params.directory))
            if ip_check:
                path = os.path.join(
                    "http://" + host + ":" + params.cfgImage.port + "/" + params.cfgImage.Directory + ":",
                    str(params.splitData[i]["dirname"]), params.splitData[i]["filename"], params.splitData[i]["imgname"])
            else:
                path = os.path.join(params.directory, str(params.splitData[i]["dirname"]),
                                    params.splitData[i]["filename"],
                                    params.splitData[i]["imgname"])
        else:
            path = os.path.join(
                "http://" + str(host) + ":" + str(params.cfgImage.port) + "/" + str(params.cfgImage.directory) + ":",
                str(params.splitData[i]["dirname"]), params.splitData[i]["filename"], params.splitData[i]["imgname"])
            outPath = os.path.join("Exports")

        print('Image Path :', path)
        return host, path, outPath

    @staticmethod
    def data_separation(data: list, dividing_percentage: int) -> list:
        """
         Segmenting incoming data

        :param data: data to be processed
        :param dividing_percentage: percentage of data fragmented
        :return: predicted masks
        """
        percentage = int(len(data) / 100 * dividing_percentage)

        for i in range(0, len(data), percentage):
            # Create an index range for l of n items:
            yield data[i:i + percentage]

    @staticmethod
    def take_objects(matchedObjects: list, take: int = 2):

        for i in range(0, len(matchedObjects), take):
            if len(matchedObjects[i:i + take]) % take == 0:
                yield matchedObjects[i:i + take]

    @staticmethod
    def get_exif_information(img_info):
        """
        :param img_info: exif object
        :return: (lat, lon), orientation, (Height, Width), FocalLength, Altitude,
        """
        information = {}
        data = img_info.extract_exif()
        try:
            information["model"] = data["model"]
            information["coordx"] = data["gps"]["latitude"]
            information["coordy"] = data["gps"]["longitude"]
            information["width"] = data["width"]
            information["height"] = data["height"]

            # Focal Length
            fLen_obj = data["gps"]["FocalLength"]
            fLen_str = f"{fLen_obj}"
            fLen_arr = fLen_str.split("/")
            fLen = float(int(fLen_arr[0]) / int(fLen_arr[1]))
            information["FocalLength"] = fLen

            hor_width = data["height"] if data["orientation"] == 1 else data["width"]
            information["orientation"] = hor_width
            # Angle of View
            aFov = np.arctan(hor_width / (2 * fLen)) * (180 / np.pi)
            information["FoV"] = aFov
        except:
            raise Exception(f"Check the image Exif Data some missing values")

        for k, v in information.items():
            if information[k] is None:
                raise Exception(f"{k} is None")
            else:
                pass

        return information

    @staticmethod
    def exif_extractor(img_urls):
        processing_format = {}
        objects_zone = []
        for key, x in enumerate(range(0, len(img_urls) - 1, 1)):
            head_url = img_urls[x]['img_url']
            tail_url = img_urls[x + 1]['img_url']
            r_head = requests.get(
                head_url)
            r_tail = requests.get(
                tail_url)
            img1_exifData = ExifRead(BytesIO(r_head.content), details=True)
            img2_exifData = ExifRead(BytesIO(r_tail.content), details=True)
            img_info_1 = Generator.get_exif_information(img1_exifData)
            img_info_2 = Generator.get_exif_information(img2_exifData)
            img_info_1['key'] = key
            img_info_2['key'] = key + 1
            pointA = (img_info_1["coordx"], img_info_1["coordy"])
            pointB = (img_info_2["coordx"], img_info_2["coordy"])
            try:
                heading = Distance.calculate_initial_compass_bearing(pointA,
                                                                     pointB)  # calculate heading from two images
            except ValueError as v:
                raise Exception(f" {v} : Check the image Exif Data some missing values")

            img_info_1['heading'] = heading
            img_info_2['heading'] = heading
            img_info_1['img_url'] = head_url
            img_info_2['img_url'] = tail_url
            objects_zone.append(img_info_1)
            if len(img_urls) - 1 == x + 1:  # if last indices set: previous heading
                objects_zone.append(img_info_2)

        processing_format["zone"] = objects_zone

        return processing_format
