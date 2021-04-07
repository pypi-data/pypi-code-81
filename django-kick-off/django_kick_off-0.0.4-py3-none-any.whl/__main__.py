# Built-in modules
import sys
import requests

# Own modules
from .cprint import cprint

# Check if there internet connection
# https://www.kite.com/python/answers/how-to-check-internet-connection-in-python
url = "http://www.google.com"
timeout = 5
try:
    request = requests.get(url, timeout=timeout)
    cprint.success(''.center(30, '-'))
    cprint.success('|' + 'Connected to the Internet'.center(28, ' ') + '|')
    cprint.success(''.center(30, '-'))
except (requests.ConnectionError, requests.Timeout) as exception:
    cprint.error(''.center(30, '-'))
    cprint.error('|' + 'No internet connection'.center(28, ' ') + '|')
    cprint.error(''.center(30, '-'))
    exit(1)

if __name__ == '__main__':
    from .core import main
    main(sys.argv)