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
import os
import threading
from datetime import datetime
from time import sleep

from axualclient.discovery import DiscoveryClient, BOOTSTRAP_SERVERS_KEY, TIMESTAMP_KEY, DiscoveryClientRegistry, \
    SCHEMA_REGISTRY_URL_KEY, DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

from axualclient import patterns, ClientConfig

logger = logging.getLogger(__name__)


class AxualAVROProducer(DiscoveryClient):

    def __init__(self,
                 client_config: ClientConfig,
                 topic: str,
                 schema_value: str,
                 config: dict = None,
                 schema_key: str = None,
                 value_dict: dict = None,
                 key_dict: dict = None,
                 *args, **kwargs):
        """
        Instantiate an AVRO producer for Axual. The _producer attribute is
         the confluent_kafka SerializingProducer class.

        Parameters
        ----------
        client_config : ClientConfig
            App config information
        topic : str
            Name of the topic to produce to:  <topicname>, for
             example:  TopicName
        schema_value : str
            AVRO schema to use to serialize value, either the AVSC string, or
             a path to the AVSC file containing the schema.
        config : dict, optional
            Additional configuration properties to set. For options, see
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        schema_key : str, optional
            AVRO schema to use to serialize value, either the AVSC string, or
             a path to the AVSC file containing the schema. The default assumes
             no AVRO schema, and serializes as string.
        *args and **kwargs :
            Other parameters that can be passed to confluent_kafka Producer.

        """
        self._producer = None                    # has not received discovery result yet
        self.topic = None                        # has not been resolved yet
        self._schema_registry_client = None      # no url available yet
        self.unresolved_topic = topic
        self.client_config = client_config
        self.init_config = config

        self.init_schema_key = schema_key
        self.init_schema_value = schema_value
        self.key_dict = key_dict
        self.value_dict = value_dict

        self.init_args = args
        self.init_kwargs = kwargs

        self.configuration = {
            # bootstrap servers & key/value serializers are not available at this point yet
            'security.protocol': 'SSL',
            'ssl.ca.location': client_config.ssl_config.root_ca_location,
            'ssl.key.location': client_config.ssl_config.private_key_location,
            'ssl.certificate.location': client_config.ssl_config.certificate_location
        }
        # Append custom producer config
        if config is not None:
            self.configuration = {**self.configuration, **config}

        self.initialized = False
        self.discovery_fetcher = DiscoveryClientRegistry.register_client(
            client_config, self
        )
        self.switch_lock = threading.Lock()
        self.init_lock = threading.Lock()

    def wait_for_initialization(self) -> None:
        if self.initialized:
            return
        with self.init_lock:
            self.discovery_fetcher.wait_for_discovery_result()

    def do_with_switch_lock(self, func):
        self.wait_for_initialization()
        with self.switch_lock:
            return func()

    def on_discovery_properties_changed(self, discovery_result: dict) -> None:
        """ A new discovery result has been received, need to switch """
        with self.switch_lock:
            # resolve topic and acquire new bootstrap servers
            self.topic = patterns.resolve_topic(discovery_result, self.unresolved_topic)
            logger.debug(
                f'Topic: {self.unresolved_topic} bootstrap.servers: {discovery_result[BOOTSTRAP_SERVERS_KEY]}'
            )
            self.configuration['bootstrap.servers'] = discovery_result[BOOTSTRAP_SERVERS_KEY]

            # initialize serializers against new schema registry
            self._schema_registry_client = SchemaRegistryClient(
                {
                    'url': discovery_result[SCHEMA_REGISTRY_URL_KEY],
                    'ssl.ca.location': self.client_config.ssl_config.root_ca_location
                }
            )
            self.configuration['key.serializer'] = self._create_key_serializer()
            self.configuration['value.serializer'] = self._create_value_serializer()

            # Switch producer
            if self.initialized:
                self._producer.flush()

                # Calculate switch time-out
                # The default is NOT KEEPING_ORDER
                switch_timeout = 0
                if self.configuration.get('max.in.flight.requests.per.connection') in [1, '1']:
                    # Strategy is KEEPING_ORDER
                    switch_timeout = (int(discovery_result[DISTRIBUTOR_TIMEOUT_KEY]) *
                                      int(discovery_result[DISTRIBUTOR_DISTANCE_KEY]) -
                                      (datetime.utcnow() - discovery_result[TIMESTAMP_KEY]).total_seconds() * 1000)
                sleep(switch_timeout / 1000)

            self._producer = SerializingProducer(self.configuration, *self.init_args, **self.init_kwargs)
            self.initialized = True

    def _create_key_serializer(self):
        if self.init_schema_key is not None:
            if os.path.isfile(self.init_schema_key):
                with open(self.init_schema_key, 'r') as f:
                    schema_key_str = f.read()
            else:
                schema_key_str = self.init_schema_key
            return AvroSerializer(
                schema_registry_client=self._schema_registry_client,
                schema_str=schema_key_str,
                to_dict=self.key_dict,
                # Converts input to dict, but should not be needed when supplying dicts
                conf={'auto.register.schemas': False}
            )
        else:
            return StringSerializer('utf-8')

    def _create_value_serializer(self):
        if os.path.isfile(self.init_schema_value):
            with open(self.init_schema_value, 'r') as f:
                schema_str = f.read()
        else:
            schema_str = self.init_schema_value
        return AvroSerializer(
            schema_registry_client=self._schema_registry_client,
            schema_str=schema_str,
            to_dict=self.value_dict,
            # Converts input to dict, but should not be needed when supplying dicts
            conf={'auto.register.schemas': False}
        )

    def delivery_report(self, err, msg):
        """
        Basic delivery report functionality. Logs to logger, user should
         have instantiated the root logger in their script to catch these
         messages.
        Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush().
        """
        if err is not None:
            logger.error('Message delivery failed: {}'.format(err))
        else:
            logger.debug(f'Message (length {len(msg)}) delivered to {msg.topic()} [{msg.partition()}]')

    def produce(self, *args, callback=None, **kwargs):
        """
        Produce message to topic. Wrapper around confluent_kafka's
         SerializingProducer.produce() method.

        Parameters
        ----------
        callback : function, optional
            Callback function. The default (None) will use the default callback
             as defined by the delivery_report() method in this class.
        *args and **kwargs :
            Arguments to pass to Producer.produce(). value, key, ...

        Returns
        -------
        None.

        """
        self.do_with_switch_lock(
            lambda: self._producer.produce(
                topic=self.topic, *args, on_delivery=self.delivery_report if callback is None else callback, **kwargs)
        )

    # producer interface
    def abort_transaction(self, *args, **kwargs):
        self.do_with_switch_lock(
            lambda: self._producer.abort_transaction(*args, **kwargs)
        )

    def begin_transaction(self, *args, **kwargs):
        self.do_with_switch_lock(
            lambda: self._producer.begin_transaction(*args, **kwargs)
        )

    def commit_transaction(self, *args, **kwargs):
        self.do_with_switch_lock(
            lambda: self._producer.commit_transaction(*args, **kwargs)
        )

    def flush(self, *args, **kwargs) -> int:
        return self.do_with_switch_lock(
            lambda: self._producer.flush(*args, **kwargs)
        )

    def init_transactions(self, *args, **kwargs) -> None:
        self.do_with_switch_lock(
            lambda: self._producer.init_transactions(*args, **kwargs)
        )

    def list_topics(self, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._producer.list_topics(*args, **kwargs)
        )

    def poll(self, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._producer.poll(*args, **kwargs)
        )

    def send_offsets_to_transaction(self, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._producer.send_offsets_to_transaction(*args, **kwargs)
        )

    # obj interface
    def __class__(self, *args, **kwargs):
        return self._producer.__class__(*args, **kwargs)

    def __dict__(self, *args, **kwargs):
        return self._producer.__dict__(*args, **kwargs)

    def __dir__(self, *args, **kwargs):
        return self._producer.__dir__(*args, **kwargs)

    def __doc__(self, *args, **kwargs):
        return self._producer.__doc__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self._producer.__eq__(*args, **kwargs)

    def __format__(self, *args, **kwargs):
        return self._producer.__format__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self._producer.__ge__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self._producer.__gt__(*args, **kwargs)

    def __hash__(self, *args, **kwargs):
        return self._producer.__hash__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self._producer.__le__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._producer.__len__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self._producer.__lt__(*args, **kwargs)

    def __module__(self, *args, **kwargs):
        return self._producer.__module__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self._producer.__ne__(*args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        return self._producer.__reduce__(*args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        return self._producer.__reduce_ex__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self._producer.__repr__(*args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        return self._producer.__sizeof__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self._producer.__str__(*args, **kwargs)

    def __weakref__(self, *args, **kwargs):
        return self._producer.__weakref__(*args, **kwargs)
