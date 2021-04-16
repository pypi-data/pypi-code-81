# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import argparse

import websocket

import time

import json

###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#


###############################################################
#
#   GLOBAL VARIABLES
#

MockServerHost = "127.0.0.1"
MockServerPort = 9001

token = "abcd1234"
ws = None

###############################################################
#
#   PROGRAM SPECIFIC VARIABLES
#

ProgramNumArgs = 0
ProgramDescription = ''
ProgramVersionStr = 'v0.0'
ProgramUsage = ''


###############################################################
#
#   CLASSES
#

###############################################################
#
#   FUNCTIONS
#

def ws_message(obj, message):
    print('_ws_message(message = {})'.format(message))

    global ws
    message = json.loads(message)
    print('message = {}'.format(message))

    if isinstance(message, dict):
        message_type = message.get('type', None)
        print('message_type = {}'.format(message_type))
        if message_type == 'TokenValid':
            # subscription_message = {
            #                             "command": "Subscribe",
            #                             "id": "42",
            #                             "payload": {
            #                                 "fields": [
            #                                 "InstrumentDescription",
            #                                 "ValuationDate",
            #                                 "StartDate",
            #                                 "EndDate",
            #                                 "Calendar",
            #                                 "FixedRate",
            #                                 "PV01AmountInDealCcy",
            #                                 "Duration",
            #                                 "ModifiedDuration",
            #                                 "ForwardCurveName",
            #                                 "DiscountCurveName",
            #                                 "ErrorMessage"
            #                                 ],
            #                                 "outputs": [
            #                                 "Data"
            #                                 ],
            #                                 "universe": [
            #                                 {
            #                                     "instrumentType": "Swap",
            #                                     "instrumentDefinition": {
            #                                     "startDate": "2017-06-28T00:00:00Z",
            #                                     "tenor": "3Y",
            #                                     "instrumentCode": "EURAB6E3Y=",
            #                                     "swapType": "Vanilla"
            #                                     }
            #                                 }
            #                                 ]
            #                             }
            #                         }

            # subscription_message = {"command": "Subscribe",
            #                          "id": "42",
            #                             "payload" : {
            #                                 "universe": [
            #                                             {"instrumentType": "Option",
            #                                                 "instrumentDefinition": {"instrumentCode": "BNPP520cX2.EX"}}
            #                                         ],
            #                                 "fields": ["Ric","Premium","ImpliedVol","DeltaPercent","GammaPercent","ErrorCode",
            # "ErrorMessage"],
            #                                 "outputs": ["Data",
            #                                             #"headers"
            #                                         ]
            #                             }
            #                         }

            # subscription_message = { "command": "Subscribe",
            #                          "id": "42",
            #                             "payload" : {"marketData":
            #                                 {
            #                                     "rics": [
            #                                         {"marketDataId": "230c9f66-d5bb-4424-a2b1-72bc8e3c7935",
            #                                             "ric": "BNPP.PA",
            #                                             "marketDataDate": "2019-04-15T00:00:00+00:00",
            #                                             "triggerPricing": True,
            #                                             "isRealtime": True,},
            #                                         {"marketDataId": "c6cff880-9d07-44d4-832e-10f88f26c77c",
            #                                             "ric": "BNPP520cX2.EX",
            #                                             "marketDataDate": "2019-04-15T00:00:00+00:00",
            #                                             "cutoff": "LSE_1500",
            #                                             "triggerPricing": True,
            #                                             "isRealtime": True,}
            #                                         ]
            #                                 }
            #                         }
            #                   }

            subscription_message = {"command": "Subscribe",
                                    "id": "42",
                                    "payload": {"fields": [
                                        "InstrumentCode",
                                        "BondType",
                                        "IssueDate",
                                        "EndDate",
                                        "CouponRatePercent",
                                        "Accrued",
                                        "CleanPrice",
                                        "DirtyPrice",
                                        "YieldPercent",
                                        "RedemptionDate",
                                        "ModifiedDuration",
                                        "Duration",
                                        "DV01Bp",
                                        "AverageLife",
                                        "Convexity"
                                        ],
                                        "outputs": [
                                            # "Headers",
                                            "Data"
                                            ],
                                        "universe": [
                                            {
                                                "instrumentType": "Bond",
                                                "instrumentDefinition": {
                                                    "instrumentTag": "TreasuryBond_10Y",
                                                    "instrumentCode": "US10YT=RR"
                                                    }
                                                }
                                            ]
                                        }
                                    }

            print('subscription_message = {}'.format(subscription_message))
            ws.send(json.dumps(subscription_message))
            print('subscription message was sent')
        return

    #   OMM
    message = message[0]
    message_type = message.get('Type', None)
    message_domain = message.get('Domain', None)
    if message_type == 'Refresh' and message_domain == 'Login':
        print('OMM protocol.........')
        subscription_message = {'ID': 111,
                                'Domain': 'MarketPrice',
                                'Key': {
                                    'Name': '0#.ALL/P1D'
                                    },
                                'Streaming': True
                                }

        print('subscription_message = {}'.format(subscription_message))
        ws.send(json.dumps(subscription_message))
        print('subscription message was sent')

        #   done
        return

    #   generic RDP
    message_type = message.get('type', None)
    if message_type == 'Ack':
        #   generic RDP protocol
        #   extract content
        state_dict = message.get('state', None)
        assert state_dict is not None

        #   check it resposne message is ok
        state_code = state_dict.get('code', None)
        if state_code == 200:
            #   login successful, then sent the subscription message

            subscription_message = {"method": "Subscribe",
                                    "streamID": "42",
                                    "service": "analytics/bond/contract",
                                    "universe": [
                                        {
                                            "instrumentType": "Bond",
                                            "instrumentDefinition": {
                                                "instrumentTag": "TreasuryBond_10Y",
                                                "instrumentCode": "US10YT=RR"
                                                }
                                            }
                                        ],
                                    "views": [
                                        "InstrumentCode",
                                        "BondType",
                                        "IssueDate",
                                        "EndDate",
                                        "CouponRatePercent",
                                        "Accrued",
                                        "CleanPrice",
                                        "DirtyPrice",
                                        "YieldPercent",
                                        "RedemptionDate",
                                        "ModifiedDuration",
                                        "Duration",
                                        "DV01Bp",
                                        "AverageLife",
                                        "Convexity"
                                        ]
                                    }

            print('subscription_message = {}'.format(subscription_message))
            ws.send(json.dumps(subscription_message))
            print('subscription message was sent')

        #   done
        return


def ws_error(obj, error):
    print('_ws_error(error = {})'.format(error))


def ws_open(message):
    print('_ws_open(message = {})'.format(message))

    global token
    login_message = {
        "streamID": "42",
        "method": "Auth",
        "token": token,
        }

    time.sleep(1)
    print('login_message = {}'.format(login_message))
    dump = json.dumps(login_message)
    print('dump = {}'.format(dump))
    global ws
    ws.send(dump)
    print('login message was sent')


def ws_close(obj, message):
    print('_ws_close(message = {})'.format(message))


def ws_ping(message):
    print('_ws_ping(message = {})'.format(message))


def ws_pong(message):
    print('_ws_pong(message = {})'.format(message))


def run_websocket():
    global ws
    ws = websocket.WebSocketApp(f'ws://{MockServerHost}:{MockServerPort}',
                                header=["User-Agent: Python"],
                                on_message=ws_message,
                                on_error=ws_error,
                                on_open=ws_open,
                                on_close=ws_close,
                                on_ping=ws_ping,
                                on_pong=ws_pong,
                                )

    try:
        print('run client websocket forever')
        ws.run_forever()
    except Exception as e:
        print('Error!!! e={}'.format(e))

    print('DONE :: run_websocket()')


def main():
    # #   parsing arguments
    # parser = argparse.ArgumentParser( description = '{}'.format( ProgramDescription ),
    #                                         usage = '{}'.format( ProgramUsage ) )
    # args = parser.parse_args()

    ###############################################################
    #   begin coding

    #   run websocket client
    run_websocket()


if __name__ == '__main__':
    #   call main function
    main()
