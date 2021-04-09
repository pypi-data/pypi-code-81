from selfcheck.algorithm_type import AlgorithmType
from selfcheck.config import SelfCheckConfig, TrainConfig, PredictConfig
from selfcheck.self_check_runner import SelfCheckRunner

if __name__ == '__main__':
    config = SelfCheckConfig(host='192.168.3.16', algorithm_name='triplet', algorithm_port=19050,
                             algorithm_url_prefix='/relation',
                             algorithm_type=AlgorithmType.relation_extraction,
                             minio_access_key='24WTCKX23M0MRI6BA72Y',
                             minio_secret_key='6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX')

    predict_config = PredictConfig(features={
        'sentence': '宜家位于印度第四大城市海德拉巴（Hyderabad）的商场将在7月19日开业',
        'entities': []
    })

    task_runner = SelfCheckRunner(config)
    task_runner.run_predict('general', predict_config)
