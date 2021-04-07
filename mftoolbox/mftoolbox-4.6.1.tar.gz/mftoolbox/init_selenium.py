"""

Creates and instace of the wedbriver as browser and clears browsing data:
    - browsing history;
    - cookies and other site data;
    - cached images and files.

This prevents the browser having cached old pages like the ones whe the destination server is down

Inspiration for this module:

    - answer starting as "Selenium provides a convenient Select class to work with select -> option constructs...".
        this presented to me the Select class. Link:
        https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
    - article "How to interact with the elements within #shadow-root (open) while Clearing Browsing Data
        of Chrome Browser using cssSelector". Link:
        https://www.thetopsites.net/article/59404504.shtml
    - article that defined the function "__expand_shadow_element" by injecting a script inside python. Link:
        https://stackoverflow.com/questions/36141681/does-anybody-know-how-to-identify-shadow-dom-web-elements-using-selenium-webdriv
    - article "How to Use Selenium WebDriver Waits using Python" so the driver can wait until cache is cleared. Link:
        https://www.techbeamers.com/selenium-webdriver-waits-python/

"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from mftoolbox.constants import Header
from selenium.webdriver import Chrome
import os
import time

class Browser(webdriver.Chrome):
    """Cria um browser, sem carregar imagens para maior performance

    Parâmetros:

    hide (True default): esconde a janela
    clean (True default): limpa o cache da janela
    """
    @classmethod
    def clear_cache(self):
        # opening clear browse data page
        self.get('chrome://settings/clearBrowserData')
        # find time range dropdown. Full xpath:
        # /html/body/# settings-ui//div[2]/settings-main//settings-basic-page//div[1]/settings-section[4]/settings-privacy-page
        # //# settings-clear-browsing-data-dialog//cr-dialog[1]/div[3]/iron-pages/div[2]/div/settings-dropdown-menu//select'
        try:
            self.__root1 = Browser.find_element_by_tag_name("settings-ui")
            self.__shadow_root1 = self.__expand_shadow_element(Browser, self.__root1)
            self.__root2 = self.__shadow_root1.find_element_by_css_selector("settings-main#main")
            self.__shadow_root2 = self.__expand_shadow_element(Browser, self.__root2)
            self.__root3 = self.__shadow_root2.find_element_by_css_selector("settings-basic-page[role='main']")
            self.__shadow_root3 = self.__expand_shadow_element(Browser, self.__root3)
            self.__webelement1 = self.__shadow_root3.find_element_by_css_selector("settings-section[page-title='Privacy and security']")
            self.__root4 = self.__webelement1.find_element_by_css_selector('settings-privacy-page')
            self.__shadow_root4 = self.__expand_shadow_element(Browser, self.__root4)
            time.sleep(1)
            self.__root5 = self.__shadow_root4.find_element_by_css_selector('settings-clear-browsing-data-dialog')
            self.__shadow_root5 = self.__expand_shadow_element(Browser, self.__root5)
            self.__root6 = self.__shadow_root5.find_element_by_id('clearBrowsingDataDialog')
            self.__webelement2 = self.__root6.find_element_by_id('clearFromBasic')
            self.__shadow_root6 = self.__expand_shadow_element(Browser, self.__webelement2)
            self.__dropdown = Select(self.__shadow_root6.find_element_by_id('dropdownMenu'))
            #select option all time
            self.__dropdown.select_by_visible_text('All time')
            """
            #wait for button Clear Data Button to appear
            try:
                while not self.__root6.find_element_by_id('clearBrowsingDataConfirm'):
                    pass
            except exceptions.StaleElementReferenceException:
                raise Sair
            """
           # click button
            self.__button = self.__root6.find_element_by_id('clearBrowsingDataConfirm')
            self.__button.click()
            # wait until button disapears
            try:
                while self.__button.is_displayed():
                    pass
            except exceptions.StaleElementReferenceException:
                if Browser.current_url == 'chrome://settings/':
                    pass
                else:
                    raise Sair

        except Exception as e:
            if e.args[0] == 'name \'Sair\' is not defined':
                pass
            else:
                raise NameError('Ocorreu um problema')



    @classmethod
    def unhide(self):
        self.set_window_position(0, 0)

    @classmethod
    def hide(self):
        self.set_window_position(10000, 10000)

    @classmethod
    def get_focus(self):
        __currentWindow = self.getWindowHandle()
        self.switchTo().window(currentWindow)


    @classmethod
    def __expand_shadow_element(self, __browser, element):
        __shadow_root = __browser.execute_script('return arguments[0].shadowRoot', element)
        return __shadow_root




    def __init__(self, hide=True, clean=True, **kwargs):

        #setting up controls
        if clean not in [True,False]:
            self.__clean = False
        else:
            self.__clean = clean
        if hide not in [True,False]:
            self.__hide = False
        else:
            self.__hide = hide

        if self.__hide and not self.__clean:
            self.__options.add_argument("headless")
        try:
            __pictures = kwargs['pictures']
        except:
            __pictures = False
        try:
            kill_chromedrivers = kwargs['kill']
        except:
            kill_chromedrivers = False
        if kill_chromedrivers:
            tabela = os.popen('tasklist').readlines()
            for linha in tabela:
                if linha.find('chromedriver.exe') != -1:
                    try:
                        os.system("taskkill /f /im  chromedriver.exe")
                    except:
                        pass
            # setting up the browser
        __caps = DesiredCapabilities().CHROME
        __caps["pageLoadStrategy"] = "eager"
        # noinspection SpellCheckingInspection
        __options = webdriver.ChromeOptions()
        if not __pictures:
            __chrome_preferences = {'profile.managed_default_content_settings.images': 2}
            # noinspection SpellCheckingInspection
            __options.add_experimental_option("prefs", __chrome_preferences)
        __options.add_argument("disable-infobars")

        session_id = ''
        command_executor = ''
        error_handler = ''
        w3c = False
        # noinspection SpellCheckingInspection
        Browser = webdriver.Chrome(options=__options, service_args=['--silent'], desired_capabilities=__caps)
        Browser.header_overrides = Header
        self.w3c = Browser.w3c
        self.session_id = Browser.session_id
        self.command_executor = Browser.command_executor
        self.error_handler = Browser.error_handler
        if self.__clean:
            if self.__hide:
                Browser.set_window_position(10000, 10000)
            # opening clear browse data page
            Browser.get('chrome://settings/clearBrowserData')
            # find time range dropdown. Full xpath:
            # /html/body/# settings-ui//div[2]/settings-main//settings-basic-page//div[1]/settings-section[4]/settings-privacy-page
            # //# settings-clear-browsing-data-dialog//cr-dialog[1]/div[3]/iron-pages/div[2]/div/settings-dropdown-menu//select'
            try:
                self.__root1 = Browser.find_element_by_tag_name("settings-ui")
                self.__shadow_root1 = self.__expand_shadow_element(Browser, self.__root1)
                self.__root2 = self.__shadow_root1.find_element_by_css_selector("settings-main#main")
                self.__shadow_root2 = self.__expand_shadow_element(Browser, self.__root2)
                self.__root3 = self.__shadow_root2.find_element_by_css_selector("settings-basic-page[role='main']")
                self.__shadow_root3 = self.__expand_shadow_element(Browser, self.__root3)
                self.__webelement1 = self.__shadow_root3.find_element_by_css_selector("settings-section[page-title='Privacy and security']")
                self.__root4 = self.__webelement1.find_element_by_css_selector('settings-privacy-page')
                self.__shadow_root4 = self.__expand_shadow_element(Browser, self.__root4)
                time.sleep(1)
                self.__root5 = self.__shadow_root4.find_element_by_css_selector('settings-clear-browsing-data-dialog')
                self.__shadow_root5 = self.__expand_shadow_element(Browser, self.__root5)
                self.__root6 = self.__shadow_root5.find_element_by_id('clearBrowsingDataDialog')
                self.__webelement2 = self.__root6.find_element_by_id('clearFromBasic')
                self.__shadow_root6 = self.__expand_shadow_element(Browser, self.__webelement2)
                self.__dropdown = Select(self.__shadow_root6.find_element_by_id('dropdownMenu'))
                #select option all time
                self.__dropdown.select_by_visible_text('All time')
                """
                #wait for button Clear Data Button to appear
                try:
                    while not self.__root6.find_element_by_id('clearBrowsingDataConfirm'):
                        pass
                except exceptions.StaleElementReferenceException:
                    raise Sair
                """
               # click button
                self.__button = self.__root6.find_element_by_id('clearBrowsingDataConfirm')
                self.__button.click()
                # wait until button disapears
                try:
                    while self.__button.is_displayed():
                        pass
                except exceptions.StaleElementReferenceException:
                    if Browser.current_url == 'chrome://settings/':
                        pass
                    else:
                        raise Sair

            except Exception as e:
                if e.args[0] == 'name \'Sair\' is not defined':
                    pass
                else:
                    raise NameError('Ocorreu um problema')