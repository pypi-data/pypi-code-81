

from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from bergen.messages.postman.unprovide.unprovide_critical import UnprovideCriticalMessage
from bergen.messages.postman.unprovide.unprovide_progress import UnprovideProgressMessage
from bergen.messages.postman.provide.provide_critical import ProvideCriticalMessage
from bergen.messages.postman.unprovide import BouncedUnprovideMessage, UnprovideDoneMessage
from bergen.clients.base import BaseBergen
from bergen.messages.base import MessageModel
from bergen.hookable.base import Hookable, hookable
from bergen.entertainer.actor import Actor, AsyncFuncActor, AsyncGenActor, ThreadedFuncActor
from bergen.messages.postman.assign.assign import AssignMessage
from bergen.provider.utils import createNodeFromActor, createNodeFromFunction
from bergen.console import console
from pydantic.main import BaseModel
from bergen.types.node import ports
from typing import Dict, Tuple, TypedDict, Union
from bergen.utils import ExpansionError, expandInputs, shrinkOutputs
from bergen.schema import Template, NodeType
from bergen.constants import ACCEPT_GQL, OFFER_GQL, SERVE_GQL
import logging
import namegenerator
import asyncio
import websockets
from bergen.models import Node, Pod
import inspect
import sys
from aiostream import stream
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial
logger = logging.getLogger()
import copy
import json
from bergen.types.model import ArnheimModel
import uuid
from bergen.messages.postman.provide import BouncedProvideMessage, ProvideProgressMessage, BouncedCancelProvideMessage


class BaseHelper(ABC):

    def __init__(self, peasent) -> None:
        self.peasent = peasent
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


class AssignationHelper():

    def __init__(self, peasent_helper: BaseHelper, message: AssignMessage, loop: AbstractEventLoop = None) -> None:
        self.peasent_helper = peasent_helper
        self.message = message
        self.loop = loop
        pass

    @abstractmethod
    def progress(self, value, percentage=None):
        pass



class ThreadedAssignationHelper(AssignationHelper):

    def progress(self, value, percentage=None):
        logger.info(f'{percentage if percentage else "--"} : {value}')
        if self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.peasent_helper.pass_progress(self.message, value, percentage=percentage), self.loop)
            return future.result()
        else:
            self.loop.run_until_complete(self.peasent_helper.pass_progress(self.message, value, percentage=percentage))


class AsyncAssignationHelper(AssignationHelper):

    async def progress(self, value, percentage=None):
        logger.info(f'{percentage if percentage else "--"} : {value}')
        await self.peasent_helper.pass_progress(self.message, value, percentage=percentage)



async def shrink(node_template_pod, outputs):
    kwargs = {}
    if isinstance(node_template_pod, Node):
        kwargs = await shrinkOutputs(node=node_template_pod, outputs=outputs)

    if isinstance(node_template_pod, Template):
        kwargs = await shrinkOutputs(node=node_template_pod.node, outputs=outputs)

    if isinstance(node_template_pod, Pod):
        kwargs = await shrinkOutputs(node=node_template_pod.template.node, outputs=outputs)


    return kwargs



async def expand(node_template_pod, inputs):
    kwargs = {}
    if isinstance(node_template_pod, Node):
        kwargs = await expandInputs(node=node_template_pod, inputs=inputs)

    if isinstance(node_template_pod, Template):
        kwargs = await expandInputs(node=node_template_pod.node, inputs=inputs)

    if isinstance(node_template_pod, Pod):
        kwargs = await expandInputs(node=node_template_pod.template.node, inputs=inputs) 
    return kwargs



threadhelper = None
try: 
    threadhelper = asyncio.to_thread
except:
    logger.warn("Threading does not work below Python 3.9")



class PodPolicy(BaseModel):
    type: str



class OneExlusivePodPolicy(PodPolicy):
    type: str = "one-exclusive"

class MultiplePodPolicy(PodPolicy):
    type: str = "multiple"



def isactor(type):
    try:
        if issubclass(type, Actor):
            return True
        else:
            return False
    except Exception as e:
        return False



class BaseProvider(Hookable):
    ''' Is a mixin for Our Bergen '''
    helperClass = None


    def __init__(self, *args, provider: int = None, loop=None, client: BaseBergen =None, **kwargs) -> None:
        super().__init__(**kwargs)
        assert provider is not None, "Provider was set to none, this is weird!!"
        self.arkitekt_provider = provider
        self.client = client
        self.loop = loop or asyncio.get_event_loop()

        self.template_actorClass_map = {}

        self.provisions = {}
        self.auto_provided_templates = [] # Templates that this provide will try to provide on startup


    def template(self, node: Node, policy: PodPolicy = MultiplePodPolicy(), auto_provide=False, on_provide=None,  on_unprovide=None, **implementation_details):

        def real_decorator(function_or_actor):
            assert callable(function_or_actor) or issubclass(function_or_actor, Actor), "Please only decorate functions or subclasses of Actor"
            # TODO: Check if function has same parameters as node

            template = OFFER_GQL.run(
            ward=self.client.main_ward,
            variables= {
                "node": node.id,
                "params": implementation_details,
                "policy": policy.dict()
            })


            if isactor(function_or_actor):
                actorClass = function_or_actor
            else:
                is_coroutine = inspect.iscoroutinefunction(function_or_actor)
                is_asyncgen = inspect.isasyncgenfunction(function_or_actor)
                is_function = inspect.isfunction(function_or_actor)

                if is_coroutine:
                    actorClass =  type(f"GeneratedActorNode{node.id}",(AsyncFuncActor,), {"assign": function_or_actor})
                elif is_asyncgen:
                    actorClass =  type(f"GeneratedActorNode{node.id}",(AsyncGenActor,), {"assign": function_or_actor})
                elif is_function:
                    actorClass = type(f"GeneratedActorNode{node.id}",(ThreadedFuncActor,), {"assign": function_or_actor})
                else:
                    raise Exception(f"Unknown type of function {function_or_actor}")
            
            self.template_actorClass_map[str(template.id)] = actorClass
            return actorClass

        return real_decorator


    def enable(self, allow_empty_doc=False, widgets={}, **implementation_details):
        """Enables the decorating function as a node on the Arnheim, you will find it as
        @provider/

        Args:
            allow_empty_doc (bool, optional): Allow the enabled function to not have a documentation. Will automatically downlevel the Node Defaults to False.
            widgets (dict, optional): Enable special widgets for the parameters. Defaults to {}.
        """
        def real_decorator(function_or_actor):
            assert callable(function_or_actor) or issubclass(function_or_actor, Actor), "Please only decorate functions or subclasses of Actor"

            if isactor(function_or_actor):
                console.log("Already is Actor. Creating Node")
                node = createNodeFromActor(function_or_actor, allow_empty_doc=allow_empty_doc, widgets=widgets)
            else:
                console.log("Is Function. Creating Node and Wrapping")
                node = createNodeFromFunction(function_or_actor, allow_empty_doc=allow_empty_doc, widgets=widgets)

            console.log("Created Node",node)
                
            # We pass this down to our truly template wrapper that takes the node and transforms it
            template_wrapper = self.template(node, **implementation_details)
            function = template_wrapper(function_or_actor)
            return function

        return real_decorator


    @abstractmethod
    async def connect(self) -> str:
        raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def disconnect(self) -> str:
        raise NotImplementedError("Please overwrite")


    @abstractmethod
    async def forward(self, message: MessageModel) -> None:
        raise NotImplementedError("Please overwrite")


    async def on_message(self, message: MessageModel):
        if isinstance(message, BouncedProvideMessage):
            logger.info("Received Provide Request")
            assert message.data.template is not None, "Received Provision that had no Template???"
            await self.handle_bounced_provide(message)

        elif isinstance(message, BouncedUnprovideMessage):
            logger.info("Received Unprovide Request")
            assert message.data.provision is not None, "Received Unprovision that had no Provision???"
            await self.handle_bounced_unprovide(message)

        else: 
            raise Exception("Received Unknown Task")


    async def handle_bounced_provide(self, message: BouncedProvideMessage):
        try:
            await self.on_bounced_provide(message)

            progress = ProvideProgressMessage(data={
            "level": "INFO",
            "message": f"Pod Pending"
            }, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})

            await self.forward(progress)
        except Exception as e:
            logger.error(e)
            critical_error = ProvideCriticalMessage(data={
            "message": str(e)
            }, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
            await self.forward(critical_error)
            raise e

    async def handle_bounced_unprovide(self, message: BouncedProvideMessage):
        try:
            await self.on_bounced_unprovide(message)

            progress = UnprovideProgressMessage(data={
            "level": "INFO",
            "message": f"Pod Unproviding"
            }, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})

            await self.forward(progress)

        except Exception as e:
            logger.error(e)
            critical_error = UnprovideCriticalMessage(data={
            "message": str(e)
            }, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})

            await self.forward(critical_error)


    @hookable("bounced_provide", overwritable=True)
    async def on_bounced_provide(self, message: BouncedProvideMessage):
        pod, task = await self.provideTemplate(message, message.data.template)
        self.provisions[message.meta.reference] = task # Run in parallel

    @hookable("bounced_unprovide", overwritable=True)
    async def on_bounced_unprovide(self, message: BouncedUnprovideMessage):
        logger.error("Overwrite me")


    
    async def provideTemplate(self, message, template_id: str):
        assert template_id in self.template_actorClass_map, f"There is no function registered for this template {template_id} not it {self.template_actorClass_map.keys()}"
            
        actorClass = self.template_actorClass_map[template_id]
        self.client.entertainer.registerActor(template_id, actorClass)
        return await self.client.entertainer.entertain(message)



    async def provide_async(self):
        while True:
            await asyncio.sleep(3)

    def provide(self):
        if self.loop.is_running():
            logger.error("Cannot do this, please await run()")
        else:
            self.loop.run_forever()

        # we enter a never-ending loop that waits for data
        # and runs callbacks whenever necessary.
        

