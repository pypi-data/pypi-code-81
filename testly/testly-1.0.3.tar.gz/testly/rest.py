import requests
import __main__
from typing import overload


def call_restendpoint():
    if __main__.debug == 1:
        print("DEBUG: REST url: ", __main__.host)

    Restyl = Restly()
    if __main__.host == '' or __main__.host == None:
        print("ERROR: Please specifiy host ")
        return __main__.sys.exit(2)

    else:
        Restyl.getStatus(__main__.host)


class Restly:
    #Dictionary to map the requestmethods to strings
    function_mappings = {
        'get': requests.get,
        'post': requests.post,
        'put': requests.put,
        'delete': requests.delete
    }

    def getStatus(self, URL):
        try:
            HTTPResponse = requests.get(URL)
            print("Status Code for {}: {} ".format(URL,
                                                   HTTPResponse.status_code))

        except requests.exceptions.RequestException as RaisedException:
            print(RaisedException)



    @overload
    def processRequest(self, URL, requestMethod):

        try:
            HTTPRequest = self.function_mappings[requestMethod](URL)
            print("Status Code for {}: {} ".format(URL,
                                                   HTTPRequest.status_code))

        except requests.exceptions.RequestException as RaisedException:
            print(RaisedException)



    
    def processRequest(self, URL, requestMethod, bodyContains,requestCode):

        try:
            HTTPRequest = self.function_mappings[requestMethod](URL)
            print("Status Code for {}: {} . Request Matched {} \n".
            format(URL,HTTPRequest.status_code, HTTPRequest.status_code==requestCode))

            ## Determine if the body contains what the user has specified                                                   
            json_response = HTTPRequest.json()
            for key, value in bodyContains.items():
                print("Response body for {} key contains {} . Body Matched : {} \n".format(
                 key, json_response[key],json_response[key]==value
             ))


        except requests.exceptions.RequestException as RaisedException:
            print(RaisedException)

     
    def processRequestPutPost(self, URL, requestMethod, bodyContains,requestCode,payload):

        try:
            HTTPRequest = self.function_mappings[requestMethod](URL,payload)
            print("Status Code for {}: {} . Request Matched {} \n".
            format(URL,HTTPRequest.status_code, HTTPRequest.status_code==requestCode))

            ## Determine if the body contains what the user has specified                                                   
            json_response = HTTPRequest.json()
            for key, value in bodyContains.items():
                print("Response body for {} key contains {} . Body Matched : {} \n".format(
                 key, json_response[key],json_response[key]==value
             ))


        except requests.exceptions.RequestException as RaisedException:
            print(RaisedException)


    def executeTests(self, testParams):

        try:
            ##If the user enters a key value pair that must be in the response
            if "bodyContains" and "payload" in testParams:
                self.processRequestPutPost(
                testParams['url'], testParams['requestMethod'],testParams['bodyContains'],
                testParams['responseCode'],testParams['payload'])

            elif "bodyContains" in testParams:

                self.processRequest(
                testParams['url'], testParams['requestMethod'],testParams['bodyContains'],
                testParams['responseCode'])
            
            else:
                 self.processRequest(
                    testParams['url'], testParams['requestMethod'])
        except Exception:
            print("Error Please check the yaml test syntax")

           

