

from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.tasks import Task
from bergen.messages.postman.provide.bounced_provide import BouncedProvideMessage
from re import M
from bergen.messages.postman.assign.bounced_cancel_assign import BouncedCancelAssignMessage
from bergen.messages.postman.assign.bounced_assign import BouncedAssignMessage
import contextvars
from typing import Type
from bergen.types.node.ports import kwarg
from bergen.messages.postman.assign.assign import AssignMessage
import uuid
from bergen.console import console
from pydantic.main import BaseModel
from bergen.utils import expandInputs, shrinkInputs, shrinkOutputs
from bergen.schema import Template
from bergen.constants import ACCEPT_GQL, OFFER_GQL, SERVE_GQL
import logging
import asyncio
from bergen.models import Node, Pod
import inspect
from aiostream import stream
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial


logger = logging.getLogger()

class HostHelper(ABC):

    def __init__(self, host) -> None:
        self.host = host
        pass

    @abstractmethod
    async def pass_yield(self, message, value):
        pass

    @abstractmethod
    async def pass_progress(self, message, value, percentage=None):
        pass

    @abstractmethod
    async def pass_result(self, message, value):
        pass

    @abstractmethod
    async def pass_exception(self, message, exception):
        pass

class PodHelper(ABC):

    def __init__(self, host) -> None:
        self.host = host
        pass

    @abstractmethod
    async def pass_provided(self, message, value):
        pass

    @abstractmethod
    async def pass_unprovided(self, message, value, percentage=None):
        pass

    @abstractmethod
    async def pass_failed(self, message, exception):
        pass




assign_var = contextvars.ContextVar('assign', default=None)

class Actor:

    def __init__(self, bounced_provide: BouncedProvideMessage, helper: HostHelper, queue:asyncio.Queue = None, loop=None) -> None:
        self.queue = queue or asyncio.Queue()
        self.template_id = bounced_provide.data.template
        self.helper = helper
        self.loop = loop
        self._provided = False
        self.assignments = {}
        pass

    async def _on_provide(self):
        self.template = await Template.asyncs.get(id=self.template_id)
        result = await self.on_provide()
        self._provided = True
        pass

    async def on_provide(self):
        pass

    def check_if_assignation_cancelled(self, assign, task: Task):
        if task.cancelled():
            console.log(f"[yellow] Assignation {task.get_name()} Succeeded and is now Done")
        elif task.exception():
            console.log(f"[red] Assignation {task.get_name()} Failed with {str(task.exception())}")
        elif task.done():
            console.log(f"[green] Assignation {task.get_name()} Succeeded and is now Done")
        

    async def run(self):
        ''' An infinitie loop assigning to itself'''
        try:
            assert self._provided, "We didnt provide this actor before running"
            console.log(f"Run for {self.__class__.__name__} on Template {self.template.id}: Pod was Provided. Reserving")
            console.log(f"Run for {self.__class__.__name__} on Template {self.template.id}: Resources were reservered. Waiting for Tasks until canceled")
            
            while True:
                message = await self.queue.get()

                if isinstance(message, BouncedAssignMessage):
                    console.log(f"[green] Assignation for {self.__class__.__name__} on Template {self.template.id}")
                    task = asyncio.create_task(self.on_assign(message))
                    task.add_done_callback(partial(self.check_if_assignation_cancelled, message))
                    self.assignments[message.meta.reference] = task

                elif isinstance(message, BouncedCancelAssignMessage):
                    console.log(f"[yellow] Cancellation for {self.__class__.__name__} on Template {self.template.id}")
                    if message.data.reference in self.assignments: 
                        console.log("Cancellation for task received. Canceling!")
                        task = self.assignments[message.data.reference]
                        if not task.done():
                            task.cancel()
                            console.log("Canceled Task!!")
                        else:
                            console.log("Task had already finished")
                    else:
                        raise Exception("Assignment never was at this pod. something went wrong")

                else:
                    raise Exception(f"Type not known {message}")

                self.queue.task_done()


        except asyncio.CancelledError:
            console.log(f"Run for {self.__class__.__name__} on Pod {self.template}: Received Entertainment Cancellation. Unreserving")
            await self.on_unprovide()
            console.log(f"Run for {self.__class__.__name__} on Pod {self.template}: Unprovided. Ciao!")
            raise

    async def _on_unprovide(self):
        await self.on_unprovide()

    async def on_unprovide(self):
        pass

    async def _progress(self, value, percentage):
        message = assign_var.get()
        print(message)
        await self.helper.pass_progress(message, value, percentage=percentage)

    async def on_assign(self, assign: AssignMessage):
        try:
            args, kwargs = await expandInputs(node=self.template.node, args=assign.data.args, kwargs=assign.data.kwargs)
            console.log(args, kwargs)
            assign_var.set(assign)
            try:
                await self._assign(**{**args, **kwargs}) # We dont do all of the handling here, as we really want to have a generic class for Generators and Normal Functions
            except Exception as e:
                # As broad as possible to send further
                await self.helper.pass_exception(assign, e)
                # Pass this further up
                raise

        except asyncio.CancelledError as e:
            console.log("We are beeing cancelled")
            raise e
    
    async def __aenter__(self):
        await self.reserve()
        return self

    async def __aexit__(self):
        await self.unreserve()



class AsyncActor(Actor):
    pass


class AsyncFuncActor(AsyncActor):

    async def progress(self, value, percentage):
        await self._progress(value, percentage)

    async def assign(self, *args, **kwargs):
        raise NotImplementedError("Please provide a func or overwrite the assign method!")

    async def _assign(self, *args, **kwargs):
        message = assign_var.get()
        result = await self.assign(*args, **kwargs)
        try:
            shrinked_returns = await shrinkOutputs(self.template.node, result)
            await self.helper.pass_result(message, shrinked_returns)
        except Exception as e:
            await self.helper.pass_exception(message, e)


class AsyncGenActor(AsyncActor):

    async def progress(self, value, percentage):
        await self._progress(value, percentage)

    async def assign(self):
        raise NotImplementedError("This needs to be overwritten in order to work")

    async def _assign(self, *args, **kwargs):
        message = assign_var.get()
        yieldstream = stream.iterate(self.assign(*args, **kwargs))
        async with yieldstream.stream() as streamer:
            async for result in streamer:
                lastresult = await shrinkOutputs(self.template.node, result)
                await self.helper.pass_yield(message, lastresult)

        await self.helper.pass_result(message, lastresult)


class ThreadedFuncActor(Actor):
    nworkers = 5

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.threadpool = ThreadPoolExecutor(self.nworkers)

    def progress(self, value, percentage):
        if self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self._progress(value, percentage=percentage), self.loop)
            return future.result()
        else:
            self.loop.run_until_complete(self._progress(value, percentage=percentage))

    def assign(self):
        raise NotImplementedError("")   

    async def _assign(self, *args, **kwargs):
        message = assign_var.get()
        result = await self.loop.run_in_executor(self.threadpool, self.assign)
        return result


