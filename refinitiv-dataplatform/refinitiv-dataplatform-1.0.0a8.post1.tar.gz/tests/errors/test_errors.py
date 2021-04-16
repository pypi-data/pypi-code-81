import refinitiv.dataplatform as rdp
import pytest


@pytest.fixture(scope="module",
                params=[rdp.RDPError, rdp.SessionError, rdp.StreamingError, rdp.StreamConnectionError, rdp.PlatformSessionError, rdp.ESGError,
                        rdp.NewsHeadlinesError, rdp.EndpointError, rdp.StreamError, rdp.StreamingPricesError])
def error_class(request):
    return request.param


def test_error_code_and_message(error_class):
    code = 0
    message = "message"
    error = error_class(code, message)

    assert error.code == code
    assert error.message == message


def test_error_raise(error_class):
    code = 0
    message = "message"
    error = error_class(code, message)
    with pytest.raises(error_class, match="message"):
        raise error


def test_error_to_str(error_class):
    code = 0
    message = "message"
    error = error_class(code, message)
    assert str(error)
