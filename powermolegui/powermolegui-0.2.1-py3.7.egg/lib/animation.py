#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: animation.py
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
Main code for transforming tkinter canvas items.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''28-02-2021'''
__copyright__ = '''Copyright 2021, Vincent Schouten'''
__credits__ = ["Vincent Schouten"]
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class AnimateItem:  # pylint: disable=too-many-instance-attributes
    """Animates the canvas item by moving horizontally in one direction and loop."""

    def __init__(self, main_window, item):
        """Instantiate the Animate object.

        Args:
            main_window: ______
            item: ______

        """
        self.status = main_window.main_frame.canvas_frame.canvas_status
        self.canvas = main_window.main_frame.canvas_frame.canvas_landscape
        self.terminate = False
        self.item = item
        self.distance = item.distance
        self.distance_index = 0
        self.width = item.total_width
        self.scale = 1

    def start(self):
        """Moves a TCP/IP packet from item to another item and loop."""
        self.item.show()

        def _animate_forward():
            if not self.terminate:
                self.canvas.move(self.item.tag, 10 * self.scale, 0)
                self.distance_index += 10 * self.scale
                if self.distance_index >= self.distance - self.width:
                    start_pos = self.distance - self.width
                    self.canvas.move(self.item.tag, start_pos * -1, 0)
                    self.distance_index = 0
                self.canvas.after(25, _animate_forward)

        _animate_forward()  # note, the animation will be threaded, so after invoking this method, it continues directly

    def stop(self):
        """Stop moving the TCP/IP packet and cleanup."""
        self.terminate = True
        self.canvas.delete(self.item.tag)

    def pause(self):
        """Temporarily pause moving the TCP/IP package."""
        self.canvas.itemconfig(self.item.tag, state='hidden')

    def resume(self):
        """Resume moving the TCP/IP package."""
        self.canvas.itemconfig(self.item.tag, state='normal')
