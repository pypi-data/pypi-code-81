import json
from collections import deque
from threading import Lock
from typing import Union, Dict, Any, Callable

from mmcc_framework.process import Process
from mmcc_framework.activity import ActivityType
from mmcc_framework.nlu_adapters import NluAdapter

CTX_COMPLETED = "_done_"
""" Context key whose value is a list of activity id for the pending gateways that allow skipping. """


class Framework(object):
    """ A sort of state machine, takes a process description and handles inputs, keeping track of the current activity.

    :ivar _process: an object that represents the process for this Framework instance
    :ivar _kb: the data that is saved between different process executions
    :ivar _ctx: the data that is not saved between different process executions
    :ivar _current: the activity of the process that is being executed
    :ivar _callback_getter: a function returning the callback of an activity given its callback id
    :ivar _nlu: provides a translation from text to data, to handle in the same way text and data input (multimodal)
    :ivar _on_save: a function called when it is time to save the kb
    :ivar _stack: a pile of Activity id that is used to handle the gateways
    :ivar _done: a list that is used to determine if a gateway is completed
    """

    def __init__(self,
                 process: Union["Process", Dict[str, Any], Callable[[], Union["Process", Dict[str, Any]]]],
                 kb: Union[Dict[str, Any], Callable[[], Dict[str, Any]]],
                 initial_context: Dict[str, Any],
                 callback_getter: Callable[
                     [str], Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], "Response"]],
                 nlu: NluAdapter,
                 on_save: Callable[[Dict[str, Any]], None]) -> None:
        """ Instantiates a Framework with the given parameters.

        The process parameter can be a Process instance or a dictionary representing a process. In alternative, it can
        also be a function that returns a Process or a dictionary.
        Similarly, the kb parameter can be a dictionary or a callback that returns a dictionary.

        :param process: the Process for this instance, a dictionary representing it, or a callable that provides it
        :param kb: the data that is saved between different process executions
        :param initial_context: can be empty or contain configuration variables
        :param callback_getter: a function that returns the callback of an activity given its id
        :param nlu: provides a translation from text to data, to handle in the same way text and data input
        :param on_save: the function called when it is time to save the kb
        """
        if callable(process):
            process = process()
        self._process = process if isinstance(process, Process) else Process.from_dict(process)
        if callable(kb):
            kb = kb()
        self._kb = kb
        self._ctx = initial_context
        self._ctx[CTX_COMPLETED] = []
        self._current = self._process.first
        self._callback_getter = callback_getter
        self._nlu = nlu
        self._on_save = on_save
        self._stack = deque()
        self._done = {}

    @classmethod
    def from_file(cls,
                  process: str,
                  kb: str,
                  initial_context: Union[str, Dict[str, Any]],
                  callback_getter: Callable[
                      [str], Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], "Response"]],
                  nlu: NluAdapter,
                  lock: Lock = Lock()) -> "Framework":
        """ Loads the configuration of a framework from the files provided.

        The process file must contain a Process description that will be handled by Process.fromDict().
        The kb and context files must contain a dictionary, the context can also be provided directly.
        The kb will be saved back to its file when the process is completed.
        If the possibility exists that the files will be handled by more than one Framework instance at the time, it is
        necessary to provide a unique lock shared by all the instances. This will allow the framework to correctly
        handle the concurrency.

        :param process: the path to a file containing the process description
        :param kb: the path to a file containing the kb
        :param initial_context: the context or the path to a file containing the context
        :param callback_getter: a function that returns the callback of an activity given its id
        :param nlu: provides a translation from text to data, to handle in the same way text and data input
        :param lock: a unique lock shared by all the instances that can use the files
        """
        with lock:
            if not isinstance(initial_context, dict):
                with open(initial_context) as ctx_file:
                    my_ctx = json.load(ctx_file)
            else:
                my_ctx = initial_context

            with open(process) as process_file, open(kb) as kb_file:
                my_framework = cls(json.load(process_file),
                                   json.load(kb_file),
                                   my_ctx,
                                   callback_getter,
                                   nlu,
                                   lambda kb_c: _on_file_save(kb_c, kb, lock))
        return my_framework

    def handle_text_input(self, text: str) -> Dict[str, Any]:
        """ Takes textual input from the user, uses the nlu to parse it, and handles the input as data.

        :param text: the textual input from the user, to be parsed
        :return: a dictionary containing an utterance and a payload
        """
        return self.handle_data_input(self._nlu.parse(text.rstrip()))

    def handle_data_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """ Takes data input from the user and handles it.

        This will call the current activity callback and pass to it the data, then will forward the returned response
        utterance and payload to the caller.
        If the callback signals that the activity was completed successfully, this moves to the next activity in the
        process.

        :param data: the data representing the input from the user, formatted accordingly to the chosen NluAdapter
        :return: a dictionary containing an utterance and a payload
        """
        # If the activity is an END, return the default utterance if it exists.
        if self._current.type == ActivityType.END:
            return Response({}, {}, True).add_utterance(self._kb, self._current.id).to_dict()

        # If the activity is a XOR, get the choice from the callback.
        if self._current.type == ActivityType.XOR:
            response = self._get_response(data)

            # If the choice is valid, push next on the stack and continue with the chosen activity.
            if response.complete:
                # Push next id on the stack, can be None.
                self._stack.append(self._current.next_id)

                # Current will not be None, because XOR must return a valid next id.
                self._current = next(x for x in self._process.activities if x.id == response.choice)

                # Add default utterance if it exists.
                response.add_utterance(self._kb, self._current.id)

                # If the task is END, save the KB.
                if self._current.type == ActivityType.END:
                    self._on_save(self._kb)
            return response.to_dict()

        # PARALLEL and OR have similar behaviour and they are handled together.
        if self._current.type == ActivityType.PARALLEL or self._current.type == ActivityType.OR:
            # Obtain the chosen task from the callback.
            response = self._get_response(data)
            if response.complete:
                # The returned task is valid, and can be None to go to the next.
                if response.choice is None:
                    # Clear the info on the current gateway, if some exist.
                    self._done.pop(self._current.id, "")
                    if self._current.id in self._ctx[CTX_COMPLETED]:
                        self._ctx[CTX_COMPLETED].remove(self._current.id)

                    # Go to next task.
                    self._go_next(response)
                else:
                    # Put the gateway on the stack.
                    self._stack.append(self._current.id)

                    # Add an entry for this gateway to done and add the choice to it.
                    if self._current.id not in self._done:
                        self._done[self._current.id] = []
                    if response.choice not in self._done[self._current.id]:
                        self._done[self._current.id].append(response.choice)

                    # Handle separately PARALLEL and OR for updating CTX_COMPLETED.
                    if self._current.type == ActivityType.PARALLEL:
                        # A PARALLEL is completed when all the sub-tasks have been chosen at least once.
                        if all(i in self._done[self._current.id] for i in self._current.choices):
                            # Completed: add to the list.
                            if self._current.id not in self._ctx[CTX_COMPLETED]:
                                self._ctx[CTX_COMPLETED].append(self._current.id)
                        else:
                            # Not completed: remove from the list.
                            if self._current.id in self._ctx[CTX_COMPLETED]:
                                self._ctx[CTX_COMPLETED].remove(self._current.id)
                    else:
                        # An OR is completed after the first valid choice.
                        if self._current.id not in self._ctx[CTX_COMPLETED]:
                            self._ctx[CTX_COMPLETED].append(self._current.id)

                    # Set the choice and optional default utterance, the choice can not be None.
                    self._current = next(x for x in self._process.activities if x.id == response.choice)
                    response.add_utterance(self._kb, self._current.id)

                    # If the task is END, save the KB.
                    if self._current.type == ActivityType.END:
                        self._on_save(self._kb)
            return response.to_dict()

        # If the activity is TASK or START, the evaluate callback is called.
        response = self._get_response(data)

        # If the activity is completed go to the next.
        if response.complete:
            self._go_next(response)
        return response.to_dict()

    def _get_response(self, data):
        # Run the callback, update the context and the kb, and return the response.
        response = self._callback_getter(self._current.callback)(data, self._kb, self._ctx)
        self._kb = response.kb
        self._ctx = response.ctx
        return response

    def _go_next(self, response):
        # Go to the next task (maybe from the stack) and add the default utterance if it exists.
        if self._current.next_id is None:
            popped = self._stack.pop()
            while popped is None:
                popped = self._stack.pop()
            self._current = next(x for x in self._process.activities if x.id == popped)
        else:
            self._current = next(x for x in self._process.activities if x.id == self._current.next_id)
        response.add_utterance(self._kb, self._current.id)

        # If the task is END, save the KB.
        if self._current.type == ActivityType.END:
            self._on_save(self._kb)

    def is_complete(self):
        """ Returns whether the current activity type is `ActivityType.END`. """
        return self._current.type == ActivityType.END


def _on_file_save(contents: Dict[str, Any], path: str, lock: Lock) -> None:
    """ The callback used to save a json formatted dictionary to a file.

    If the file is shared, provide a lock that is unique for all the instances, and this method will handle concurrent
    access to the file.

    :param contents: the dictionary to save
    :param path: the path of the destination file
    :param lock: a lock shared by all instances that have access to the file
    """
    with lock:
        with open(path, "w") as kb_file:
            json.dump(contents, kb_file, indent=2)


class Response(object):
    def __init__(self,
                 kb: Dict[str, Any],
                 ctx: Dict[str, Any],
                 complete: bool,
                 utterance: str = None,
                 payload: Dict[str, Any] = None,
                 choice: str = None) -> None:
        """ Creates a Response with the provided parameters.

        If the current activity is one of ActivityType.get_require_choice(), and is completed, the Response will contain
        the choice of the user. This must be the id of one of the choices provided in the description.

        :param kb: the updated knowledge
        :param ctx: the updated context
        :param complete: whether the current activity is completed
        :param utterance: an optional utterance to be displayed
        :param payload: an optional payload to be returned to the caller
        :param choice: if the current activity is in ActivityType.get_require_choice() this can contain the user choice
        """
        self.kb = kb
        self.ctx = ctx
        self.complete = complete
        self.utterance = utterance if utterance is not None else ""
        self.payload = payload if payload is not None else {}
        self.choice = choice

    def to_dict(self) -> Dict[str, Any]:
        """ Returns a dictionary with utterance and payload, that can be returned to the caller. """
        return {"utterance": self.utterance, "payload": self.payload}

    def add_utterance(self, kb: Dict[str, Any], key: str, fallback: str = "") -> "Response":
        """ Adds an utterance to this response.

        The utterance is taken from the kb using the provided key, if it is not present a fallback (empty by default) is
        used. If this response does not already contain an utterance, in the end it will contain the added utterance.
        If the utterance to add can not be found and a fallback is not provided, nothing is added.
        If an utterance is provided and one already exists, the new one is appended on a new line.

        :param kb: the kb from which to take the utterance to add
        :param key: the key to retrieve the utterance from the kb
        :param fallback: the value that is used if the key is not in the kb
        :return: the updated Response
        """
        my_utt = kb[key] if key in kb else fallback
        if self.utterance == "":
            self.utterance = my_utt
        elif my_utt != "":
            self.utterance += "\n" + my_utt
        return self
