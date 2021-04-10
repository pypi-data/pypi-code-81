#!/usr/bin/python

# python standard imports
from argparse import ArgumentParser
from json import dumps
from pathlib import Path

# internal imports
from . import Citator

BASE_JS_PATH =  Path(__file__).parent.absolute() / 'citeurl.js'

COPYRIGHT_MESSAGE = """
// This script was made with CiteURL, an extensible framework to turn
// legal references into URLs.
//
// The "schemas" variable directly below holds the data necessary to 
// turn each kind of citation into a URL. Some or all of the schemas may
// have been made by a third party and are not part of CiteURL itself.
//
// CiteURL is copyright of Simon Raindrum Sherred under the MIT License,
// and is available at https://github.com/raindrum/citeurl.
"""

HTML_HEADER = """<!DOCTYPE html>
<html>
<head>
  <title>CiteURL-JS</title>
  <meta content="width=device-width, initial-scale=1" name="viewport" />
  <style media = "all">
    body {font-size: 125%; background-color: #333;
    color: white; text-align: center;}
    input {font-size: 150%; border: none; padding: 0.5rem;}
    a {color: #AAA;}
  </style>
</head>
<body hidden>
"""

HTML_REMAINDER = """
<p>
  Type a legal citation into the box below, and I'll try to send you to
  whatever it references:
</p>
<form class="main-search" onsubmit="handleSearch(event)">
  <input type="search" placeholder="Enter citation..." name="q" id="q">
  <input type="submit" value="Go"><br>
  <label for="q" id="explainer" class="search-label"></label>
</form>
<p>
  If you want to see each step in the URL generation process, press
  <code>CTRL + SHIFT + J</code> to open the developer console before you
  run a search.
</p>
<p>
  This lookup tool was made with
  <a href="github.com/raindrum/citeurl/">CiteURL</a>.
</p>
</body>
</html>
"""

def main():
    """
    Print a JavaScript implementation of CiteURL's lookup function,
    populated with the schemas from the specified YAML files, plus the
    built-in schemas by default.
    
    The JavaScript is meant to be embedded in a HTML page that contains
    a search bar with name="q", inside of a form with
    onsubmit="handleSearch(event)".
    """
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "yaml_files",
        nargs="*",
        help="files containing custom citation schemas to include. "
            + "See https://raindrum.github.io/citeurl/#schema-yamls/",
    )
    parser.add_argument(
        "-n", "--no-default-schemas",
        action="store_true",
        help="don't include CiteURL's default schemas",
    )
    parser.add_argument(
        "-f", "--full-html",
        action="store_true",
        help="generate a usable HTML page instead of just JavaScript",
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="write output to a file instead of stdout",
    )
    args = parser.parse_args()
    
    citator = Citator(
        yaml_paths=args.yaml_files,
        defaults=False if args.no_default_schemas else True,
    )
    
    # translate each schema to json
    json_schemas = []
    for schema in citator.schemas:
        # skip schemas without URL templates
        if 'URL' not in schema.__dict__:
            continue
        
        json = {}
        
        # some parts of a schema can be copied over easily
        for key in ['name', 'defaults', 'URL']:
            json[key] = schema.__dict__[key]
        regex_source = (schema.broadRegex or schema.regex)
        json['regex'] = regex_source.replace('?P<', '?<')
        
        # only add the relevant data from each mutation
        if 'mutations' in schema.__dict__:
            json['mutations'] = []
        for mut in schema.mutations:
            mutation = {}
            for key in ['token', 'case', 'omit', 'splitter', 'joiner']:
                if mut.__dict__[key]:
                    mutation[key] = mut.__dict__[key]
            json['mutations'].append(mutation)
        
        # only add the relevant data from each substitution
        if 'substitutions' in schema.__dict__:
            json['substitutions'] = []
        for sub in schema.substitutions:
            substitution = {}
            for key in ['token', 'index']:
                substitution[key] = sub.__dict__[key]
            for key in ['useRegex', 'allowUnmatched']:
                if sub.__dict__[key]:
                    substitution[key] = True
            if sub.outputToken != sub.token:
                substitution['outputToken'] = sub.outputToken
            json['substitutions'].append(substitution)

        json_schemas.append(json)
    
    # write json to str
    json_str = dumps(
        json_schemas,
        indent=4,
        sort_keys=False,
        ensure_ascii=False,
    )
    
    # generate javascript
    javascript = (
        COPYRIGHT_MESSAGE
        + '\nconst schemas = ' 
        + json_str + ';\n\n'
        + BASE_JS_PATH.read_text()
    )
    
    # optionally embed the javascript into an HTML page
    if args.full_html:
        output = (
            HTML_HEADER
            + '<script>' + javascript + '</script>'
            + HTML_REMAINDER
        )
    else:
        output = javascript
    
    # save or print output
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
