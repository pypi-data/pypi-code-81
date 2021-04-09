from selfcheck.algorithm_type import AlgorithmType
from selfcheck.config import SelfCheckConfig, TrainConfig, PredictConfig
from selfcheck.constant import APP_ID_KEY
from selfcheck.self_check_runner import SelfCheckRunner


if __name__ == '__main__':
    config = SelfCheckConfig(host='172.16.99.29', algorithm_name='dialog_act', algorithm_port=10999,
                             algorithm_offline_port=10999,
                             algorithm_url_prefix='/mlp/tagger',
                             algorithm_type=AlgorithmType.text_classification,
                             minio_access_key='24WTCKX23M0MRI6BA72Y',
                             minio_secret_key='6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX')

    extend = {
        APP_ID_KEY: '54735ecc0908434196612c098be61afd'
    }

    train_config = TrainConfig(data_path='./static/classify_train.csv', extend=extend)
    predict_config = PredictConfig(features={'sentence': '什么情况下，需要进行居家隔离'}, extend=extend)

    task_runner = SelfCheckRunner(config)
    task_runner.run_all(train_config, predict_config)
    # task_runner.run_predict('fa4229e111c64943bc83236fe3e5e330', predict_config)
