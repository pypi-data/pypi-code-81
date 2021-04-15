def user_agent_common():
    """."""
    import random

    l = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    )
    # TODO: eventually, I would like to have an updated list of common user agents which get cached
    return random.choice(l)
    # from websites import website_get_section_containing

    # common_user_agent = website_get_section_containing('https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/', 'Mozilla/5.0')
    # return common_user_agent
