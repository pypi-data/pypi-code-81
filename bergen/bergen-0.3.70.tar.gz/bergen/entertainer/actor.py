

from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.tasks import Task
from bergen.messages.types import RESERVE_CRITICAL, RESERVE_DONE
from typing import Generic, Union
from bergen.messages import *
import contextvars
from bergen.console import console
from bergen.utils import expandInputs, shrinkOutputs
from bergen.schema import Template
import logging
import asyncio
from aiostream import stream
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial


logger = logging.getLogger()

class HostHelper:

    def __init__(self, host) -> None:
        self.host = host
        pass

    async def forward(self, message: MessageModel):
        await self.host.forward(message)

    async def pass_yield(self, message: AssignMessage, value):
        yield_message = AssignYieldsMessage(data={"yields": value}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.host.forward(yield_message)

    async def pass_progress(self, message: AssignMessage, value, percentage=None):
        value = f'{percentage if percentage else "--"} : {value}'
        progress_message = AssignProgressMessage(data={"message": value, "level": "INFO"}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.host.forward(progress_message)

    async def pass_result(self,message: AssignMessage, value):
        return_message = AssignReturnMessage(data={"returns": value}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.host.forward(return_message)

    async def pass_exception(self, message: AssignMessage, exception):
        error_message = AssignCriticalMessage(data={"message": str(exception)}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.host.forward(error_message)

    async def pass_cancelled_done(self, message: BouncedUnassignMessage):
        error_message = UnassignDoneMessage(data={"assignation": message.data.assignation}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.host.forward(error_message)

    async def pass_cancelled_failed(self, message: BouncedUnassignMessage, exception: Union[Exception,str]):
        error_message = UnassignCriticalMessage(data={"message": str(exception)}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.host.forward(error_message)


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



T = TypeVar("T")
assign_var = contextvars.ContextVar('assign', default=None)
reservation_var = contextvars.ContextVar("reservation", default=None)

class Actor(Generic[T]):

    def __init__(self, helper: HostHelper, queue:asyncio.Queue = None, loop=None) -> None:
        self.queue = queue or asyncio.Queue()
        self.helper = helper
        self.loop = loop
        self._provided = False
        self.assignments = {}
        self.reservations = {}

        self._current_provision_context = None
        pass

    async def _on_provide(self, bounced_provide: BouncedProvideMessage):
        self.template_id = bounced_provide.data.template
        self.template = await Template.asyncs.get(id=self.template_id)
        self._current_provision_context = await self.on_provide(bounced_provide)
        self._provided = True
    

    @property
    def current_bounced(self):
        message: BouncedForwardedAssignMessage = assign_var.get()
        return message.meta.token

    @property
    def current_reservation_context(self):
        return reservation_var.get()

    @property
    def current_provision_context(self):
        return self._current_provision_context

    async def on_provide(self, bounced_provide):
        pass

    def check_if_assignation_cancelled(self, assign, task: Task):
        if task.cancelled():
            console.log(f"[yellow] Assignation {task.get_name()} Cancelled and is now Done")
        elif task.exception():
            console.log(f"[red] Assignation {task.get_name()} Failed with {str(task.exception())}")
        elif task.done():
            console.log(f"[green] Assignation {task.get_name()} Succeeded and is now Done")

    async def on_reserve(self, message) -> T:
        return None

    async def on_unreserve(self, reservations: T) -> T:
        return None

    async def _on_reserve(self, message: BouncedForwardedReserveMessage):
        try:
            console.log("[magenta] Reserving")
            reservation_results = await self.on_reserve(message)
            self.reservations[message.meta.reference] = reservation_results

            console.log(f"[magenta] Reservation Done {message.meta.reference}")
            await self.helper.forward(message)

        except Exception as e:
            console.print_exception()
            await self.helper.forward(ReserveCriticalMessage(data={"message": str(e)}, meta={**message.meta.dict(), "type": RESERVE_CRITICAL}))

    async def _on_unreserve(self, message: BouncedUnreserveMessage):
        try:
            console.log("[magenta] Unreserving")
            info = await self.on_unreserve(self.reservations[message.data.reservation])
            del self.reservations[message.data.reservation]
            await self.helper.forward(message)
        except Exception as e:
            console.print_exception()
            await self.helper.forward(ReserveCriticalMessage(data={"message": str(e)}, meta={**message.meta, "type": RESERVE_CRITICAL}))
            
    async def run(self, bounced_provide: BouncedProvideMessage):
        ''' An infinitie loop assigning to itself'''
        try:

            await self._on_provide(bounced_provide)

            try:
                assert self._provided, "We didnt provide this actor before running"
                
                while True:
                    message = await self.queue.get()
                    logger.info("")

                    if isinstance(message, BouncedForwardedReserveMessage):
                        console.log(f"[green] Reservation")
                        await self._on_reserve(message)

                    elif isinstance(message, BouncedUnreserveMessage):
                        console.log(f"[magenta] Unreservation")
                        await self._on_unreserve(message)

                    elif isinstance(message, BouncedForwardedAssignMessage):
                        console.log(f"[green] Assigning")
                        task = asyncio.create_task(self.on_assign(message))
                        task.add_done_callback(partial(self.check_if_assignation_cancelled, message))
                        self.assignments[message.meta.reference] = task

                    elif isinstance(message, BouncedUnassignMessage):
                        console.log(f"[yellow] Cancellation of Assignment")
                        if message.data.assignation in self.assignments: 
                            console.log("Cancellation for task received. Canceling!")
                            task = self.assignments[message.data.assignation]
                            if not task.done():
                                task.cancel()
                                await self.helper.pass_cancelled_done(message)

                                console.log("Canceled Task!!")
                            else:
                                await self.helper.pass_cancelled_failed(message, "Task was already Done")
                                console.log("Task had already finished")
                                #TODO: Maybe send this to arkitekt as well?
                        else:
                            raise Exception("Assignment never was at this pod. something went wrong")

                    else:
                        raise Exception(f"Type not known {message}")

                    self.queue.task_done()


            except asyncio.CancelledError:
                await self.on_unprovide()
                raise

        except Exception as e:
            console.print_exception()

    async def _on_unprovide(self):
        await self.on_unprovide()

    async def on_unprovide(self):
        pass

    async def _progress(self, value, percentage):
        message = assign_var.get()
        await self.helper.pass_progress(message, value, percentage=percentage)

    async def on_assign(self, assign: BouncedForwardedAssignMessage):
        try:
            args, kwargs = await expandInputs(node=self.template.node, args=assign.data.args, kwargs=assign.data.kwargs)
            console.log(args, kwargs)
            assign_var.set(assign)
            reservation_var.set(self.reservations[assign.data.reservation])
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


