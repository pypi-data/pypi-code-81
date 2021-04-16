import asyncio
import traceback

from typing import Union, Callable, Type, Optional, TypeVar, Any
from logging import Logger, INFO, ERROR, WARN, getLevelName
from applipy.application.apphandle import AppHandle
from applipy.application.module import Module
from applipy.config.config import Config
from applipy_inject import Injector


T = TypeVar('T')
BindFunction = Callable[
    [
        Type[T],
        Union[T, Callable[[Any], T]],
        Optional[str],
        Optional[bool]
    ],
    None
]
RegisterFunction = Callable[[Module], None]


class ModuleManager:

    def __init__(self, injector: Injector) -> None:
        self._injector = injector
        self._modules = set()

    def install(self, module: Type[Module]) -> 'ModuleManager':
        if module not in self._modules:
            self._modules.add(module)
            self._injector.bind_provider(Module, module)
            for dep in module.depends_on():
                self.install(dep)

        return self

    def configure_all(self, bind_function: BindFunction,
                      register_function: RegisterFunction) -> None:
        instances = self.injector.get_all(Module)
        for instance in instances:
            instance.configure(bind_function, register_function)
            self._log(INFO, f'Installing module `{instance.__class__.__module__}.{instance.__class__.__name__}`')

        self._modules = set()

    @property
    def injector(self):
        return self._injector

    def _log(self, level, fmt, *args, **kwargs):
        try:
            self._injector.get(Logger).log(level, fmt, *args, **kwargs)
        except Exception:
            print(f"[{getLevelName(level)}]", fmt % args)


AppHandleProvider = Union[Type[AppHandle], Callable[[], AppHandle]]


class AppHandleManager:

    def __init__(self, injector: Injector) -> None:
        self._injector = injector

    def register(self,
                 app_handle_provider: AppHandleProvider) -> 'AppHandleManager':
        self._injector.bind_provider(AppHandle, app_handle_provider)

    async def init_all(self):
        app_handles = self._injector.get_all(AppHandle)
        tasks = (asyncio.get_event_loop().create_task(app_handle.on_init(),
                                                      name=app_handle.__class__.__name__ + '.on_init')
                 for app_handle in app_handles)
        await asyncio.gather(*tasks, return_exceptions=True)

    async def start_all(self):
        app_handles = self._injector.get_all(AppHandle)
        tasks = (asyncio.get_event_loop().create_task(app_handle.on_start(),
                                                      name=app_handle.__class__.__name__ + '.on_start')
                 for app_handle in app_handles)
        await asyncio.gather(*tasks, return_exceptions=True)

    async def shutdown_all(self):
        app_handles = self._injector.get_all(AppHandle)
        tasks = (asyncio.get_event_loop().create_task(app_handle.on_shutdown(),
                                                      name=app_handle.__class__.__name__ + '.on_shutdown')
                 for app_handle in app_handles)
        await asyncio.gather(*tasks, return_exceptions=True)


class Application:

    def __init__(self,
                 config,
                 shutdown_timeout_seconds=1,
                 injector=None,
                 module_manager=None,
                 app_handle_manager=None,
                 loop=None,
                 signal_=None):
        self._config = config
        self._shutdown_timeout_seconds = shutdown_timeout_seconds
        self._loop = loop
        self._injector = injector or Injector()
        self._app_handle_manager = (app_handle_manager or AppHandleManager(self._injector))
        self._module_manager = module_manager or ModuleManager(self._injector)
        self._running = False

    def install(self, module):
        self._module_manager.install(module)
        return self

    def register(self, app_handle_provider):
        self._app_handle_manager.register(app_handle_provider)
        return self

    @property
    def injector(self):
        return self._injector

    def run(self):
        self._loop = self._loop or asyncio.get_event_loop()

        self._injector.bind(Config, self._config)
        self._module_manager.configure_all(
            self._injector.bind,
            self._app_handle_manager.register
        )

        core_tasks = []

        self._running = True
        app_name = self._config.get('app.name', 'applipy')
        core_tasks.append(self._loop.create_task(self._run_app(), name=app_name))
        self._loop.run_forever()
        self._running = False
        core_tasks.append(self._loop.create_task(self._shutdown_app(), name=app_name + '.shutdown_app'))

        core_tasks.append(
            self._loop.create_task(asyncio.wait_for(self._loop.shutdown_asyncgens(), self._shutdown_timeout_seconds),
                                   name=app_name + '.shutdown_asyncgens')
        )
        if hasattr(self._loop, 'shutdown_default_executor'):
            core_tasks.append(
                self._loop.create_task(asyncio.wait_for(self._loop.shutdown_default_executor(),
                                                        self._shutdown_timeout_seconds),
                                       name=app_name + '.shutdown_default_executor')
            )

        self._cancel_loop_tasks(core_tasks)

    def stop(self):
        if self._loop is not None:
            self._loop.stop()

    async def _run_app(self):
        try:
            await self._app_handle_manager.init_all()
            await self._app_handle_manager.start_all()
        except asyncio.CancelledError:
            self._log(WARN, traceback.format_exc())
        except Exception:
            self._log(ERROR, traceback.format_exc())
        finally:
            if self._running:
                self.stop()

    async def _shutdown_app(self):
        try:
            await asyncio.wait_for(self._app_handle_manager.shutdown_all(), self._shutdown_timeout_seconds)
        except asyncio.TimeoutError:
            self._log(ERROR, traceback.format_exc())

    def _cancel_loop_tasks(self, core_tasks):
        core_future = asyncio.gather(*core_tasks)
        try:
            self._loop.run_until_complete(asyncio.wait_for(asyncio.shield(core_future), self._shutdown_timeout_seconds))
        except asyncio.TimeoutError:
            for t in (t for t in asyncio.all_tasks(self._loop) if not t.done() and t not in core_tasks):
                t.cancel()
                self._log(WARN, 'Cancelled task %s', t.get_name())
        try:
            self._loop.run_until_complete(asyncio.wait_for(asyncio.shield(core_future), self._shutdown_timeout_seconds))
        except asyncio.TimeoutError:
            for t in (t for t in asyncio.all_tasks(self._loop) if not t.done()):
                t.cancel()
                self._log(ERROR, "Task %s didn't finish", t.get_name())

    def _log(self, level, fmt, *args, **kwargs):
        try:
            self._injector.get(Logger).log(level, fmt, *args, **kwargs)
        except Exception:
            print(f"[{getLevelName(level)}]", fmt % args)
