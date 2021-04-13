import os, sys
import hashlib

sys.path.append(os.path.dirname(__file__) + os.sep + './')

from metadata import MetaData
from labeldata import LabelData
from utils import util

class File():
    def __init__(self, filepath, basepath, datasetName):
        self.metadata = {}
        self.labeldata = LabelData()
        self.datasetName = datasetName
        if basepath == "":
            self.objectPath = os.path.basename(filepath)
            self.osspath = datasetName + "/" + os.path.basename(filepath)
        else:
            basepath = basepath.rstrip("/")
            if filepath.find(basepath) < 0:
                raise Exception(f"basepath must be part of filepath!")
            self.osspath = datasetName + "/" + filepath.split(basepath + "/")[1]
            self.objectPath = filepath.split(basepath + "/")[1]

        self.referId = ""
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.md5 = util.getFileMd5(self.filepath)
        self.filesize = int(util.getFileSize(self.filepath))
        self.type = util.getFiletype(self.filepath)

        with open(self.filepath, "rb") as bf:
            file_md5 = hashlib.md5(bf.read())
            self.md5 = file_md5.hexdigest()

    #数据自查
    def SelfCheck(self):
        if not self.referId:
            raise Exception(f"referid must be setted!")


    def AddmetaData(self, madedata):
        self.metadata = MetaData(madedata)

    def AddReferId(self, ref_id):
        if ref_id == "":
            raise Exception(f"referId can not be empty string!")
        self.referId = ref_id

    #添加box
    def AddBox2D(self, box2d, label="", instance="", attrs={}):
        # 数据格式检查
        if not type(box2d) is dict:
            raise Exception(f"box must be a dict, {type(box2d)} gavin")

        keys = list(set(box2d.keys()))
        keys.sort()
        if keys != ['height', 'width', 'x', 'y']:
            raise Exception(f"box keys must be ['height', 'width', 'x', 'y'], {type(box2d)} gavin")

        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="box2d", data=box2d)

    #添加椭圆
    def AddEllipse(self, ellipse, label="", instance="", attrs={}):
        if not type(ellipse) is dict:
            raise Exception(f"box must be a dict, {type(ellipse)} gavin")

        keys = list(set(ellipse.keys()))
        keys.sort()
        if keys != ['height', 'width', 'x', 'y']:
            raise Exception(f"ellipse keys must be ['height', 'width', 'x', 'y'], {type(ellipse)} gavin")

        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="ellipse", data=ellipse)

    def AddPolygon(self, polygon, label="", instance="", attrs={}):
        if not type(polygon) is list:
            raise Exception(f"polygon must be a list, {type(polygon)} gavin")

        for poly in polygon:
            keys = list(set(poly.keys()))
            if keys != ["x", "y"]:
                raise Exception(f"poly point keys must be ['x', 'y'], {poly} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="polygon", data=polygon)


    def AddLine(self, line, label="", instance="", attrs={}):
        if not type(line) is list:
            raise Exception(f"polygon must be a list, {type(line)} gavin")

        for point in line:
            keys = list(set(point.keys()))
            if keys != ["x", "y"]:
                raise Exception(f"line point keys must be ['x', 'y'], {point} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="line", data=point)


    def AddCurve(self, curve, label="", instance="", attrs={}):
        if not type(curve) is list:
            raise Exception(f"polygon must be a list, {type(curve)} gavin")

        for point in curve:
            keys = list(set(point.keys()))
            if keys != ["x", "y"]:
                raise Exception(f"curve point keys must be ['x', 'y'], {point} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="curve", data=curve)

    def AddPoint(self, point, label="", instance="", attrs={}):
        if not type(point) is dict:
            raise Exception(f"curve must be a list, {type(point)} gavin")

        keys = list(set(point.keys()))
        if keys != ["x", "y"]:
            raise Exception(f"curve point keys must be ['x', 'y'], {point} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="poit", data=point)


    def AddParalle(self, paralle, label="", instance="", attrs={}):
        if not type(paralle) is list:
            raise Exception(f"paralle must be a list, {type(paralle)} gavin")

        if len(paralle) != 4:
            raise Exception(f"paralle points numbers must be 4, {len(paralle)} gavin")

        for point in paralle:
            keys = list(set(point.keys()))
            if keys != ["x", "y"]:
                raise Exception(f"paralle point keys must be ['x', 'y'], {point} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="paralle", data=paralle)



