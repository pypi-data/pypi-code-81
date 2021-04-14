import logging
import os
import yaml

from datetime import date, datetime, timedelta


class Config():

    LOCAL_PATH = '/tmp'

    def __init__(self, config_file=None, logfile=None):
        try:
            #Initialize config parameters
            with open(config_file) as file:
                params = yaml.full_load(file)
            self.access_key = params.get('aws_access_key')
            self.secret_key = params.get('aws_secret_key')
            self.region = params.get('aws_region')
            self.tenant_id = params.get('tenant_id')
            self.datalake = params.get('datalake')
            self.forecast_role = params.get('forecast_role')
            self.dataset_frequency = params.get('deepar_training')[0].get('dataset_frequency')
            self.forecast_horizon = params.get('deepar_training')[1].get('forecast_horizon')
            self.forecast_types = params.get('deepar_training')[2].get('forecast_types')
            self.input_window = params.get('deepar_training')[3].get('input_window')
            self.epochs = params.get('deepar_training')[4].get('epochs')
            self.neurons = params.get('deepar_training')[5].get('neurons')
            self.hidden_layers = params.get('deepar_training')[6].get('hidden_layers')
            self.backtests = params.get('deepar_training')[7].get('backtests')
            self.backtest_horizon = params.get('deepar_training')[8].get('backtest_horizon')
            self.use_location = params.get('deepar_training')[9].get('use_location')
            self.dataset_import_path = params.get('deepar_training')[10].get('dataset_import_path')
            self.backtest_export_path = params.get('deepar_training')[11].get('backtest_export_path')
            self.forecast_export_path = params.get('deepar_prediction')[0].get('forecast_export_path')
            self.results_path = params.get('transform')[0].get('results_path')
            self.logfile = logfile + '_' + datetime.today().strftime("%Y%m%d-%H%M%S") + '.log'
            # Initialize logger
            self.logger = logging.getLogger('__name__')
            self.logger.setLevel(logging.DEBUG)
            self.file_handler = logging.FileHandler(os.path.join(Config.LOCAL_PATH, self.logfile))
            self.file_format = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            self.file_handler.setLevel(logging.DEBUG)
            self.file_handler.setFormatter(self.file_format)
            self.logger.addHandler(self.file_handler)
        except FileNotFoundError as err:
            self.logger.exception(f'Config file not found. Please check entered path: {err}')
            raise
        finally:
            file.close()

