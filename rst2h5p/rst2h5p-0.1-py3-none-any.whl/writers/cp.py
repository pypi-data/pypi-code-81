#!/usr/bin/env python

import json

from docutils.writers import html5_polyglot

from ..elements import AdvancedText
from .visitor import VisitorSpecialSingleChoice, VisitorSpecialMultiChoice

class Slide():
    def __init__(self, title = "No title"):
        self.elements = []
    def add_title(self, title):
        title = "\n".join(title) if isinstance(title, list) else str(title)
        elem = AdvancedText(title, x=3, y=6, width=94, height=10)
        self.elements.append(elem)
    def add_element(self, elem):
        self.elements.append(elem)
    def get_object(self):
        return {
            "elements": [e.get_object() for e in self.elements],
            "slideBackgroundSelector": {},
        }

class CoursePresentationWriter(html5_polyglot.Writer):
    format_name = "json"
    def __init__(self):
        self.parts = {}
        self.translator_class = CoursePresentationTranslator

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        output = {
            "presentation": {
                "slides": visitor.slides
            }
        }
        self.output = json.dumps(output, indent=2)+"\n"
        self.h5p = json.dumps({
                "title": visitor.title,
                "language": "und",
                "mainLibrary": "H5P.CoursePresentation",
                "embedTypes": [
                    "div"
                ],
                "license": "U",
                "defaultLanguage": "en",
                "preloadedDependencies": [
                    {
                        "machineName": "H5P.AdvancedText",
                        "majorVersion": "1",
                        "minorVersion": "1"
                    },
                    {
                        "machineName": "H5P.MultiChoice",
                        "majorVersion": "1",
                        "minorVersion": "14"
                    },
                    {
                        "machineName": "H5P.SingleChoiceSet",
                        "majorVersion": "1",
                        "minorVersion": "11"
                    },
                    {
                        "machineName": "H5P.CoursePresentation",
                        "majorVersion": "1",
                        "minorVersion": "22"
                    },
                    {
                        "machineName": "FontAwesome",
                        "majorVersion": "4",
                        "minorVersion": "5"
                    },
                    {
                        "machineName": "H5P.FontIcons",
                        "majorVersion": "1",
                        "minorVersion": "0"
                    },
                    {
                        "machineName": "H5P.JoubelUI",
                        "majorVersion": "1",
                        "minorVersion": "3"
                    },
                    {
                        "machineName": "H5P.Transition",
                        "majorVersion": "1",
                        "minorVersion": "0"
                    },
                    {
                        "machineName": "Drop",
                        "majorVersion": "1",
                        "minorVersion": "0"
                    },
                    {
                        "machineName": "Tether",
                        "majorVersion": "1",
                        "minorVersion": "0"
                    }
                ]
            }, indent=2)+"\n"

    def assemble_parts(self):
        self.parts = {
            "content/content.json": self.output,
            "h5p.json": self.h5p,
        }

class CoursePresentationTranslator(html5_polyglot.HTMLTranslator):
    def __init__(self, document):
        self.slides = []
        self.current_slide = None
        self.special = None
        super().__init__(document)
    def take_body(self, as_list = False):
        body = "\n".join(self.body) if not as_list else self.body
        self.body = []
        return body
    def depart_document(self, node):
        super().depart_document(node)
        self.title = node.get("title")
    def visit_section(self, node):
        self.current_slide = Slide()
    def depart_section(self, node):
        if len(self.body) > 0:
            self.current_slide.add_element(AdvancedText("".join(self.body), x=3, y=17, width=94, height=77))
        self.slides.append(self.current_slide.get_object())
    def visit_title(self, node):
        if self.current_slide:
            self.take_body()
    def depart_title(self, node):
        if self.current_slide:
            self.current_slide.add_title("<h2>"+self.take_body()+"</h2>")
    def visit_singlechoice(self, node):
        self.special = VisitorSpecialSingleChoice(x=3, y=17, width=94, height=77)
    def depart_singlechoice(self, node):
        self.current_slide.add_element(self.special.get_element())
        self.special = None
    def visit_multichoice(self, node):
        self.special = VisitorSpecialMultiChoice(node["correct"], x=3, y=17, width=94, height=77)
    def depart_multichoice(self, node):
        self.current_slide.add_element(self.special.get_element())
        self.special = None
    def visit_bullet_list(self, node):
        if self.special:
            self.special.set_question(self.take_body())
        else:
            super().visit_bullet_list(node)
    def depart_bullet_list(self, node):
        if not self.special:
            super().depart_bullet_list(node)
    def visit_list_item(self, node):
        if self.special:
            self.take_body()
        else:
            super().visit_list_item(node)
    def depart_list_item(self, node):
        if self.special:
            self.special.add_option(self.take_body())
        else:
            super().depart_list_item(node)

