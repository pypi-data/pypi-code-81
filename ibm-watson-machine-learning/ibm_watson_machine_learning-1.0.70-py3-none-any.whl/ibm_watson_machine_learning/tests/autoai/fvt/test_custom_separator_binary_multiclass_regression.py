import unittest

from lale.operators import TrainablePipeline

from os import environ

from ibm_watson_machine_learning import APIClient

from ibm_watson_machine_learning.experiment import AutoAI
from ibm_watson_machine_learning.deployment import WebService

from ibm_watson_machine_learning.helpers.connections import S3Connection, S3Location, DataConnection, AssetLocation

from ibm_watson_machine_learning.tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, get_env



class TestAutoAIRemote(unittest.TestCase):
    wml_client: 'APIClient' = None
    experiment: 'AutoAI' = None
    remote_auto_pipelines = None
    hyperopt_pipelines = None
    prefix = None
    new_pipeline = None
    wml_credentials = None
    cos_credentials = None
    pipeline_opt = None
    service: 'WebService' = None

    data_dir = './autoai/data/datasets_different_delimeter'
    binary_file_name = 'credit_risk_training_light_different_delimeter.csv'
    multiclass_file_name = 'iris_dataset_different_delimeter.csv'
    regression_file_name = 'insurance_different_delimeter.csv'

    bin_target_column = 'Risk'
    multi_target_column = 'species'
    regression_target_column = 'charges'

    bin_sep = ' '
    multi_sep = ';'
    reg_sep = '\\'

    trained_pipeline_details = None
    run_id = None

    data_connection = None
    results_connection = None

    train_data = None
    holdout_data = None

    cos_endpoint = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    if "BUCKET_NAME" in environ:
        bucket_name = environ['BUCKET_NAME']
    else:
        bucket_name = "wml-autoai-tests-qa"

    data_cos_dir = 'data'

    results_cos_path = 'results_wml_autoai'

    # CP4D CONNECTION DETAILS:

    if is_cp4d():
        space_id = 'bfbd284f-331a-4761-bba9-140b8a594bdc'
        project_id = '94a6074d-48db-4279-bacb-90cd6f3358c7'
    else:  # WML77
        project_id = None
        space_id = None

    best_pipeline: 'Pipeline' = None
    deployed_pipeline = None


    asset_id = None

    @classmethod
    def setUp(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.wml_credentials = get_wml_credentials()
        if not is_cp4d():
            cls.cos_credentials = get_cos_credentials()
            if 'endpoint_url' in cls.cos_credentials:
                cls.cos_endpoint = cls.cos_credentials['endpoint_url']

        cls.wml_client = APIClient(wml_credentials=cls.wml_credentials.copy())

    def test_01_initialize_AutoAI_experiment__pass_credentials__object_initialized(self):
        if is_cp4d():
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials.copy(),
                                                 project_id=self.project_id,
                                                 space_id=self.space_id)
        else:
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials)

        self.assertIsInstance(self.experiment, AutoAI, msg="Experiment is not of type AutoAI.")

    # BINARY OPTIMIZER #

    def test_02__binary__save_remote_data_and_DataConnection_setup(self):
        if is_cp4d():
            self.wml_client.set.default_project(self.project_id)
            asset_details = self.wml_client.data_assets.create(
                name=self.binary_file_name,
                file_path='/'.join([self.data_dir, self.binary_file_name]))
            asset_id = asset_details['metadata']['guid']

            TestAutoAIRemote.data_connection = DataConnection(
                                location=AssetLocation(asset_id=asset_id))
            TestAutoAIRemote.results_connection = None

        else: #for cloud and COS
            TestAutoAIRemote.data_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path='/'.join([self.data_cos_dir, self.binary_file_name]))
            )
            TestAutoAIRemote.results_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.results_cos_path)
            )
            TestAutoAIRemote.data_connection.write(data='/'.join([self.data_dir, self.binary_file_name]),
                                                   remote_name='/'.join([self.data_cos_dir, self.binary_file_name]))

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)

    def test_03__binary__initialize_optimizer(self):
        from ibm_watson_machine_learning.experiment.autoai.optimizers import RemoteAutoPipelines

        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.binary_file_name.split('.')[0],
            prediction_type=AutoAI.PredictionType.BINARY,
            prediction_column=self.bin_target_column,
            scoring=AutoAI.Metrics.ROC_AUC_SCORE,
            csv_separator=self.bin_sep
        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    def test_04__binary__get_configuration_parameters_of_remote_auto_pipeline(self):
        parameters = self.remote_auto_pipelines.get_params()
        print(parameters)
        self.assertIsInstance(parameters, dict, msg='Config parameters are not a dictionary instance.')

    def test_05__binary__fit_run_training_of_auto_ai_in_wml(self):
        TestAutoAIRemote.trained_pipeline_details = self.remote_auto_pipelines.fit(
            training_data_reference=[self.data_connection],
            training_results_reference=self.results_connection,
            background_mode=False)

        TestAutoAIRemote.run_id = self.trained_pipeline_details['metadata']['id']

        self.assertIsNotNone(self.data_connection.auto_pipeline_params,
                             msg='DataConnection auto_pipeline_params was not updated.')

        TestAutoAIRemote.train_data, TestAutoAIRemote.holdout_data = self.remote_auto_pipelines.get_data_connections()[0].read(with_holdout_split=True)

        print("train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)
        print("holdout data sample:")
        print(self.holdout_data.head())
        self.assertGreater(len(self.holdout_data), 0)


    def test_06__binary__get_pipeline__load_lale_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.best_pipeline = self.remote_auto_pipelines.get_pipeline()
        print(f"Fetched pipeline type: {type(self.best_pipeline)}")

        self.assertIsInstance(self.best_pipeline, TrainablePipeline,
                              msg="Fetched pipeline is not of TrainablePipeline instance.")
        predictions = self.best_pipeline.predict(
            X=self.holdout_data.drop([self.bin_target_column], axis=1).values[:5])
        print(predictions)

        self.assertGreater(len(predictions), 0)


    # MULTICLASS #

    def test_07__multiclass__save_remote_data_and_DataConnection_setup(self):
        if is_cp4d():
            self.wml_client.set.default_project(self.project_id)
            asset_details = self.wml_client.data_assets.create(
                name=self.multiclass_file_name,
                file_path='/'.join([self.data_dir, self.multiclass_file_name]))
            asset_id = asset_details['metadata']['guid']

            TestAutoAIRemote.data_connection = DataConnection(
                                location=AssetLocation(asset_id=asset_id))
            TestAutoAIRemote.results_connection = None

        else: #for cloud and COS
            TestAutoAIRemote.data_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path='/'.join([self.data_cos_dir, self.multiclass_file_name]))
            )
            TestAutoAIRemote.results_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.results_cos_path)
            )
            TestAutoAIRemote.data_connection.write(data='/'.join([self.data_dir, self.multiclass_file_name]),
                                                   remote_name='/'.join([self.data_cos_dir, self.multiclass_file_name]))

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)

    def test_08__multiclass__initialize_optimizer(self):
        from ibm_watson_machine_learning.experiment.autoai.optimizers import RemoteAutoPipelines

        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.binary_file_name.split('.')[0],
            prediction_type=AutoAI.PredictionType.MULTICLASS,
            prediction_column=self.multi_target_column,
            scoring=AutoAI.Metrics.ACCURACY_SCORE,
            csv_separator=self.multi_sep
        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    def test_09__multiclass__get_configuration_parameters_of_remote_auto_pipeline(self):
        parameters = self.remote_auto_pipelines.get_params()
        print(parameters)
        self.assertIsInstance(parameters, dict, msg='Config parameters are not a dictionary instance.')

    def test_10__multiclass__fit_run_training_of_auto_ai_in_wml(self):
        TestAutoAIRemote.trained_pipeline_details = self.remote_auto_pipelines.fit(
            training_data_reference=[self.data_connection],
            training_results_reference=self.results_connection,
            background_mode=False)

        TestAutoAIRemote.run_id = self.trained_pipeline_details['metadata']['id']

        self.assertIsNotNone(self.data_connection.auto_pipeline_params,
                             msg='DataConnection auto_pipeline_params was not updated.')

        TestAutoAIRemote.train_data, TestAutoAIRemote.holdout_data = self.remote_auto_pipelines.get_data_connections()[0].read(with_holdout_split=True)

        print("train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)
        print("holdout data sample:")
        print(self.holdout_data.head())
        self.assertGreater(len(self.holdout_data), 0)

    def test_11__multiclass__get_pipeline__load_lale_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.best_pipeline = self.remote_auto_pipelines.get_pipeline()
        print(f"Fetched pipeline type: {type(self.best_pipeline)}")

        self.assertIsInstance(self.best_pipeline, TrainablePipeline,
                              msg="Fetched pipeline is not of TrainablePipeline instance.")
        predictions = self.best_pipeline.predict(
            X=self.holdout_data.drop([self.multi_target_column], axis=1).values[:5])
        print(predictions)

        self.assertGreater(len(predictions), 0)

    # REGRESSION #

    def test_12__regression__save_remote_data_and_DataConnection_setup(self):
        if is_cp4d():
            self.wml_client.set.default_project(self.project_id)
            asset_details = self.wml_client.data_assets.create(
                name=self.regression_file_name,
                file_path='/'.join([self.data_dir, self.regression_file_name]))
            asset_id = asset_details['metadata']['guid']

            TestAutoAIRemote.data_connection = DataConnection(
                location=AssetLocation(asset_id=asset_id))
            TestAutoAIRemote.results_connection = None

        else:  # for cloud and COS
            TestAutoAIRemote.data_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path='/'.join([self.data_cos_dir, self.regression_file_name]))
            )
            TestAutoAIRemote.results_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.results_cos_path)
            )
            TestAutoAIRemote.data_connection.write(data='/'.join([self.data_dir, self.regression_file_name]),
                                                   remote_name='/'.join([self.data_cos_dir, self.regression_file_name]))

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)

    def test_13__regression__initialize_optimizer(self):
        from ibm_watson_machine_learning.experiment.autoai.optimizers import RemoteAutoPipelines

        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.binary_file_name.split('.')[0],
            prediction_type=AutoAI.PredictionType.REGRESSION,
            prediction_column=self.regression_target_column,
            scoring=AutoAI.Metrics.ROOT_MEAN_SQUARED_ERROR,
            csv_separator=self.reg_sep
        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    def test_14__regression__get_configuration_parameters_of_remote_auto_pipeline(self):
        parameters = self.remote_auto_pipelines.get_params()
        print(parameters)
        self.assertIsInstance(parameters, dict, msg='Config parameters are not a dictionary instance.')

    def test_15__regression__fit_run_training_of_auto_ai_in_wml(self):
        TestAutoAIRemote.trained_pipeline_details = self.remote_auto_pipelines.fit(
            training_data_reference=[self.data_connection],
            training_results_reference=self.results_connection,
            background_mode=False)

        TestAutoAIRemote.run_id = self.trained_pipeline_details['metadata']['id']

        self.assertIsNotNone(self.data_connection.auto_pipeline_params,
                             msg='DataConnection auto_pipeline_params was not updated.')

        TestAutoAIRemote.train_data, TestAutoAIRemote.holdout_data = self.remote_auto_pipelines.get_data_connections()[
            0].read(with_holdout_split=True)

        print("train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)
        print("holdout data sample:")
        print(self.holdout_data.head())
        self.assertGreater(len(self.holdout_data), 0)

    def test_16__regression__get_pipeline__load_lale_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.best_pipeline = self.remote_auto_pipelines.get_pipeline()
        print(f"Fetched pipeline type: {type(self.best_pipeline)}")

        self.assertIsInstance(self.best_pipeline, TrainablePipeline,
                              msg="Fetched pipeline is not of TrainablePipeline instance.")
        predictions = self.best_pipeline.predict(
            X=self.holdout_data.drop([self.regression_target_column], axis=1).values[:5])
        print(predictions)

        self.assertGreater(len(predictions), 0)