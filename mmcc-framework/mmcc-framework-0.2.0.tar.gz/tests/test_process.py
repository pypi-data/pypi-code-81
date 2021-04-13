from unittest.case import TestCase

from mmcc_framework.exceptions import DescriptionException
from mmcc_framework.process import Process
from mmcc_framework.activity import Activity, ActivityType


class TestProcess(TestCase):
    def test_init(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_process = Process(my_activities, "one")
        self.assertEqual(my_process.activities, my_activities, "The activities are saved")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is saved")

    def test_init_with_dict(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_dicts = [
            {"my_id": my_activities[0].id, "next_id": my_activities[0].next_id, "my_type": my_activities[0].type.value},
            {"my_id": my_activities[1].id, "next_id": my_activities[1].next_id, "my_type": my_activities[1].type.value, "choices": my_activities[1].choices}]
        my_process = Process(my_dicts, "one")
        self.assertEqual(my_process.activities, my_activities, "The activities are saved")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is saved")

    def test_init_with_missing_first(self):
        with self.assertRaises(DescriptionException, msg="Raise if first activity id has no corresponding activity"):
            Process([Activity("one", None, ActivityType.TASK)], "two").check()

    def test_from_dict(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_dict = {
            "activities": [
                {"my_id": my_activities[0].id, "next_id": my_activities[0].next_id, "my_type": my_activities[0].type.value},
                {"my_id": my_activities[1].id, "next_id": my_activities[1].next_id, "my_type": my_activities[1].type.value, "choices": my_activities[1].choices}],
                "first_activity_id": my_activities[0].id
        }
        my_process = Process.from_dict(my_dict)
        self.assertEqual(my_process.activities, my_activities, "The activities are correctly set")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is correctly set")

    def test_from_dict_shuffled(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_dict = {
            "first_activity_id": my_activities[0].id,
            "activities": [
                {"my_id": my_activities[0].id, "next_id": my_activities[0].next_id, "my_type": my_activities[0].type.value},
                {"my_id": my_activities[1].id, "next_id": my_activities[1].next_id, "my_type": my_activities[1].type.value, "choices": my_activities[1].choices}]
        }
        my_process = Process.from_dict(my_dict)
        self.assertEqual(my_process.activities, my_activities, "The activities are correctly set")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is correctly set")

    def test_from_dict_with_wrong_params(self):
        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. activities"):
            Process.from_dict({"first_activity_id": "one"}).check()

        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. first id"):
            Process.from_dict({"activities": [{"my_id": "one", "next_id": "two", "my_type": "task"}]}).check()

        with self.assertRaises(DescriptionException, msg="With more params than needed, raise"):
            Process.from_dict(
                {"activities": [{"my_id": "one", "next_id": "two", "my_type": "task"}], "first_activity_id": "one",
                 "other": True}).check()

    def test_check_first_with_more_correspondences(self):
        with self.assertRaises(DescriptionException, msg="Raise if first activity id has more correspondences"):
            Process([Activity("one", None, ActivityType.TASK),
                     Activity("one", None, ActivityType.TASK)], "one").check()

    def test_check_exists_unique_next_id(self):
        with self.assertRaises(DescriptionException, msg="Raise if a next id is not unique"):
            Process([Activity("one", "two", ActivityType.TASK),
                     Activity("two", None, ActivityType.TASK),
                     Activity("two", None, ActivityType.TASK)], "one").check()

        with self.assertRaises(DescriptionException, msg="Raise if a next id is not found"):
            Process([Activity("one", "two", ActivityType.TASK)], "one").check()

    def test_check_next_id_is_not_self(self):
        with self.assertRaises(DescriptionException, msg="Raise if a next id is equal to id"):
            Process([Activity("one", "one", ActivityType.TASK)], "one").check()

    def test_check_exists_unique_choices(self):
        with self.assertRaises(DescriptionException, msg="Raise if a choice is not unique"):
            Process([Activity("one", None, ActivityType.OR, ["two"]),
                     Activity("two", None, ActivityType.TASK),
                     Activity("two", None, ActivityType.TASK)], "one").check()

        with self.assertRaises(DescriptionException, msg="Raise if a choice is not found"):
            Process([Activity("one", None, ActivityType.OR, ["two"])], "one").check()

    def test_check_choice_not_allowed(self):
        with self.assertRaises(DescriptionException, msg="Raise if a choice is None"):
            Process([Activity("one", None, ActivityType.OR, ["two", None]),
                     Activity("two", None, ActivityType.TASK)], "one").check()

        with self.assertRaises(DescriptionException, msg="Raise if a choice is the same as the id"):
            Process([Activity("one", None, ActivityType.OR, ["one"])], "one").check()

        with self.assertRaises(DescriptionException, msg="Raise if a choice contains duplicates"):
            Process([Activity("one", None, ActivityType.OR, ["two", "two"]),
                     Activity("two", None, ActivityType.TASK)], "one").check()
