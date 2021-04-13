from enum import Enum
from typing import Any, Dict, List, Optional, Union

from mmcc_framework.exceptions import DescriptionException


class Activity(object):
    """ An element of a `Process` description, a single step in which the user has to do something.

    :ivar id: the unique id of this activity (unique)
    :ivar next_id: the id of the `Activity` that comes after this, when completed (can be `None`)
    :ivar type: the `ActivityType` of this activity
    :ivar choices: a list of id that this activity offers as choices (can be `None`)
    :ivar callback: the callback identifier for this activity
    """

    def __init__(self,
                 my_id: str,
                 next_id: Optional[str],
                 my_type: Union[str, "ActivityType"],
                 choices: List[str] = None,
                 callback: Optional[str] = None) -> None:
        """ Creates a new activity with the provided parameters; performs some checks.

        The parameter `next_id` is `None` if the activity is the last "inside" one of the
        `ActivityType.get_require_choice()` gateways.

        The `choices` are required only if `my_type` is in `ActivityType.get_require_choice()`.

        The action used by this activity is provided as a separate callback. This callback is
        identified with the `callback` attribute; if the attribute is not provided, `my_id` will
        be used instead.

        :param my_id: the unique id of this activity
        :param next_id: the id of the `Activity` that comes after this, when completed
        :param my_type: the `ActivityType` of this activity or a string representing it
        :param choices: a list of id that this activity offers as choices
        :param callback: the callback identifier if different from `id`
        :raises DescriptionException: if `choices` is provided and not needed, or is missing
        :raises KeyError: if can not recognize the `ActivityType` provided
        """
        self.id = my_id
        self.next_id = next_id
        self.type = my_type if isinstance(
            my_type, ActivityType) else ActivityType[my_type.upper()]
        if self.type in ActivityType.get_require_choice():
            if choices is None:
                raise DescriptionException(
                    self.id, "Expected some choices, but found none.")
            if not choices:
                raise DescriptionException(
                    self.id, "Expected some choices, but found an empty list.")
        elif choices is not None or choices:
            raise DescriptionException(self.id, "Found unexpected choices.")
        self.choices = choices
        self.callback = my_id if callback is None else callback

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "Activity":
        """ Returns the `Activity` represented by a given dictionary, if possible.

        Example:
            my_activity = Activity.from_dict({"my_id": "an id",
                                              "next_id": "another id",
                                              "my_type": "xor",
                                              "choices": ["id", "more id"],
                                              "callback": "second_callback"})

        See `Activity.__init__` for more info.

        :param dictionary: a dictionary that represents an `Activity`
        :return: an `Activity` instance with the provided attributes
        :raises DescriptionException: if parameters are missing, or unknown parameters are provided
        """
        try:
            return cls(**dictionary)
        except TypeError as err:
            raise DescriptionException(
                dictionary, "Did not find a required parameter in this activity.") from err

    def __eq__(self, o: object) -> bool:
        """ Returns `True` if two activities have the same attributes. """
        return isinstance(o, Activity) and \
            self.id == o.id and self.next_id == o.next_id and self.type == o.type \
            and self.choices == o.choices and self.callback == o.callback

    def __ne__(self, o: object) -> bool:
        """ Returns `True` if `__eq__` would return `False`. """
        return not self == o


class ActivityType(Enum):
    """ The various types of activities in a process. """

    TASK = "task"
    """ Represents an operation to be done to complete the process.
    The `Response` contains `True` if the user can move on to the next activity.
    """
    START = "start"
    """ It is the entry point of the process.
    Its `Response` must contain `True` and can be used to prepare the state using the payload.
    """
    END = "end"
    """ A "sink" state that represents the termination of the process. """
    PARALLEL = "parallel"
    """ A task that gives some options to the user, the user can choose which one to execute.
    This is completed when all options have been chosen at least once.
    Its callback must return the id of the chosen activity if the user input was valid, `None` to
    move on to the next task.
    """
    XOR = "xor"
    """ A task that gives some options to the user, the user can choose which one to execute.
    This allows the user to choose exactly one of the options.
    Its callback must return the id of the chosen activity if the user input was valid.
    """
    OR = "or"
    """ A task that gives some options to the user, the user can choose which one to execute.
    This is completed when the user has chosen at least one of the options.
    Its callback must return the id of the chosen activity if the user input was valid, `None` to
    move on to the next task.
    """

    @staticmethod
    def get_require_choice() -> List["ActivityType"]:
        """ Returns a list of the `ActivityType`s that require the choices in the description. """
        return [ActivityType.PARALLEL, ActivityType.XOR, ActivityType.OR]
