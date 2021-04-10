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


targetTag = [
    [
        ["root","tr", 8],
        [["child","td","searchResultsTitleValue",["child","a","classifiedTitle",[]]],
         ["child","td","searchResultsAttributeValue",["sibling",2]],
         ["child","td","searchResultsPriceValue",["child","div",None, []]],
         ["child","td","searchResultsLocationValue",[]]
         ]
    ]
]

tagFast = [
    ["a","classifiedTitle"],
    ["div",None],
    ["td","searchResultsAttributeValue"],
    ["td","searchResultsLocationValue"]
]