from itertools import chain


class Test:

    def __init__(self, ue: int, suite: int, index: int, name: str):
        self.name = name
        self.ue = ue
        self.suite = suite
        self.index = index
        self.global_fail_counter: int = 0
        self.group_fail_counters: {int} = {}
        self.global_total_counter: int = 1
        self.group_total_counters: {int} = {}

    def fail(self, group: str):
        self.global_fail_counter += 1
        if group in self.group_fail_counters:
            self.group_fail_counters[group] += 1
        else:
            self.group_fail_counters[group] = 1

    def inc(self, group: str):
        self.global_total_counter += 1
        if group in self.group_total_counters:
            self.group_total_counters[group] += 1
        else:
            self.group_total_counters[group] = 1

    def group_success(self, group: str) -> float:
        if group in self.group_fail_counters:
            if self.group_total_counters[group] == 0:
                return 0
            return float(self.group_total_counters[group] - self.group_fail_counters[group]) / float(
                self.group_total_counters[group]) * float(100)
        if group not in self.group_total_counters:
            return 0
        return 100

    def fail_count(self, groups: [str]) -> float:
        return sum([(self.group_fail_counters[group] if group in self.group_fail_counters else 0) for group in groups])

    def global_success(self, groups: [str] = None) -> float:
        if groups is None:
            if self.global_total_counter == 0:
                return 0
            return float(self.global_total_counter - self.global_fail_counter) / float(self.global_total_counter) * float(
                100)
        else:
            global_total_counter = sum([(self.group_total_counters[group] if group in self.group_total_counters else 0) for group in groups])
            global_fail_counter = sum([(self.group_fail_counters[group] if group in self.group_fail_counters else 0) for group in groups])
            if global_total_counter == 0:
                return 0
            return float(global_total_counter - global_fail_counter) / float(global_total_counter) * float(100)

    def flat_name(self) -> str:
        return "{}.{}.{} {}".format(self.ue, self.suite, self.index, self.name)

    def test_no(self) -> str:
        return "{}.{}.{}".format(self.ue, self.suite, self.index)


class TestIndex:

    def __init__(self):
        self.index: {{Test}} = {}

    def get_test(self, suite: int, index: int):
        return self.index[suite][index]

    def create_test(self, ue: int, suite: int, index: int, name: str) -> Test:
        if suite in self.index and index in self.index[suite]:
            test = self.get_test(suite, index)
            if test.name == name:
                return self.get_test(suite, index)
            else:
                raise Exception("test duplicate detected! (expected: {}, got: {})".format(test.name, name))
        else:
            test = Test(ue, suite, index, name)
            if suite in self.index:
                suite_index = self.index[suite]
            else:
                suite_index = {}
                self.index[suite] = suite_index
            suite_index[index] = test
            return test

    def flat(self) -> [Test]:
        return [test for test in list(chain.from_iterable([item.values() for item in self.index.values()]))]
