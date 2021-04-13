from typing import Any, Dict, List, Union

from mmcc_framework.exceptions import DescriptionException
from mmcc_framework.activity import Activity, ActivityType


class Process(object):
    """ The description of a process, with a list of activities and the first activity.

    :ivar activities: a list of `Activity` objects representing this process
    :ivar first: the first Activity of the process
    """

    def __init__(self, activities: List[Union["Activity", Dict[str, Any]]], first_activity_id: str) -> None:
        """ Creates a new process description with the provided activities and first activity id.

        If the provided activities list contains the activities as dictionaries instead of
        `Activity` objects, this will call `Activity.from_dict(...)` on each of them before adding
        it.

        Example:
            my_process = Process([Activity("one", "two", ActivityType.TASK), ...], "one")

        :param activities: a list of objects or dictionaries representing the process activities
        :param first_activity_id: the id of the first activity of the process
        :raises DescriptionException: if first activity id has no corresponding activity
        """
        self.activities = []
        for a in activities:
            self.activities.append(a if isinstance(
                a, Activity) else Activity.from_dict(a))
        try:
            self.first = next(
                x for x in self.activities if x.id == first_activity_id)
        except StopIteration as err:
            raise DescriptionException(
                first_activity_id, "Found no activity with the provided id.") from err

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "Process":
        """ Returns the `Process` represented by a given dictionary, if possible.

        Example:
            my_process = Process.from_dict({
                            "first_activity_id": "one",
                            "activities": [
                                { "my_id": "one", "next_id": "two", "my_type": "task" },
                                ...
                            ]})


        See `Process.__init__` for more info.

        :param dictionary: a dictionary that represents a `Process`
        :return: a `Process` instance with the provided attributes
        :raises DescriptionException: if parameters are missing, or unknown parameters are provided
        """
        try:
            return cls(**dictionary)
        except TypeError as err:
            raise DescriptionException(
                dictionary, "Did not find a required parameter in the process.") from err

    def check(self) -> None:
        """ Performs some checks on the description, both syntactic and semantic (for example id are unique...).

        :raises DescriptionException: if the check is not passed
        """

        # Assume the first activity id is not found.
        found_first = 0

        for a in self.activities:
            # Check that next id is not equal to id.
            if a.next_id == a.id:
                raise DescriptionException(
                    a.id, "Found an activity that is the next of itself.")

            # Count how many activities have first id as their id.
            if self.first.id == a.id:
                found_first += 1

            # If this is a OR, XOR or PARALLEL, check that choices exist unique.
            choices = {}
            if a.type in ActivityType.get_require_choice():
                # Choices list is provided because of previous checks in Activity constructor.
                for c in a.choices:
                    if c is None:
                        raise DescriptionException(
                            a.id, "Fond an activity that contains None in the choices.")
                    if c == a.id:
                        raise DescriptionException(
                            a.id, "Found an activity with itself in its choices.")
                    if c in choices:
                        raise DescriptionException(
                            a.id, "Found an activity that contains duplicate choices.")
                    choices[c] = 0

            # Also count how many other activities have this next id as their id.
            found_next = 0
            for b in self.activities:
                if b.id == a.next_id:
                    found_next += 1

                # And count how many activities correspond to a choice.
                if b.id in choices:
                    choices[b.id] += 1

            # Raise an exception if a choice does not have a corresponding activity or has more than one.
            for c, v in choices.items():
                if v == 0:
                    raise DescriptionException(
                        a.id, f"The following does not have a corresponding activity: {c}.")
                if v > 1:
                    raise DescriptionException(
                        a.id, f"The following have multiple corresponding activities: {c}.")

            # Raise exceptions if next id or first id do not have exactly one corresponding activity.
            if a.next_id is not None:
                if found_next == 0:
                    raise DescriptionException(
                        a.id, "The provided next id does not have a corresponding activity.")
                if found_next > 1:
                    raise DescriptionException(
                        a.next_id, "Found a next id that has multiple corresponding activities.")
        if found_first == 0:
            raise DescriptionException(
                self.first.id, "First activity id has no corresponding activity.")
        if found_first > 1:
            raise DescriptionException(
                self.first.id, "First activity id has multiple corresponding activities.")
