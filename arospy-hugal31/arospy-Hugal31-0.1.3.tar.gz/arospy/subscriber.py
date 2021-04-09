import asyncio
import logging
import rospy
import threading


_logger = logging.getLogger(name="arospy.subscriber")


class Subscriber:
    """
    Async subscriber. Must be created from a coroutine, or the wrong event loop will be used.

    Can be used as an async source (i.e. iterator).
    """

    def __init__(self, name: str,
                 data_class,
                 queue_size=None,
                 buff_size=rospy.topics.DEFAULT_BUFF_SIZE,
                 event_loop=None):
        self.inner = rospy.Subscriber(name,
                                      data_class,
                                      callback=self._on_message,
                                      queue_size=queue_size,
                                      buff_size=buff_size)
        self.queue = asyncio.Queue(maxsize=queue_size if queue_size is not None else 0)
        self.event_loop = event_loop if event_loop is not None else asyncio.get_running_loop()
        self._last_message = None

        _logger.debug(f"Subscriber({name}, {data_class}) created in thread {threading.get_ident()}")

    def __aiter__(self):
        return self

    def __anext__(self):
        return self.get_next_message()

    def unregister(self):
        self.inner.unregister()

    async def get_next_message(self):
        self._last_message = await self.queue.get()
        return self._last_message

    async def get_latest_message(self):
        """Return the last available message, or wait if not was received."""
        if self._last_message is None:
            self._last_message = await self.queue.get()
        return self.get_latest_message_nowait()

    def get_latest_message_nowait(self):
        """Return the last available message for now, or return None"""
        while not self.queue.empty():
            self._last_message = self.queue.get_nowait()
        return self._last_message

    def _on_message(self, message):
        _logger.debug(f"Subscriber({self.inner.name}) received a message in {threading.get_ident()}")
        if self.event_loop.is_closed():
            self.inner.unregister()
            return
        self.event_loop.call_soon_threadsafe(self._put_message, message)

    def _put_message(self, message):
        """Must be called from the EVENT_LOOP.event_loop"""
        _logger.debug(f"Subscriber({self.inner.name}) dispatch a message in {threading.get_ident()}")
        try:
            self.queue.put_nowait(message)
        except asyncio.QueueFull:
            self.queue.get_nowait()
            self.queue.put_nowait(message)
