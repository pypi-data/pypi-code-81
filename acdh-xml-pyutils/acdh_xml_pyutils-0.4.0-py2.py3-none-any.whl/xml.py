import time
import datetime
import requests
import lxml.etree as ET

from collections import Counter


class XMLReader():

    """ Class to parse, preprocess and save XML/TEI

    :param xml: An XML Document, either a File Path, an URL to an XML or an XML string
    :type xml: str

    :return: A XMLReader instance
    :rtype: `xml.XMLReader`

    """

    def __init__(self, xml=None, xsl=None):

        """ initializes the class

        :param xml: An XML Document, either a File Path, an URL to an XML or an XML string
        :type xml: str

        :param xsl: Path to an XSL Stylesheet
        :type xsl: str

        :return: A XMLReader instance
        :rtype: `xml.XMLReader`

        """
        self.ns_tei = {'tei': "http://www.tei-c.org/ns/1.0"}
        self.ns_xml = {'xml': "http://www.w3.org/XML/1998/namespace"}
        self.ns_tcf = {'tcf': "http://www.dspin.de/data/textcorpus"}
        self.nsmap = {
            'tei': "http://www.tei-c.org/ns/1.0",
            'xml': "http://www.w3.org/XML/1998/namespace",
            'tcf': "http://www.dspin.de/data/textcorpus"
        }
        self.file = xml.strip()
        if xsl:
            self.xsl = ET.parse(xsl)
        else:
            self.xsl = None
        if self.file.startswith('http'):
            r = requests.get(
                self.file,
                headers={
                    'Content-type': 'application/xml; charset=utf-8',
                    'Accept-Charset': 'utf-8'
                    }
                )
            try:
                self.original = ET.fromstring(r.content.decode('utf-8'))
            except ValueError:
                self.original = ET.fromstring(r.content.decode('utf-8').encode('utf-8'))
        elif self.file.startswith('<'):
            try:
                self.original = ET.parse(self.file)
            except OSError:
                self.original = ET.fromstring(self.file.encode('utf8'))
        else:
            self.original = ET.parse(self.file)
        self.tree = self.original
        if self.xsl:
            transform = ET.XSLT(self.xsl)
            self.tree = transform(self.tree)

    def get_elements(self):
        """ returns a list of all element names of the current tree

        :return: A list of all element names
        :rtype: list

        """
        all_elements = [element.tag for element in self.tree.iter()]
        return all_elements

    def get_element_stats(self):
        """ returns a `collections.Counter` object holding element count

        :return: A list of all element names
        :rtype: `collections.Counter`
        """
        return Counter(self.get_elements())

    def return_byte_like_object(self):
        """ returns current doc as byte like object"""

        return ET.tostring(self.tree, encoding="utf-8")

    def return_string(self):

        """
        returns current doc as string

        :rtype: str

        """
        return self.return_byte_like_object().decode('utf-8')

    def tree_to_file(self, file=None):
        """
        saves current tree to file

        :param file: A filename/location to save the current doc
        :type file: str

        :return: The save-location
        :rtype: str

        """
        if file:
            pass
        else:
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
            file = "{}.xml".format(timestamp)

        with open(file, 'wb') as f:
            f.write(ET.tostring(self.tree, encoding="UTF-8"))
        return file
