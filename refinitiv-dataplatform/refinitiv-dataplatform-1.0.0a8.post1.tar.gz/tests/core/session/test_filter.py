import pytest

import refinitiv.dataplatform.log as log


class Record(object):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


@pytest.mark.parametrize("testing_data", [
    (Record("module:awesome"), "", False),
    (Record("module"), "*", True),
    (Record("session:module:a"), "session*", True),
    (Record("session:module:a"), "session:mod*", True),
    (Record("module:a:session"), "session*", False),
    (Record("module:a:session"), "module:a:*", True),
    (Record("module:b"), "session*, module:b, module:c", True),
    (Record("session:a"), "session*,module:b,module:c", True),
    (Record("module:a"), "*,-module:a", False),
    (Record("module:g"), "module:*, -module:b, -module:c", True),
    (Record("module:c"), "module:*, -module:b, -module:c", False),
    (Record("module:session"), "-module:*", False),
    ])
def test_make_filter(testing_data):
    record, filter_by, expected = testing_data
    filterer = log.make_filter(filter_by)
    result = filterer(record)
    assert result == expected, f"record={record.name}, filter_by={filter_by}"
