from sreup.selenium.elements import BasePageElement
from selenium import webdriver
from sreup.selenium.locators import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
from selenium.webdriver.common.keys import Keys
class UploadElement(BasePageElement):
    locator=UploadPageLocators.INPUT
    is_find_hide=True
class TitleUploadElement(BasePageElement):
    locator=UploadPageLocators.TITLE
    is_click_on = True
class DescriptionUploadElement(BasePageElement):
    locator = UploadPageLocators.DESCRIPTION
    is_click_on = True
class TagUploadElement(BasePageElement):
    locator = UploadPageLocators.TAG
class ThumbnailUploadElement(BasePageElement):
    locator = UploadPageLocators.CUSTOM_THUMB
    is_find_hide = True
class VideoLinkUploadElement(BasePageElement):
    locator = UploadPageLocators.VIDEO_LINK
class EmailLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_LOGIN
class PassWordLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.PASS_WORD_LOGIN
class EmailRecoElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_RECO

class EmailRecoElement2(BasePageElement):
    delay = 5
    locator = LoginPageLocators.EMAIL_RECO2
class LocationElement(BasePageElement):
    delay= 5
    locator = UploadPageLocators.UPL_LOCATION_INPUT
    is_click_on = True
class LocationTABElement(BasePageElement):
    delay= 5
    locator = UploadPageLocators.UPL_LOCATION_INPUT
    is_clear_text = False
class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""
    def __init__(self, driver):
        self.driver = driver

class UploadPage(BasePage):
    upload_path_element=UploadElement()
    title=TitleUploadElement()
    description=DescriptionUploadElement()
    tag=TagUploadElement()
    thumb=ThumbnailUploadElement()
    video_link=VideoLinkUploadElement()
    loc_video=LocationElement()
    def check_language(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON))
        if "English" in self.driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON).text:
            print("Ok English")
        else:
            print("change language")
            self.driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON).click()
            time.sleep(1)
            self.driver.find_element(*UploadPageLocators.LANGUAGE_ENGLISH_US).click()
            time.sleep(3)
    def is_custom_thumb(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(UploadPageLocators.CUSTOM_THUMB_BUTTON))
            return True;
        except Exception as e:
            print(e)
        return False;
    def wait_custom_thumb_avail(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(UploadPageLocators.THUMB_AVAIL))
            return True;
        except Exception as e:
            print(e)
        return False;

    def wait_title_input_avail(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(UploadPageLocators.TITLE))
            return True;
        except Exception as e:
            print(e)
            traceback.print_exc()
        return False
    def set_title_vid(self,title):
        tmp_title=title
        while True:
            self.title = tmp_title + Keys.ENTER
            try:
                self.driver.find_element(*UploadPageLocators.STEP_BADGE)
                tmp_title = tmp_title[:-1]
            except:
                break
                pass
    def is_upload_page(self):
        print("check is_upload_page: " + self.driver.current_url)
        return "youtube.com" in self.driver.current_url and "videos/upload" in self.driver.current_url
    def is_avail_upload(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(UploadPageLocators.START_BUTTON_UPLOAD))
            self.driver.find_element(*UploadPageLocators.START_BUTTON_UPLOAD)
            return True
        except Exception as e:
            print(e)
        return False;
    def click_no_kids_details(self):
        self.driver.find_element(*UploadPageLocators.NOT_MADE_FOR_KIDS).click()
        time.sleep(1)
        action = webdriver.ActionChains(self.driver)
        element = self.driver.find_element(*UploadPageLocators.DETAILS_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        action.move_to_element(element)
        action.perform()
        time.sleep(1)
        element.click()
    def set_tag_vid(self, tag_text):
        try:
            self.tag = tag_text
            is_error_tag=True
            while is_error_tag:
                xd=self.driver.find_element_by_xpath('id("tags-count")').text
                tags_count=xd.split("/")[0]
                if int(tags_count) > 500:
                    self.driver.find_element_by_xpath('//ytcp-form-input-container[@id="tags-container"]//ytcp-icon-button[@id="clear-button"]').click()
                    pad_tag=int(tags_count) - 430
                    tag_text= tag_text[:(-1*pad_tag)]
                    time.sleep(1)
                    self.driver.find_element(*UploadPageLocators.TAG).send_keys(tag_text)
                    # self.tag=tag_text
                    time.sleep(3)
                else:
                    break
        except:
            pass
    def set_vid_lang(self,lang_code='en'):
        try:
            self.driver.find_element(*UploadPageLocators.UPL_LANGUAGE_BTN).click()
            time.sleep(3)
            self.driver.find_element_by_xpath(f"//tp-yt-paper-item[@test-id=\"{lang_code}\"]").click()
            time.sleep(1)
        except:
            pass
    def set_vid_loc(self,location='USA'):
        try:
            location_comp = self.driver.find_element(*UploadPageLocators.UPL_LOCATION_INPUT)
            location_comp.clear()
            time.sleep(1)
            location_comp.send_keys(location)
            location_comp.send_keys(Keys.TAB)
            time.sleep(3)
            self.driver.find_element(*UploadPageLocators.UPL_LOCATION_BTN_CLICK).click()
        except:
            pass

    def set_vid_cate(self,cate_code='CREATOR_VIDEO_CATEGORY_PETS'):
        try:
            self.driver.find_element(*UploadPageLocators.UPL_CATE_BTN)
            time.sleep(1)
            self.driver.find_element_by_xpath(f"//tp-yt-paper-item[contains(@test-id,\"{cate_code}\")]").click()
        except:
            pass

    def wait_vid_progress(self,):
        is_next = True
        count=0
        while (is_next and count<3600):
            try:
                is_next = False
                self.driver.find_element(*UploadPageLocators.UPL_UPLOAD_PROGRESS)
                count+=1
                is_next = True
                time.sleep(1)
            except:
                pass
    def publish(self):
        try:
            self.driver.find_element(*UploadPageLocators.NEXT_BTN).click()
            time.sleep(2)
            self.driver.find_element(*UploadPageLocators.NEXT_BTN).click()
            time.sleep(2)
            try:
                self.driver.find_element(*UploadPageLocators.NEXT_BTN).click()
                time.sleep(2)
            except:
                pass
            self.driver.find_element(*UploadPageLocators.PUBLIC_BTN).click()
            time.sleep(2)
            self.driver.find_element(*UploadPageLocators.DONE_BTN).click()
        except:
            pass
class WatchPage(BasePage):
    def subscribe(self):
        try:
            self.driver.find_element(*WatchPageLocators.SUBS_BUTTON).click()
        except:
            pass
class EditPage(BasePage):
    def publish(self):
        try:
            video_id = self.driver.find_element(*EditPageLocators.PUBLISH_BUTTON).get_attribute("data-video-id")
            self.driver.get("https://www.youtube.com/edit?o=U&video_id="+video_id)
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(
                    *UploadPageLocators.TITLE))
            if "hbt2" not in self.driver.find_element(*UploadPageLocators.TITLE).text:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.find_element(
                        *EditPageLocators.SAVE_BUTTON))
                self.driver.find_element(*EditPageLocators.SAVE_BUTTON).click()
                time.sleep(5)
        except:
            pass

class LoginPage(BasePage):
    email_login=EmailLoginElement()
    pass_word_login=PassWordLoginElement()
    email_reco_login=EmailRecoElement()
    email_reco_login2=EmailRecoElement2()
    def is_login(self):
        return "accounts.google.com" in self.driver.current_url
    def is_en_lang(self):
        return "English" in self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).text
    def click_cofirm_reco(self,email_reco):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(
                    *LoginPageLocators.RECO_EMAIL_BUTTON))
            self.driver.find_element(*LoginPageLocators.RECO_EMAIL_BUTTON).click()
        except:
            pass
        try:
            self.email_reco_login2=email_reco+Keys.RETURN
        except:
            pass
        try:
            self.email_reco_login=email_reco+Keys.RETURN
        except:
            pass
    def click_profile_indentifier(self):
        self.driver.find_element(*LoginPageLocators.PROFILE_INDENTIFIER).click()
        time.sleep(2)
    def click_next_verify(self):
        self.driver.find_element(*LoginPageLocators.VERIFY_NEXT).click()
        time.sleep(2)
    def change_language(self):
        if self.is_en_lang():
            return
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *LoginPageLocators.LANG_CHOOSE_BUTTON))
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_IT).click()
        time.sleep(2)
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_EN).click()
        time.sleep(2)
    def click_done_button(self):
        self.driver.find_element(*LoginPageLocators.DONE_BUTTON).click()
        time.sleep(2)



class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source


class AboutMePage(BasePage):
    def fill_text(self, element, text):
        element = self.driver.find_element(*element)
        element.clear()
        element.send_keys(text)
    def change_name(self, full_name):
        first_name=full_name.split(" ")[0]
        last_name=full_name.split(" ")[1]
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME,first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.SUR_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FULL_NAME, full_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME_ROLE, first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME_ROLE, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.driver.find_element(AboutMeLocators.OK_BUTTON).click()
            time.sleep(3)
            self.driver.find_element(AboutMeLocators.CONFIRM_BUTTON).click()
        except:
            pass