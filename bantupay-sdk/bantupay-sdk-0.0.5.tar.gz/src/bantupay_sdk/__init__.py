from stellar_sdk import Keypair, TransactionEnvelope
from stellar_sdk.exceptions import Ed25519SecretSeedInvalidError
import json
import base64
import requests


def account():
    keypair = Keypair.random()
    return {"secret": keypair.secret, "publicKey": keypair.public_key}


def signHttp(uri, body, secretKey):
    try:
        if not uri:
            raise Exception("uri field is requreid")

        if not secretKey:
            raise Exception("secretKey field is required")

        string_body = body if body else ""

        if body:
            if type(body) is dict:
                string_body = json.dumps(body)

        key_pair = Keypair.from_secret(secretKey)
        data = bytes(uri + string_body, "utf-8")
        signed_data = key_pair.sign(data)
        signed_data = base64.b64encode(signed_data).decode("utf-8")
        return signed_data
    except Exception as e:
        print(" here....s")
        return e


def signTxn(secretKey, transactionXDR, networkPhrase):
    try:
        if not networkPhrase:
            raise Exception("networkPhrase field is required")

        if not transactionXDR:
            raise Exception("transactionXDR field is required")

        if not secretKey:
            raise Exception("secretKey field is required")

        key_pair = Keypair.from_secret(secretKey)
        txn = TransactionEnvelope.from_xdr(transactionXDR, networkPhrase)
        txn_signature = key_pair.sign(txn.hash())
        txn_signature = base64.b64encode(txn_signature).decode()

        return txn_signature

    except Exception as e:
        return e


def confirmPaymentDetail(
    username, destination, memo, amount, secretKey, assetIssuer="", assetCode=""
):
    """
    Confirm Payment Details

    ...

    Params
    ---------

    username : str
        this will be your username
    destination : str
        the user to receive the payment
    memo : str
        A litte note no mor than 24 chr
    amount : str
        amount to send, should be > 0
    secretKey : str
        this will be your secrete key (a valid 56 char str)
    assetIsuer : str
        assets public key
    assetcode : str
        asset code
    """
    try:
        payload = {
            "destination": destination,
            "memo": memo,
            "amount": amount,
            "assetIssuer": assetIssuer,
            "assetCode": assetCode,
        }
        keypair = Keypair.from_secret(secretKey)
        destinationKey = keypair.public_key
        uri = f"/v2/users/{username}/payments"
        signature = signHttp(uri, payload, secretKey)

        mainUrl = f"https://api.bantupay.org/v2/users/{username}/payments"
        headers = {
            "X-BANTUPAY-PUBLIC-KEY": destinationKey,
            "X-BANTUPAY-SIGNATURE": signature,
        }
        r = requests.post(mainUrl, json=payload, headers=headers)

        return {"data": r.json(), "statusCode": r.status_code}
    except Exception as e:
        raise Exception(e)


def makePayment(username, serverResponse, secretKey):
    """
    Make Payment

    ...

    Params
    ---------

    username : str
        this will be your username
    serverResponse : str
        this will be the response from confirmPaymentDetail function
    payload : json
        this will be the data you wish to send to the server
    secretKey : str
        this will be your secrete key (a valid 56 char str)
    """

    try:
        transaction = serverResponse["transaction"]
        networkPass_phrase = serverResponse["networkPassPhrase"]

        transaction_signature = signTxn(secretKey, transaction, networkPass_phrase)

        serverResponse["transactionSignature"] = transaction_signature
        keypair = Keypair.from_secret(secretKey)
        destinationKey = keypair.public_key
        uri = f"/v2/users/{username}/payments"
        mainUrl = f"https://api.bantupay.org/v2/users/{username}/payments"

        new_signature = signHttp(uri, serverResponse, secretKey)
        new_headers = {
            "X-BANTUPAY-PUBLIC-KEY": destinationKey,
            "X-BANTUPAY-SIGNATURE": new_signature,
        }

        r = requests.post(mainUrl, json=serverResponse, headers=new_headers)
        return r.json()
    except Exception as e:
        raise Exception(e)


def expressPay(
    username, destination, memo, amount, secretKey, assetIssuer="", assetCode=""
):
    """
    Express Pay - this call the confirmPayment and makePayment function

    ...

    Params
    ---------

    username : str
        this will be your username
    destination : str
        the user to receive the payment
    memo : str
        A litte note no mor than 24 chr
    amount : str
        amount to send, should be > 0
    secretKey : str
        this will be your secrete key (a valid 56 char str)
    assetIsuer : str
        assets public key
    assetcode : str
        asset code

    """
    try:
        firstCall = confirmPaymentDetail(
            username, destination, memo, amount, secretKey, assetIssuer, assetCode
        )

        if firstCall["statusCode"] == 202:
            payment = makePayment(
                username,
                firstCall["data"],
                secretKey,
            )
            return payment
        else:
            return {"error": firstCall["data"]}
    except Exception as e:
        raise Exception(e)
