import unittest
from bffacilities.socketserver import TcpSocketServer, SocketClient, logger
from bffacilities.utils import changeLoggerLevel
import logging
changeLoggerLevel(logger, logging.DEBUG)

class TestTcpSocketServer(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)

    def setUp(self):
        self.tcpServer = TcpSocketServer("0.0.0.0", 54134)
        super().setUp()

    def tearDown(self):
        self.tcpServer.stop()
        self.tcpServer.shutdown()
        return super().tearDown()

    def test_connect(self):
        self.tcpServer.serve_once()
        client = SocketClient.createTcpClient(("127.0.0.1", 54134))
        client.connect()

        self.tcpServer.serve_once()
        client.sock.send(b"[This is a test]")

        self.tcpServer.serve_once(0.05)
        # self.tcpServer.stop()
        client.shutdown()

if __name__ == "__main__":
    # unittest.main()
    tcpServer = TcpSocketServer("0.0.0.0", 54134)
    tcpServer.serve_forever()