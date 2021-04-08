from herdpy.client import Report


class FakeResponse:
    status_code = 200

class FakeSession:
    def post(self, url, json={}):
        return FakeResponse()


def test_client():

    sess = FakeSession()

    r = Report(sess)

    r.url = "http://nowhere.local"
    r.node_name = "testclient"
    r.group = "testgroup"
    r.status_code = "E200OK"
    r.add_tag("test")
    r.add_tag("dev")

    r.send() # This should not raise an exception
