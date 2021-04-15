from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Type,
)

from requests.exceptions import (
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects,
)

whitelist = [
    'admin',
    'miner',
    'net',
    'txpool'
    'testing',
    'evm',
    'klay_protocolVersion',
    'klay_syncing',
    'klay_coinbase',
    'klay_mining',
    'klay_hashrate',
    'klay_gasPrice',
    'klay_accounts',
    'klay_blockNumber',
    'klay_getBalance',
    'klay_getStorageAt',
    'klay_getProof',
    'klay_getCode',
    'klay_getBlockByNumber',
    'klay_getBlockByHash',
    'klay_getBlockTransactionCountByNumber',
    'klay_getBlockTransactionCountByHash',
    'klay_getUncleCountByBlockNumber',
    'klay_getUncleCountByBlockHash',
    'klay_getTransactionByHash',
    'klay_getTransactionByBlockHashAndIndex',
    'klay_getTransactionByBlockNumberAndIndex',
    'klay_getTransactionReceipt',
    'klay_getTransactionCount',
    'klay_call',
    'klay_estimateGas',
    'klay_newBlockFilter',
    'klay_newPendingTransactionFilter',
    'klay_newFilter',
    'klay_getFilterChanges',
    'klay_getFilterLogs',
    'klay_getLogs',
    'klay_uninstallFilter',
    'klay_getCompilers',
    'klay_getWork',
    'klay_sign',
    'klay_signTypedData',
    'klay_sendRawTransaction',
    'personal_importRawKey',
    'personal_newAccount',
    'personal_listAccounts',
    'personal_listWallets',
    'personal_lockAccount',
    'personal_unlockAccount',
    'personal_ecRecover',
    'personal_sign',
    'personal_signTypedData',
]


def check_if_retry_on_failure(method) -> bool:
    root = method.split('_')[0]
    if root in whitelist:
        return True
    elif method in whitelist:
        return True
    else:
        return False


def exception_retry_middleware(
    make_request,
    errors: Collection[Type[BaseException]],
    retries: int = 5,
):
    """
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPProvider.
    """
    def middleware(method, params: Any):
        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return make_request(method, params)
                # https://github.com/python/mypy/issues/5349
                except errors:  # type: ignore
                    if i < retries - 1:
                        continue
                    else:
                        raise
            return None
        else:
            return make_request(method, params)
    return middleware


def http_retry_request_middleware(
    make_request, web3
):
    return exception_retry_middleware(
        make_request,
        (ConnectionError, HTTPError, Timeout, TooManyRedirects)
    )
