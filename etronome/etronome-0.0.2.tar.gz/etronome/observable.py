from typing import Generic, Protocol, TypeVar

T = TypeVar('T')
S = TypeVar('S', contravariant=True)


class Observer(Protocol[S]):
    def update_(self, value: S) -> None:
        ...


class Observable(Generic[T]):
    def __init__(self, observers: str) -> None:
        self.observers = observers

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __set__(self, instance: object, value: T) -> None:
        instance.__dict__[self.name] = value
        observers = instance.__dict__[self.observers]
        for observer in observers:
            observer.update_(value)

    def __get__(self, instance: object, owner: type = None) -> T:
        return instance.__dict__[self.name]
