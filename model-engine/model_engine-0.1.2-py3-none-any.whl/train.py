from typing import Dict, Any, Tuple, Optional, Union, List

import tensorflow as tf


# XXX: Depends on usage in other models; may be unnecessary
class TrainingConfigProvider(object):
    def get_config(self) -> Dict[str, Any]:
        pass

    def __getitem__(self, item):
        pass


class TrainingDataProvider(object):
    def training_data(self, config) -> Tuple[tf.data.Dataset, Optional[tf.data.Dataset]]:
        pass


class BaseModelTrain(object):
    def train(self, data_provider: TrainingDataProvider, config_provider: Union[TrainingConfigProvider, dict],
              callbacks: Optional[List[tf.keras.callbacks.Callback]]):
        pass
