def get_headers(api_key):
    return {
        "Authorization" : "Api-Key {}".format(api_key)
    }
