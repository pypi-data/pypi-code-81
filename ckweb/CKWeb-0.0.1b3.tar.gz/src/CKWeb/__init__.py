# encoding: utf-8
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as GCOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from robot.api.deco import keyword
import logging

cmd = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class CKWeb(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    @keyword('Browser Open')
    def browseropen(self, browserType='chrome', headless='off'):
        """ 
        browserType
            |    = Browser =    |        = Name(s) =       |
            | Firefox           | firefox, ff              |
            | Google Chrome     | googlechrome, chrome, gc |

        headless
            |    = Options =    |
            | off               |
            | on                |

        Examples:
            | `Browser Open` | chrome  |         |
            | `Browser Open` | chrome  | on      |
            | `Browser Open` | chrome  | off     |
        """
        global driver
        global actions
        if (browserType == 'chrome' or 'gc' or 'googlechrome'):
            driver_path = cwd + "/driver/chromedriver.exe"
            options = GCOptions()
            if (headless=='on'):
                options.headless = True
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
        elif(browserType == 'firefox' or 'ff'):
            driver_path = cwd + "/driver/geckodriver.exe"
            options = FFOptions()
            if (headless=='on'):
                options.headless = True
            driver = webdriver.Firefox(executable_path=driver_path, options=options)
        driver.implicitly_wait(1)
        actions = ActionChains(driver)

    @keyword('Browser Goto')
    def browsergoto(self, url):
        """ 
        Examples:
            | Browser Goto     | https://www.google.com/  |
        """
        driver.get(url)
        driver.implicitly_wait(1)

    @keyword('Browser Input')
    def browserinput(self, xPath, text):
        """ 
        Examples:
            | Browser Input     | //*[@name='q']  |  test     |
        """
        input_text = driver.find_element(By.XPATH, xPath)
        input_text.location_once_scrolled_into_view
        input_text.clear()
        input_text.send_keys(text)
        driver.implicitly_wait(1)

    @keyword('Browser Click')
    def browserclick(self, xPath):
        """ 
        Examples:
            | Browser Click     | //*[@name='q']  |
        """
        click_element = driver.find_element(By.XPATH, xPath)
        click_element.location_once_scrolled_into_view
        click_element.click()
        driver.implicitly_wait(1)

    @keyword('Browser Get')
    def browserget(self, xPath):
        """ 
        Examples:
            | ${value}   | Browser Get     | //*[@name='q']  |
        """
        get_element = driver.find_element(By.XPATH, xPath)
        get_element.location_once_scrolled_into_view
        get = get_element.text
        driver.implicitly_wait(1)
        return get

    @keyword('Browser Select Frame')
    def browseriframe(self, xPath):
        """ 
        Examples:
            | Browser Select Frame     | //*[@name='q']  |
        """
        browseriframe = driver.find_element(By.XPATH, xPath)
        browseriframe.location_once_scrolled_into_view
        driver.switchTo.frame(browseriframe)
        driver.implicitly_wait(1)

    @keyword('Browser Unselect Frame')
    def browseruniframe():
        """ 
        Examples:
            | Browser Unselect Frame     |
        """
        uniframe = driver.switchTo.default_content()
        uniframe.location_once_scrolled_into_view
        driver.implicitly_wait(1)

    @keyword('Browser Select Value')
    def selectValue(self, xPath, value):
        """ 
        Examples:
            | Browser Select Value     | //*[@name='q']  |  test     |
        """
        selectValue = driver.find_element(By.XPATH, xPath)
        selectValue.location_once_scrolled_into_view
        dropdown = Select(selectValue)
        dropdown.select_by_value(value);
        driver.implicitly_wait(1)

    @keyword('Browser Select Index')
    def selectIndex(self, xPath, index):
        """ 
        Examples:
            | Browser Select Index     | //*[@name='q']  |  test     |
        """
        selectIndex = driver.find_element(By.XPATH, xPath)
        selectIndex.location_once_scrolled_into_view
        dropdown = Select(selectIndex)
        dropdown.select_by_index(index);
        driver.implicitly_wait(1)

    @keyword('Browser Select Text')
    def selectText(self, xPath, text):
        """ 
        Examples:
            | Browser Select Text     | //*[@name='q']  |  test     |
        """
        selectText = driver.find_element(By.XPATH, xPath)
        selectText.location_once_scrolled_into_view
        dropdown = Select(selectText)
        dropdown.select_by_visible_text(text);
        driver.implicitly_wait(1)

    @keyword('Browser Close')
    def close(self):
        """ 
        Examples:
            | Browser Close     |
        """
        driver.quit()
        debuglog('close')
