# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of Django nor the names of its contributors may be used
#        to endorse or promote products derived from this software without
#        specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import asyncio
import asyncio.coroutines
import functools
import os
import queue
import sys
import threading
import time
from concurrent.futures import Executor, Future, ThreadPoolExecutor
try:
    import contextvars  # Python 3.7+ only.
except ImportError:
    contextvars = None


class Local:
    """
    A drop-in replacement for threading.locals that also works with asyncio
    Tasks (via the current_task asyncio method), and passes locals through
    sync_to_async and async_to_sync.
    Specifically:
     - Locals work per-coroutine on any thread not spawned using asgiref
     - Locals work per-thread on any thread not spawned using asgiref
     - Locals are shared with the parent coroutine when using sync_to_async
     - Locals are shared with the parent thread when using async_to_sync
       (and if that thread was launched using sync_to_async, with its parent
       coroutine as well, with this working for indefinite levels of nesting)
    Set thread_critical to True to not allow locals to pass from an async Task
    to a thread it spawns. This is needed for code that truly needs
    thread-safety, as opposed to things used for helpful context (e.g. sqlite
    does not like being called from a different thread to the one it is from).
    Thread-critical code will still be differentiated per-Task within a thread
    as it is expected it does not like concurrent access.
    This doesn't use contextvars as it needs to support 3.6. Once it can support
    3.7 only, we can then reimplement the storage more nicely.
    """

    CLEANUP_INTERVAL = 60  # seconds

    def __init__(self, thread_critical=False):
        self._storage = {}
        self._last_cleanup = time.time()
        self._clean_lock = threading.Lock()
        self._thread_critical = thread_critical

    def _get_context_id(self):
        """
        Get the ID we should use for looking up variables
        """
        # Prevent a circular reference
        # from .sync import AsyncToSync, SyncToAsync

        # First, pull the current task if we can
        context_id = SyncToAsync.get_current_task()
        # OK, let's try for a thread ID
        if context_id is None:
            context_id = threading.current_thread()
        # If we're thread-critical, we stop here, as we can't share contexts.
        if self._thread_critical:
            return context_id
        # Now, take those and see if we can resolve them through the launch maps
        for i in range(sys.getrecursionlimit()):  # noqa: B007
            try:
                if isinstance(context_id, threading.Thread):
                    # Threads have a source task in SyncToAsync
                    context_id = SyncToAsync.launch_map[context_id]
                else:
                    # Tasks have a source thread in AsyncToSync
                    context_id = AsyncToSync.launch_map[context_id]
            except KeyError:
                break
        else:
            # Catch infinite loops (they happen if you are screwing around
            # with AsyncToSync implementations)
            raise RuntimeError("Infinite launch_map loops")
        return context_id

    def _cleanup(self):
        """
        Cleans up any references to dead threads or tasks
        """
        for key in list(self._storage.keys()):
            if isinstance(key, threading.Thread):
                if not key.is_alive():
                    del self._storage[key]
            elif isinstance(key, asyncio.Task):
                if key.done():
                    del self._storage[key]
        self._last_cleanup = time.time()

    def _maybe_cleanup(self):
        """
        Cleans up if enough time has passed
        """
        if time.time() - self._last_cleanup > self.CLEANUP_INTERVAL:
            with self._clean_lock:
                self._cleanup()

    def __getattr__(self, key):
        context_id = self._get_context_id()
        if key in self._storage.get(context_id, {}):
            return self._storage[context_id][key]
        else:
            raise AttributeError("%r object has no attribute %r" % (self, key))

    def __setattr__(self, key, value):
        if key in ("_storage", "_last_cleanup", "_clean_lock", "_thread_critical"):
            return super().__setattr__(key, value)
        self._maybe_cleanup()
        self._storage.setdefault(self._get_context_id(), {})[key] = value

    def __delattr__(self, key):
        context_id = self._get_context_id()
        if key in self._storage.get(context_id, {}):
            del self._storage[context_id][key]
        else:
            raise AttributeError("%r object has no attribute %r" % (self, key))


class _WorkItem(object):
    """
    Represents an item needing to be run in the executor.
    Copied from ThreadPoolExecutor (but it's private, so we're not going to rely on importing it)
    """

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return
        try:
            result = self.fn(*self.args, **self.kwargs)
        except BaseException as exc:
            self.future.set_exception(exc)
            # Break a reference cycle with the exception 'exc'
            self = None
        else:
            self.future.set_result(result)


class CurrentThreadExecutor(Executor):
    """
    An Executor that actually runs code in the thread it is instantiated in.
    Passed to other threads running async code, so they can run sync code in
    the thread they came from.
    """

    def __init__(self):
        self._work_thread = threading.current_thread()
        self._work_queue = queue.Queue()
        self._broken = False

    def run_until_future(self, future):
        """
        Runs the code in the work queue until a result is available from the future.
        Should be run from the thread the executor is initialised in.
        """
        # Check we're in the right thread
        if threading.current_thread() != self._work_thread:
            raise RuntimeError(
                "You cannot run CurrentThreadExecutor from a different thread"
            )
        # Keep getting work items and checking the future
        try:
            while True:
                # Get a work item and run it
                try:
                    work_item = self._work_queue.get(block=False)
                except queue.Empty:
                    # See if the future is done (we only exit if the work queue is empty)
                    if future.done():
                        return
                    # Prevent hot-looping on nothing
                    time.sleep(0.001)
                else:
                    work_item.run()
                    del work_item
        finally:
            self._broken = True

    def submit(self, fn, *args, **kwargs):
        # Check they're not submitting from the same thread
        if threading.current_thread() == self._work_thread:
            raise RuntimeError(
                "You cannot submit onto CurrentThreadExecutor from its own thread"
            )
        # Check they're not too late or the executor errored
        if self._broken:
            raise RuntimeError("CurrentThreadExecutor already quit or is broken")
        # Add to work queue
        f = Future()
        work_item = _WorkItem(f, fn, args, kwargs)
        self._work_queue.put(work_item)
        # Return the future
        return f


class AsyncToSync:
    """
    Utility class which turns an awaitable that only works on the thread with
    the event loop into a synchronous callable that works in a subthread.
    If the call stack contains an async loop, the code runs there.
    Otherwise, the code runs in a new loop in a new thread.
    Either way, this thread then pauses and waits to run any thread_sensitive
    code called from further down the call stack using SyncToAsync, before
    finally exiting once the async task returns.
    """

    # Maps launched Tasks to the threads that launched them (for locals impl)
    launch_map = {}

    # Keeps track of which CurrentThreadExecutor to use. This uses an asgiref
    # Local, not a threadlocal, so that tasks can work out what their parent used.
    executors = Local()

    def __init__(self, awaitable, force_new_loop=False):
        self.awaitable = awaitable
        if force_new_loop:
            # They have asked that we always run in a new sub-loop.
            self.main_event_loop = None
        else:
            try:
                self.main_event_loop = asyncio.get_event_loop()
            except RuntimeError:
                # There's no event loop in this thread. Look for the threadlocal if
                # we're inside SyncToAsync
                self.main_event_loop = getattr(
                    SyncToAsync.threadlocal, "main_event_loop", None
                )

    def __call__(self, *args, **kwargs):
        # You can't call AsyncToSync from a thread with a running event loop
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            pass
        else:
            if event_loop.is_running():
                raise RuntimeError(
                    "You cannot use AsyncToSync in the same thread as an async event loop - "
                    "just await the async function directly."
                )
        # Make a future for the return information
        call_result = Future()
        # Get the source thread
        source_thread = threading.current_thread()
        # Make a CurrentThreadExecutor we'll use to idle in this thread - we
        # need one for every sync frame, even if there's one above us in the
        # same thread.
        if hasattr(self.executors, "current"):
            old_current_executor = self.executors.current
        else:
            old_current_executor = None
        current_executor = CurrentThreadExecutor()
        self.executors.current = current_executor
        # Use call_soon_threadsafe to schedule a synchronous callback on the
        # main event loop's thread if it's there, otherwise make a new loop
        # in this thread.
        try:
            if not (self.main_event_loop and self.main_event_loop.is_running()):
                # Make our own event loop - in a new thread - and run inside that.
                loop = asyncio.new_event_loop()
                loop_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='AsyncToSync')
                loop_future = loop_executor.submit(
                    self._run_event_loop,
                    loop,
                    self.main_wrap(
                        args, kwargs, call_result, source_thread, sys.exc_info()
                    ),
                )
                if current_executor:
                    # Run the CurrentThreadExecutor until the future is done
                    current_executor.run_until_future(loop_future)
                # Wait for future and/or allow for exception propagation
                loop_future.result()
            else:
                # Call it inside the existing loop
                self.main_event_loop.call_soon_threadsafe(
                    self.main_event_loop.create_task,
                    self.main_wrap(
                        args, kwargs, call_result, source_thread, sys.exc_info()
                    ),
                )
                if current_executor:
                    # Run the CurrentThreadExecutor until the future is done
                    current_executor.run_until_future(call_result)
        finally:
            # Clean up any executor we were running
            if hasattr(self.executors, "current"):
                del self.executors.current
            if old_current_executor:
                self.executors.current = old_current_executor
        # Wait for results from the future.
        return call_result.result()

    def _run_event_loop(self, loop, coro):
        """
        Runs the given event loop (designed to be called in a thread).
        """
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(coro)
        finally:
            try:
                if hasattr(loop, "shutdown_asyncgens"):
                    loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                loop.close()
                asyncio.set_event_loop(self.main_event_loop)

    def __get__(self, parent, objtype):
        """
        Include self for methods
        """
        func = functools.partial(self.__call__, parent)
        return functools.update_wrapper(func, self.awaitable)

    async def main_wrap(self, args, kwargs, call_result, source_thread, exc_info):
        """
        Wraps the awaitable with something that puts the result into the
        result/exception future.
        """
        current_task = SyncToAsync.get_current_task()
        self.launch_map[current_task] = source_thread
        try:
            # If we have an exception, run the function inside the except block
            # after raising it so exc_info is correctly populated.
            if exc_info[1]:
                try:
                    raise exc_info[1]
                except:  # noqa: B001
                    result = await self.awaitable(*args, **kwargs)
            else:
                result = await self.awaitable(*args, **kwargs)
        except Exception as e:
            call_result.set_exception(e)
        else:
            call_result.set_result(result)
        finally:
            del self.launch_map[current_task]


class SyncToAsync:
    """
    Utility class which turns a synchronous callable into an awaitable that
    runs in a threadpool. It also sets a threadlocal inside the thread so
    calls to AsyncToSync can escape it.
    If thread_sensitive is passed, the code will run in the same thread as any
    outer code. This is needed for underlying Python code that is not
    threadsafe (for example, code which handles SQLite database connections).
    If the outermost program is async (i.e. SyncToAsync is outermost), then
    this will be a dedicated single sub-thread that all sync code runs in,
    one after the other. If the outermost program is sync (i.e. AsyncToSync is
    outermost), this will just be the main thread. This is achieved by idling
    with a CurrentThreadExecutor while AsyncToSync is blocking its sync parent,
    rather than just blocking.
    """

    # If they've set ASGI_THREADS, update the default asyncio executor for now
    if "ASGI_THREADS" in os.environ:
        loop = asyncio.get_event_loop()
        loop.set_default_executor(
            ThreadPoolExecutor(max_workers=int(
                os.environ["ASGI_THREADS"]), thread_name_prefix='SyncToAsync_ASGI')
        )

    # Maps launched threads to the coroutines that spawned them
    launch_map = {}

    # Storage for main event loop references
    threadlocal = threading.local()

    # Single-thread executor for thread-sensitive code
    single_thread_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='SyncToAsync')

    def __init__(self, func, thread_sensitive=False):
        self.func = func
        functools.update_wrapper(self, func)
        self._thread_sensitive = thread_sensitive
        self._is_coroutine = asyncio.coroutines._is_coroutine
        try:
            self.__self__ = func.__self__
        except AttributeError:
            pass

    async def __call__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()

        # Work out what thread to run the code in
        if self._thread_sensitive:
            if hasattr(AsyncToSync.executors, "current"):
                # If we have a parent sync thread above somewhere, use that
                executor = AsyncToSync.executors.current
            else:
                # Otherwise, we run it in a fixed single thread
                executor = self.single_thread_executor
        else:
            executor = None  # Use default

        if contextvars is not None:
            context = contextvars.copy_context()
            child = functools.partial(self.func, *args, **kwargs)
            func = context.run
            args = (child,)
            kwargs = {}
        else:
            func = self.func

        # Run the code in the right thread
        future = loop.run_in_executor(
            executor,
            functools.partial(
                self.thread_handler,
                loop,
                self.get_current_task(),
                sys.exc_info(),
                func,
                *args,
                **kwargs
            ),
        )
        return await asyncio.wait_for(future, timeout=None)

    def __get__(self, parent, objtype):
        """
        Include self for methods
        """
        return functools.partial(self.__call__, parent)

    def thread_handler(self, loop, source_task, exc_info, func, *args, **kwargs):
        """
        Wraps the sync application with exception handling.
        """
        # Set the threadlocal for AsyncToSync
        self.threadlocal.main_event_loop = loop
        # Set the task mapping (used for the locals module)
        current_thread = threading.current_thread()
        if AsyncToSync.launch_map.get(source_task) == current_thread:
            # Our parent task was launched from this same thread, so don't make
            # a launch map entry - let it shortcut over us! (and stop infinite loops)
            parent_set = False
        else:
            self.launch_map[current_thread] = source_task
            parent_set = True
        # Run the function
        try:
            # If we have an exception, run the function inside the except block
            # after raising it so exc_info is correctly populated.
            if exc_info[1]:
                try:
                    raise exc_info[1]
                except:  # noqa: B001
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        finally:
            # Only delete the launch_map parent if we set it, otherwise it is
            # from someone else.
            if parent_set:
                del self.launch_map[current_thread]

    @staticmethod
    def get_current_task():
        """
        Cross-version implementation of asyncio.current_task()
        Returns None if there is no task.
        """
        try:
            if hasattr(asyncio, "current_task"):
                # Python 3.7 and up
                return asyncio.current_task()
            else:
                # Python 3.6
                return asyncio.Task.current_task()
        except RuntimeError:
            return None


# Lowercase is more sensible for most things
sync_to_async = SyncToAsync
async_to_sync = AsyncToSync
