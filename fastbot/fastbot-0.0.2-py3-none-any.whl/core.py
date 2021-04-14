import abc
from typing import Dict, List, Callable
from fastbot.responses import Request, Response
Handler = Callable[..., Response]


class Dialog(abc.ABC):

    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def get_handler(self) -> Handler:
        raise NotImplemented

    @abc.abstractmethod
    def get_default(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def get_next(self) -> dict:
        raise NotImplemented


class DialogSet(abc.ABC):

    @abc.abstractmethod
    def get_root(self) -> Dialog:
        raise NotImplemented

    @abc.abstractmethod
    def get_dialog(self, name: str) -> Dialog:
        raise NotImplemented

    @abc.abstractmethod
    def add_root(self, handler=None, default_next=None, **kwargs):
        raise NotImplemented

    @abc.abstractmethod
    def add_dialog(self, dialog: Dialog):
        raise NotImplemented


class DataStore(abc.ABC):

    @abc.abstractmethod
    def get(self, session_key) -> dict:
        raise NotImplemented

    @abc.abstractmethod
    def update(self, session_key, **state):
        raise NotImplemented

    @abc.abstractmethod
    def remove(self, session_key):
        raise NotImplemented


class InMemoryDialog(Dialog):
    def __init__(self, name=None, handler=None, default=None, **kwargs):
        self.handler = handler
        self.default = default
        self._next = kwargs
        self.name = name

    def get_name(self) -> str:
        return self.name

    def get_handler(self) -> Handler:
        return self.handler

    def get_default(self) -> str:
        return self.default or self.name

    def get_next(self) -> dict:
        return self._next


class InMemoryDialogSet(DialogSet):
    INITIAL_DIALOGUE = "root"

    def __init__(self):
        self.dialogs: Dict[str, Dialog] = {}

    def add_root(self, handler=None, default=None, **kwargs):
        self.dialogs[self.INITIAL_DIALOGUE] = InMemoryDialog(
            name=self.INITIAL_DIALOGUE,
            handler=handler,
            default=default if default else self.INITIAL_DIALOGUE,
            **kwargs)

    def add_dialog(self, dialog: Dialog):
        self.dialogs[dialog.get_name()] = dialog

    def get_root(self) -> Dialog:
        return self.dialogs[self.INITIAL_DIALOGUE]

    def get_dialog(self, name: str) -> Dialog:
        return self.dialogs[name]


class DialogManager(object):
    DIALOG_ROUTE = "internal_dialog_route"
    RETRY_MESSAGE = "internal_retry_message"

    def __init__(self, data_store: DataStore, dialog_set: DialogSet, **kwargs):
        self.data_store = data_store
        self.dialog_set = dialog_set

    def handle(self, request: Request):
        session: str = request.session
        state: dict = self.data_store.get(session)
        route: str = state.get(self.DIALOG_ROUTE, "")
        last_route = route.split(",")[-1]
        dialog = self.dialog_set.get_dialog(last_route) \
            if last_route else self.dialog_set.get_root()

        if last_route and request.text:
            name = dialog.get_next().get(request.text.strip(), dialog.get_default())
            dialog = self.dialog_set.get_dialog(name)

        return self.run(request=request, state=state, dialog=dialog)

    def get_routes(self, state=None, **kwargs) -> List[str]:
        route = state.get(self.DIALOG_ROUTE, "")
        return route.split(",") if route else []

    def run(self, dialog=None, request=None, state=None, **kwargs) -> Response:
        handle: Handler = dialog.get_handler()
        response = handle(dialog=dialog, request=request, state=state, **kwargs)

        current_route: str

        if response.session_type == 'RETRY':
            current_route = state[self.DIALOG_ROUTE]
        else:
            routes = self.get_routes(state=state, **kwargs)
            routes.append(dialog.get_name())
            current_route = ",".join(routes)

            state[self.DIALOG_ROUTE] = current_route
            if response.text:
                state[self.RETRY_MESSAGE] = response.text
            if 'END' == response.session_type:
                self.data_store.remove(request.session)
            else:
                self.data_store.update(session_key=request.session, **state)

        return response

    def dialogue(self, name=None, default=None, states=None):
        def our_decorator(func):
            _name = name if name else func.__name__
            _default = default if default else _name
            _next = states if states else {}
            self.dialog_set.add_dialog(InMemoryDialog(name=_name, handler=func, default=_default, _next=_next))
            return func

        return our_decorator

    def root(self, default=None, _next=None):
        _default = default if default else None
        _next = _next if _next else {}

        def add(func):
            self.dialog_set.add_root(handler=func, default=_default, _next=_next)
            return func

        return add


class InMemoryDataStore(DataStore):
    def __init__(self):
        self.client = {}

    def get(self, session_key) -> dict:
        return self.client.get(session_key, {})

    def update(self, session_key, **state):
        self.client[session_key] = state

    def remove(self, session_key):
        self.client.pop(session_key)
