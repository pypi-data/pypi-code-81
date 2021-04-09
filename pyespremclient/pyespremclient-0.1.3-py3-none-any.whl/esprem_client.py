
import os
import re
import io
from pathlib import Path

import requests


def test3( ) :
    return( 3 )
    
def esprem_rpc(host: str, port: str, endpoint: str,
               params_dict, rq_id: int = 0):
    """Makes an RPC request to an ESPREM server.

    Parameters
    ----------
    host
        ESPREM server IP/URI string.
    port
        ESPREM server port string.
    endpoint
        ESPREM RPC endpoint.
    params_dict
        Dictionary of the job parameters to send.

    Returns
    -------
    Dict
        Dictionary of the JSON response.
    """
    url = "http://" + host + ":" + port + "/jsonrpc"
    headers = {'content-type': 'application/json'}
    payload = {"method": endpoint,
               "params": params_dict,
               "jsonrpc": "2.0",
               "id": rq_id, }
    response = requests.post(
        url, json=payload, headers=headers).json()
    # url, data=json.dumps(payload), headers=headers).json()
    if "result" in response:
        return response["result"]
    return response["error"]


def trepem_deserial(targetpath, trepem_resp):
    """Deserializes the trepem server response dictionary into
    output files in the filesystem.

    Parameters
    ----------
    targetpath
        String target path in which to write the outputs hierarchy.
    trepem_resp The trepem response dictionary.

    Returns
    -------
        None
    """
    targetpath = targetpath + "/"
    if not os.path.exists(targetpath):
        os.makedirs(targetpath)
        os.makedirs(targetpath + "/trepem")
        os.makedirs(targetpath + "/mulassis")
        os.makedirs(targetpath + "/trajectory")
        os.makedirs(targetpath + "/mcict")
    else:
        print("Output diretory already exists aborting.")
        return
    for filename, string in trepem_resp.items():
        with open(targetpath + filename, "w+") as targetfile:
            targetfile.write(string)
    return


def esprem_deserial(targetpath, dictin):
    """Deserializes the esprem server response dictionary into output files in
    the filesystem.

    Parameters
    ----------
    targetpath
        Target path in which to write the outputs hierarchy.
    trepem_resp
        The trepem response dictionary.

    Returns
    -------
        None
    """
    Path(targetpath).mkdir(parents=True, exist_ok=True)

    for filename, string in dictin.items():
        filename = targetpath / Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w") as myfd:
            myfd.write(str(string))
    return


def get_mulassis_block(ml_output: str, block_name_str: str) -> str:
    """From the Mulassis output file, get the analysis block output.
    first match only until End of block.

    Parameters
    ----------
    ml_output
        The mulassis result file as a string.
    block_name_str
        The output block name, any of: {"DOSE ANALYSIS",
        "NID ANALYSIS", "PULSE-HEIGHT ANALYSIS"}

    Returns
    -------
        The block string.
    """
    with io.StringIO(ml_output) as ml_f:
        return re.findall(block_name_str + '(.*?)End of', ml_f.read(), re.S)[0]


if __name__ == '__main__':
    print( "Hello from main!" )

