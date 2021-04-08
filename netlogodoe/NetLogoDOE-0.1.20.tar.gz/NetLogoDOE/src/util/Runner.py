import multiprocessing
import traceback


class Process(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = multiprocessing.Pipe()
        self._exception = None

    def run(self):
        try:
            multiprocessing.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


class Runner:

    def __init__(self, function, args):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.child_process = Process(target=function, args=((self.child_conn,) + args))

    def run(self):
        self.child_process.start()

    def get_result(self):
        if self.parent_conn.poll(1):
            child_return = self.parent_conn.recv()
            return child_return
        return None