import logging

# this is to force etree to use the python implementation so we can implement our own classes
import sys
sys.modules['_elementtree'] = None

from xml.etree.ElementTree import parse as etree_parse
from xml.etree.ElementTree import ElementTree

from .dynamicxmlparser import DynamicXmlParser
from .dynamicelement import DynamicElement

def parse(path_to_xml:str) -> DynamicElement:

    try:
        with open(path_to_xml, 'r') as f:
            tree = etree_parse(f, parser=DynamicXmlParser())
            return tree.getroot()
    except BaseException as e:
        logging.error(f"Unable to parse {path_to_xml}, {e}")
        return None

def write(path_to_xml:str, node:DynamicElement, *args, **kwargs) -> bool:

    try:
        et = ElementTree(node)
        et.write(path_to_xml, *args, **kwargs)
        return True
    except BaseException as e:
        logging.error(f"Unable to write to {path_to_xml}, {e}")
        return False