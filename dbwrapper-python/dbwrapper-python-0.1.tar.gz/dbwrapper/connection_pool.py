
import threading
import weakref
import sys

class ConnectionPool:
    def __init__(self, connection_factory, args=[], kwargs={}, per_thread=True, check_nrefs=True, logger=None):
        self.factory = connection_factory
        self.args = args or []
        self.kwargs = kwargs or {}

        self._per_thread = per_thread
        self._check_nrefs = check_nrefs

        self._logger = logger

        self._pool = []

        self._pool_lock = threading.RLock()

    def close(self):
        with self._pool_lock:
            for (key, conn) in self._pool:
                try:
                    if isinstance(conn, weakref.ref):
                        if conn() is not None:
                            conn().close()
                    else:
                        conn.close()
                except Exception as e:
                    self._error("Error closing connection.", exc_info=e)

    def prune(self, hard=True):
        with self._pool_lock:
            invalid = []
            for e in self._pool:
                if isinstance(e[1], weakref.ref) and e[1]() is None:
                    invalid.append(e)
                elif hard and sys.getrefcount(e[1]) == 2:
                    e[1].close()
                    invalid.append(e)
            
            for e in invalid:
                self._pool.remove(e)

            if len(invalid) > 0:
                self._debug("Pruned %d unused connections.", len(invalid))

    def _prune(self, _):
        self.prune(False)

    def release(self, conn):
        with self._pool_lock:
            if self._check_nrefs:
                if sys.getrefcount(conn) > 2:
                    raise RuntimeError("Connection has more than one reference and check_nrefs == True. Cannot release.")
            
            for i, e in enumerate(self._pool):
                if e[1] == conn:
                    del self._pool[i]
                    self._pool.add((None, e[1]))

    def get_connection(self, keyval=None, weak_conn=False):
        with self._pool_lock:
            self.prune(False)

            if self._per_thread and keyval is None:
                keyval = threading.currentThread()
                self._debug("per_thread=True and keyval is None: Using thread %s as key", keyval)

            i, key, conn = e = self.find_connection(lambda k, c: k == keyval, or_unallocated=False)

            if conn is None:
                i, key, conn = e = self.find_connection(or_unallocated=True)
            else:
                self._debug("Found connection with same key: %s, %s", key, conn)
                
            if key is None and conn is not None:
                del self._pool[i]
                self._pool.append((weakref.ref(keyval), conn if not weak_conn else weakref.ref(conn, self._prune)))
                self._debug("Found unallocation connection: %s. Reallocating with different key: %s", conn, keyval)

            if conn is None:
                conn = self.factory(*self.args, **self.kwargs)
                self._pool.append((weakref.ref(keyval), conn if not weak_conn else weakref.ref(conn, self._prune)))
                self._debug("No available connection found, creating one: %s, %s", keyval, conn)

            self._info("Connection: %s: %s", keyval, conn)
            return conn

    def find_connection(self, predicate=None, or_unallocated=True):
        with self._pool_lock:
            for i, (key, conn) in enumerate(self._pool):
                if isinstance(key, weakref.ref):
                    key = key()

                if isinstance(conn, weakref.ref):
                    conn = conn()
                    if conn is None:
                        self._debug("Skipping GC'd connection. (key=%s)", key)
                        continue

                if self._check_nrefs:
                    n = sys.getrefcount(conn)
                    if n > 3:
                        self._debug("Skipping connection %s (%d>3).", conn, n)
                        continue
                    else:
                        key = None

                if predicate is not None:
                    if predicate(key, conn):
                        self._debug("Connection matches predicate (%s, %s).", key, conn)
                        return i, key, conn

                if or_unallocated and key is None:
                    self._debug("Found unallocated connection (%s, %s).", key, conn)
                    return i, key, conn
                
                if not or_unallocated:
                    self._debug("Found a connection (%s, %s).", key, conn)
                    return i, key, conn

        self._debug("No connection found. Predicate=%s or_unallocated=%s.", predicate, or_unallocated)
        return -1, None, None

    def _debug(self, msg, *args, exc_info=None):
        if self._logger is not None:
            self._logger.debug(msg, *args, exc_info=exc_info)

    def _info(self, msg, *args, exc_info=None):
        if self._logger is not None:
            self._logger.info(msg, *args, exc_info=exc_info)
            
    def _error(self, msg, *args, exc_info=None):
        if self._logger is not None:
            self._logger.error(msg, *args, exc_info=exc_info)
            