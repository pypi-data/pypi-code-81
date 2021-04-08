import logging


def to_json(response):
    res_decoded, decoding_err = try_json(response)

    if decoding_err:
        # decoding error, report, but assume unrecoverable
        logging.exception(decoding_err)
        return None

    if not isinstance(res_decoded, dict):
        logging.error(f"Invalid response type: {type(res_decoded)} (expected: dict)")
        return None

    return res_decoded


def try_json(response):
    """ Decodes response as json, returns decoded and optional error """
    try:
        return response.json(), None
    except ValueError as e:
        return None, e
