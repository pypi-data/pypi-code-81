import sys
import os
import argparse
import requests
from io import BytesIO

from docutils.core import publish_parts
from docutils.parsers.rst import directives

from collections import namedtuple
from zipfile import ZipFile

from .writers.cp import CoursePresentationWriter
from .directives import SingleChoice, MultiChoice

directives.register_directive("multichoice", MultiChoice)
directives.register_directive("singlechoice", SingleChoice)

Format = namedtuple("Format", ["hubname", "writer"])

formats = {
    "course-presentation": Format(hubname="H5P.CoursePresentation", writer=CoursePresentationWriter)
}

def main(args = sys.argv[1:]):
    parser = argparse.ArgumentParser("rst2h5p")
    parser.add_argument("format", choices=formats.keys())
    parser.add_argument("input", type=argparse.FileType('r'))
    parser.add_argument("output")

    args = parser.parse_args(args)

    req = requests.get("https://api.h5p.org/v1/content-types/{}".format(formats[args.format].hubname))
    if req.status_code != 200:
        print("Cannot download content type", file=sys.stderr)

    with ZipFile(args.output, mode="w") as zip:
        # Copy everything except content/* and h5p.json
        # There is unfortunately no way to overwrite them
        with ZipFile(BytesIO(req.content)) as hubzip:
            for item in hubzip.infolist():
                if item.filename == "H5P.CoursePresentation-1.22/dist/h5p-course-presentation.css":
                    h5p_css = hubzip.read(item.filename) + b"""
                    pre { line-height: 125%; }
                    td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
                    span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
                    td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
                    span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
                    pre.code .hll { background-color: #ffffcc }
                    pre.code { background: #f8f8f8; }
                    pre.code .c { color: #408080; font-style: italic } /* Comment */
                    pre.code .err { border: 1px solid #FF0000 } /* Error */
                    pre.code .k { color: #008000; font-weight: bold } /* Keyword */
                    pre.code .o { color: #666666 } /* Operator */
                    pre.code .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
                    pre.code .cm { color: #408080; font-style: italic } /* Comment.Multiline */
                    pre.code .cp { color: #BC7A00 } /* Comment.Preproc */
                    pre.code .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
                    pre.code .c1 { color: #408080; font-style: italic } /* Comment.Single */
                    pre.code .cs { color: #408080; font-style: italic } /* Comment.Special */
                    pre.code .gd { color: #A00000 } /* Generic.Deleted */
                    pre.code .ge { font-style: italic } /* Generic.Emph */
                    pre.code .gr { color: #FF0000 } /* Generic.Error */
                    pre.code .gh { color: #000080; font-weight: bold } /* Generic.Heading */
                    pre.code .gi { color: #00A000 } /* Generic.Inserted */
                    pre.code .go { color: #888888 } /* Generic.Output */
                    pre.code .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
                    pre.code .gs { font-weight: bold } /* Generic.Strong */
                    pre.code .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
                    pre.code .gt { color: #0044DD } /* Generic.Traceback */
                    pre.code .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
                    pre.code .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
                    pre.code .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
                    pre.code .kp { color: #008000 } /* Keyword.Pseudo */
                    pre.code .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
                    pre.code .kt { color: #B00040 } /* Keyword.Type */
                    pre.code .m { color: #666666 } /* Literal.Number */
                    pre.code .s { color: #BA2121 } /* Literal.String */
                    pre.code .na { color: #7D9029 } /* Name.Attribute */
                    pre.code .nb { color: #008000 } /* Name.Builtin */
                    pre.code .nc { color: #0000FF; font-weight: bold } /* Name.Class */
                    pre.code .no { color: #880000 } /* Name.Constant */
                    pre.code .nd { color: #AA22FF } /* Name.Decorator */
                    pre.code .ni { color: #999999; font-weight: bold } /* Name.Entity */
                    pre.code .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
                    pre.code .nf { color: #0000FF } /* Name.Function */
                    pre.code .nl { color: #A0A000 } /* Name.Label */
                    pre.code .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
                    pre.code .nt { color: #008000; font-weight: bold } /* Name.Tag */
                    pre.code .nv { color: #19177C } /* Name.Variable */
                    pre.code .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
                    pre.code .w { color: #bbbbbb } /* Text.Whitespace */
                    pre.code .mb { color: #666666 } /* Literal.Number.Bin */
                    pre.code .mf { color: #666666 } /* Literal.Number.Float */
                    pre.code .mh { color: #666666 } /* Literal.Number.Hex */
                    pre.code .mi { color: #666666 } /* Literal.Number.Integer */
                    pre.code .mo { color: #666666 } /* Literal.Number.Oct */
                    pre.code .sa { color: #BA2121 } /* Literal.String.Affix */
                    pre.code .sb { color: #BA2121 } /* Literal.String.Backtick */
                    pre.code .sc { color: #BA2121 } /* Literal.String.Char */
                    pre.code .dl { color: #BA2121 } /* Literal.String.Delimiter */
                    pre.code .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
                    pre.code .s2 { color: #BA2121 } /* Literal.String.Double */
                    pre.code .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
                    pre.code .sh { color: #BA2121 } /* Literal.String.Heredoc */
                    pre.code .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
                    pre.code .sx { color: #008000 } /* Literal.String.Other */
                    pre.code .sr { color: #BB6688 } /* Literal.String.Regex */
                    pre.code .s1 { color: #BA2121 } /* Literal.String.Single */
                    pre.code .ss { color: #19177C } /* Literal.String.Symbol */
                    pre.code .bp { color: #008000 } /* Name.Builtin.Pseudo */
                    pre.code .fm { color: #0000FF } /* Name.Function.Magic */
                    pre.code .vc { color: #19177C } /* Name.Variable.Class */
                    pre.code .vg { color: #19177C } /* Name.Variable.Global */
                    pre.code .vi { color: #19177C } /* Name.Variable.Instance */
                    pre.code .vm { color: #19177C } /* Name.Variable.Magic */
                    pre.code .il { color: #666666 } /* Literal.Number.Integer.Long */
                    /* Literal Blocks */
                    pre.literal-block, pre.doctest-block,
                    pre.math, pre.code {
                        font-family: monospace;
                    }
                    """
                    zip.writestr(item, h5p_css)
                elif not item.filename.startswith("content/") and not item.filename == "h5p.json":
                    zip.writestr(item, hubzip.read(item.filename))

        parts = publish_parts(source=args.input.read(), writer=formats[args.format].writer(), settings_overrides={"syntax_highlight": "short"})

        for file, content in parts.items():
            zip.writestr(file, content)



