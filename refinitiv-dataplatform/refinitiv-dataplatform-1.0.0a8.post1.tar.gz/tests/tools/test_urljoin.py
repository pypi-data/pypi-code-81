from refinitiv.dataplatform.tools._common import urljoin


def test_0():
    expected = ""
    url = urljoin()
    assert url == expected


def test_1():
    expected = "https://api.refinitiv.com/data/news/beta1"
    url = urljoin("https://api.refinitiv.com", "data/news/beta1")
    assert url == expected


def test_2():
    expected = "https://api.refinitiv.com/data/news/beta1"
    url = urljoin("https://api.refinitiv.com/", "data/news/beta1")
    assert url == expected


def test_3():
    expected = "https://api.refinitiv.com/data/news/beta1"
    url = urljoin("https://api.refinitiv.com/", "/data/news/beta1")
    assert url == expected


def test_4():
    expected = "https://api.refinitiv.com"
    url = urljoin("https://api.refinitiv.com")
    assert url == expected


def test_5():
    expected = "/data/news/beta1"
    url = urljoin("/", "data/news/beta1")
    assert url == expected


def test_6():
    expected = "data/news/beta1/"
    url = urljoin("data/news/beta1", "/")
    assert url == expected


def test_7():
    expected = "https://api.refinitiv.com/data/news/beta1/"
    url = urljoin("https://api.refinitiv.com/", "/data/news/beta1/")
    assert url == expected


def test_8():
    url = urljoin("/data/news/beta1", "view")
    expected = "/data/news/beta1/view"
    assert url == expected


def test_9():
    url = urljoin("/", "/data/news/beta1")
    expected = "/data/news/beta1"
    assert url == expected


def test_10():
    url = urljoin("data/news/beta1/", "/")
    expected = "data/news/beta1/"
    assert url == expected


def test_11():
    url = urljoin("data/news/beta1/", "/{universe}")
    expected = "data/news/beta1/{universe}"
    assert url == expected
