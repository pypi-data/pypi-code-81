# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import pytest

from unittest.mock import MagicMock

import asyncio

###############################################################
#
#   REFINITIV IMPORTS
#

import refinitiv.dataplatform as rdp


###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   TEST CASES
#

def test_default_api():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)

    assert omm_stream.api == 'pricing'


def test_with_api():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session, api='foo')

    assert omm_stream.api == 'foo'


def test_get_open_stream_message_all_parameters():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._stream_id = 1
    omm_stream._domain = 'foo'
    omm_stream._name = 'bar'
    omm_stream._with_updates = False

    omm_stream._service = 'elektron'
    omm_stream._fields = ['open', 'close']

    #   open message
    open_message = omm_stream._get_open_stream_message()

    assert open_message['ID'] == omm_stream._stream_id
    assert open_message['Domain'] == omm_stream._domain
    assert open_message['Key']['Name'] == omm_stream._name
    assert open_message['Streaming'] == omm_stream._with_updates

    assert open_message['Key']['Service'] == omm_stream._service
    assert open_message['View'] == omm_stream._fields


def test_get_open_stream_message():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._stream_id = 1
    omm_stream._domain = 'foo'
    omm_stream._name = 'bar'
    omm_stream._with_updates = False

    #   open message
    open_message = omm_stream._get_open_stream_message()

    assert open_message['ID'] == omm_stream._stream_id
    assert open_message['Domain'] == omm_stream._domain
    assert open_message['Key']['Name'] == omm_stream._name
    assert open_message['Streaming'] == omm_stream._with_updates

    assert 'Service' not in open_message['Key']
    assert 'View' not in open_message


def test_get_close_stream_message():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._stream_id = 1

    #   close message
    close_message = omm_stream._get_close_stream_message()

    assert close_message['ID'] == omm_stream._stream_id


###############################################################
#   callback functions when received messages

def test_on_refresh():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._subscribe_response_future = asyncio.get_event_loop().create_future()

    omm_stream._on_refresh({'ID': 2, 'Type': 'Refresh', 'Key': {'Service': 'ELEKTRON_EDGE', 'Name': 'EUR='},
                            'State': {'Stream': 'Open', 'Data': 'Ok', 'Text': 'All is well'},
                            'Qos': {'Timeliness': 'Realtime', 'Rate': 'TickByTick'}, 'PermData': 'AwEsUmw=', 'SeqNumber': 35342,
                            'Fields': {'PROD_PERM': 526, 'RDNDISPLAY': 153, 'DSPLY_NAME': 'EQUA BANK    PRG', 'TIMACT': '08:28:00',
                                       'NETCHNG_1': -0.0034, 'HIGH_1': 1.1332, 'LOW_1': 1.1277, 'CURRENCY': 'USD',
                                       'ACTIV_DATE': '2020-07-07', 'OPEN_PRC': 1.1306, 'HST_CLOSE': 1.1308, 'BID': 1.1274,
                                       'BID_1': 1.1278, 'BID_2': 1.1276, 'ASK': 1.1277, 'ASK_1': 1.128, 'ASK_2': 1.1278,
                                       'ACVOL_1': 46700, 'TRD_UNITS': '4DP ', 'PCTCHNG': -0.3, 'OPEN_BID': 1.1306, 'OPEN_ASK': 1.131,
                                       'CLOSE_BID': 1.1308, 'CLOSE_ASK': 1.131, 'NUM_MOVES': 92463, 'OFFCL_CODE': 'EQBK        ',
                                       'HSTCLSDATE': '2020-07-06', 'YRHIGH': 1.1492, 'YRLOW': 1.0638, 'BCKGRNDPAG': 'EQBK',
                                       'BID_NET_CH': -0.0034, 'BID_TICK_1': '⇩', 'MID_PRICE': 1.1276, 'MID_NET_CH': -0.0033,
                                       'MID_CLOSE': 1.1309, 'HIGHTP_1': 'B', 'LOWTP_1': 'A', 'BID_HIGH_1': 1.1332, 'BID_LOW_1': 1.1274,
                                       'YRBIDHIGH': 1.1492, 'YRBIDLOW': 1.0635, 'HST_CLSBID': 1.1308, 'HSTCLBDDAT': '2020-07-06',
                                       'NUM_BIDS': 46700, 'RECORDTYPE': 209, 'ACT_TP_1': 'B⇩', 'ACT_TP_2': 'B⇧', 'ACT_TP_3': 'B⇧',
                                       'SEC_ACT_1': 1.1277, 'SEC_ACT_2': 1.128, 'SEC_ACT_3': 1.1278, 'SC_ACT_TP1': ' A',
                                       'SC_ACT_TP2': ' A', 'SC_ACT_TP3': ' A', 'OPEN_TIME': '21:00:00', 'HIGH_TIME': '00:42:00',
                                       'LOW_TIME': '08:28:00', 'YRHIGHDAT': '2020-03-09', 'YRLOWDAT': '2020-03-20', 'IRGPRC': -0.3,
                                       'TIMCOR': '08:28:43', 'PRIMACT_1': 1.1274, 'PRIMACT_2': 1.1278, 'PRIMACT_3': 1.1276,
                                       'BASE_CCY': 'EUR', 'BCAST_REF': None, 'CROSS_SC': '1E+00', 'DLG_CODE1': 'EQBK  ',
                                       'DLG_CODE2': 'CKLU  ', 'DLG_CODE3': 'RBSL  ', 'CTBTR_1': 'EQUA BANK   ',
                                       'CTBTR_2': 'CARL KLIEM  ', 'CTBTR_3': 'RBS         ', 'CTB_LOC1': 'PRG', 'CTB_LOC2': 'LUX',
                                       'CTB_LOC3': 'LON', 'CTB_PAGE1': 'EQBK', 'CTB_PAGE2': 'CKLU', 'CTB_PAGE3': 'RBSL',
                                       'VALUE_DT1': '2020-07-07', 'VALUE_DT2': '2020-07-07', 'VALUE_DT3': '2020-07-07',
                                       'SEC_HIGH': 1.1335, 'SEC_HI_TP': 'A', 'SEC_LOW': 1.1277, 'SEC_LO_TP': 'B', 'OPEN_TYPE': 'B ',
                                       'CLOSE_TYPE': 'B ', 'BKGD_REF': 'Euro', 'GEN_TEXT16': '<EUR/BKGDINFO>', 'GEN_VAL3': 1.131,
                                       'GEN_VAL4': 1.1284, 'GV1_TEXT': 'SPOT', 'GV2_TEXT': 'EURUSD', 'GV4_TEXT': 'SPOT',
                                       'VALUE_TS1': '08:28:45', 'VALUE_TS2': '08:28:45', 'VALUE_TS3': '08:28:45', 'QUOTIM': '08:28:45',
                                       'GEN_VAL5': 1.124, 'GEN_VAL6': 1.1345, 'GEN_VAL7': 1.1238, 'GEN_VAL8': 1.1348,
                                       'GEN_VAL9': 1.1242, 'GEN_VAL10': 1.1244, 'GV5_TEXT': 'OP_BID', 'GV6_TEXT': 'BID_HI',
                                       'GV7_TEXT': 'BID_LO', 'GV8_TEXT': 'ASK_HI', 'GV9_TEXT': 'ASK_LO', 'GV10_TEXT': 'OP_ASK',
                                       'GN_TXT16_2': '<EURVOL>', 'GV1_TIME': '08:00:00', 'PREF_DISP': 6205, 'GN_TXT24_1': '<0#EURF=>',
                                       'DSO_ID': 16416, 'RDN_EXCHD2': 'NY$', 'PREV_DISP': 60, 'ASIA_CL_DT': '2020-07-07',
                                       'ASIA_CLOSE': 1.1284, 'ASIA_HI_TM': '00:42:00', 'ASIA_HIGH': 1.1332, 'ASIA_LOW': 1.1282,
                                       'ASIA_LW_TM': '07:28:00', 'ASIA_NETCH': -0.0012, 'ASIA_OP_TM': '21:00:00', 'ASIA_OPEN': 1.1306,
                                       'EURO_CL_DT': '2020-07-06', 'EURO_CLOSE': 1.1306, 'EURO_HI_TM': '05:16:00', 'EURO_HIGH': 1.1316,
                                       'EURO_LOW': 1.1277, 'EURO_LW_TM': '08:28:00', 'EURO_NETCH': -0.0032, 'EURO_OP_TM': '05:00:00',
                                       'EURO_OPEN': 1.131, 'US_CL_DT': '2020-07-06', 'US_CLOSE': 1.1308, 'US_HI_TM': '13:51:00',
                                       'US_HIGH': 1.1345, 'US_LOW': 1.1294, 'US_LW_TM': '11:08:00', 'US_NETCH': 0.006,
                                       'US_OP_TM': '11:00:00', 'US_OPEN': 1.1295, 'ASK_SPREAD': 1.1279, 'BID_SPREAD': 1.1274,
                                       'MID_SPREAD': 1.1292, 'MONTH_HIGH': 1.1345, 'MONTH_LOW': 1.1186, 'PCTCHG_3M': 3.54,
                                       'PCTCHG_6M': 1.1, 'PCTCHG_MTD': 0.38, 'PCTCHG_YTD': 0.57, 'QUOTE_DATE': '2020-07-07',
                                       'WEEK_HIGH': 1.1345, 'WEEK_LOW': 1.1241, 'ASK_HIGH_1': 1.1335, 'ASK_HI_TME': '00:42:00',
                                       'ASK_LOW_1': 1.1277, 'ASK_LO_TME': '08:28:00', 'BID_ASK_DT': '2020-07-06', 'HIGH_2': 1.1331,
                                       'HIGH_3': 1.133, 'HIGH_4': 1.1329, 'HIGH_5': 1.1328, 'HIGH_TIME2': '00:42:00',
                                       'HIGH_TIME3': '00:40:00', 'HIGH_TIME4': '00:40:00', 'HIGH_TIME5': '00:27:00', 'LOW_2': 1.1278,
                                       'LOW_3': 1.1279, 'LOW_4': 1.128, 'LOW_5': 1.1281, 'LOW_TIME2': '08:28:00',
                                       'LOW_TIME3': '08:28:00', 'LOW_TIME4': '08:28:00', 'LOW_TIME5': '08:28:00', 'SCALING': '1',
                                       'START_DT': '2020-07-09', 'WKHI_DT': '2020-07-06', 'WKLO_DT': '2020-07-05',
                                       'MTHHI_DT': '2020-07-06', 'MTHLO_DT': '2020-07-01', 'QUOTIM_MS': 30525932, 'MID_HIGH': 1.1333,
                                       'MID_LOW': 1.1276, 'MID_HTIM': '00:42:45', 'MID_LTIM': '08:28:43', 'MID_OPEN': 1.1308,
                                       'CONTEXT_ID': 3312, 'BID_HIGH_2': 1.1331, 'BID_HIGH_3': 1.133, 'BID_HIGH_4': 1.1329,
                                       'BID_HIGH_5': 1.1328, 'BID_LOW_2': 1.1275, 'BID_LOW_3': 1.1276, 'BID_LOW_4': 1.1277,
                                       'BID_LOW_5': 1.1278, 'ASK_HIGH_2': 1.1334, 'ASK_HIGH_3': 1.1333, 'ASK_HIGH_4': 1.1332,
                                       'ASK_HIGH_5': 1.1331, 'ASK_LOW_2': 1.1278, 'ASK_LOW_3': 1.1279, 'ASK_LOW_4': 1.128,
                                       'ASK_LOW_5': 1.1281, 'PRV_BID_H': 1.1345, 'PRV_ASK_H': 1.1348, 'PRV_BID_L': 1.1238,
                                       'PRV_ASK_L': 1.1242, 'DDS_DSO_ID': 12348, 'BR_LINK1': None, 'BR_LINK2': None, 'BR_LINK3': None,
                                       'SPS_SP_RIC': '.[SPSEVAI-VAH10-P4', 'QUOTIM_2': '08:28:45', 'QUOTIM_3': '08:28:45',
                                       'QUOTE_DT2': '2020-07-07', 'QUOTE_DT3': '2020-07-07', 'ASKYRHIDAT': '2020-03-09',
                                       'ASKYRLODAT': '2020-03-20', 'BIDYRHIDAT': '2020-03-09', 'BIDYRLODAT': '2020-03-22',
                                       'ASIABAC_DT': '2020-07-07', 'EUBAC_DT': '2020-07-06', 'USBAC_DT': '2020-07-06',
                                       'HST_NUMBID': 92463, 'ASK_FWDOR': None, 'BID_FWDOR': None, 'AMERCL_ASK': 1.131,
                                       'AMERCL_BID': 1.1308, 'AMERHI_ASK': 1.1348, 'AMERHI_BID': 1.1345, 'AMERLO_ASK': 1.1294,
                                       'AMERLO_BID': 1.1292, 'AMEROP_ASK': 1.1296, 'AMEROP_BID': 1.1295, 'ASIACL_ASK': 1.1288,
                                       'ASIACL_BID': 1.1284, 'ASIAHI_ASK': 1.1335, 'ASIAHI_BID': 1.1332, 'ASIALO_ASK': 1.1282,
                                       'ASIALO_BID': 1.1279, 'ASIAOP_ASK': 1.131, 'ASIAOP_BID': 1.1306, 'BIDPCTCHNG': -0.3,
                                       'EURCL_ASK': 1.1309, 'EURCL_BID': 1.1306, 'EURHI_ASK': 1.1318, 'EURHI_BID': 1.1316,
                                       'EURLO_ASK': 1.1277, 'EURLO_BID': 1.1274, 'EUROP_ASK': 1.1313, 'EUROP_BID': 1.131,
                                       'HST_HIMID': 1.1346, 'HST_LOMID': 1.124, 'HST_OPNASK': 1.1244, 'HST_OPNBID': 1.124,
                                       'YRASKHIGH': 1.1496, 'YRASKLOW': 1.0638, 'ASIA_BNC': -0.0012, 'EURO_BNC': -0.0032,
                                       'MTH_ASK_LO': 1.1186, 'MTH_BID_HI': 1.1345, 'US_BNC': 0.006, 'WK_ASK_LO': 1.1241,
                                       'WK_BID_HI': 1.1345, 'BID_HOURLY': 1.1284, 'RCS_AS_CL2': '                        ',
                                       'MTH_ALO_DT': '2020-07-01', 'MTH_BHI_DT': '2020-07-06', 'WK_ALO_DT': '2020-07-05',
                                       'WK_BHI_DT': '2020-07-06', 'FXMM_TYPE': '        ', 'ASIA_AH_MS': '00:42:45.912',
                                       'ASIA_AL_MS': '07:28:05.993', 'ASIA_AO_MS': '21:00:03.641', 'ASIA_BH_MS': '00:42:48.169',
                                       'ASIA_BL_MS': '07:32:47.229', 'ASIA_BO_MS': '21:00:01.079', 'EURO_AH_MS': '05:10:49.801',
                                       'EURO_AL_MS': '08:28:44.977', 'EURO_AO_MS': '05:00:00.603', 'EURO_BH_MS': '05:16:20.944',
                                       'EURO_BL_MS': '08:28:43.45', 'EURO_BO_MS': '05:00:00.603', 'US_AH_MS': '13:51:04.727',
                                       'US_AL_MS': '11:08:01.864', 'US_AO_MS': '11:00:00.508', 'US_BH_MS': '13:51:05.455',
                                       'US_BL_MS': '11:07:11.558', 'US_BO_MS': '11:00:00.508', 'OPN_BID_MS': '21:00:01.08',
                                       'ASKHI1_MS': '00:42:45.912', 'ASKHI2_MS': '00:42:39.936', 'ASKHI3_MS': '00:40:54.944',
                                       'ASKHI4_MS': '00:40:19.748', 'ASKHI5_MS': '00:28:09.182', 'ASKLO1_MS': '08:28:44.977',
                                       'ASKLO2_MS': '08:28:39.838', 'ASKLO3_MS': '08:28:39.361', 'ASKLO4_MS': '08:28:29.687',
                                       'ASKLO5_MS': '08:28:24.575', 'BIDHI1_MS': '00:42:48.169', 'BIDHI2_MS': '00:42:32.769',
                                       'BIDHI3_MS': '00:40:53.389', 'BIDHI4_MS': '00:40:20.589', 'BIDHI5_MS': '00:27:16.704',
                                       'BIDLO1_MS': '08:28:43.45', 'BIDLO2_MS': '08:28:40.167', 'BIDLO3_MS': '08:28:38.143',
                                       'BIDLO4_MS': '08:28:29.128', 'BIDLO5_MS': '08:28:26.13', 'MIDHI1_MS': '00:42:45.912',
                                       'MIDLO1_MS': '08:28:43.45', 'BID_HR_MS': '08:00:00.416'}})

    assert omm_stream._subscribe_response_future.done()
    assert omm_stream._state == rdp.delivery.StreamState.Open


def test_on_update():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._state = rdp.delivery.StreamState.Open

    omm_stream._on_refresh({'ID': 2, 'Type': 'Update', 'UpdateType': 'Unspecified', 'DoNotConflate': True,
                            'Key': {'Service': 'ELEKTRON_EDGE', 'Name': 'EUR='}, 'SeqNumber': 35646,
                            'Fields': {'PCTCHG_3M': 3.54, 'PCTCHG_6M': 1.1, 'PCTCHG_MTD': 0.38, 'PCTCHG_YTD': 0.57}})

    assert omm_stream._state == rdp.delivery.StreamState.Open


def test_on_status_open():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._state = rdp.delivery.StreamState.Open

    omm_stream._on_status({'status': 'Open', 'code': 'Open', 'message': 'All is well'})

    assert omm_stream._state == rdp.delivery.StreamState.Open


def test_on_status_close():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._state = rdp.delivery.StreamState.Open

    omm_stream._on_status({'status': 'Closed', 'code': 'Closed', 'message': '...'})

    assert omm_stream._state == rdp.delivery.StreamState.Closed


def test_on_complete():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._state = rdp.delivery.StreamState.Open

    omm_stream._on_complete()


def test_on_error():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    omm_stream = rdp.OMMStream(session)
    omm_stream._subscribe_response_future = asyncio.get_event_loop().create_future()

    omm_stream._on_error({'foo': 'bar'})

    assert omm_stream._subscribe_response_future.done()
