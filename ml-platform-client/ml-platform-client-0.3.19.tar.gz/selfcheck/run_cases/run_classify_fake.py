from selfcheck.algorithm_type import AlgorithmType
from selfcheck.config import SelfCheckConfig, TrainConfig, PredictConfig
from selfcheck.self_check_runner import SelfCheckRunner

if __name__ == '__main__':
    config = SelfCheckConfig(host='127.0.0.1', algorithm_name='fake_alg', algorithm_port=5002,
                             algorithm_offline_port=5002,
                             algorithm_type=AlgorithmType.text_classification,
                             minio_host='172.16.99.29',
                             minio_access_key='24WTCKX23M0MRI6BA72Y',
                             minio_secret_key='6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX')

    train_config = TrainConfig(data_path='../static/classify_train.csv')
    predict_config = PredictConfig(features={'sentence': '什么情况下，需要进行居家隔离'})

    task_runner = SelfCheckRunner(config)
    task_runner.run_all(train_config, predict_config)
