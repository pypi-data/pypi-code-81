import os

from selenium import webdriver
import atApiBasicLibrary.log as log
def create_chrome_options(head="–-headless",gpu="-–disable-gpu",sandbox="–-no-sandbox"):
    '''
    创建chrome webdriver的options参数
    :param head:
    :param gpu:
    :param sandbox:
    :return:
    '''
    options = webdriver.ChromeOptions()
    if os.name.lower().startswith('win'):
        return
    elif os.name.lower().startswith('linux'):
        options.add_argument(head)
        options.add_argument(gpu)
        options.add_argument(sandbox)
    log.info('create_chrome_options.options:%s'% options)
    return options



if __name__ == '__main__':
    create_chrome_options()
