# Copyright 2021 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from flask import current_app
from fpdf import FPDF

from kadi.lib.utils import utcnow


class PDF(FPDF):
    """Base PDF generation class using FPDF.

    :param title: (optional) The title of the PDF, which will appear in the header on
        each page and in the metadata of the PDF itself.
    """

    def __init__(self, title=""):
        self.title = title
        self.generated_at = utcnow()

        fonts_path = current_app.config["FONTS_PATH"]
        super().__init__(font_cache_dir=fonts_path)

        self.set_title(self.title)
        self.add_font(
            "DejaVu",
            fname=os.path.join(fonts_path, "dejavu", "DejaVuSans.ttf"),
            uni=True,
        )
        self.add_font(
            "DejaVu",
            fname=os.path.join(fonts_path, "dejavu", "DejaVuSans-Bold.ttf"),
            uni=True,
            style="B",
        )
        self.add_font(
            "DejaVu",
            fname=os.path.join(fonts_path, "dejavu", "DejaVuSans-Oblique.ttf"),
            uni=True,
            style="I",
        )
        self.set_font("DejaVu")
        self.add_page()

    def header(self):
        """Automatically renders a header on each page of the generated PDF."""
        self.set_font(size=10)
        self.truncated_cell(self.epw * 0.85, txt=self.title, align="L")
        self.cell(self.epw * 0.15, txt="Kadi4Mat", align="R")
        self.section(top=3, bottom=8, r=0, g=0, b=0)

    def footer(self):
        """Automatically renders a footer on each page of the generated PDF."""
        self.set_font(size=10)
        self.set_text_color(r=150, g=150, b=150)
        self.set_y(-10)
        self.cell(
            self.epw / 2,
            txt=f"Generated at {self.format_date(self.generated_at)}",
            align="L",
        )
        self.cell(self.epw / 2, txt=str(self.page_no()), align="R")

    def section(self, top=None, bottom=None, r=200, g=200, b=200):
        """Render a section separated by a horizontal line.

        :param top: The top margin of the section.
        :param bottom: The bottom margin of the section.
        :param r: The R value of the RGB line color.
        :param g: The G value of the RGB line color.
        :param b: The B value of the RGB line color.
        """
        self.ln(top)
        self.set_draw_color(r=r, g=g, b=b)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(bottom)

    def truncated_cell(self, w, txt="", **kwargs):
        r"""Render a cell with truncated text based on the cell's width.

        Wraps the original :func:`cell` function and uses :meth:`truncate_string` to
        truncate the given text content.

        :param w: The width of the cell.
        :param txt: (optional) The text content of the cell.
        :param \**kwargs: Additional keyword arguments to pass to :func:`cell`.
        """
        super().cell(w, txt=self.truncate_string(txt, w), **kwargs)

    def truncate_string(self, string, width):
        """Truncate a string based on a given width.

        :param string: The string to truncate.
        :param width: The maximum width of the string.
        :return: The truncated string, if its rendered width is larger than the given
            width, or the original string.
        """
        truncated_string = string
        while self.get_string_width(truncated_string) > width:
            truncated_string = truncated_string[:-1]

        if truncated_string != string:
            truncated_string = truncated_string[:-3] + "..."

        return truncated_string

    @staticmethod
    def format_date(date_time, include_micro=False):
        """Format a datetime object.

        :param date_time: The datetime object to format.
        :param include_micro: (optional) Flag indicating whether to include microseconds
            in the formatted datetime or not.
        :return: The formatted datetime string.
        """
        fmt = "%Y-%m-%d %H:%M:%S"
        if include_micro:
            fmt += ".%f"

        return date_time.strftime(f"{fmt} %Z")
