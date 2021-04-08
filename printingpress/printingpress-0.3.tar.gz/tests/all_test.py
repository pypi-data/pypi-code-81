import printingpress


def test_printingpress():
    ret = printingpress.me()
    assert "printingpress" in ret
