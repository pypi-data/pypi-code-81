
from datetime import datetime
import json
import os

from ..details import AccountDetails, LineDetails

DIRPATH = os.path.dirname(__file__)


def test_account_details():

    with open(DIRPATH + '/data/get-other-lines.json', 'r') as fil:
        jsonDict = json.loads(fil.read())

    deets = AccountDetails.from_dict(**jsonDict)
    assert len(deets.confirmed_lines) == 1
    assert deets.return_code == 1
    assert deets.return_text == 'sucess'


def test_account_line_details():
    with open(DIRPATH + '/data/get-other-lines.json', 'r') as fil:
        jsonDict = json.loads(fil.read())

    deets = AccountDetails.from_dict(**jsonDict)
    assert deets.confirmed_lines[0].hash == 'FFFFFFFF'


def test_line_details():
    with open(DIRPATH + '/data/get-details.json', 'r') as fil:
        jsonDict = json.loads(fil.read())

    deets = LineDetails.from_dict(**jsonDict)
    assert deets.phone_number == 'AAAAAAAAAA'
    assert deets.voice_balance == -1
    assert deets.messaging_balance == -1
    assert deets.data_balance == 2874
    assert deets.time != 0
    assert deets.start_date == datetime(year=2021, month=4, day=2).date()
    assert deets.end_date == datetime(year=2021, month=5, day=4).date()
