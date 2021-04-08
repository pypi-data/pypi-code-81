import logging
import socket
from time import time, sleep
from typing import List

LOGGER = logging.getLogger('moonspec')


class InetApi:
    @staticmethod
    def tcp_check_open(host: str, port: int, timeout_ms: int = 1000) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout_ms / 1000)
            result = sock.connect_ex((host, port))
            sock.close()
        except BaseException as e:
            LOGGER.warning('Failed to test remote port %s:%d', host, port, exc_info=e)
            return False

        return 0 == result

    @staticmethod
    def tcp_latency(host: str, port: int, timeout_ms: int = 1000) -> float:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout_ms / 1000)
        time_start = time()

        try:
            sock.connect((host, port))
            sock.shutdown(socket.SHUT_RD)
        except BaseException as e:
            LOGGER.warning('Failed to test latency to remote port %s:%d', host, port, exc_info=e)
            return -1.0

        return float((time() - time_start) * 1000)

    @staticmethod
    def tcp_latency_avg(host: str, port: int, runs: int = 5, timeout_ms: int = 1000, delay_ms: int = 100) -> float:
        results: List[float] = []

        for _ in range(0, runs):
            results.append(InetApi.tcp_latency(host, port, timeout_ms=timeout_ms))

            if delay_ms > 0:
                sleep(delay_ms / 1000)

        return sum(results) / runs

