try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import subprocess
import os
import time
import PyPDF2
import csv
import re
import pdfplumber
import datetime
from datetime import timezone
from dateparser_data.settings import default_parsers
from dateparser.search import search_dates
from datetime import timezone
from rdflib import Namespace,URIRef, BNode, Literal,Graph, plugin
from dateutil.parser import parse
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from uuid import uuid4
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD

SHC = Namespace("http://data.shinc.co.uk/")
NS = { 'foaf': FOAF, 'rdfs' : RDFS, "owl" : OWL, 'xsd' : XSD, 'rdf' : RDF, 'shc' : SHC}

class SOFImageExtractor:

    def __init__(self, image, tmppath='/tmp'):
        self.tmppath = tmppath
        self.image = image


    def ocr(self, image):
        fn = self.tmppath + "/" + str(uuid4())
        cp = subprocess.run(["tesseract", "{}".format(image), "{}".format(fn)], check=True)
        if cp.returncode != 0:
            del environ[response_key]
            raise SOFException("Error running ocr " + image + " " + fn)
        else:
            time_to_wait = 5
            time_counter = 0
            while not os.path.exists(fn + ".txt"):
                time.sleep(1)
                time_counter += 1
                if time_counter > time_to_wait:break
            if os.path.exists(fn + ".txt"):
                result_file = open(fn + ".txt", 'r')
                result = result_file.read()
                result_file.close()
                os.remove(fn + ".txt")
            else:
                raise SOFException("Error writing OCR " + image + " " + fn + ".txt")
        return result

    def processOcrLine(self, n):
        return n.strip()

    def extract(self):
        return list(map(self.processOcrLine, self.ocr(self.image).split("\n")))



class SOFTextExtractor:

    DATEPATTERNS = [

        {
            "name": 'dd-mmmm-yyyy',
            "mask": "%d/%m/%Y",
            "regex": '((31(?!\-(FEB|Feb(ruary)?|APR|Apr(il)?|JUN|June?|(SEP|Sep(?=\b|t)t?|NOV|Nov)(ember)?)))|((30|29)(?!\-FEB|Feb(ruary)?))|(29(?=\-FEB|Feb(ruary)?\-(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\-(JAN|Jan(uary)?|FEB|Feb(ruary)?|MAR|Ma(r(ch)?|y)|APR|Apr(il)?|JUL|Ju((ly?)|(ne?))|AUG|Aug(ust)?|OCT|Oct(ober)?|(SEP|Sep(?=\b|t)t?|NOV|Nov|DEC|Dec)(ember)?)\-((1[6-9]|[2-9]\d)\d{2})',
            "delimiter": '-',
            "function":"date_parse",
            "type" : "dmy"
        },

        {
            "name": 'dd/mmmm/yyyy',
            "mask": "%d/%m/%Y",
            "regex": '((31(?!\/(FEB|Feb(ruary)?|APR|Apr(il)?|JUN|June?|(SEP|Sep(?=\b|t)t?|NOV|Nov)(ember)?)))|((30|29)(?!\/FEB|Feb(ruary)?))|(29(?=\/FEB|Feb(ruary)?\/(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\/(JAN|Jan(uary)?|FEB|Feb(ruary)?|MAR|Ma(r(ch)?|y)|APR|Apr(il)?|JUL|Ju((ly?)|(ne?))|AUG|Aug(ust)?|OCT|Oct(ober)?|(SEP|Sep(?=\b|t)t?|NOV|Nov|DEC|Dec)(ember)?)\/((1[6-9]|[2-9]\d)\d{2})',
            "delimiter": '/',
            "function":"date_parse",
            "type" : "dmy"
        },


        {
            "name": 'dd mmmm yyyy',
            "mask": "%d/%m/%Y",
            "regex": '((31(?!\ (FEB|Feb(ruary)?|APR|Apr(il)?|JUN|June?|(SEP|Sep(?=\b|t)t?|NOV|Nov)(ember)?)))|((30|29)(?!\ FEB|Feb(ruary)?))|(29(?=\ FEB|Feb(ruary)?\ (((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\ (JAN|Jan(uary)?|FEB|Feb(ruary)?|MAR|Ma(r(ch)?|y)|APR|Apr(il)?|JUL|Ju((ly?)|(ne?))|AUG|Aug(ust)?|OCT|Oct(ober)?|(SEP|Sep(?=\b|t)t?|NOV|Nov|DEC|Dec)(ember)?)\ ((1[6-9]|[2-9]\d)\d{2})',
            "delimiter": ' ',
            "function":"date_parse",
            "type" : "dmy"
        },

        {

            "name": 'mmmm dd yyyy',
            "mask": "%m/%d/%Y",
            "regex" : "(JAN|Jan|January|FEB|Feb|February|MAR|Mar|March|APR|Apr|April|MAY|May|JUN|Jun|June|JUL|Jul|July|AUG|Aug|August|SEP|Sep|September|OCT|Oct|October|NOV|Nov|November|DEC|Dec|December)[^A-Za-z0-9]+([1-9]|[1-3][0-9])[^A-Za-z0-9]+\d{4}",
            "delimiter" : "[^A-Za-z0-9]+",
            "function":"date_parse",
            "type":"mdy"    
        },

        {

            "name": 'dd mmmm yyyy',
            "mask": "%m/%d/%Y",
            "regex" : "([1-9]|[1-3][0-9])[^A-Za-z0-9]+(JAN|Jan|January|FEB|Feb|February|MAR|Mar|March|APR|Apr|April|MAY|May|JUN|Jun|June|JUL|Jul|July|AUG|Aug|August|SEP|Sep|September|OCT|Oct|October|NOV|Nov|November|DEC|Dec|December)[^A-Za-z0-9]+\d{4}",
            "delimiter" : "[^A-Za-z0-9]+",
            "function":"date_parse",
            "type":"dmy"    
        } 

    ]

    TIMEPATTERNS = [

        {
            "name": 'hh:mm',
            "regex": "([01]\d|2[0-3]):([0-5]\d)",
            "delimiter": ':'
        },  

        {
            "name": 'hh.mm',
            "regex": "([01]\d|2[0-3])[.]([0-5]\d)",
            "delimiter": '.'
        },  

        {
            "name": 'hhmm',
            "regex": "([01]\d|2[0-3])([0-5]\d)",
            "delimiter": ''
        }  ,  

        {
            "name": 'hh mm',
            "regex": "([01]\d|2[0-3])[ ]([0-5]\d)",
            "delimiter": ' '
        },

        {
            "name": 'hh,mm',
            "regex": "([01]\d|2[0-3])[,]([0-5]\d)",
            "delimiter": ','
        }    

    ]
        

    def __init__(self, soflist, timepatterns=None, datepatterns=None):
        self.soflist = soflist
        if timepatterns:
            self.timepatterns = timepatterns
        else:
            self.timepatterns = SOFTextExtractor.TIMEPATTERNS
        if datepatterns:
            self.datepatterns = datepatterns
        else:
            self.datepatterns = SOFTextExtractor.DATEPATTERNS
        pass

    def extract(self, text, starttext=None, endtext=None, startdate=None, enddate=None, dateorder=None, timemask="hh:mm", timezone=timezone.utc):
        sofs = []
        summary_sofs = []
        date_count = startdate
        lines = text.splitlines()
        if starttext:
            started = False
        else:
            started = True
        for line in lines:
            if started and self.textContainsSof(line):
                sof= self.extractLine(line, date_count, dateorder, timemask, timezone)
                if sof.startdatetime:
                    date_count = sof.startdatetime
                sofs.append(sof)
                if next((x for x in self.soflist.softypes if x.id == sof.id and x.summary), None):
                    summary_sofs.append(sof)
            elif started and self.extractDate(line,dateorder):
                date_count = self.extractDate(line,dateorder)[0]
            else:
                if starttext and starttext in line:
                    print("started reading")
                    started = True
        return sofs
                    

                

    def extractLine(self, text, date_count, dateorder, timemask, timezone=timezone.utc):

        restext = text
        softype = self.textContainsSof(text)
        id = SHC + str(uuid4())
        sof = SOFEvent(id, softype.id, softype.description)
        times = self.extractTime(text, timemask)
        time_from = None
        time_to = None
        date_from = None
        date_to = None
        if times:
            time_from = times[0]
            time_to = None
            if softype.bounded and len(times) > 1:
                time_to = times[1]
        dates = self.extractDate(text, dateorder)
        if dates:
            date_from = dates[0]
            date_to = None
            if len(dates) > 1:
                date_to = dates[1]
        else:
            date_from = date_count
            date_to = None
        if (times and not dates) and (softype.bounded and time_to) and (time_to < time_from):
            date_to = date_count + datetime.timedelta(days=1)
        if not time_from:
            time_from = date_from
        if date_from and time_from:
            sof.startdatetime = self.generateDatetime(date_from, time_from,timezone)
        if softype.bounded and time_to:
            if not date_to:
                date_to = date_from
            sof.enddatetime = self.generateDatetime(date_to, time_to,timezone)
        return sof

    def textContainsSof(self, text):
        res = False
        for sof in self.soflist.softypes:
            if sof.description in text:
                return sof
        return res

    def extractTime(self, text, timemask=None):
        res = None
        if timemask:
            timepattern = next((x for x in self.timepatterns if x['name'] == timemask), None)
        else:
            timepattern = containsTime(text)
        if timepattern:
            res = []
            times = re.findall(timepattern['regex'], text)
            if times and len(times):
                res.append(datetime.time(int(times[0][0]), int(times[0][1])))
                if len(times) > 1:
                    res.append(datetime.time(int(times[1][0]), int(times[1][1])))    

        return res

    def containsTime(self, text):
        for mask in self.timepatterns:
            if re.findall(mask['regex'], text):
                return mask
        return None

    def parseTime(self, timestring, delimiter):
        return time(int(timestring.split(delimiter)[0]), int(timestring.split(delimiter)[1]),0)

    def parseDate(self, datestring, delimiter):
        return date(int(datestring.split(delimiter)[2]), int(datestring.split(delimiter)[1]), int(datestring.split(delimiter)[0]))

    
    def extSearch(self, text, regex):
        resultset=None
        while re.search(regex, text):
            if not resultset:
                resultset = []
            res = re.search(regex, text,re.IGNORECASE).group(0)
            resultset.append(res)
            text = text.replace(res, "", 1)
        return resultset


    def extractDate(self, text, dateorder):
        res = None
        
        if dateorder:
            dates =  search_dates(text, settings={'DATE_ORDER': dateorder, 'RELATIVE_BASE': datetime.datetime(1925, 1, 1)})
        else:
            dates =  search_dates(text, settings={'RELATIVE_BASE': datetime.datetime(1925, 1, 1)})
        if dates and len(dates) > 0:
            for adate in dates:
                delimiters = list(filter(self.checkDelim, re.split("[a-zA-Z0-9]+", adate[0])))

                if  adate[1].year > 1970 and not (self.containsTime(adate[0])) and len(delimiters) == 2 and (delimiters[0] == delimiters[1]):
                    if not res:
                        res = []
                    res.append(adate[1])   

        if not res:
            for datepattern in self.datepatterns:
                patternres = self.extSearch(text, datepattern['regex'])
                if patternres:
                    if not res:
                        res = []
                    mth = getattr(self, datepattern['function'])
                    for pattern in patternres:
                        if pattern and len(re.split('[^a-zA-Z0-9]+', pattern)) > 2:
                            res.append(mth(pattern,datepattern))
                    return res

        return res

    def checkDelim(self, delim):
        return delim != ""

    def generateDatetime(self, dateobj, timeobj, timezone):
        return datetime.datetime(year=dateobj.year, month=dateobj.month, day=dateobj.day,hour=timeobj.hour,minute=timeobj.minute, tzinfo=timezone.utc)


    def monthToNum(self, textMonth):
        return {
                'jan' : 1,
                'feb' : 2,
                'mar' : 3,
                'apr' : 4,
                'jun' : 6,
                'jul' : 7,
                'aug' : 8,
                'sep' : 9, 
                'oct' : 10,
                'nov' : 11,
                'dec' : 12,
                'january' : 1,
                'february' : 2,
                'march' : 3,
                'april' : 4,
                'may' : 5,
                'june' : 6,
                'july' : 7,
                'august' : 8,
                'september' : 9, 
                'october' : 10,
                'november' : 11,
                'december' : 12
        }[textMonth.lower()]



    def date_parse(self, datestring, datepattern):
        dateparts = re.split('[^a-zA-Z0-9]+', datestring)
        thirddate = int(dateparts[2])
        if datepattern['type'].lower() == 'dmy':
            firstdate = int(dateparts[0])
            seconddate = self.monthToNum(dateparts[1])
        else:
            firstdate = int(dateparts[1])
            seconddate = self.monthToNum(dateparts[0])
        return datetime.datetime(day=firstdate, month=seconddate, year=thirddate)


    def dd_mmmm_yyyy(self, result, delimiter):
        if len(delimiter) == 2:
            firstdate = result.split(delimiter[0])[0]
            remaingdate = result.replace(firstdate + delimiter[0],"",1)
            seconddate = remainingdate.split(delimiter[1])[0]
            thirddate = remainingdate.split(delimter[1])[1]
            return datetime.datetime(day=int(firstdate), month=self.monthToNum(seconddate), year=int(thirddate)) 
        else:
            fulldate = result.split(delimiter)
            return datetime.datetime(day=int(fulldate[0]), month=self.monthToNum(fulldate[1]), year=int(fulldate[2]))

    def mmmm_dd_yyyy(self, result, delimiter):
        string = re.sub("")
        if len(delimiter) == 2:
            seconddate = result.split(delimiter[0])[0]
            remaingdate = result.replace(firstdate + delimiter[0],"",1)
            firstdate = remainingdate.split(delimiter[1])[0]
            thirddate = remainingdate.split(delimter[1])[1]
            return datetime.datetime(day=int(firstdate), month=self.monthToNum(seconddate), year=int(thirddate)) 
        else:
            fulldate = result.split(delimiter)
            return datetime.datetime(day=int(fulldate[0]), month=self.monthToNum(fulldate[1]), year=int(fulldate[2])) 



class SOFPDFExtractor:
    def __init__(self, pdf):
        self.pdf = pdf

    def createTextFromPdf(self, pdf):
        content = ""
        with pdfplumber.open(pdf) as pdf:
            for page in pdf.pages:
                content += page.extract_text()
        
        return content

    def extract(self):
        return self.createTextFromPdf(self.pdf)



class SOFEvent:
    def __init__(self, id, type=None, description=None, time_from=None, time_to=None, date_from=None, date_to=None):
        self.id = id
        self.type = type
        self.startdatetime = date_from
        self.description = description
        self.enddatetime = time_to

    def __eq__(self, other):
        if (isinstance(other, SOFEvent)):
            return self.id == other.id and self.type == other.type and self.startdatetime == other.startdatetime and self.description == other.description
        return False

    def __str__(self):
        return str(self.id) + "\t" + str(self.type) + "\t" + str(self.startdatetime) + "\t" + str(self.description) + "\t" + str(self.enddatetime)
        

class SOF:
    def __init__(self, id, sofs=None):
        self.id = id
        self.sofs = sofs

    def add(self, sof):
        checked = False
        if not (x for x in self.sofs if x == sof):
            self.sofs.append(sof)

    def reorder(self):
        orderedsofs = sorted(self.sofs, key=lambda x: x.startdatetime)
        self.sofs = orderedsofs



class SOFType:
    def __init__(self,id, description, bounded=False, notation=False, stoppage=False, display=False, summary=False):
        self.id = id
        self.description = description
        self.bounded = bounded
        self.notation = notation
        self.stoppage = stoppage
        self.display = display
        self.summary = summary

class SOFList:
    def __init__(self, file):
        self.file = file
        self.sofs = None
        self.softypes = []

    def generate(self):
        return self.createListFromFile(self.file)

    def createListFromFile(self, file):
        self.sofs = Graph()
        f = open(file, "r")
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                name = row[0]
                uri = URIRef(SHC + name.replace(" ","-"))
                softype = SOFType(SHC + name.replace(" ","-"), name)
                softype.description = name
                self.sofs.add((uri, RDFS.label, Literal(name, lang="en")))
                self.sofs.add((uri, RDFS.subClassOf, SHC.Event))
                if row[1] == "1":
                    self.sofs.add((uri, RDFS.subClassOf, SHC.BoundedEvent))
                    softype.bounded = True
                if row[4] == "1":
                    self.sofs.add((uri, RDFS.subClassOf, SHC.DisplayableEvent))  
                    softype.notation = True
                if row[5] == "1":
                    self.sofs.add((uri, RDFS.subClassOf, SHC.SummaryEvent))  
                    softype.summary = True
                self.softypes.append(softype)  
        f.close()
        return self.sofs

    def getUriFromDescription(self, text):
        rows = self.sofs.query("SELECT ?type WHERE {?type rdfs:label '" + text + "' } ", initNs=NS)
        return str(rows[0])


class SOFException(Exception):
    pass
