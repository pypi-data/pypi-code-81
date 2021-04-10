import platform
import atApiBasicLibrary.log as log
from selenium.webdriver.chrome.options import Options


def create_chrome_options():
    '''
    创建chrome webdriver的options参数
    :param head:
    :param gpu:
    :param sandbox:
    :return:
    '''
    # options = webdriver.ChromeOptions()
    options = Options()
    if platform.system().lower().startswith('win'):
        return
    elif platform.system().lower().startswith('linux'):
        options.add_argument("–-headless")
        options.add_argument("-–disable-gpu")
        options.add_argument("–-no-sandbox")
        log.info('create_chrome_options.options:%s'% options)
    return options



if __name__ == '__main__':
    create_chrome_options()
