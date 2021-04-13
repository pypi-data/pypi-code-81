
class Assert:

    def __init__(self, ex: int, suite: int, test: int, assertion: int, message: str, test_name: str, subassertion: int = 0):
        self.test = test
        self.suite = suite
        self.ex = ex
        self.assertion = assertion
        self.subassertion = subassertion
        self.message = message
        self.counters: {int} = {}
        self.test_name = test_name

    def inc(self, group: str):
        if group in self.counters:
            self.counters[group] += 1
        else:
            self.counters[group] = 1

    def count(self, groups: [str]):
        return sum([self.counters[group] if group in self.counters else 0 for group in groups])


class TypeSystem:

    def __init__(self, identifier: str, message: str):
        self.identifier = identifier
        self.message = message
        self.students = []

    def inc(self, group: str, student_id: str):
        if (group, student_id) not in self.students:
            self.students += [(group, student_id)]

    def count(self, groups: [str]):
        return len(list(filter(lambda tuple: tuple[0] in groups, self.students)))


class FailIndex:

    def __init__(self):
        self.asserts = {}
        self.typesys = {}

    def inc_assert(self, assert_index: str, assert_msg: str, test_name: str, group: str):
        if assert_index in self.asserts:
            assert_obj = self.asserts[assert_index]
        else:
            parts = assert_index.split(".")
            if len(parts) == 4:
                assert_obj = Assert(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), assert_msg, test_name)
            elif len(parts) == 5:
                assert_obj = Assert(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), assert_msg, test_name, int(parts[4]))
            else:
                raise Exception("invalid assert index")
            self.asserts[assert_index] = assert_obj
        assert_obj.inc(group)

    def inc_typesys(self, identifier: str, message: str, student_id: str, group: str):
        if identifier in self.typesys:
            self.typesys[identifier].inc(group, student_id)
        else:
            typesys = TypeSystem(identifier, message)
            self.typesys[identifier] = typesys
            typesys.inc(group, student_id)