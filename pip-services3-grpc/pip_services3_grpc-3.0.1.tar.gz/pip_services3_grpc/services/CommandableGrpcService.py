# -*- coding: utf-8 -*-

from abc import ABC

from pip_services3_commons.commands.ICommandable import ICommandable
from pip_services3_commons.commands.CommandSet import CommandSet

from .GrpcService import GrpcService


class CommandableGrpcService(GrpcService, ABC):
    __name = ''
    __command_set = None

    def __init__(self, name):
        super().__init__(None)
        self.__name = name
        self._dependency_resolver.put('controller', 'none')

    # Registers all service routes in gRPC endpoint.
    # Call automaticaly in open component procedure
    def register(self):
        controller = self._dependency_resolver.get_one_required('controller')
        self.__command_set = controller.get_command_set()

        commands = self.__command_set.get_commands()

        for index in range(0, len(commands)):
            command = commands[index]
            method = '' + self.__name + '.' + command.get_name()

            def inner(correlation_id, args, getted_method):
                for _index in range(0, len(commands)):
                    _command = commands[_index]
                    _method = '' + self.__name + '.' + _command.get_name()
                    if getted_method == _method:
                        timing = self._instrument(correlation_id, _method)

                        try:
                            result = _command.execute(correlation_id, args)
                            timing.end_timing()
                            return result
                        except Exception as ex:
                            timing.end_timing()
                            self._instrument_error(correlation_id, _method, ex, True)

            self.register_commadable_method(method, None, inner)
