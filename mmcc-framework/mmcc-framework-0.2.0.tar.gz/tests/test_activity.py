from unittest.case import TestCase

from mmcc_framework.exceptions import DescriptionException
from mmcc_framework.activity import Activity, ActivityType


class TestActivity(TestCase):
    def setUp(self) -> None:
        self.my_id = "my id"
        self.next_id = "next id"
        self.choices = ["a", "b", "c"]
        self.callback = "a callback"
        self.value = {}

    def test_init(self):
        for t in ActivityType:
            self.value[t] = Activity(self.my_id, self.next_id, t, self.choices if t in ActivityType.get_require_choice() else None)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None, "The choices are correctly set")
            self.assertEqual(self.value[t].callback, self.my_id, "The callback is correctly set")

    def test_init_with_type_from_text(self):
        for t in ActivityType:
            self.value[t] = Activity(self.my_id, self.next_id, t.value, self.choices if t in ActivityType.get_require_choice() else None)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly casted and set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None, "The choices are correctly set")
            self.assertEqual(self.value[t].callback, self.my_id, "The callback is correctly set")

    def test_init_with_callback(self):
        c_name = "a callback"
        for t in ActivityType:
            self.value[t] = Activity(self.my_id, self.next_id, t.value, self.choices if t in ActivityType.get_require_choice() else None, c_name)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly casted and set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None, "The choices are correctly set")
            self.assertEqual(self.value[t].callback, c_name, "The callback is correctly set")

    def test_init_with_wrong_choices(self):
        for t in ActivityType:
            with self.assertRaises(DescriptionException, msg="If wrong choices are provided, should raise exception"):
                Activity(self.my_id, self.next_id, t, None if t in ActivityType.get_require_choice() else self.choices)

    def test_init_with_wrong_type(self):
        with self.assertRaises(KeyError, msg="If the type is wrong, should raise an exception"):
            Activity(self.my_id, self.next_id, "no_type")

    def test_from_dict(self):
        for t in ActivityType:
            my_dict = {"my_id": self.my_id, "next_id": self.next_id, "my_type": t.value}
            if t in ActivityType.get_require_choice():
                my_dict["choices"] = self.choices
            self.value[t] = Activity.from_dict(my_dict)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None, "The choices are correctly set")
            self.assertEqual(self.value[t].callback, self.my_id, "The callback is correctly set")

    def test_from_dict_shuffled(self):
        for t in ActivityType:
            my_dict = {"next_id": self.next_id, "my_id": self.my_id, }
            my_dict["callback"] = self.callback
            if t in ActivityType.get_require_choice():
                my_dict["choices"] = self.choices
            my_dict["my_type"] = t.value
            self.value[t] = Activity.from_dict(my_dict)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None, "The choices are correctly set")
            self.assertEqual(self.value[t].callback, self.callback, "The callback is correctly set")

    def test_from_dict_with_wrong_params(self):
        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. my_id"):
            Activity.from_dict({"next_id": self.next_id, "my_type": ActivityType.XOR, "choices": self.choices})

        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. next_id"):
            Activity.from_dict({"my_id": self.my_id, "my_type": ActivityType.XOR, "choices": self.choices})

        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. my_type"):
            Activity.from_dict({"my_id": self.my_id, "next_id": self.next_id, "choices": self.choices})

        with self.assertRaises(DescriptionException, msg="With more params than needed, raise"):
            Activity.from_dict({"my_id": self.my_id, "next_id": self.next_id, "my_type": ActivityType.XOR, "choices": self.choices, "other": True})

    def test_eq_ne(self):
        subject = Activity(self.my_id, self.next_id, ActivityType.TASK)
        equal = Activity(self.my_id, self.next_id, ActivityType.TASK)
        diff_id = Activity("different", self.next_id, ActivityType.TASK)
        diff_next = Activity(self.my_id, "different", ActivityType.TASK)
        diff_type = Activity(self.my_id, self.next_id, ActivityType.OR, self.choices)
        diff_callback = Activity(self.my_id, self.next_id, ActivityType.TASK, callback="callback")
        subject_choices = Activity(self.my_id, self.next_id, ActivityType.OR, ["a"])

        self.assertEqual(subject, subject, "Activity should be equal to itself")
        self.assertEqual(subject, equal, "Activities with same attributes should be equal")
        self.assertNotEqual(subject, diff_id, "Activities with different id should not be equal")
        self.assertNotEqual(subject, diff_next, "Activities with different next id should not be equal")
        self.assertNotEqual(subject, diff_type, "Activities with different type should not be equal")
        self.assertNotEqual(subject_choices, diff_type, "Activities with different choices should not be equal")
        self.assertNotEqual(subject, diff_callback, "Activities with different callbacks should not be equal")
