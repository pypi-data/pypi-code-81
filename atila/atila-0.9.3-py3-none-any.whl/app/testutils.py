import skitai

class TestUtils:
    def test_client (self, point = "/", approot = ".", numthreads = 1):
        # 2021. 4. 16
        # removed officially, this is used by only unittest
        from skitai import testutil
        from skitai.testutil import client

        class Client (client.Client):
            def make_request (self, *args, **karg):
                request = client.Client.make_request (self, *args, **karg)
                return self.handle_request (request)

            def __enter__ (self):
                return self

            def __exit__ (self, type, value, tb):
                pass

        testutil.activate ()
        testutil.install_vhost_handler ()
        testutil.mount (point, (self, approot))
        return Client ()

    def run (self, address = '127.0.0.1', port = 5000, mount = '/', pref = None):
        skitai.mount (mount, self, pref)
        skitai.run (address = address, port = port)
