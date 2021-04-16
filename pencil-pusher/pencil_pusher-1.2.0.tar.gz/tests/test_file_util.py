from pencil_pusher.file_util import FileUtil


def test_query_directory():
    """
    Tests that source files are queried properly
    """
    result = FileUtil.query_directory("pencil_pusher", [".py"])

    count = 0
    for r in result:
        if "pencil_pusher/__init__.py" in r:
            count += 1
        if "pencil_pusher/__main__.py" in r:
            count += 1

    assert count == 2
