#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: items.py
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
Main code for various tkinter canvas items.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import uuid
import re
from abc import ABC, abstractmethod
from itertools import cycle

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''06-12-2019'''
__copyright__ = '''Copyright 2021, Vincent Schouten'''
__credits__ = ["Vincent Schouten"]
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# Constants
FONT_SIZE = 10
THICKNESS_LINE_CLIENT = 2
THICKNESS_LINE_HOST = 2
THICKNESS_LINE_AGENT = 2
THICKNESS_LINE_TUNNEL = 1
THICKNESS_LINE_PACKET = 1
THICKNESS_PACKET = 2
WIDTH_PACKET = 20
BACKGROUND_CANVAS = '#232729'
LABEL_FONT_COLOUR = 'white'
PACKET_OUTLINE_COLOUR = '#c0c0c0'
PACKET_FILL_COLOUR = '#232729'
NON_OPERATION = 'white'
OK_COLOUR = 'green'
NOK_COLOUR = 'red'


class CanvasItem(ABC):
    """Enforces methods to be implemented and provide other methods for the subclasses of this object to operate."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.canvas_landscape = main_window.main_frame.canvas_frame.canvas_landscape
        self.canvas_status = main_window.main_frame.canvas_frame.canvas_status
        self.scale = main_window.scale
        self.item_name = self._determine_item_name()
        self.tag = f"{self.item_name}-{self._uuid}"
        self.label = 0

    @property
    def _uuid(self):
        uuid_ = f'{uuid.uuid4().hex}'
        return uuid_

    def _determine_item_name(self):
        return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', type(self).__name__)[0]  # split words at CamelCase

    def _add_label(self):
        coord_x1, coord_y1, coord_x2, _ = self.canvas_landscape.coords(self.tag)
        distance = coord_x2 - coord_x1
        pos_x = coord_x1 + (distance / 2)  # to determine the coordinates of the center of the shape (host/client)
        pos_y = coord_y1 - (10 * self.scale)  # put the label a few pixels above the shape
        self.label = self.canvas_landscape.create_text(pos_x,
                                                       pos_y,
                                                       text=self.item_name,
                                                       font=('', FONT_SIZE, 'normal'),
                                                       fill=LABEL_FONT_COLOUR)

    @abstractmethod
    def show(self):
        """Shows the item."""

    @abstractmethod
    def hide(self):
        """Hides the item."""

    @abstractmethod
    def setup_ok(self):
        """________________."""

    @abstractmethod
    def setup_nok(self):
        """."""

    @abstractmethod
    def dim(self):
        """."""


class Effect:
    """."""

    def __init__(self, main_window, canvas_item, filling_type):
        self.canvas_landscape = main_window.main_frame.canvas_frame.canvas_landscape
        self.canvas_status = main_window.main_frame.canvas_frame.canvas_status
        self.flicker_index = 0
        self.canvas_item = canvas_item
        self.filling_type = filling_type

    def flicker(self):
        """Changes the brightness of the canvas item irregularly appearing as a fluctuating light.

        The after function is threaded, so it doesn't block.

        """
        self.canvas_landscape.itemconfig(self.canvas_item, state='normal')
        colours = ['#b2b2b2', '#b2b2b2', '#7f7f7f', '#b2b2b2', 'white']
        colour_cycle = cycle(colours)
        max_elements = len(colours)

        def _flicker():
            self.flicker_index += 1
            selected_colour = next(colour_cycle)
            if self.filling_type == 'outline':
                self.canvas_landscape.itemconfig(self.canvas_item, outline=selected_colour)
                self.canvas_status.itemconfig(self.canvas_item, outline=selected_colour)
            elif self.filling_type == 'fill':
                self.canvas_landscape.itemconfig(self.canvas_item, fill=selected_colour)
                self.canvas_status.itemconfig(self.canvas_item, fill=selected_colour)
            if self.flicker_index == max_elements:
                return
            self.canvas_landscape.after(120, _flicker)
        _flicker()

    def setup_ok(self):
        """Colours the canvas item to state OK (green)."""
        arguments = {self.filling_type: OK_COLOUR}
        self.canvas_landscape.itemconfig(self.canvas_item, **arguments)
        self.canvas_status.itemconfig(self.canvas_item, **arguments)

    def setup_nok(self):
        """Colours the canvas item to state NOK (red)."""
        arguments = {self.filling_type: NOK_COLOUR}
        self.canvas_landscape.itemconfig(self.canvas_item, **arguments)
        self.canvas_status.itemconfig(self.canvas_item, **arguments)

    def dim(self):
        """Colours the canvas item to a non-operational state (white).

        To colour the outline of 'rectangles', the outline has to be configured.
        To colour the items made of 'lines', the fill has to be configured.
        """
        arguments = {self.filling_type: NON_OPERATION}
        self.canvas_landscape.itemconfig(self.canvas_item, **arguments)
        self.canvas_status.itemconfig(self.canvas_item, **arguments)


class ConnectionCalculator:
    """Calculates all properties that is needed to render a connection between two canvas items."""

    def __init__(self, main_window, component_a, component_b):
        """Initialize the ConnectionCalculator object.

        Note: canvas.bbox doesn't return values when the item's state is 'hidden'

        Args:
            main_window: ______
            component_a: ______
            component_b: ______

        """
        self.canvas_landscape = main_window.main_frame.canvas_frame.canvas_landscape
        self.component_a = component_a.tag
        self.component_b = component_b.tag
        self.factor = 0.05

    def get_connection_length_inner(self):
        """Returns the distance between two items starting from right side first item to left side second item."""
        _, _, ax2, _ = self.canvas_landscape.bbox(self.component_a)
        bx1, _, _, _ = self.canvas_landscape.bbox(self.component_b)
        distance = bx1 - ax2
        return distance

    def get_connection_length_outer(self):
        """Returns the distance between two items starting from right side first item to left side second item."""
        ax1, _, _, _ = self.canvas_landscape.bbox(self.component_a)
        _, _, bx2, _ = self.canvas_landscape.bbox(self.component_b)
        distance = bx2 - ax1
        return distance

    def get_connection_height(self):
        """Returns the height of a connection based on the height of the item."""
        _, by1, _, by2 = self.canvas_landscape.bbox(self.component_b)
        return (by2 - by1) * self.factor  # use bbox to return the bounding box for client & host == more sophisticated

    def get_x_pos_connection_right_side(self):
        """Returns the starting position on the X-axis of the connection item."""
        _, _, ax2, _ = self.canvas_landscape.bbox(self.component_a)
        return ax2

    def get_x_pos_connection_left_side(self):
        """Returns the starting position on the X-axis of the connection item."""
        ax1, _, _, _ = self.canvas_landscape.bbox(self.component_a)
        return ax1

    def get_y_pos_connection(self):
        """Returns the first position on the Y-axis of the connection item."""
        _, by1, _, by2 = self.canvas_landscape.bbox(self.component_b)
        return by1 + ((by2 - by1) / 2)


class ClientCanvasItem(CanvasItem):
    """."""

    def __init__(self, main_window, start_pos_x, start_pos_y):
        """Initialize the ClientCanvasItem object.

        Args:
            main_window: _______
            start_pos_x: _______
            start_pos_y: _______

        """
        super().__init__(main_window)
        self.client_effect = Effect(main_window, self.tag, 'outline')
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.width = 90 * self.scale
        self.height = self.width * 0.7
        self.components = []
        self._create()

    def _create(self):
        self._draw_outer_screen()
        self._draw_inner_screen()
        self._draw_keyboard()
        self._draw_spacebar()

    def show(self):  # this code is exactly the same as HostShape
        self.client_effect.flicker()
        self._add_label()

    def hide(self):
        pass

    def _draw_outer_screen(self):
        component = self.canvas_landscape.create_rectangle(self.start_pos_x,
                                                           self.start_pos_y,
                                                           self.start_pos_x + self.width,
                                                           self.start_pos_y + self.height,
                                                           width=THICKNESS_LINE_CLIENT * self.scale,
                                                           outline=NON_OPERATION,
                                                           tags=self.tag
                                                           # state='hidden'
                                                           )
        self.components.append(component)

    def _draw_inner_screen(self):
        coord_x1, coord_y1, coord_x2, coord_y2 = self.canvas_landscape.coords(self.components[0])
        total_width = coord_x2 - coord_x1
        total_height = coord_y2 - coord_y1
        width = (coord_x2 - coord_x1) * 0.9
        height = (coord_y2 - coord_y1) * 0.9
        start_pos_x = coord_x1 + ((total_width - width) / 2)
        start_pos_y = coord_y1 + ((total_height - height) / 2)
        component = self.canvas_landscape.create_rectangle(start_pos_x,
                                                           start_pos_y,
                                                           start_pos_x + width,
                                                           start_pos_y + height,
                                                           width=1,
                                                           outline=NON_OPERATION,
                                                           tags=self.tag
                                                           # state='hidden'
                                                           )
        self.components.append(component)

    def _draw_keyboard(self):
        coord_x1, coord_y1, coord_x2, coord_y2 = self.canvas_landscape.coords(self.components[0])
        width = coord_x2 - coord_x1
        total_height = coord_y2 - coord_y1
        height = (coord_y2 - coord_y1) * 0.7
        start_pos_x = coord_x1
        start_pos_y = coord_y2 + (total_height * 0.05)  # value should not be hardcoded, but calculated
        component = self.canvas_landscape.create_rectangle(start_pos_x,
                                                           start_pos_y,
                                                           start_pos_x + width,
                                                           start_pos_y + height,
                                                           width=THICKNESS_LINE_CLIENT * self.scale,
                                                           outline=NON_OPERATION,
                                                           tags=self.tag
                                                           # state='hidden'
                                                           )
        self.components.append(component)

    def _draw_spacebar(self):
        coord_x1, coord_y1, coord_x2, coord_y2 = self.canvas_landscape.coords(self.components[2])
        total_width = coord_x2 - coord_x1
        total_height = coord_y2 - coord_y1
        width = total_width * 0.5
        height = total_height * 0.2
        start_pos_x = coord_x1 + ((total_width - width) * 0.5)
        start_pos_y = coord_y1 + ((total_height - height) * 0.8)
        component = self.canvas_landscape.create_rectangle(start_pos_x,
                                                           start_pos_y,
                                                           start_pos_x + width,
                                                           start_pos_y + height,
                                                           fill='',
                                                           width=1,
                                                           outline=NON_OPERATION,
                                                           tags=self.tag
                                                           # state='hidden'
                                                           )
        self.components.append(component)

    def setup_ok(self):
        self.client_effect.setup_ok()

    def setup_nok(self):
        self.client_effect.setup_nok()

    def dim(self):
        self.client_effect.dim()


class HostCanvasItem(CanvasItem):
    """."""

    def __init__(self, main_window, start_pos_x, start_pos_y):
        """Initialize the HostCanvasItem object.

        Args:
            main_window: ________
            start_pos_x: ________
            start_pos_y: ________

        """
        super().__init__(main_window)
        self.host_effect = Effect(main_window, self.tag, 'outline')
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.width = 90 * self.scale
        self.height = self.width * 1.4
        self._create()

    def _create(self):
        host_x1 = self.start_pos_x
        host_y1 = self.start_pos_y
        host_x2 = self.start_pos_x + self.width
        host_y2 = self.start_pos_y + self.height
        self.canvas_landscape.create_rectangle(host_x1,
                                               host_y1,
                                               host_x2,
                                               host_y2,
                                               width=THICKNESS_LINE_HOST * self.scale,
                                               outline=NON_OPERATION,
                                               tags=self.tag,
                                               # state='hidden'
                                               )

    def show(self):  # this code is exactly the same as ShapeClient
        self.host_effect.flicker()
        self._add_label()

    def hide(self):
        pass

    def setup_ok(self):
        self.host_effect.setup_ok()

    def setup_nok(self):
        self.host_effect.setup_nok()

    def dim(self):
        self.host_effect.dim()


class AgentCanvasItem(CanvasItem):
    """."""

    def __init__(self, main_window, client, host):
        """Initialize the AgentCanvasItem object.

        Args:
            main_window: _______
            client: _______
            host: _______

        """
        super().__init__(main_window)
        self.agent_effect = Effect(main_window, self.tag, 'outline')
        self.coords_client = self.canvas_landscape.coords(client.tag)
        self.coords_host = self.canvas_landscape.coords(host.tag)
        self.terminate = False
        self.distance_index = 0
        self.distance = 0
        self.width = 0
        self._create()

    def _create(self):

        def _create_agent_derived_from_host():
            hx1, hy1, hx2, hy2 = self.coords_host
            # the variables (m*) give the coordinates of two diagonally opposite corners of the rectangle
            initial_x1 = hx2 - (hx2 - hx1) * 0.7
            initial_y1 = hy2 - (hy1 - hy2) * -0.6
            initial_x2 = hx2 - (hx2 - hx1) * 0.2
            initial_y2 = hy2 - (hy1 - hy2) * -0.1
            self.width = initial_x2 - initial_x1
            self.canvas_landscape.create_rectangle(initial_x1,
                                                   initial_y1,
                                                   initial_x2,
                                                   initial_y2,
                                                   fill=BACKGROUND_CANVAS,
                                                   width=THICKNESS_LINE_AGENT * self.scale,
                                                   outline=NON_OPERATION,
                                                   tags=self.tag,
                                                   # state='hidden'
                                                   )

        def _place_agent_on_position_client():
            ax1, ay1, _, ay2 = self.canvas_landscape.coords(self.tag)
            _, _, cx2, _ = self.coords_client
            self.distance = ax1 - cx2  # here comes explanation
            start_pos_x1 = cx2  # here comes explanation
            pos_y1 = ay1
            pos_y2 = ay2
            self.canvas_landscape.coords(self.tag,
                                         start_pos_x1,
                                         pos_y1,
                                         start_pos_x1 + self.width,
                                         pos_y2)

        _create_agent_derived_from_host()
        _place_agent_on_position_client()

    def show(self):
        self.canvas_landscape.itemconfig(self.tag, state='normal')

    def hide(self):
        pass

    def move(self):
        """Moves the Agent-item (with its outline in a dash pattern) from Client item to destination Host item."""

        def _animate():
            if not self.terminate:
                # print(self.distance_index)
                self.distance_index -= self.distance / 10
                self.canvas_landscape.move(self.tag, self.distance / 10, 0)
                if self.distance_index <= 0:
                    self._add_label()
                    self.terminate = True
                self.canvas_landscape.after(8, _animate)

        self.canvas_landscape.itemconfig(self.tag, dash=(5, 5), width=1)
        self.distance_index = self.distance
        _animate()  # note, the animation will be threaded, so after invoking this method, it continues immediately

    def transfer_ok(self):
        """Turns the outline with its dash pattern into a solid line."""
        self.canvas_landscape.itemconfig(self.tag,
                                         dash=(1, 1),  # default to normal, it was dash=(5, 5)
                                         outline=NON_OPERATION,
                                         width=THICKNESS_LINE_AGENT * self.scale)

    def transfer_nok(self):
        """Colours the outline, still with a dash pattern, red."""
        self.canvas_landscape.itemconfig(self.tag, dash=(5, 5))  # default to normal, it was dash=(5, 5)
        self.canvas_landscape.itemconfig(self.tag, outline=NOK_COLOUR)
        self.canvas_landscape.itemconfig(self.tag, width=THICKNESS_LINE_AGENT * self.scale)

    def setup_ok(self):
        self.agent_effect.setup_ok()

    def setup_nok(self):
        self.agent_effect.setup_nok()

    def dim(self):
        self.agent_effect.dim()


class ConnectionCanvasItem(CanvasItem):  # pylint: disable=too-many-instance-attributes
    """."""

    def __init__(self, main_window, host_item_1, host_item_2):
        """Initialize the ConnectionCanvasItem object.

        Args:
            main_window: ________
            host_item_1: ________
            host_item_2: ________

        """
        super().__init__(main_window)
        self.connection_calculator = ConnectionCalculator(main_window, host_item_1, host_item_2)  # called composition
        self.connection_effect = Effect(main_window, self.tag, 'fill')
        self.item_id_1 = host_item_1.tag
        self.item_id_2 = host_item_2.tag
        self.start_pos_x = self.connection_calculator.get_x_pos_connection_right_side()
        self.pos_y = self.connection_calculator.get_y_pos_connection()
        self.distance = self.connection_calculator.get_connection_length_inner()
        self.terminate = False
        self.distance_index = 0
        self.components = []
        self._create()

    def _create(self):
        top_line = self.canvas_landscape.create_line(self.start_pos_x,
                                                     self.pos_y - 10,
                                                     self.start_pos_x + self.distance,
                                                     self.pos_y - 10,
                                                     fill=NON_OPERATION,
                                                     width=THICKNESS_LINE_TUNNEL * self.scale,
                                                     tags=self.tag,
                                                     # state='hidden'
                                                     )
        self.components.append(top_line)
        bottom_line = self.canvas_landscape.create_line(self.start_pos_x,
                                                        self.pos_y + 10,
                                                        self.start_pos_x + self.distance,
                                                        self.pos_y + 10,
                                                        fill=NON_OPERATION,
                                                        width=THICKNESS_LINE_TUNNEL * self.scale,
                                                        tags=self.tag,
                                                        # state='hidden'
                                                        )
        self.components.append(bottom_line)

    def show(self):
        self.canvas_landscape.itemconfig(tagOrId=self.tag, state='normal')

        def animate():
            if not self.terminate:
                self.canvas_landscape.coords(self.components[0],
                                             self.start_pos_x,
                                             self.pos_y - 10,
                                             self.start_pos_x + self.distance_index,
                                             self.pos_y - 10)
                self.canvas_landscape.coords(self.components[1],
                                             self.start_pos_x,
                                             self.pos_y + 10,
                                             self.start_pos_x + self.distance_index,
                                             self.pos_y + 10)
                self.distance_index += self.distance / 10
                self.canvas_landscape.after(8, animate)
                if self.distance_index >= self.distance:
                    self._add_label()
                    self.terminate = True

        animate()  # note, the animation will be threaded, so after invoking this method, the def continues immediately

    def hide(self):
        self.canvas_landscape.itemconfig(tagOrId=self.tag, state='hidden')
        self.canvas_landscape.itemconfig(tagOrId=self.label, state='hidden')

    def setup_ok(self):
        self.connection_effect.setup_ok()

    def setup_nok(self):
        self.connection_effect.setup_nok()

    def dim(self):
        pass


class StatusBannerCanvasItem(CanvasItem):
    """."""

    def __init__(self, main_window):
        super().__init__(main_window)
        self.tag_text_item = f"{self.tag}-1"
        self.tag_box_item = f"{self.tag}-2"
        self._create_text()
        self._create_box()
        self.text_effect = Effect(main_window, self.tag_text_item, 'fill')
        self.box_effect = Effect(main_window, self.tag_box_item, 'outline')

    def _create_text(self):
        width = self.canvas_status.winfo_width()
        pos_x = width / 2
        status_height = self.canvas_status.winfo_height()
        pos_y = status_height / 2
        text = 'UNESTABLISHED'.center(30)
        self.canvas_status.create_text(pos_x,
                                       pos_y,
                                       text=text,
                                       font=('', 20, 'normal'),
                                       # anchor=N,
                                       fill=NON_OPERATION,
                                       tags=self.tag_text_item)

    def _create_box(self):
        ax1, ay1, ax2, ay2 = self.canvas_status.bbox(self.tag_text_item)
        ax1 -= (20 * self.scale)  # horizontal padding
        ax2 += (20 * self.scale)  # horizontal padding
        ay1 -= (10 * self.scale)  # horizontal padding
        ay2 += (10 * self.scale)  # horizontal padding
        self.canvas_status.create_rectangle(ax1,
                                            ay1,
                                            ax2,
                                            ay2,
                                            outline=NON_OPERATION,
                                            width=THICKNESS_PACKET,
                                            tags=self.tag_box_item)

    # def create(self):
    #     self._create_box(self._create_text())

    def _show_text(self, state=None):
        if state is None:
            self.canvas_status.itemconfig(self.tag_text_item, state='normal')
            self.text_effect.flicker()
        elif state == 'established':
            text = 'CONNECTION ESTABLISHED'.center(30)
            self.canvas_status.itemconfig(self.tag_text_item, text=text, fill=OK_COLOUR)
        elif state == 'broken':
            text = 'CONNECTION BROKEN'.center(30)
            self.canvas_status.itemconfig(self.tag_text_item, text=text, fill=NOK_COLOUR)
        elif state == 'restored':
            text = 'CONNECTION RESTORED'.center(30)
            self.canvas_status.itemconfig(self.tag_text_item, text=text, fill=OK_COLOUR)

    def _show_box(self, state=None):
        if state is None:
            self.canvas_status.itemconfig(self.tag_box_item, state='normal')
            self.box_effect.flicker()
        if state == 'established':
            self.canvas_status.itemconfig(self.tag_box_item, outline=OK_COLOUR)
        elif state == 'broken':
            self.canvas_status.itemconfig(self.tag_box_item, outline=NOK_COLOUR)
        elif state == 'restored':
            self.canvas_status.itemconfig(self.tag_box_item, outline=OK_COLOUR)

    def show(self, state=None):  # fix pylint eror: arguments-differ / Parameters differ from overridden 'show' method
        self._show_text(state)
        self._show_box(state)

    def hide(self):
        self.canvas_status.itemconfig(self.tag_text_item, state='hidden')
        self.canvas_status.itemconfig(self.tag_box_item, state='hidden')

    def setup_ok(self):
        self.text_effect.setup_ok()
        self.box_effect.setup_ok()

    def setup_nok(self):
        pass

    def dim(self):
        text = 'UNESTABLISHED'.center(26)
        self.canvas_status.itemconfig(self.tag_text_item, text=text)
        self.text_effect.dim()
        self.box_effect.dim()

    # def setup_ok(self, filling_type=None):
    #     """Colours the canvas item to state OK (green)."""
    #     arguments = {'fill': OK_COLOUR}
    #     self.canvas.itemconfig(self.text_item, **arguments)
    #     arguments = {'outline': OK_COLOUR}
    #     self.canvas.itemconfig(self.box_item, **arguments)
    #
    # def dim(self, filling_type=None):
    #     self.status.itemconfig(self.tag, fill=NON_OPERATION)
    #     self.status.itemconfig(self.tag, outline=NON_OPERATION)


class PacketCanvasItem(CanvasItem):
    """Creates a visualised TCP packet."""

    def __init__(self, main_window, connection_items):
        """Initialize the PacketShape object.

        Args:
            main_window: _________
            connection_items: _________

        """
        super().__init__(main_window)
        self.connection_calculator = ConnectionCalculator(main_window, connection_items[0], connection_items[-1])
        self.total_width = WIDTH_PACKET + (2 * THICKNESS_LINE_PACKET) * self.scale
        self.start_pos_x = self.connection_calculator.get_x_pos_connection_left_side()
        self.pos_y = self.connection_calculator.get_y_pos_connection()
        self.distance = self.connection_calculator.get_connection_length_outer()
        self._create()

    def _create(self):
        self.canvas_landscape.create_rectangle(self.start_pos_x,
                                               self.pos_y - 4,
                                               self.start_pos_x + WIDTH_PACKET,
                                               self.pos_y + 4,
                                               fill=PACKET_FILL_COLOUR,
                                               outline=PACKET_OUTLINE_COLOUR,
                                               width=THICKNESS_LINE_PACKET,
                                               # state='hidden',
                                               tags=self.tag)

    def show(self):
        self.canvas_landscape.itemconfig(self.tag, state='normal')

    def hide(self):
        self.canvas_landscape.itemconfig(self.tag, state='hidden')

    def setup_ok(self):
        pass

    def setup_nok(self):
        pass

    def dim(self):
        pass
