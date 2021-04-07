from typing import Optional
import time
import redis
import struct

from .exceptions import TooLateError, TimeOutError

"""
This is the main module of PyProcSync.
"""


class ProcSync:
    """
    PyProcSync main class.

    An instance of class represents a single "run" with their own Redis connection.
    Each synchronization point (`sync()` calls) is tied to the context of a ProcSync instance with an unique `run_id`.
    """

    def __init__(self, redis_client: redis.Redis, run_id: str = "", delay: float = 1.0):
        """
        Upon creation the appropriate channel is being subscribed to.

        Although the `run_id` is optional it is strongly recommended to be set to a different value at each creation.
        The `run_id` must be the same on all nodes that takes part of the same "run".

        :param redis_client: A `redis.Redis` instance that's connected to a redis server.
        :param run_id: An arbitrary id (str) that identifies this specific run. (Should be unique across all runs and the same on all nodes)
        :param delay: Time spent waiting after the continue time is announced. (Default is 1 sec)
        """

        if type(delay) not in [float, int] or delay <= 0:
            raise ValueError("delay parameter must be a positive float")

        self._delay = delay
        self._nodewait_key_prefix = f"nodewait:{run_id}:"
        self._continue_channel_prefix = f"continue:{run_id}:"

        # setup redis
        self._redis_client = redis_client
        self._redis_pubsub = self._redis_client.pubsub()
        self._redis_pubsub.psubscribe(self._continue_channel_prefix + "*")

    @staticmethod
    def _sleep_until(timestamp: float):
        # Catching the exception is a little faster then checking it with an if (see. perf_tests)
        # (that's what happens internally anyways)
        # But only when there isn't an exception. If the result is negative for some reason,
        # than this is is actually slower
        try:
            time.sleep(timestamp - time.time())  # TODO: use a precision timer
        except ValueError:  # sleep length must be non-negative error
            raise TooLateError(
                """Synchronization time have already expired.
                This could be caused by high network latency or unsynchronized system clocks.
                Try increasing delay."""
            )

    def sync(self, event_name: str, nodes: int, timeout: Optional[float] = None):
        """
        Start waiting for each node (number of nodes specified by `nodes` parameter) to arrive at
        the synchronization point specified by `event_name`.

        WARNING: All parameters of this method MUST BE the same on every node for the same event (including timeout).
        If parameters supplied for this method differ from other nodes, this would not only cause malfunction
        in the current instance but would confuse other nodes waiting for this synchronization point as well!

        If configured properly, this method returns at the same time (according to their system clock) on all nodes.

        Exceptions this method may raise:
          - ValueError: Some parameters are invalid.
          - pyprocsync.TooLateError: Synchronization time already expired when recieved (system clocks not in sync or configured delay lower than network latency)
          - pyprocsync.TimeOutError: (only when timeout is not none) Given up waiting for other nodes.
          - AssertionError: Unexpected values read from Redis.
          - Redis related exceptions (see. pyredis docs).

        :param event_name: The name of the event. This is the same across all nodes that want to synchronize.
        :param nodes: Amount of nodes to sync the event between.
        :param timeout: Maximum time to wait for all nodes to reach the synchronization point defined by event_name in seconds. Set to `None` for infinite wait time. TimeOutError raised when the timeout expire.
        """
        # Do preparations before increasing the counter to
        # minimize time spent between announcing and waiting for announcement

        if (type(nodes) is not int) or (nodes <= 0):
            raise ValueError("nodes parameter must be a positive integer!")

        if timeout and (type(timeout) not in [int, float] or timeout <= 0):
            raise ValueError("timeout parameter must be a positive float!")

        if (not event_name) or (type(event_name) is not str):
            raise ValueError("event_name must be a non-empty string")

        nodewait_key = (self._nodewait_key_prefix + event_name).encode()
        continue_channel = (self._continue_channel_prefix + event_name).encode()

        if timeout:
            deadline = time.time() + timeout
        else:
            deadline = None

        # The real deal
        nodes_waiting = self._redis_client.incr(nodewait_key)

        if nodes_waiting == nodes:
            # this was the last node, announcing continue time
            cont_time = time.time() + self._delay  # each client have _delay seconds to receive sync time and prepare

            # struct packing faster than using strings (see. perf_tests)
            self._redis_client.publish(continue_channel, struct.pack("!d", cont_time))
            self._redis_client.expire(nodewait_key, int(self._delay) + 1)  # Rounding up without ceil()

        elif nodes_waiting > nodes:
            raise AssertionError(
                """The number nodes currently waiting for this event is higher than the nodes attribute!
                This could be caused by the run_id being reused between runs or the nodes parameter may be inconsistent between nodes"""
            )

        else:  # nodes_waiting < nodes
            if timeout:
                # Extend the lifetime to the life of the counter to the maximum timeout
                # Since every node calls this, then the timeout will always reflect the last node's timeout
                # Part of the reason why the timeout must be the same on all nodes
                self._redis_client.expire(nodewait_key, int(timeout) + 1)

        # waiting for continue time to be announced (this will consume the message emitted above as well)
        while True:
            message = self._redis_pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)

            if message and message['channel'] == continue_channel:
                cont_time = struct.unpack("!d", message['data'])[0]  # Using struct is a lot faster than strings
                break

            if deadline and time.time() > deadline:
                raise TimeOutError(
                    """Time out while waiting for all nodes to synchronize.
                    Is it possible that one of the nodes crashed, or did not reach the synchronization point in time.
                    Try increasing the deadline, or set it to None for infinite wait time."""
                )

        # Each node should sleep until the timestamp they agreed on
        self._sleep_until(cont_time)

    def close(self):
        """
        Close Redis connection.
        After calling this method. The instance should not be used anymore.
        """
        self._redis_pubsub.close()
        self._redis_client.close()
