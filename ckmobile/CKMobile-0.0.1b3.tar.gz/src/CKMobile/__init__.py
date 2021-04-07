# encoding: utf-8
import os
import time
import logging
from datetime import datetime
from robot.api.deco import keyword
import uiautomator2 as U2

dir_file = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class CKMobile(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    @keyword('Android Connect')
    def connect(self, deviceName=''):
        """
        Example
        | Android Connect |              |
        | Android Install | 124555323235 |
        | Android Install | android-9    |
        """
        global d
        if (deviceName == ''):
            d = U2.connect()
            xml = d.dump_hierarchy()
            d.implicitly_wait(1)
        else:
            d = U2.connect(deviceName)
            xml = d.dump_hierarchy()
            d.implicitly_wait(1)

    @keyword('Android Install')
    def install(self, apk):
        """
        Example
        | Android Install | app.apk                    |
        | Android Install | http://domain.com/app.apk  |
        """
        d.app_install(apk)
        d.implicitly_wait(1)

    @keyword('Android Start Application')
    def startApp(self, packageName):
        """
        Example
        | Android Start Application | .MainActivity        |
        | Android Start Application | .MainPckageActivity  |
        """
        d.app_start(packageName)
        d.implicitly_wait(1)

    @keyword('Android Current App')
    def currentApp(self):
        """
        Example
        | ${Retunr} | Android Current App | //*[@id="Example"]      |
        | ${Retunr} | Android Current App | //*[@name="Example"]    |
        """
        appName = d.current_app()
        d.implicitly_wait(1)
        return appName['package']

    @keyword('Android Click xPath')
    def xpathClick(self, xPath):
        """
        Example
        | Android Click xPath | //*[@id="Example"]    |
        | Android Click xPath | //*[@name="Example"]  |
        """
        d.xpath(xPath).click()
        d.implicitly_wait(1)

    @keyword('Android Click Element')
    def elementClick(self, attribute, value):
        """
        Example
        | Android Click Element | id          | Example |
        | Android Click Element | resourceid  | Example |
        | Android Click Element | text        | Example |
        """
        if 'text' in attribute:
            d(textContains=value).click()
            d.implicitly_wait(1)
        elif 'resourceid' or 'id' in attribute:
            d(resourceId=value).click()
            d.implicitly_wait(1)


    @keyword('Android Double Click xPath')
    def xpathDoubleClick(self, xPath):
        """
        Example
        | Android Double Click xPath | //*[@id="Example"]    |
        | Android Double Click xPath | //*[@name="Example"]  |
        """
        d.xpath(xPath).double_click()
        d.implicitly_wait(1)

    @keyword('Android Double Click Element')
    def elementDoubleClick(self, attribute, value):
        """
        Example
        | Android Double Click Element | id          | Example |
        | Android Double Click Element | resourceid  | Example |
        | Android Double Click Element | text        | Example |
        """
        if 'text' in attribute:
            d(textContains=value).double_click()
            d.implicitly_wait(1)
        elif 'resourceid' or 'id' in attribute:
            d(resourceId=value).double_click()
            d.implicitly_wait(1)

    @keyword('Android Home')
    def home(self):
        """
        Example
        | Android Home |
        """
        appName = d.current_app()
        d.app_stop(appName['package'])
        d.implicitly_wait(1)
        
    @keyword('Android Back')
    def back(self):
        """
        Example
        | Android Back |
        """
        d.press("back")
        d.implicitly_wait(1)

    @keyword('Android Text Input')
    def textInput(self, attribute, element, text):
        """
        Example
        | Android Text Input | id          | Example | Test    |
        | Android Text Input | resourceid  | Example | Test    |
        | Android Text Input | text        | Example | Test    |
        """
        if 'text' in attribute:
            d(textContains=element).click()
        elif 'resourceid' or 'id' in attribute:
            d(resourceId=element).click()
        d.send_keys(text)
        d.implicitly_wait(1)
        d.press("back")

    @keyword('Android xPath Input')
    def xpathInput(self, xPath, text):
        """
        Example
        | Android xPath Input | //*[@id="Example"]    | Test    |
        | Android xPath Input | //*[@name="Example"]  | Example |
        """
        d.xpath(element).click()
        d.send_keys(text)
        d.implicitly_wait(1)
        d.press("back")

    @keyword('Android Get Text')
    def getText(self, attribute, value):
        """
        Example
        | Android Get Text | id          | Example    |
        | Android Get Text | resourceid  | id/Example |
        | Android Get Text | text        | Example    |
        """
        if 'resourceid' or 'id' in attribute:
            text = d(resourceId=value).get_text()
            d.implicitly_wait(1)
        elif 'text' in attribute:
            text = d(textContains=value).get_text()
            d.implicitly_wait(1)
        return text

    @keyword('Android Screenshot')
    def screenshot(self, dir_path=''):
        """
        Example
        | Android Screenshot |          |
        | Android Screenshot | D:/test  |
        """
        now = datetime.now()
        time = now.strftime("%Y%m%dT%H%M%S")
        if dir_path=='':
            file_screen = 'Screenshot-{}.png'.format(time)
        else:
            file_screen = '{}/Screenshot-{}.png'.format(dir_path,time)
        d.screenshot(file_screen)
        d.implicitly_wait(1)

    @keyword('Android Swipe To Value')
    def swipeToValue(self, element):
        """
        Example
        | Android Swipe To Value | Example    |
        | Android Swipe To Value | Test       |
        """
        d(scrollable=True).scroll.to(textContains=element)
        d.implicitly_wait(1)

    @keyword('Android Swipe To Element')
    def swipeToElement(self, attribute, value):
        """
        Example
        | Android Swipe To Element | id         | Example    |
        | Android Swipe To Element | resourceid | id/Example |
        | Android Swipe To Element | desc       | Example    |
        """
        if 'resourceid' or 'id' in attribute:
            d(scrollable=True).drag_to(resourceId=value)
        elif 'desc' in attribute:
            d(scrollable=True).drag_to(descriptionContains=value)
        d.implicitly_wait(1)

    @keyword('Android Unlock PIN')
    def unlockPIN(self, pin_no, enter='OK'):
        """
        Example
        | Android Unlock PIN  | 112233  |        |
        | Android Unlock PIN  | 112233  | ok     |
        | Android Unlock PIN  | 112233  | enter  |
        """
        d.unlock()
        for pin in list(pin_no):
            d(textContains=pin).click()
        d(textContains=enter).click(timeout=10)
        appName = d.current_app()
        d.app_stop(appName['package'])
        d.implicitly_wait(1)

    @keyword('Android Notification')
    def notification(self):
        """
        Example
        | Android Notification  |
        """
        d.open_notification()
        d.implicitly_wait(1)

    @keyword('Android Skip Popups')
    def skipPopups(self, skip=True):
        """
        Example
        | Android Skip Popups  |        |
        | Android Skip Popups  | True   |
        | Android Skip Popups  | False  |
        """
        if skip==True:
            d.disable_popups()
            d.implicitly_wait(1)
        else:
            d.disable_popups(False)
            d.implicitly_wait(1)

    @keyword('Android Turn Screen')
    def screenTurn(self, turn=True):
        """
        Example
        | Android Turn Screen  |        |
        | Android Turn Screen  | True   |
        | Android Turn Screen  | False  |
        """
        if turn == True:
            d.screen_on()
            d.implicitly_wait(1)
        else:
            d.screen_off()
            d.implicitly_wait(1)

    @keyword('Android Key Events')
    def keyEvents(self, key):
        """
        These key names are currently supported:
        | home                 |
        | back                 |
        | left                 |
        | right                |
        | up                   |
        | down                 |
        | center               |
        | menu                 |
        | search               |
        | enter                |
        | delete               |
        | volume_up            |
        | volume_down          |
        | volume_mute          |
        | camera               |
        | power                |
        """
        d.press(key)
        d.implicitly_wait(1)