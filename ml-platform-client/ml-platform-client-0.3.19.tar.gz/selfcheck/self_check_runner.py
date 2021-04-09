import json

from selfcheck.algorithm_type import AlgorithmType
from selfcheck.config import SelfCheckConfig, TrainConfig, PredictConfig
from selfcheck.constant import APP_ID_KEY
from selfcheck.executor.train_executor import TrainExecutor
from selfcheck.executor.predict_executor import PredictExecutor
from selfcheck.executor.unload_executor import UnloadExecutor
from selfcheck.executor.load_executor import LoadExecutor
from selfcheck.executor.status_executor import StatusExecutor


class SelfCheckRunner:
    def __init__(self, config: SelfCheckConfig):
        self.config = config
        self.config.validate()

    def run_train(self, train_config: TrainConfig):
        model_id = self._execute_train(train_config)
        print('train started, model_id: {}'.format(model_id))
        print()

        self._execute_status(model_id, train_config.extend.get(APP_ID_KEY, None))
        print('train done')
        print()
        return model_id

    def run_predict(self, model_id: str, predict_config: PredictConfig):
        # self._execute_load(model_id, predict_config)
        # print('load done')
        # print()

        predictions = self._execute_predict(model_id, predict_config)
        print('prediction done:')
        print(json.dumps(predictions, ensure_ascii=False, indent=4))
        self.validate_prediction(predictions)
        print()

        # self._execute_unload(model_id, predict_config)
        # print('unload done')
        # print()

    def run_all(self, train_config: TrainConfig, predict_config: PredictConfig):
        model_id = self.run_train(train_config)
        self.run_predict(model_id, predict_config)

    def _execute_train(self, train_config: TrainConfig):
        return self._execute(TrainExecutor(self.config, train_config))

    def _execute_status(self, model_id, app_id):
        return self._execute(StatusExecutor(self.config, model_id, app_id))

    def _execute_load(self, model_id, predict_config):
        return self._execute(LoadExecutor(self.config, model_id, predict_config.extend))

    def _execute_predict(self, model_id, predict_config: PredictConfig):
        return self._execute(PredictExecutor(self.config, model_id, predict_config))

    def _execute_unload(self, model_id, predict_config):
        return self._execute(UnloadExecutor(self.config, model_id, predict_config.extend))

    @staticmethod
    def _execute(executor):
        executor.prepare()
        return executor.execute()

    def validate_prediction(self, predictions):
        if self.config.algorithm_type == AlgorithmType.text_classification or self.config.algorithm_type == AlgorithmType.text_generation:
            self.validate_text_classification(predictions)

        if self.config.algorithm_type == AlgorithmType.text_sequence_labeling:
            self.validate_text_sequence_labelilng(predictions)

        if self.config.algorithm_type == AlgorithmType.text_cluster:
            self.validate_text_cluster(predictions)

        if self.config.algorithm_type == AlgorithmType.relation_extraction:
            self.validate_relation_extraction(predictions)

    def validate_text_cluster(self, predictions):
        assert isinstance(predictions, list)
        for prediction in predictions:
            assert 'score' in prediction
            self.validate_score(prediction['score'])

            assert 'cluster_name' in prediction
            assert isinstance(prediction['cluster_name'], str)

            assert 'cluster' in prediction
            assert isinstance(prediction['cluster'], list)
            for cluster in prediction['cluster']:
                assert isinstance(cluster, str)

            if 'other_info' in prediction:
                self.validate_other_info(prediction['other_info'])

    def validate_text_sequence_labelilng(self, predictions):
        assert isinstance(predictions, list)
        for prediction in predictions:
            assert 'score' in prediction
            self.validate_score(prediction['score'])

            assert 'entity_list' in prediction
            assert isinstance(prediction['entity_list'], list)

            entity = prediction['entity_list'][0]
            assert 'name' in entity
            assert isinstance(entity['name'], str)

            assert 'start_pos' in entity
            assert isinstance(entity['start_pos'], int)

            assert 'end_pos' in entity
            assert isinstance(entity['end_pos'], int)

            assert 'label' in entity
            assert isinstance(entity['label'], str)

            assert 'score' in entity
            assert self.validate_score(entity['score'])

    def validate_text_classification(self, predictions):
        assert isinstance(predictions, list)
        for prediction in predictions:
            assert 'label' in prediction
            assert isinstance(prediction['label'], str)

            assert 'score' in prediction
            self.validate_score(prediction['score'])

            if 'other_info' in prediction:
                self.validate_other_info(prediction['other_info'])

    def validate_relation_extraction(self, predictions):
        assert isinstance(predictions, list)
        for prediction in predictions:
            assert 'score' in prediction
            assert self.validate_score(prediction['score'])

            assert 'subject' in prediction
            self.validate_entity(prediction['subject'])

            assert 'object' in prediction
            self.validate_entity(prediction['object'])

            assert 'predicate' in prediction
            self.validate_predicate(prediction['predicate'])

    def validate_predicate(self, predicate):
        assert 'text' in predicate
        assert isinstance(predicate['text'], str)

        assert 'mention' in predicate
        assert isinstance(predicate['mention'], list)
        for mention in predicate['mention']:
            assert 'text' in mention
            assert isinstance(mention['text'], str)

            assert 'start' in mention
            assert isinstance(mention['start'], int)

            assert 'end' in mention
            assert isinstance(mention['end'], int)

            if 'pos' in mention:
                assert isinstance(mention['pos'], list)

        if 'property' in predicate:
            assert isinstance(predicate['property'], list)
            for prop in predicate['property']:
                assert 'label' in prop
                assert isinstance(prop['label'], str)

                assert 'value' in prop
                assert isinstance(prop['value'], list)

                for value in prop['value']:
                    assert 'text' in value
                    assert isinstance(value['text'], str)

                    assert 'start' in value
                    assert isinstance(value['start'], int)

                    assert 'end' in value
                    assert isinstance(value['end'], int)

                    if 'pos' in value:
                        assert isinstance(value['pos'], str)

    def validate_entity(self, entity):
        assert 'name' in entity
        assert isinstance(entity['name'], str)

        assert 'start' in entity
        assert isinstance(entity['start'], int)

        assert 'end' in entity
        assert isinstance(entity['end'], int)

        if 'pos' in entity:
            assert isinstance(entity['pos'], str)

        assert 'label' in entity
        assert isinstance(entity['label'], str)

    def validate_other_info(self, other_infos):
        assert isinstance(other_infos, list)
        for other_info in other_infos:
            assert 'key' in other_info
            assert isinstance(other_info['key'], str)

            assert 'value' in other_info

    def validate_score(self, score):
        return isinstance(score, float) or isinstance(score, int)
