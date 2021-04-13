import unittest
import rdflib
import datetime
from datetime import timezone
from rdflib import Namespace,URIRef, BNode, Literal,Graph, plugin
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from uuid import uuid4
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from shinc.ocr.sofextractor import SOFImageExtractor, SOFList, NS, SOFPDFExtractor, SOFTextExtractor, SHC

class SOFExtractorTestCase(unittest.TestCase):

    def setUp(self):
        self.test_line_unbounded1 = """08:00 PILOT ON BOARD"""
        self.test_line_unbounded2 = """08:00PILOT ON BOARD"""
        self.test_line_unbounded4 = """0800 PILOT ON BOARD"""
        self.test_line_unbounded5 = """08.00 PILOT ON BOARD 20.10.05"""
        self.test_line_unbounded6 = """08.00 PILOT ON BOARD 20/10/05"""
        self.test_line_bounded1 = """08.00 12.00 HOLD CLEANING 20/10/05"""
        self.test_line_real = """10-January-2017 12-January-2017 07:12 ARRIVED AT PILOT STATION"""
        self.test_line_real2 = """January, 10 2017 07:12 ARRIVED AT PILOT STATION"""
        self.test_line_real3 = """Aug 19" 2013"""

        textfile = open('./text/sof-test1.txt')
        self.softext = textfile.read()
        textfile.close()


        textfile = open('./text/sof-test2.txt')
        self.sof_funny_dates_text = textfile.read()
        textfile.close()

        textfile = open('./text/sof-test3.txt')
        self.sof_incomplete_text = textfile.read()
        textfile.close()

        self.generator = SOFList('./sofs/sof-master-test.csv')
        self.generator.generate()
        

    def test_ocrextractor(self):
        extractor = SOFImageExtractor('./images/test_image.jpg','./tmpdata')
        result = extractor.extract()
        res = False
        for line in result:
            if "FINAL DRAFT SURVEY" in line:
                res = True
        assert res

    def test_sof_generator(self):
        
        #print(result.serialize(format="turtle").decode("utf-8"))
        assert self.generator.sofs.query("ASK {shc:AWAITING-TRUCKS rdfs:subClassOf shc:Event.}", initNs=NS)
        assert self.generator.sofs.query("ASK {shc:AWAITING-TRUCKS rdfs:subClassOf shc:BoundedEvent.}", initNs=NS)

    

    def test_text_time_extractor(self):
        textextractor = SOFTextExtractor(self.generator)
        assert textextractor.extractTime(self.test_line_unbounded1, "hh:mm")[0].hour == 8 and textextractor.extractTime(self.test_line_unbounded1, "hh:mm")[0].minute == 0
        assert textextractor.extractTime(self.test_line_unbounded2, "hh:mm")[0].hour == 8 and textextractor.extractTime(self.test_line_unbounded2, "hh:mm")[0].minute == 0
        assert textextractor.extractTime(self.test_line_unbounded4, "hhmm")[0].hour == 8
        assert textextractor.extractTime(self.test_line_unbounded4, "hhmm")[0].minute == 0
        assert textextractor.extractTime(self.test_line_unbounded5, "hh.mm")[0].hour == 8
        assert textextractor.extractTime(self.test_line_unbounded5, "hh.mm")[0].minute == 0
        assert textextractor.extractTime(self.test_line_bounded1, "hh.mm")[0].hour == 8
        assert textextractor.extractTime(self.test_line_bounded1, "hh.mm")[0].minute == 0
        assert textextractor.extractTime(self.test_line_bounded1, "hh.mm")[1].hour == 12
        assert textextractor.extractTime(self.test_line_bounded1, "hh.mm")[1].minute == 0

    def test_text_date_extractor(self):
        textextractor = SOFTextExtractor(self.generator)
        assert textextractor.extractDate(self.test_line_bounded1, "DMY")[0].day == 20
        assert textextractor.extractDate(self.test_line_bounded1, "DMY")[0].month == 10
        assert textextractor.extractDate(self.test_line_bounded1, "DMY")[0].year == 2005
        assert textextractor.extractDate(self.test_line_unbounded6, "DMY")[0].day == 20
        assert textextractor.extractDate(self.test_line_unbounded6, "DMY")[0].month == 10
        assert textextractor.extractDate(self.test_line_unbounded6, "DMY")[0].year == 2005

        assert textextractor.extractDate(self.test_line_real, "DMY")[0].day == 10
        assert textextractor.extractDate(self.test_line_real, "DMY")[0].month == 1
        assert textextractor.extractDate(self.test_line_real, "DMY")[0].year == 2017
        assert textextractor.extractDate(self.test_line_real, "DMY")[1].day == 12
        assert textextractor.extractDate(self.test_line_real, "DMY")[1].month == 1
        assert textextractor.extractDate(self.test_line_real, "DMY")[1].year == 2017

        assert textextractor.extractDate(self.test_line_real2, "MDY")[0].day == 10
        assert textextractor.extractDate(self.test_line_real2, "MDY")[0].month == 1
        assert textextractor.extractDate(self.test_line_real2, "MDY")[0].year == 2017

        assert textextractor.extractDate(self.test_line_real3, "MDY")[0].day == 19
        assert textextractor.extractDate(self.test_line_real3, "MDY")[0].month == 8
        assert textextractor.extractDate(self.test_line_real3, "MDY")[0].year == 2013
        


    def test_line_extractor(self):
        textextractor = SOFTextExtractor(self.generator)
        sof = textextractor.extractLine(self.test_line_bounded1, None, "DMY", "hh.mm", timezone=timezone.utc)
        assert sof.id
        assert sof.description == "HOLD CLEANING"
        assert sof.type == SHC + "HOLD-CLEANING"
        assert sof.startdatetime.day == 20 and sof.startdatetime.month == 10 and sof.startdatetime.year == 2005 and sof.startdatetime.hour == 8 and sof.startdatetime.minute == 0
        assert sof.enddatetime.day == 20 and sof.enddatetime.month == 10 and sof.enddatetime.year == 2005 and sof.enddatetime.hour == 12 and sof.enddatetime.minute == 0
        


    def test_text_extractor(self):
        textextractor = SOFTextExtractor(self.generator)
        sofs = textextractor.extract(self.softext, starttext="Terminal / Comment", dateorder="DMY", timemask="hh:mm")
        assert len(sofs) == 10

        sofs2 = textextractor.extract(self.sof_funny_dates_text, dateorder="MDY", timemask="hh.mm")
        assert len(sofs2) == 5

        sofs3 = textextractor.extract(self.sof_incomplete_text, dateorder="MDY", timemask="hh.mm", startdate=datetime.datetime(year=2013, month=8, day=12))
        assert len(sofs3) == 2
        assert sofs3[0].startdatetime.year == 2013
        assert sofs3[0].startdatetime.month == 8
        assert sofs3[0].startdatetime.day == 12


    def test_pdfextractor(self):
        extractor = SOFPDFExtractor('./pdfs/test.pdf')
        result = extractor.extract()
        textextractor = SOFTextExtractor(self.generator)
        sofs = textextractor.extract(result, starttext="Terminal / Comment", dateorder="DMY", timemask="hh:mm")
        assert len(sofs) == 10
        