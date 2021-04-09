import os
import random
import time
import uuid
from os import path

import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from ml_platform_client.algorithm_base import AlgorithmBase, PredictorBase
from ml_platform_client.minio_accessor import MinIOAccessor
from ml_platform_client.logger import log


class MyAlgorithm(AlgorithmBase):

    def train(self, model_id: str, model_path: str, data_config: dict, parameters: dict, extend: dict):
        log.info(f'{model_id} train start')

        # 训练数据路径
        location = data_config['location']

        # 拼接bucket名称，实际使用需要配置成环境变量
        full_location = os.path.join('ml-platform-data', location)

        # 本地文件路径，加上uuid或时间戳避免同时训练时冲突
        data_file_name = 'temp' + str(uuid.uuid4())

        # 从minio路径拉取到本地
        MinIOAccessor.fget_object(full_location, data_file_name)

        # 数据处理
        df = pd.read_csv(data_file_name)
        X = df[['weight', 'height']]
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(df['gender'])

        # 模型定义
        lr = LogisticRegression()

        # 模型训练
        lr.fit(X, y)

        # 保存到磁盘
        local_model_path = model_id
        joblib.dump(lr, local_model_path)

        # 上传到minio，存储桶和路径自行决定
        MinIOAccessor.save_object(local_model_path, os.path.join('your-bucket-name', local_model_path))

        # 删除本地数据文件
        os.remove(data_file_name)

        # 删除本地模型文件
        os.remove(local_model_path)

        log.info(f'{model_id} train done')

    def load(self, model_id: str, model_path: str) -> PredictorBase:

        log.info(f'{model_id} load start')
        # 从minio拉取模型文件
        full_path = path.join('your-bucket-name', model_id)

        # 如果model path中有值，则从model_path路径下载模型文件
        if model_path:
            full_path = model_path

        temp_path = model_id
        MinIOAccessor.fget_object(full_path, temp_path)

        # 加载到内存
        lr = joblib.load(temp_path)
        os.remove(temp_path)

        # 返回predictor对象
        predictor = MyPredictor(lr, model_id)

        log.info(f'{model_id} load done')

        return predictor


class MyPredictor(PredictorBase):

    def __init__(self, model, model_id):
        super().__init__(model)
        self.model_id = model_id

    def predict(self, features: dict, params: dict):
        weight = features['weight']
        height = features['height']
        result = self.model.predict([[weight, height]]).tolist()[0]
        label = None
        if result == 1:
            label = '男'
        if result == 0:
            label = '女'

        prediction = [{'label': label, 'score': 100}]

        log.info(f'{self.model_id} prediction: {prediction}')

        return prediction


class FakeAlgorithm(AlgorithmBase):

    # 如果需要指定model_id，重写这个方法，默认随机生成uuid
    def generate_model_id(self, extend: dict):
        return str(uuid.uuid4()).replace('-', '') + '_' + time.strftime('%Y%m%d%H%M%S', time.localtime())

    def train(self, model_id: str, model_path: str, data_config: dict, parameters: dict, extend: dict):
        # mock训练过程
        time.sleep(random.randint(1, 20))
        if random.randint(1, 10) > 8:
            raise Exception('train fail')

    def load(self, model_id: str, model_path: str) -> PredictorBase:
        # 从minio拉取模型文件
        # 返回predictor对象
        predictor = FakePredictor(None, model_id)
        return predictor


class FakePredictor(PredictorBase):

    def __init__(self, model, other_info):
        super().__init__(model)
        self.other_info = other_info

    def predict(self, features: dict, params: str):
        return [{'label': str(random.randint(0, 10)), 'score': 100}]
