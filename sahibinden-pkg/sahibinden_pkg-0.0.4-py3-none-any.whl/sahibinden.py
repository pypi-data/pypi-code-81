import requests
import requests.exceptions as r_e
from bs4 import BeautifulSoup
from bs4 import Tag
from bs4 import element
import re
from statistics import mean
from statistics import median
import time
import json


parameters = {
    'url_base':"https://www.sahibinden.com",

    'current_filter': "searchResultsItem",
    'current_page_filter':"pageNaviButtons",

    'connect_parametre':{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.90 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0"
    },
    "tag-selection-tag-page_number": "pageNaviButtons",
    "tag-selection-text-total_page_number":"mbdef",
    "tag-selection-text-total_total_advert":"result-text",
    "tag-selection-tag-search-data": "searchResultsItem"

}


tagFast = [
    ["a","classifiedTitle"],
    ["div",None],
    ["td","searchResultsAttributeValue"],
    ["td","searchResultsLocationValue"]
]






class sahibinden:

    def __init__(self, url):
        try:
            self.paramaters = parameters
            self.initialUrl = url
            self.tagFast = tagFast
            self.current_raw_data = None
            self.current_prepared_data = None
            self.page_index_data = None

            self.TagMapPicture = []
            self.PageMapPicture = []
            self.pageUrl = None
            self.totalPage = None
            self.processedPage = None
            self.use_URL = None

        except ImportError as e:
            print("There is an error of importing configuration {}".format(e))

    def createUrl(self):
        if self.current_raw_data == None:
            try:
                if self.initialUrl:
                    self.use_URL = self.initialUrl
                    return self.use_URL
                else:
                    return None
            except Exception as e:
                print(e)
        else:
            if self.processedPage:
                if self.totalPage >= self.processedPage:
                    self.use_URL = self.initialUrl+"?pagingOffset="+str(self.processedPage*20)
                    return self.use_URL
                else:
                    return None

    def _printRawData(self):
        print(self.current_raw_data.prettify())

    def _getsample(self,tg: element.Tag):
        print("Main",tg.name)
        for i in tg.contents:
            if type(i) == element.Tag:
                print(i.name)
                self._getsample(i)
                if i.name == None:
                    print("All",i)

    def _calculateRawPageData(self):
        try:
            url = self.createUrl()
            r = requests.get(url, headers=self.paramaters['connect_parametre'])
            self.current_raw_data = BeautifulSoup(r.text, "lxml")
        except r_e.RequestException:
            print(r_e)

    def _getspecificTag(self, filter):
        return self.current_raw_data.find_all(class_= filter)

    def _extractString(self,tg:element.Tag):
        data = []
        if tg.string == None:
            for i in tg.next_elements:
                if i.name == tg.name:
                    break
                if i.string:
                    if i.string.strip():
                        data.append(i.string.strip())
            return data

    def _resetTagPicture(self):
        self.TagMapPicture.clear()

    def _resetPagePicture(self):
        self.PageMapPicture.clear()

    def _createPageFast(self):
        ### Connect the site and get the 1.Page Data
        self._calculateRawPageData()
        self.current_prepared_data = \
            self._getspecificTag(self.paramaters['tag-selection-tag-search-data'])

        ####
        for page in self.current_prepared_data:
            index = self.current_prepared_data.index(page)
            if "classicNativeAd" in page.attrs['class']:
                continue
            self._createTagDataFast(page)
            self.PageMapPicture.append([index,self.TagMapPicture.copy()])
            self._resetTagPicture()

    def _createTagDataFast(self,tg: element.Tag):
        a = self._baseRule(tg)
        if a:
            self.TagMapPicture.append(a)
            return
        for i in tg.contents:
            if type(i) == element.Tag:
                self._createTagDataFast(i)

    def _baseRule(self,tg: element.Tag):
        for ruledata in self.tagFast:
            if tg.name == ruledata[0]:
                if ruledata[1]:
                    if tg.has_attr("class"):
                        if ruledata[1] in tg.attrs['class']:
                            if tg.string:
                                return [tg.name,tg.string.strip()]
                            else:
                                self._extractString(tg)
                                return [tg.name,self._extractString(tg)]
                    else:
                        continue
                else:
                    if tg.string:
                        return [tg.name,tg.string.strip()]
                    else:
                        continue
            else:
                continue
        return None



    def _processSinglePage(self):
        self._createPageFast()
        rlist = []
        def processName():
            for i in self.PageMapPicture:
                rlist.insert(self.PageMapPicture.index(i),[self.PageMapPicture.index(i)])
        processName()
        def processMetreKare():
            for i in self.PageMapPicture:
                rlist[self.PageMapPicture.index(i)].append(int(i[1][1][1]))
        processMetreKare()
        def processRoom():
            for i in self.PageMapPicture:
                if i[1][2][1] == "Stüdyo (1+0)":
                    roomlist = [1.0,0.0]
                elif i[1][2][1] == "10 Üzeri":
                    roomlist = [11.0,1.0]
                else:
                    roomlist = i[1][2][1].split('+')
                    roomlist = [float(a) for a in roomlist]
                rlist[self.PageMapPicture.index(i)].append(roomlist)
        processRoom()
        def processPrice():
            for i in self.PageMapPicture:
                price = i[1][3][1].split(" ")
                price = price[0]
                if price.find("."):
                    stripled_text = price.replace(".", "")
                    price = int(stripled_text)
                else:
                    price = int(price)
                rlist[self.PageMapPicture.index(i)].append(price)
        processPrice()
        def processNeighbourHood():
            for i in self.PageMapPicture:
                data = i[1][4][1]
                rlist[self.PageMapPicture.index(i)].append(data)
        processNeighbourHood()
        self._createTargetDataPerPage(rlist)
        self._resetPagePicture()
        return rlist

    def _pageIndex(self):
        self.page_index_data = self._getspecificTag("mbdef")
        list = self.page_index_data[0].string.split(" ")
        self.totalPage = int(list[1])

    def _getQueryData(self):
        if self.current_raw_data == None:
            list = self._processSinglePage()
            print(self.use_URL)
            print(list)
            self._pageIndex()
            self.processedPage = 1
            print("Waiting for 60 sec for next page extraction")
            time.sleep(60)

        while self.use_URL:
            self.use_URL = self.createUrl()
            print(self.use_URL)
            list = self._processSinglePage()
            print(list)
            self.processedPage += 1
            print("Waiting for 60 sec for next page extraction")
            time.sleep(60)

    def _createTargetDataPerPage(self, rlist):
        try:
            with open("data.txt","a+") as f:
                json.dump(rlist,f)
        except Exception as e:
            print(e)




