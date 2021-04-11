from typing import List, Callable
from enum import Enum
import asyncio
from collections import defaultdict


class Events(Enum):
    ANY = 0
    ON_START = 1
    ON_STOP = 2
    ON_SOMEONE_SUBSCRIBE = 3
    ON_SOMEONE_UNSUBSCRIBE = 4


class AbstractEventObserver(EventReceiver):
    def on_event(self, event, *args, **kwargs):
        pass

    async def on_event_async(self, event, *args, **kwargs):
        pass


class ObserverFunctionWrapper(AbstractEventObserver):
    def __init__(self, func: Callable):
        self.__func = func
        self.__is_async = asyncio.iscoroutinefunction(func)

    @property
    def func(self) -> Callable:
        return self.__func

    @property
    def is_async(self) -> bool:
        return self.__is_async

    def on_event(self, event, *args, **kwargs):
        if not self.__is_async:
            self.__func(event, *args, **kwargs)

    async def on_event_async(self, event, *args, **kwargs):
        if self.__is_async:
            await self.__func(event, *args, **kwargs)


class AbstractEventProvider:
    def subscribe(self, event, observer: AbstractEventObserver):
        pass

    def unsubscribe(self, event, observer: AbstractEventObserver):
        pass

    def unsubscribe_all(self, observer: AbstractEventObserver):
        pass

    def get_events(self) -> list:
        pass

    def get_observers(self) -> List[AbstractEventObserver]:
        pass

    def get_observers_by_event(self, event) -> List[AbstractEventObserver]:
        pass

    def clear(self):
        pass


class BaseEventProvider(AbstractEventProvider, AbstractEventObserver):
    def __init__(self):
        self._events_to_observers = defaultdict(list)

    def on_event(self, event, *args, **kwargs):
        observers: List[AbstractEventObserver] = self._events_to_observers[event]
        if len(observers) < 1:
            del self._events_to_observers[event]
            return
        for observer in observers:
            observer.on_event(event, *args, **kwargs)

    async def on_event_async(self, event, *args, **kwargs):
        observers: List[AbstractEventObserver] = self._events_to_observers[event]
        if len(observers) < 1:
            del self._events_to_observers[event]
            return
        for observer in observers:
            await observer.on_event_async(event, *args, **kwargs)

    def subscribe(self, event, observer: AbstractEventObserver):
        if observer in self._events_to_observers[event]:
            if len(self._events_to_observers[event]) < 1:
                del self._events_to_observers[event]
            return
        self._events_to_observers[event].append(observer)

    def unsubscribe(self, event, observer: AbstractEventObserver):
        if observer in self._events_to_observers[event]:
            self._events_to_observers[event].remove(observer)
        if len(self._events_to_observers[event]) < 1:
            del self._events_to_observers[event]

    def unsubscribe_all(self, observer: AbstractEventObserver):
        for event in self.get_events_by_observer(observer):
            self.unsubscribe(event, observer)

    def subscribe_function(self, event, func: Callable):
        observer = ObserverFunctionWrapper(func)
        self.subscribe(event, observer)

    def sub(self, event):
        def decorator(func: Callable):
            self.subscribe_function(event, func)
            return func
        return decorator

    def get_events(self) -> list:
        return self._events_to_observers.keys()

    def get_events_by_observer(self, observer: AbstractEventObserver) -> list:
        ret = []
        for event, observers in self._events_to_observers.items():
            if observer in observers:
                ret.append(event)
        return ret

    def get_observers(self) -> List[AbstractEventObserver]:
        ret = []
        for observers in self._events_to_observers.values():
            for observer in observers:
                if observer not in ret:
                    ret.append(observer)
        return ret

    def get_observers_by_event(self, event) -> List[AbstractEventObserver]:
        return self._events_to_observers[event]

    def clear(self):
        self._events_to_observers = defaultdict(list)
