
import json
import logging
import os
import requests
import subprocess
import time
import uuid

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains

from appium import webdriver

URL = 'https://fluffy-dragon.test.ai'

class TestAiDriver():
    def __init__(self, driver, api_key):
        self.driver = driver
        self.api_key = api_key
        self.run_id = str(uuid.uuid1())

    def find_element(self, by='id', value=None, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element(by=by, value=value)
        if label:
            self._update_elem(el, key)
        return el

    def find_element_by_class_name(self, class_name, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_class_name(class_name)
        if label:
            self._update_elem(el, key)
        return el

    def find_element_by_css_selector(self, css_selector, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_css_selector(css_selector)
        if label:
            self._update_elem(el, key)
        return el

    def find_element_by_id(self, id_, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_id(id_)
        if label:
            self._update_elem(el, key)
        return el


    def find_element_by_link_text(self, link_text, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_link_text(link_text)
        if label:
            self._update_elem(el, key)
        return el


    def find_element_by_name(self, name, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_name(name)
        if label:
            self._update_elem(el, key)
        return el

    
    def find_element_by_partial_link_text(self, link_text, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_partial_link_text(link_text)
        if label:
            self._update_elem(el, key)
        return el


    def find_element_by_tag_name(self, name, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(label)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_tag_name(name)
        if label:
            self._update_elem(el, key)
        return el


    def find_element_by_xpath(self, xpath, label=None):
        key = None
        if label is not None:
            el, key = self.find_by_label(xpath)
            if el is not None:
                return el
        
        # Run the standard selector
        el = self.driver.find_element_by_xpath(name)
        if label:
            self._update_elem(el, key)
        return el



    def _update_elem(self, elem, key):
        data = {
            'key': key,
            'api_key': self.api_key,
            'run_id': self.run_id,
            'x': elem.rect['x'],
            'y': elem.rect['y'],
            'width': elem.rect['width'],
            'height': elem.rect['height']
        }
        try:
            action_url = URL + '/add_action'
            _ = requests.post(action_url, data=data)
        except Exception:
            pass


    def find_by_label(self, label):
        element = None
        run_key = None
        # Call service
        ## Get screenshot & page source
        screenshotBase64 = self.driver.get_screenshot_as_base64()
        try:
            source = self.driver.page_source
        except Exception:
            source = ''

        # Check results
        try:
            data = {'screenshot': screenshotBase64, 'source': source,
                    'api_key':self.api_key, 'label': label, 'run_id': self.run_id}
            classify_url = URL + '/classify'
            r = requests.post(classify_url, data=data)
            #print('r.text: %s', r.text)
            response = json.loads(r.text)
            run_key = response['key']
            if response.get('success', False):
                print('successful classification of label: %s' % label)
                pred_elem = response['elem']

                root_elem = self.driver.find_element_by_xpath("//*")
                element = testai_elem(root_elem.parent, root_elem._id, pred_elem, self.driver)
                # Found elem, use image matcher
                # self.driver.update_settings({"getMatchedImageResult": True})
                # element = self.driver.find_element_by_image('/Users/chris/test_ai/api/next.png')
            else:
                logging.error('Classification failed for label: %s - Please visit %s to classify' % (label, URL+'/label/'+self.run_id))
        except Exception:
            logging.error('exception during classification')
        return element, run_key


class testai_elem(webdriver.webelement.WebElement):
    def __init__(self, parent, _id, elem, driver):
        super(testai_elem, self).__init__(parent, _id)
        self.driver = driver
        self._text = elem.get('text', '')
        self._size = {'width': elem.get('width', 0), 'height': elem.get('height', 0)}
        self._location = {'x': elem.get('x', 0), 'y': elem.get('y', 0)}
        self._property = elem.get('class', '')
        self._rect = self._size | self._location
        self._tag_name = elem.get('class', '')
        self._cx = elem.get('x', 0) + elem.get('width', 0) / 2
        self._cy = elem.get('y', 0) + elem.get('height', 0) / 2

    
    @property
    def text(self):
        return self._text
    @property
    def size(self):
        return self._size
    @property
    def location(self):
        return self._location
    @property
    def rect(self):
        return self._rect
    @property
    def tag_name(self):
        return self._tag_name

    def click(self):
        self.driver.tap([(self._cx, self._cy)])

    def send_keys(self, value, click_first=True):
        if click_first:
            self.click()
        actions = ActionChains(self.driver)
        actions.send_keys(value)
        actions.perform()

    def submit(self):
        self.send_keys('\n', click_first=False)

    def clear(self):
        pass

    def is_selected(self):
        return True
    def is_enabled(self):
        return True
    def is_displayed(self):
        return True
