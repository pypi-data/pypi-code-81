# -*- coding: utf-8 -*-
#
#      Copyright (C) 2020 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

from axualclient import ClientConfig
from axualclient.AVROConsumer import AxualAVROConsumer
from axualclient.AVROProducer import AxualAVROProducer
from axualclient.Consumer import AxualConsumer
from axualclient.Producer import AxualProducer

logger = logging.getLogger(__name__)


class AxualClient:

    def __init__(self, client_config: ClientConfig):
        self._config = client_config

    def get_consumer(self,
                     topic_list,
                     config=None,
                     *args, **kwargs):
        return AxualConsumer(client_config=self._config,
                             topic_list=topic_list,
                             config=config,
                             *args, **kwargs)

    def get_producer(self,
                     topic,
                     config=None,
                     *args, **kwargs):
        return AxualProducer(topic=topic,
                             client_config=self._config,
                             config=config,
                             *args, **kwargs)

    def get_avro_consumer(self,
                          topic_list,
                          config=None,
                          from_value_dict=None,
                          from_key_dict=None,
                          *args, **kwargs):
        return AxualAVROConsumer(self._config,
                                 topic_list, config=config,
                                 from_value_dict=from_value_dict,
                                 from_key_dict=from_key_dict,
                                 *args, **kwargs)

    def get_avro_producer(self, topic, schema_value=None,
                          config=None, schema_key=None, key_dict=None, value_dict=None, *args, **kwargs):
        return AxualAVROProducer(self._config,
                                 topic, schema_value=schema_value,
                                 config=config, schema_key=schema_key,
                                 key_dict=key_dict, value_dict=value_dict,
                                 *args, **kwargs)
