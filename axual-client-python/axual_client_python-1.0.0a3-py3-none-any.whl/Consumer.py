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
import threading
from datetime import datetime
from time import sleep

from axualclient.discovery import DiscoveryClient, DiscoveryClientRegistry, BOOTSTRAP_SERVERS_KEY, TIMESTAMP_KEY, \
    DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY
from confluent_kafka import Consumer

from axualclient import patterns, ClientConfig
from axualclient.util import parse_list

logger = logging.getLogger(__name__)

DEFAULT_POLL_SPEED = 0.2


class AxualConsumer(DiscoveryClient):
    """Simple balanced consumer class.
    Implements __iter__ to be able to create a for loop on the consumer
     to iterate through messages: for msg in AxualConsumer. Set pause
     attribute to break from loop.
    Set poll_speed attribute to change the polling speed (default: 0.2 [secs])."""

    def __init__(self,
                 client_config: ClientConfig,
                 topic_list,
                 config: dict = None,
                 *args, **kwargs):
        """
        Instantiate a consumer for Axual. Derives from confluent_kafka
         Consumer class.
        Note that auto-commit is set to False, so received messages must
         be committed by your script's logic.

        Parameters
        ----------
        client_config : ClientConfig
            App config information
        topic_list : str, or list of str
            List of names of the topic(s) to consume from:
                <topicname>
             for example:  ['TopicName', 'OtherTopic']
        config : dict, optional
            Additional configuration properties to set. For options, see
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md`
        *args and **kwargs :
            Other parameters that can be passed to confluent_kafka Consumer.
        """
        self.unresolved_topic_list = parse_list(topic_list)
        self.unresolved_group_id = client_config.application_id
        self.topics = []          # have not been resolved yet
        self._consumer = None
        self.init_config = config
        self.init_args = args
        self.init_kwargs = kwargs

        self.configuration = {
            # bootstrap servers & group.id are not available at this point yet
            'security.protocol': 'SSL',
            'ssl.ca.location': client_config.ssl_config.root_ca_location,
            'ssl.key.location': client_config.ssl_config.private_key_location,
            'ssl.certificate.location': client_config.ssl_config.certificate_location,
        }
        # Append custom consumer config
        if config is not None:
            self.configuration = {**self.configuration, **config}

        self.poll_speed = DEFAULT_POLL_SPEED
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
            # resolve topics and acquire new bootstrap servers
            self.topics = [patterns.resolve_topic(discovery_result, topic) for topic in self.unresolved_topic_list]
            self.configuration['bootstrap.servers'] = discovery_result[BOOTSTRAP_SERVERS_KEY]
            self.configuration['group.id'] = patterns.resolve_group(discovery_result, self.unresolved_group_id)
            logger.debug(f'topics: {self.topics} {BOOTSTRAP_SERVERS_KEY}')
            logger.debug(f'group.id: {self.configuration["group.id"]}')
            logger.debug(f'bootstrap.servers: {self.configuration[BOOTSTRAP_SERVERS_KEY]}')

            # Switch consumer
            if self.initialized:
                assignment = self._consumer.assignment()
                # sleep(self.poll_speed)  # Wait outstanding polls before closing consumer
                self._consumer.close()

                # Calculate switch time-out
                if len(assignment) > 0:
                    if self._is_at_least_once():
                        switch_timeout = int(discovery_result['ttl'])
                    else:
                        switch_timeout = max(int(discovery_result[DISTRIBUTOR_TIMEOUT_KEY]) *
                                             int(discovery_result[DISTRIBUTOR_DISTANCE_KEY]) -
                                             (datetime.utcnow() -
                                              discovery_result[TIMESTAMP_KEY]).total_seconds() * 1000,
                                             int(discovery_result['ttl']))
                    sleep(switch_timeout / 1000)

            self._consumer = Consumer(self.configuration, *self.init_args, **self.init_kwargs)
            self._consumer.subscribe(self.topics)
            self.initialized = True

    def _is_at_least_once(self) -> bool:
        return self.configuration.get('auto.offset.reset') in ['earliest', 'smallest', 'begin', 'start']

    def __iter__(self):
        """Continuously loop through messages until self.pause is set to True"""
        self.pause = False
        while not self.pause:
            msg = self.poll(self.poll_speed)
            yield msg

    # Kafka Consumer interface
    def assign(self, partitions, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.assign(partitions, *args, **kwargs)
        )

    def assignment(self, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.assignment(*args, **kwargs)
        )

    def close(self, *args, **kwargs):
        DiscoveryClientRegistry.deregister_client(self.unresolved_group_id)
        return self.do_with_switch_lock(
            lambda: self._consumer.close(*args, **kwargs)
        )

    def commit(self, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.commit(*args, **kwargs)
        )

    def committed(self, partitions, timeout=None):
        return self.do_with_switch_lock(
            lambda: self._consumer.committed(partitions, timeout)
        )

    def consume(self, num_messages=1, *args,
                **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.consume(num_messages, *args, **kwargs)
        )

    def consumer_group_metadata(self):
        return self.do_with_switch_lock(
            lambda: self._consumer.consumer_group_metadata()
        )

    def get_watermark_offsets(self, partition, timeout=None, *args,
                              **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.get_watermark_offsets(partition, timeout, *args, **kwargs)
        )

    def list_topics(self, topic=None, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.assign(topic, *args, **kwargs)
        )

    def offsets_for_times(self, partitions, timeout=None):
        return self.do_with_switch_lock(
            lambda: self._consumer.assign(partitions, timeout)
        )

    def pause(self, partitions):
        return self.do_with_switch_lock(
            lambda: self._consumer.pause(partitions)
        )

    def poll(self, timeout=-1):
        return self.do_with_switch_lock(
            lambda: self._consumer.poll(timeout=timeout)
        )

    def position(self, partitions):
        return self.do_with_switch_lock(
            lambda: self._consumer.position(partitions)
        )

    def resume(self, partitions):
        return self.do_with_switch_lock(
            lambda: self._consumer.resume(partitions)
        )

    def seek(self, partition):
        return self.do_with_switch_lock(
            lambda: self._consumer.seek(partition)
        )

    def store_offsets(self, message=None, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.store_offsets(message, *args, **kwargs)
        )

    def subscribe(self, topics, on_assign=None, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.subscribe(topics, on_assign, *args, **kwargs)
        )

    def unassign(self, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.unassign(*args, **kwargs)
        )

    def unsubscribe(self, *args, **kwargs):
        return self.do_with_switch_lock(
            lambda: self._consumer.unsubscribe(*args, **kwargs)
        )
