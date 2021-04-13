import requests
import base64
import datetime
import traceback
import json

############################# NEXUS REST API V2 Functions ############################
class NEXUSIC_REST():
    """
    NEXUS IC REST API class allows the user to communicate with Wood NEXUS IC REST API using python.

    Prerequisites:
    -------------
        - Python > 3.7
        - NEXUS IC > V6.6
        - IC-Web > V6.6

    NEXUS IC Documentation:
    ----------------------
        The NEXUS IC REST API documentation can be found in the below link:
        https://docs.nexusic.com/6.6/ic-web.rest.v2.html

        A specific NEXUS IC version can be specified in the above link by changing **6.6** to the desired NEXUS IC version*
    """

    _error_msgs = ['An existing connection was forcibly closed by the remote host',
                   'Remote end closed connection without response']

    def __init__(self, icweb_uri, authentication_type='APIKEY',
                 username=None, password=None, api_key=None,
                 max_attempts=1, timeout=None, verbose=False, verify=True):
        """

            :param icweb_uri: (``string``) - IC-Web URL.
            :param authentication_type: (``string`` - optional) - This can be one of the following values  (default value APIKEY).

                .. code-block:: python

                        ['APIKEY', 'BASIC']

            :param username: (``string`` - optional) - Default value None.
            :param password: (``string`` - optional) - Default value None.
            :param api_key: (``string`` - optional) - Default value None.
            :param max_attempts: (``int`` - optional) - Maximum number of attempts if disconnected (default value 1).
            :param timeout: (``int`` - optional) - Timeout threshold in seconds (default value None).
            :param verbose: (``bool`` - optional) - Print internal messages if True (default value False).
            :param verify: (``bool`` - optional) - By pass SSL verification if True (default value True).

            :returns: None
        """

        self.icweb_uri = icweb_uri
        self.authentication_type = authentication_type

        self.api_key = api_key
        self.username = username
        self.password = password

        self.max_attempts = max_attempts
        self.timeout = timeout   # TODO: To be added to the REST calls
        self.verbose = verbose
        self.verify = verify

        assert authentication_type in ['APIKEY', 'BASIC'], 'Incorrect authentication type'

        if authentication_type == 'APIKEY':
            if self.api_key != None:
                self.key_64 = self.generate_base64(api_key)
            else:
                raise Exception('API Key is not valid, please provide a valid API Key')
        elif authentication_type == 'BASIC':
            if self.username != None or self.password != None:
                self.key_64 = self.generate_base64(self.username + ':' + self.password)
            else:
                raise Exception('Username and/or password are not valid, please provide a valid username/password')
        else:
            raise Exception('Authentication type was not specified')

        self.hash = self.generate_hash()

        # Get current NEXUS version
        version, version_status_code = self.getVersion()
        self.version = version['version'].split('.')
        self.schema = version['schema'].split('.')

    ################################ Core REST API Calls #################################
    ######################################################################################
    def generate_base64(self, value):
        """
            Generate base64 string

            :param value: (``string``) - String value to be converted to base64.

            :returns: (``String``) - base64 string.
        """
        return str(base64.b64encode(bytes(value, 'utf-8')), "utf-8")

    ######################################################################################
    def generate_hash(self, verbose=False):
        """
            Generate hash key to be used in the REST calls

            :param verbose: (``bool`` - optional) - Print internal messages if True (default value False).

            :return: (``string``) - Hash key
        """

        result, result_code = self.authenticate(verbose=verbose)

        if result_code == 200:
            return result.get('hash')
        else:
            errorMsg = traceback.format_exc()
            raise Exception(result + '\n' + errorMsg)

    ######################################################################################
    def addParamToURI(self, uri, param, value):
        if '?' in uri:
            newUri = uri + '&' + param + '=' + value
        else:
            newUri = uri + '?' + param + '=' + value

        return newUri

    ######################################################################################
    def validate_and_return_response(self, response, message, raw=False):
        """
            Validate response by comparing it against the acceptable status codes. Returns response and status code.

            :param response: (``requests.response``) - The response from the query.
            :param message: (``string`` - optional) - Desired custom error message.
            :param raw: (``bool`` - optional) - Defines whether to return response raw format or json (default value False).

            :return: (``tuple`` - dict or string, string) - response (json, raw or error string) and response status code.
        """

        if response.status_code in [200]:
            if raw:
                return response.raw, response.status_code
            else:
                return response.json(), response.status_code
        else:
            return str(message) + str(response.status_code) + ': ' + str(response.text), \
                   response.status_code

    ######################################################################################
    def authenticate(self, verbose=False):
        """
            Authenticate with NEXUS IC using the defined authentication type used in the class constructor.
            For more details see https://docs.nexusic.com/6.6/ic-web.rest.security.login.html#ic-web-rest-security-login

            :param verbose: (``bool`` - optional) - Print internal messages if True (default value False).

            :return: (``tuple`` - dict or string, string) - response (json, raw or error string) and response status code.
        """

        if self.verbose or verbose:
            print('Authenticating with NEXUS IC...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/security/login'
        res = requests.get(uri, headers={'Authorization': self.authentication_type + ' ' + self.key_64},
                           verify=self.verify)

        return self.validate_and_return_response(res, 'Authentication error ')

    ######################################################################################
    def getVersion(self, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Getting NEXUS IC version...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/version' + '?hash=' + self.hash

        try:
            res = requests.get(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get version error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getVersion(current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def getTable(self, tableDBName, xFilter=None, pageSize=None,
                 current_attempt=1, verbose=False):
        """
            Execute GET REST call to get data from specific table

            :param tableDBName: (``string``) - Table name as specified in the database (not the NEXUS IC display table name).
            :param xFilter: ( ``dict`` in ``JSON`` fomrat - optional) - Used to filter data from the required table (default value None).
            :param pageSize: (``int`` - optional) - Page size for response (default value None). When default is used the default NEXUS IC page size will be used (100).
            :param current_attempt: (``int`` - **don't use**) - This arugment is intended for internal method use only.
            :param verbose: (``bool`` - optional) - Print internal messages if True (default value False).

            :return: (``tuple`` - dict or string, string) - response (json, raw or error string) and response status code.
        """

        if self.verbose or verbose:
            print('Getting ' + str(tableDBName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableDBName + '/'

        # Adding pageSize
        if pageSize == None:
            pageSize = 100

        uri = self.addParamToURI(uri, 'pageSize', str(pageSize))

        # Adding startRow
        startRow = 0
        uri = self.addParamToURI(uri, 'startRow', str(startRow))

        # Adding hash value
        uri = self.addParamToURI(uri, 'hash', self.hash)

        try:
            if xFilter != None:
                res = requests.get(uri, headers={'X-NEXUS-Filter': xFilter}, verify=self.verify)
            else:
                res = requests.get(uri, verify=self.verify)

            result, result_code = self.validate_and_return_response(res, 'Get ' + tableDBName + ' table error ')

            # Get next page
            uri = uri.replace('startRow=' + str(startRow), 'startRow=' + str(pageSize))
            startRow = pageSize
            while len(result['rows']) < result['totalRows']:
                if xFilter != None:
                    res = requests.get(uri, headers={'X-NEXUS-Filter': xFilter}, verify=self.verify)
                else:
                    res = requests.get(uri, verify=self.verify)

                result2, result_code2 = self.validate_and_return_response(res, 'Get ' + tableDBName + ' table error ')
                result['rows'].extend(result2['rows'])

                prevStartRow = startRow
                startRow += pageSize
                uri = uri.replace('startRow=' + str(prevStartRow), 'startRow=' + str(startRow))

            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getTable(tableDBName, xFilter=xFilter, pageSize=pageSize,
                                        current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def deleteRecord(self, tableDBName, keyValue, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Deleting from ' + str(tableDBName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableDBName + '/' + str(keyValue) + '/' + '?hash=' + self.hash

        try:
            res = requests.delete(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Delete ' + tableDBName + ' table error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.deleteRecord(tableDBName, keyValue, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def getMultimedia(self, rd_id, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Getting multimedia: ' + str(rd_id) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        xFilter = str(rd_id) + '/File_Data'
        uri = baseURI + '/bo/' + 'Repository_Data' + '/' + xFilter + '/' + '?hash=' + self.hash

        try:
            res = requests.get(uri, stream=True, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get multimeida error ', raw=True)
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getMultimedia(rd_id, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    # V6.6 only
    def getDashboard(self, dashboard_Name, current_attempt=1, verbose=False):
        # Check if minor version is 6
        if not(int(self.version[1]) >= 6):
            return 'This function is not supported in the current NEXUS IC version', 404

        if self.verbose or verbose:
            print('Generating NEXUS IC dashboard...')

        # Get RT_ID
        xFilter = '{"where": [{"field": "Name", "value": "' + dashboard_Name + '"}]}'
        report_json, report_status = self.getTable('Report_Template', xFilter=xFilter)

        if report_status == 404:
            return str(report_status) + ': ' + str(report_json), report_status
        else:
            rt_id = report_json['rows'][0]['RT_ID']

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/dashboard/' + str(rt_id) + '/' + '?hash=' + self.hash

        try:
            res = requests.get(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get ' + dashboard_Name + ' error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getDashboard(dashboard_Name, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def generateReport(self, report_name, recipient, format='XLSX', current_attempt=1,
                       verbose=False):
        if self.verbose or verbose:
            print('Generating NEXUS IC report...')

        # Get RT_ID
        xFilter = '{"where": [{"field": "Name", "value": "' + report_name + '"}]}'
        report_json, report_status = self.getTable('Report_Template', xFilter=xFilter)

        if report_status == 404:
            return str(report_status) + ': ' + str(report_json), report_status
        else:
            rt_id = report_json['rows'][0]['RT_ID']

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        # Generate report
        uri = baseURI + '/web/generateReport'
        uri += '?key=' + str(rt_id) + '&format=' + format + '&recipient=' + recipient + '&hash=' + self.hash

        try:
            res = requests.post(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Generate ' + report_name + ' report error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.generateReport(report_name, recipient, format=format,
                                              current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def execFunction(self, functionName, parameters=None, current_attempt=1,
                     verbose=False):
        if self.verbose or verbose:
            print('Executing ' + str(functionName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/function/' + functionName
        uri += '/' + '?hash=' + self.hash

        try:
            res = requests.post(uri, json=parameters, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Execute function ' + functionName + ' error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.execFunction(functionName, parameters=parameters,
                                            current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def execUpdate(self, tableDBName, tableID, body, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Updating ' + str(tableDBName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableDBName + '/' + tableID
        uri += '?hash=' + self.hash

        try:
            res = requests.post(uri, json=body, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Updating ' + tableDBName + ' error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.execUpdate(tableDBName, tableID, body,
                                          current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def createNewRecord(self, tableDBName, body, key_value=0, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Creating new record in ' + str(tableDBName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableDBName + '/' + str(key_value)
        uri += '?hash=' + self.hash

        try:
            res = requests.put(uri, json=body, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Creating new record in ' + tableDBName + ' error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.execUpdate(tableDBName, body, key_value=key_value,
                                               current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ############################ Specific REST API Calls #################################
    ######################################################################################
    def getAssetLocationByName(self, assetName, assetView,
                         pageSize=None, verbose=False):
        x_filter = {"operator": "and",
                    "where": [{"field": "Comp_View.Name", "value": assetView},
                              {"field": "Component.Name", "value": assetName}]
                    }

        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('View_Node', xFilter=x_filter, pageSize=pageSize, verbose=verbose)

        return result, result_code

    ######################################################################################
    def getAssetLocationByID(self, assetID, assetView,
                         pageSize=None, verbose=False):
        x_filter = {"operator": "and",
                    "where": [{"field": "Comp_View.Name", "value": assetView},
                              {"field": "Component.Component_ID", "value": assetID}]
                    }

        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('View_Node', xFilter=x_filter, pageSize=pageSize, verbose=verbose)

        return result, result_code

    ######################################################################################
    def getAssetChildren(self, assetLocation, assetView=None, searchType='MAX LEVEL', assetTypes=None,
                         maxLevel=-1, atLevel=-1, pageSize=None, verbose=False):
        assert searchType in ['MAX LEVEL', 'AT LEVEL'], 'Incorrect search type'

        x_filter = {"operator": "and",
                    "where": [{"field": "View_Node.VN_ID", "method": "ch", "value": assetLocation}]
                    }

        # Apply asset view filter
        if assetView != None:
            x_filter['where'].append({"field": "Comp_View.Name", "value": assetView})

        # Apply asset type filters
        if assetTypes != None:
            # Get asset type IDs
            assetTypeIDs = self.getAssetTypesID(assetTypes, pageSize=pageSize, verbose=verbose)

            # Asset children filter
            x_filter['where'].append({"field": "CT_ID", "method": "in", "items": assetTypeIDs})

        # Apply level filter
        if searchType == 'MAX LEVEL' and maxLevel != -1:
            x_filter['where'].append({"field": "Level", "method": "le", "value": maxLevel})
        elif searchType == 'AT LEVEL' and atLevel != -1:
            x_filter['where'].append({"field": "Level", "value": atLevel})

        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('View_Node', xFilter=x_filter, pageSize=pageSize, verbose=verbose)

        return result, result_code

    ######################################################################################
    def getAssetTypesID(self, assetTypes, pageSize=None, verbose=False):
        assetTypeIDs = []
        for assetType in assetTypes:
            at_x_filter = {"where": [{"field": "Name", "value": assetType}]}
            at_x_filter = json.dumps(at_x_filter)
            result, result_code = self.getTable('Comp_Type', xFilter=at_x_filter,
                                                pageSize=pageSize, verbose=verbose)

            if len(result['rows']) != 0:
                assetTypeIDs.append(result['rows'][0]['CT_ID'])
            else:
                assetTypeIDs.append('Asset type does not exist in the database')

        return assetTypeIDs

    ######################################################################################
    def getTableDBNames(self, tableNames, tableType, pageSize=None, verbose=False):
        tableDBNames = []

        for tableIndex, tableName in enumerate(tableNames):
            x_filter = {"operator": "and",
                        "where": [{"field": "Name", "value": tableName},
                                  {"field": "Def_Type.Name", "value": tableType}]
                        }
            x_filter = json.dumps(x_filter)

            result, result_code = self.getTable('Table_Def', xFilter=x_filter,
                                                pageSize=pageSize, verbose=verbose)

            for row in result['rows']:
                tableDBNames.append(row['Table_Name'])

        return tableDBNames

    ######################################################################################
    def getAssetByFullLocation(self, fullLocation, assetView=None, pageSize=None, verbose=False):
        """
            Get Asset details from View_Node table using full location.

            :param fullLocation: (``string``) - Full location is specified the same way it is defined in a typical NEXUS import sheet (single column)
            :param assetView: (``string`` - optional) - Asset view name (default value None)
            :param pageSize: (``int`` - optional) - Page size for response (default value None). When default is used the default NEXUS IC page size will be used (100).
            :param verbose: (``bool`` - optional) - Print internal messages if True (default value False).

            :return: (``tuple`` - dict or string, string) - response (json, raw or error string) and response status code.
        """

        x_filter = {"operator": "and",
                    "where": [{'field': 'View_Node.Full_Location', 'value': fullLocation}]
                    }

        # Apply asset view filter
        if assetView != None:
            x_filter['where'].append({"field": "Comp_View.Name", "value": assetView})

        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('View_Node', xFilter=x_filter,
                                            pageSize=pageSize, verbose=verbose)

        return result, result_code

    ######################################################################################
    def getTableDefInfo(self, tableName, tableType, pageSize=None, verbose=False):
        x_filter = {"operator": "and",
                    "where": [{"field": "Name", "value": tableName},
                              {"field": "Def_Type.Name", "value": tableType}]
                    }
        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('Table_Def', xFilter=x_filter,
                                            pageSize=pageSize, verbose=verbose)

        return result, result_code

    ######################################################################################
    def createNewEvents(self, events, pageSize=None, verbose=False):
        """
            Imports new events in the NEXUS IC database. This function creates new event and doesn't update existing events

            :param events: (``list``) - Events to be imported. Must follow the following format:

                .. code-block:: python

                        events = [{'asset_full_location': 'xxxx / xxxx',
                                    'event_type': 'xxxx',
                                    'workpack_name': 'xxxx',
                                    'survey_set': 'xxxx',
                                    'start_clock': 'YYYY-MM-DDThh:mm:ss.ssssZ',
                                    'end_clock': 'YYYY-MM-DDThh:mm:ss.ssssZ',
                                    'comment': 'xxxxx',
                                    'fields': {'<Field Name 1>': xxx,
                                                '<Field Name 2>': xxx,
                                                '<Field Name 3>': xxx
                                                }
                                    }
                                ]

                where:

                - asset_full_location: Follows the same format as the standard NEXUS import sheet (single column)
                - survey_set: Optional (default value is Raw Survey Data)
                - start_clock and end_clock: YYYY for years, MM for months, DD for days, hh for hours, mm for minutes, ss for seconds and .ssss for milliseconds
                - fields: NEXUS field names are the keys (as shown in NEXUS IC)

            :param pageSize: (``int`` - optional) - Page size for response (default value None). When default is used the default NEXUS IC page size will be used (100).
            :param verbose: (``bool`` - optional) - Print internal messages if True (default value False).

            :return: (``tuple`` - list, list) - List of imported events and missed events.
        """

        if self.verbose or verbose:
            print('Importing new events...')

        imported_events = []
        missed_events = []
        for event in events:
            # Get Asset by Full Location
            # --------------------------
            if 'asset_full_location' in event.keys():
                result, result_code = self.getAssetByFullLocation(event['asset_full_location'], pageSize=pageSize,
                                                                  verbose=verbose)
                if len(result['rows']) == 0:
                    missed_events.append({'Event': event,
                                          'Reason': 'Asset was not found in database'})
                    continue
                else:
                    component_id = result['rows'][0]['Component_ID']
            else:
                missed_events.append({'Event': event,
                                      'Reason': 'asset_full_location key was not found in input dictionary'})
                continue

            # Get Workpack ID
            # ---------------
            if 'workpack_name' in event.keys():
                x_filter = {"operator": "and",
                            "where": [{'field': 'Workpack.Name', 'value': event['workpack_name']}]
                            }
                x_filter = json.dumps(x_filter)
                result, result_code = self.getTable('Workpack', xFilter=x_filter, pageSize=pageSize, verbose=verbose)
                if len(result['rows']) == 0:
                    missed_events.append({'Event': event,
                                          'Reason': 'Workpack was not found in database'})
                    continue
                else:
                    workpack_id = result['rows'][0]['Workpack_ID']
            else:
                missed_events.append({'Event': event,
                                      'Reason': 'workpack_name key was not found in input dictionary'})
                continue

            # Get table def information
            # -------------------------
            if 'event_type' in event.keys():
                result, result_code = self.getTableDefInfo(event['event_type'], 'Event', pageSize=pageSize,
                                                           verbose=verbose)
                if len(result['rows']) == 0:
                    missed_events.append({'Event': event,
                                          'Reason': 'Event type was not found in database'})
                    continue
                else:
                    td_id = result['rows'][0]['TD_ID']
                    tableDBName = result['rows'][0]['Table_Name']
            else:
                missed_events.append({'Event': event,
                                      'Reason': 'event_type key was not found in input dictionary'})
                continue

            # Get Survey Set ID
            # -----------------
            if 'survey_set' in event.keys():
                survey_set = event['survey_set']
            else:
                survey_set = 'Raw Survey Data'

            x_filter = {"operator": "and",
                        "where": [{'field': 'Survey_Set.Name', 'value': survey_set}]
                        }
            x_filter = json.dumps(x_filter)
            result, result_code = self.getTable('Survey_Set', xFilter=x_filter, pageSize=pageSize, verbose=verbose)
            ss_id = result['rows'][0]['SS_ID']

            # Check if start_clock and end_clock is in input dictionary
            # ---------------------------------------------------------
            if not ('start_clock' in event.keys()):
                missed_events.append({'Event': event,
                                      'Reason': 'start_clock key was not found in input dictionary'})
                continue

            if not ('end_clock' in event.keys()):
                missed_events.append({'Event': event,
                                      'Reason': 'end_clock key was not found in input dictionary'})
                continue

            # Check event fields type
            # -----------------------
            event_body = {}
            for eventFieldName in event['fields'].keys():
                x_filter = {'operator': 'and',
                            'where': [{'field': 'Field_Def.Name', 'value': eventFieldName}]
                            }
                x_filter = json.dumps(x_filter)
                result, result_code = self.getTable('Field_Def', xFilter=x_filter, pageSize=pageSize,
                                                    verbose=verbose)

                if len(result['rows']) == 0:
                    if 'comment' in event.keys():
                        event['comment'] += '\nCheck this field: ' + eventFieldName + ': ' + str(
                            event['fields'][eventFieldName]) + ' '
                    else:
                        event['comment'] = eventFieldName + ': ' + str(event['fields'][eventFieldName]) + ' '
                else:
                    dbFieldName = result['rows'][0]['Field_Name']

                    # Check if field is lookup list type
                    if 'LL_ID' in result['rows'][0].keys():
                        x_filter = {'operator': 'and',
                                    'where': [{'field': 'Lookup_Item.LL_ID', 'value': result['rows'][0]['LL_ID']},
                                              {'field': 'Lookup_Item.Comments',
                                               'value': event['fields'][eventFieldName]}]
                                    }
                        x_filter = json.dumps(x_filter)
                        result, result_code = self.getTable('Lookup_Item', xFilter=x_filter, pageSize=pageSize,
                                                            verbose=verbose)

                        if len(result['rows']) == 0:
                            if 'comment' in event.keys():
                                event['comment'] += '\nCheck this field: ' + eventFieldName + ': ' + str(
                                    event['fields'][eventFieldName]) + ' '
                            else:
                                event['comment'] = eventFieldName + ': ' + str(event['fields'][eventFieldName]) + ' '
                        else:
                            event_body[dbFieldName] = result['rows'][0]['LI_ID']
                    else:
                        event_body[dbFieldName] = event['fields'][eventFieldName]

            # Create new header record
            # ------------------------
            header_body = {'TD_ID': td_id,
                           'Start_Clock': event['start_clock'],
                           'End_Clock': event['end_clock'],
                           'Workpack_ID': workpack_id,
                           'Component_ID': component_id,
                           'SS_ID': ss_id}

            result, result_code = self.createNewRecord('Header', header_body, verbose=verbose)
            event_body['Header_ID'] = result['rows'][0]['Header_ID']

            # Create new event record
            # -----------------------
            result, result_code = self.createNewRecord(tableDBName, event_body, verbose=verbose)

            # Create new commtenary record
            # ----------------------------
            if 'comment' in event.keys():
                commentary_body = {'Header_ID': event_body['Header_ID'],
                                   'Notes': event['comment']}
                result, result_code = self.createNewRecord('Commentary', commentary_body, verbose=verbose)

            imported_events.append(event)

        if self.verbose or verbose:
            print('Imported ' + str(len(imported_events)) + ' new events...')
            print('Missed ' + str(len(missed_events)) + ' events from input...')

        return imported_events, missed_events

    ######################################################################################
    def getLookupListItem(self, LI_ID, verbose=False):
        """
            Gets lookup item ifnormation given a lookup item ID

            :param LI_ID: (``int``) - Lookup item ID in the database
            :param verbose: (``bool`` - optional) - Print internal messages if True (default value False).

            :return: (``tuple`` - dict or string, string) - response (json, raw or error string) and response status code.
        """

        x_filter = {'operator': 'and',
                    'where': [{'field': 'Lookup_Item.LI_ID', 'value': LI_ID}]
                    }
        x_filter = json.dumps(x_filter)
        result, result_code = self.getTable('Lookup_Item', xFilter=x_filter, verbose=verbose)
        return result, result_code

######################################################################################
################################### Start Script #####################################
if __name__ == '__main__':
    baseURI = ''
    apiKey = ''

    startTime = datetime.datetime.now()

    ## Program start here
    print(NEXUSIC_REST.__doc__)
    ## End of program

    endTime = datetime.datetime.now()
    elapsedTime = endTime - startTime

    print('NEXUS IC REST API actions completed.....runtime: %s' % (str(elapsedTime)))


