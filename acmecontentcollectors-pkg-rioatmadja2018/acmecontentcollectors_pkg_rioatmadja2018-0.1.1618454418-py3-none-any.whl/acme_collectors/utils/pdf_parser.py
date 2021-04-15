#!/usr/bin/env python 
from acme_collectors.utils.constants import HEADERS
from pdfreader.viewer.simple import SimplePDFViewer 
from typing import Dict
from uuid import uuid4
import re
from urllib import request
import os
import ssl

def ACME_BROWSER(url: str) -> bytes:
    """
    Description
    -----------
    This is the current browser for the ACME project 

    Parameters
    ----------
    :url: given a valid url 

    Return
    ------
    :return: A http/https response, otherwise return the error message 
    """
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response: bytes = request.urlopen(request.Request(url=url, headers=HEADERS), context=ctx).read()
        return response 

    except ConnectionError as e: 
        raise ConnectionError(f"Unable to connect to the following URLs {url}") from e 

def parse_pdf_text(document_url: str, save_pdf: bool = False, file_name: str = str(uuid4())) -> Dict:
    """
    Description
    -----------
    Helper function to extract the text from the given document url. If the file is located remotely, this function will attempt to fetch the file and parse it.
    Otherwise, open the document and extract the text. 

    Paramters
    ---------
    :document_url: given a valid pdf URLs
    :save_pdf: an option argument with default set to False (To save the file)
    :file_name: an option argument with default set to UUID4, unless specified 

    Return
    ------
    :return: a dictionary with the extracted text and page numbers, if save_pdf is set to true, there is an additional attributes called file_name. 
    """ 
    # check if this is a URLS  
    is_url = re.match(r"^(www|http|[a-z]+).*.\.[a-z]{2,3}(/\w+){0,}", document_url.lower() )
    raw_document = None 
    extracted_text: Dict = {}

    if is_url: 
        raw_document = ACME_BROWSER(url=is_url.group())
    # if it's not a url link, attempt to open the local file 
    if not raw_document: 
        if not os.path.exists(document_url): 
            raise FileNotFoundError(f"[+] Unable to find the following file {document_url}")

        raw_document: bytes = open(document_url, 'rb').read() 

    pdf_contents: SimplePDFViewer = SimplePDFViewer(raw_document)
    while True:
        try:
            pdf_contents.render() 
            pdf_iterator = pdf_contents.iter_pages()
            extracted_text[pdf_iterator.viewer.current_page_number] = ''.join(pdf_iterator.viewer.canvas.strings) 
            pdf_iterator.viewer.next() 

        except:
            break 

    if save_pdf:
        with open(file_name, 'wt') as f: 
            for page_number, content in extracted_text.items():
                f.write(f"[{page_number}] {content}\n")
        f.close()

    return {**extracted_text, **{'file_name': file_name } } if save_pdf else extracted_text