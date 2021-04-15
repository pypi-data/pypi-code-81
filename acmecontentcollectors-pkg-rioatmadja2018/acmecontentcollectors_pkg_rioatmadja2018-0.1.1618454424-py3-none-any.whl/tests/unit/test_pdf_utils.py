#!/usr/bin/env python
import pytest 
from unittest import TestCase
from acme_collectors.utils.pdf_parser import parse_pdf_text
import os 

class TestPDFUtils(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == "master" or os.getenv('BITBUCKET_BRANCH') == "develop", reason='Local Test')
    def test_pdf_extract(self):
        pdf_url: str = "https://justpaste.it/cosrtfis/pdf"
        extracted_document = parse_pdf_text(document_url=pdf_url) 
        return self.assertEqual(len(extracted_document), 10)

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == "master" or os.getenv('BITBUCKET_BRANCH') == "develop", reason='Local Test')
    def test_save_pdf_document(self): 
        pdf_url: str = "https://justpaste.it/cosrtfis/pdf"
        extracted_document = parse_pdf_text(document_url=pdf_url, file_name='local_test.pdf', save_pdf=True)
        print("EXTRACTED KEYS", extracted_document.keys() )
        file_name: str = extracted_document.get('file_name', None)
        
        self.assertEqual(os.path.exists(file_name), True)

