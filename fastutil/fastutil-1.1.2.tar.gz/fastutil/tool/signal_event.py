import multiprocessing
import signal

from fastutil.tool.custom_exception import GracefulExitException

exit_event = multiprocessing.Event()


def term_with_exception(sig_num, frame):
    raise GracefulExitException()


def term_with_flag(sig_num, frame):
    exit_event.set()


def register_exit_signal(flag=True, exception=False):
    if flag:
        signal.signal(signal.SIGINT, term_with_flag)
        signal.signal(signal.SIGTERM, term_with_flag)
        signal.signal(signal.SIGHUP, term_with_flag)
    if exception:
        signal.signal(signal.SIGINT, term_with_exception)
        signal.signal(signal.SIGTERM, term_with_exception)
        signal.signal(signal.SIGHUP, term_with_exception)
