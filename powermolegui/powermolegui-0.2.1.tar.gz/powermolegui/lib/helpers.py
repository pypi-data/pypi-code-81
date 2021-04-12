#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: helpers.py
#
# Copyright 2021 Vincent Schouten
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Import all parts from helpers here.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import logging
import threading
from time import sleep
from powermolelib import Configuration
from powermolelib.powermolelibexceptions import InvalidConfigurationFile
from powermolegui.lib.logging import LoggerMixin, LOGGER_BASENAME as ROOT_LOGGER_BASENAME
from powermolegui.lib.items import ClientCanvasItem, HostCanvasItem, ConnectionCanvasItem, AgentCanvasItem, \
    PacketCanvasItem, StatusBannerCanvasItem
from powermolegui.powermoleguiexceptions import SetupFailed

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''08-10-2020'''
__copyright__ = '''Copyright 2021, Vincent Schouten'''
__credits__ = ["Vincent Schouten"]
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging.
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(f'{ROOT_LOGGER_BASENAME}.helpers')  # non-class objects like fn will consult this object


def parse_configuration_file(config_file_path):
    """Parses the configuration file to a (dictionary) object."""
    try:
        configuration = Configuration(config_file_path)
    except InvalidConfigurationFile:
        return None
    if configuration.mode == 'FOR':
        LOGGER.info('mode FOR enabled')
    elif configuration.mode == 'TOR':
        LOGGER.info('mode TOR enabled')
    elif configuration.mode == 'PLAIN':
        LOGGER.info('mode PLAIN enabled')
    return configuration


class ItemsGenerator(LoggerMixin):
    """Creates items for the components Client, Connection(s), Host(s) and Agent."""

    def __init__(self, main_window, configuration):
        """Initialize the ShapeGenerator object."""
        super().__init__()
        self.main_window = main_window
        self.config = configuration
        self.status = main_window.main_frame.canvas_frame.canvas_status
        self.canvas = main_window.main_frame.canvas_frame.canvas_landscape
        self.scale = main_window.scale
        self.iteration = 0
        self.quit = False
        self._wipe_canvas()

    def _wipe_canvas(self):
        self.canvas.delete("all")

    def create_canvas_items(self):
        """Create all items and hide.

        The number of host items are derived on the total amount of hosts.
        The ConnectionCanvasItem needs not-hidden items to create a connection_canvas_item as it uses bbox.
        Bbox cannot work with hidden items.
        Once all canvas items are created, they are hidden.

        Returns:
            A list containing items. Each type of item has its own position:
            • element 0: client - the Client is given an unique position on the X-axis
            • element 1: [hosts] - each Host is given an unique position on the X-axis
            • element 2: [connection] - each Connection is given its from and to destination
            • element 3: agent - an Agent is a 'child' of the target destination host

        """
        start_y_pos = 60 * self.scale
        start_x_pos = 70 * self.scale
        amount_hosts = len(self.config.gateways) + 1
        client_item = ClientCanvasItem(self.main_window, start_x_pos, start_y_pos)
        host_items = []
        connection_items = []
        for i in range(amount_hosts):
            start_x_pos += 220 * self.scale
            host_item = HostCanvasItem(self.main_window, start_x_pos, start_y_pos)
            host_items.append(host_item)
            if i == 0:
                connection_item = ConnectionCanvasItem(self.main_window, client_item, host_items[i])
            else:
                connection_item = ConnectionCanvasItem(self.main_window, host_items[i - 1], host_items[i])
            connection_items.append(connection_item)
        agent_item = AgentCanvasItem(self.main_window, client_item, host_items[-1])
        packet_item = PacketCanvasItem(self.main_window, connection_items)
        status_item = StatusBannerCanvasItem(self.main_window)
        self.status.itemconfig('all', state='hidden')
        self.canvas.itemconfig('all', state='hidden')
        return client_item, host_items, connection_items, agent_item, packet_item, status_item

    def show_landscape(self, canvas_items):  # pylint: disable=no-self-use
        """Shows the shapes of Client and Host(s).

        Modifying the scroll region only works after the items
        have been changed ("configured") from hidden to normal.

        """
        client_item, host_items, _, _, _, status_item = canvas_items
        sleep(0.5)  # otherwise the drawing begins earlier than the eye notices
        client_item.show()  # show client item
        for host in host_items:  # show host items
            host.show()
            sleep(0.1)  # to allow this host to finish flickering before the next host is shown
        status_item.show()


class ClientAdapter:
    """."""  # need Costas to help me fill out docstring

    def __init__(self, item):
        """____________."""
        self.item = item

    def __str__(self):
        return 'Client'

    def stop(self):
        """____________."""
        self.item.dim()
        return True


class TunnelAdapter:
    """Adapts a tunnel object to a representational state for the GUI."""

    def __init__(self, object_, items):
        """____________."""
        # self.__class__.__name__ = 'Tunnel'
        self.object_ = object_
        self.items = items

    def __str__(self):
        return 'Tunnel'

    def stop(self):
        """____________."""
        for item in self.items:
            item.hide()
        return self.object_.stop()


class HostAdapter:
    """Adapts a host object to a representational state for the GUI."""

    def __init__(self, items):
        """____________."""
        self.items = items

    def __str__(self):
        return 'Host'

    def stop(self):
        """____________."""
        for host in self.items:
            host.dim()
        return True


class AgentAdapter:
    """Adapts an agent object to a representational state for the GUI."""

    def __init__(self, item):
        """____________."""
        self.item = item

    def __str__(self):
        return 'Agent'

    def stop(self):
        """____________."""
        self.item.dim()
        return True


class SetupLink(LoggerMixin):  # pylint: disable=too-many-instance-attributes
    """Establishes a connection to target destination host via intermediaries by starting various objects.

    This function also passes the instantiated objects to the StateManager, which
    will stop the Tunnel and Instructor after a KeyboardInterrupt (by the user
    or by the program (in FILE mode)).
    """

    def __init__(self, state, transfer_agent, tunnel, bootstrap_agent, instructor,  # pylint: disable=too-many-arguments
                 client_item, host_items, agent_item, connection_items):
        """Initializes the SetupLink object.

        Args:
            state (StateManager): An instantiated StateManager object.
            transfer_agent (TransferAgent): An instantiated TransferAgent object.
            tunnel (Tunnel): An instantiated Tunnel object.
            bootstrap_agent (BootstrapAgent): ...
            instructor (Instructor): ...
            client_item (ClientCanvasItem): ...
            host_items (HostCanvasItem): ...
            agent_item (AgentCanvasItem): ...
            connection_items (ConnectionCanvasItem): ...

        """
        super().__init__()
        self.is_terminate_query_scp = False
        self.terminate_query_ssh = False
        self.state = state
        self.transfer_agent = transfer_agent
        self.tunnel = tunnel
        self.bootstrap_agent = bootstrap_agent
        self.instructor = instructor
        self.client_item = client_item
        self.host_items = host_items
        self.agent_item = agent_item
        self.connection_items = connection_items

    def start(self):
        """."""
        self.start_client()
        self.start_transfer_agent()
        self.start_tunnel()
        self.start_bootstrap_agent()
        self.start_instructor()

    def _query_connection_transfer_agent(self):
        self._logger.debug('querying for authenticated hosts...')
        while True:
            if len(self.transfer_agent.authenticated_hosts) == len(self.transfer_agent.all_hosts):
                self.agent_item.move()
                break
            if self.is_terminate_query_scp:
                break

    def _query_ssh_proxyjump_connection(self):
        """Shows a connection canvas item every time the tunnel.authenticated_hosts is appended with a new host."""
        self._logger.debug('querying for authenticated hosts...')
        index = 0
        while index < len(self.tunnel.all_hosts):
            if index == 0 and self.tunnel.all_hosts[index] in self.tunnel.authenticated_hosts:  # shows the 1st conn.
                self.connection_items[index].show()
                index += 1
            if index > 0 and self.tunnel.all_hosts[index] in self.tunnel.authenticated_hosts:  # shows the nth conn.
                self.connection_items[index].show()
                index += 1
            if self.is_terminate_query_scp:
                break
            sleep(0.1)  # otherwise, tk behaves erratic; drawing 2 moving canvas items simultaneously

    def start_client(self):
        """Shows the client item.

        This method also adds the instance of the client adapter to the context manager.

        """
        self.state.add_object(ClientAdapter(self.client_item))
        self.client_item.setup_ok()

    def start_transfer_agent(self):
        """."""
        # the TransferAgent object is a disposable one-trick pony
        # no need to invoke state.add_object()
        self.agent_item.show()
        thread = threading.Thread(target=self._query_connection_transfer_agent)
        thread.start()
        if not self.transfer_agent.start():
            self.agent_item.transfer_nok()
            self.is_terminate_query_scp = True
            raise SetupFailed(self.transfer_agent)
        while not thread.is_alive():
            break
        self.agent_item.transfer_ok()
        self._logger.info('Agent has been transferred securely to destination host')
        sleep(0.15)  # to keep following the movements of items on canvas possible

    def start_tunnel(self):
        """."""
        self.state.add_object(TunnelAdapter(self.tunnel, self.connection_items))
        self.state.add_object(HostAdapter(self.host_items))
        thread = threading.Thread(target=self._query_ssh_proxyjump_connection)
        thread.start()
        if not self.tunnel.start():
            for conn, host in zip(self.connection_items, self.host_items):
                conn.setup_nok()
                host.setup_nok()
            self.terminate_query_ssh = True
            raise SetupFailed(self.tunnel)
        self._logger.info('Tunnel has been opened...')
        while not thread.is_alive():
            break
        for conn, host in zip(self.connection_items, self.host_items):
            conn.setup_ok()
            host.setup_ok()
        sleep(0.15)  # to keep following the movements of items on canvas possible

    def start_bootstrap_agent(self):
        """."""
        # the BootstrapAgent object is a disposable one-trick pony
        if not self.bootstrap_agent.start():
            self.agent_item.setup_nok()
            raise SetupFailed(self.bootstrap_agent)
        self._logger.info('Agent has been executed')
        self.agent_item.setup_ok()

    def start_instructor(self):
        """."""
        self.state.add_object(self.instructor)
        self.state.add_object(AgentAdapter(self.agent_item))
        if not self.instructor.start():
            self.agent_item.setup_nok()
            raise SetupFailed(self.instructor)
        self._logger.info('Instructor has been executed')
        self.agent_item.setup_ok()


class StateVisualiser:  # pylint: disable=too-few-public-methods
    """Shows the state of the encrypted tunnel by a banner and by visualising the packet flow."""

    def __init__(self, heartbeat, animated_packet, status_item):
        """Initializes the StateVisualiser object.

        Args:
            animated_packet: __________
            heartbeat: An instantiated Heartbeat context manager object which determines periodically the
                        state of the tunnel.
            status_item: __________

        """
        self.animated_packet = animated_packet
        self.heartbeat = heartbeat
        self.status_item = status_item

    def start(self):
        """_____________."""
        self.status_item.show('established')
        self.animated_packet.start()
        while not self.heartbeat.terminate:
            if not self.heartbeat.is_tunnel_intact:
                self.status_item.show('broken')
                self.animated_packet.pause()
                while not self.heartbeat.is_tunnel_intact:
                    sleep(0.2)
                self.status_item.show('restored')
                self.animated_packet.resume()
            sleep(0.2)
        self.animated_packet.stop()
        self.status_item.dim()
