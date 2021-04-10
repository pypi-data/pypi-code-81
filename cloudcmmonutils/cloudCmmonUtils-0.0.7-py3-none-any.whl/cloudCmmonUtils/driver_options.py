import os

from selenium import webdriver
import atApiBasicLibrary.log as log
from selenium.webdriver.chrome.options import Options


def create_chrome_options(head="–-headless",gpu="-–disable-gpu",sandbox="–-no-sandbox"):
    '''
    创建chrome webdriver的options参数
    :param head:
    :param gpu:
    :param sandbox:
    :return:
    '''
    # options = webdriver.ChromeOptions()
    options = Options()
    if os.name.lower().startswith('nt'):
        return
    elif os.name.lower().startswith('posix'):
        options.add_argument(head)
        options.add_argument(gpu)
        options.add_argument(sandbox)
        log.info('create_chrome_options.options:%s'% options)
    return options



if __name__ == '__main__':
    create_chrome_options()
