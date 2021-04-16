from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import backoff
import socket

from googleapiclient.errors import HttpError



class MctAccountLostAccessException(Exception):
    """Raised when we cannot access to an account."""
    pass


class MerchantCenterServiceDownException(Exception):
    """Raised when we cannot access to MCC service """
    pass


def get_mct_service(adscale_key: str, cache_discovery=True):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        adscale_key, scopes=['https://www.googleapis.com/auth/content'])
    service = discovery.build('content', 'v2.1', credentials=credentials, cache_discovery=cache_discovery)
    return service


@backoff.on_exception(backoff.expo, (socket.timeout), max_tries=3)
def get_mct_account_details(merchant_id: int, adscale_key: str):

    try:
        service = get_mct_service(adscale_key)
        # Get account status alerts from MCT
        request_account_statuses = service.accounts().get(merchantId=merchant_id,
                                                          accountId=merchant_id)
        response_account_statuses = request_account_statuses.execute()
    except HttpError as err:
        print(err)
        if err.resp.status >= 400 and err.resp.status < 500:
            raise MctAccountLostAccessException(f"We cannot access your Merchant Center account with the id: {merchant_id}. Are you sure you grant access and give correct ID?")
        else:
            raise MerchantCenterServiceDownException(f"The Merchent Center API does not respond. Thus, we cannot check if we can access your Merchant Center account with the id: {merchant_id}. Please try later" )
    return response_account_statuses['name']


@backoff.on_exception(backoff.expo, (socket.timeout), max_tries=3)
def check_if_multi_client_account(merchant_id: int, adscale_key: str):
    """ Sends an error if the account is a MCA """
    try:
        service = get_mct_service(adscale_key)

        # This API method is only available to sub-accounts, thus it will fail if the merchant id is a MCA
        request_account_products = service.products().list(merchantId=merchant_id)
        response_account_statuses = request_account_products.execute()
    except HttpError as err:
        if err.resp.status >= 400 and err.resp.status < 500:
            raise MctAccountLostAccessException(f"This merchant id ({merchant_id} is for multi acccounts. You can only link sub-accounts.")
        else :
            raise MerchantCenterServiceDownException(f"The Merchent Center API does not respond. Thus, we cannot check if we can access your Merchant Center account with the id: {merchant_id}. Please try later" )
    return response_account_statuses
