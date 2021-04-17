from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    GO_BUTTON = (By.ID, 'submit')

class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    pass
class UploadPageLocators(object):
    INPUT = (By.XPATH,'//ytcp-uploads-file-picker//input')
    STEP_BADGE=(By.XPATH,'//button[@id="step-badge-0" and @state="error"]')
    TITLE = (By.XPATH,'//ytcp-mention-textbox//div[@id="textbox" and contains(@aria-label,"Add a title")]')
    DESCRIPTION = (By.XPATH,'//ytcp-mention-textbox//div[@id="textbox" and contains(@aria-label,"about your video")]')
    TAG = (By.XPATH,'//input[@id="text-input" and @aria-label="Tags"]')
    NOTIFY = (By.XPATH,'//div[contains(@class,"upload-item-alert")]/div[@class="yt-alert-content"]/div[@class="yt-alert-message"]')
    IS_ON_PUBLISH=(By.XPATH,'//div[@class="save-cancel-buttons"]/button[contains(.,"Publish") and not(@disabled)]')
    PUBLISH=(By.XPATH,'//div[@class="save-cancel-buttons"]/button[contains(.,"Publish")]')
    LANGUAGE_BUTTON=(By.ID,'yt-picker-language-button')
    LANGUAGE_ENGLISH_US=(By.XPATH,"//button[contains(.,\"English\")]")
    CUSTOM_THUMB_BUTTON = (By.XPATH, "//div[@class=\"custom-thumb-container\"]//button")
    CUSTOM_THUMB=(By.XPATH,'//div[@id="still-picker"]//ytcp-thumbnails-compact-editor-uploader//input')
    THUMB_AVAIL=(By.XPATH,'//div[contains(@class,"custom-thumb")]//img')
    VIDEO_LINK=(By.XPATH,'//a[contains(@class,"ytcp-video-info") and contains(@href,"youtu.be")]')
    START_BUTTON_UPLOAD=(By.XPATH,'//ytcp-button[@id="select-files-button"]')
    RESTORE_BUTTON=(By.XPATH,'//button[@id="restoreTab"]')
    FAIL_UPLOAD_STRIKE=(By.XPATH,'//div[@id="active-uploads-containbutton"]//div[contains(.,"cannot upload")]')

    NOT_MADE_FOR_KIDS=(By.NAME,'NOT_MADE_FOR_KIDS')
    DETAILS_BTN=(By.XPATH,'//ytcp-button[contains(.,"Show more")]')
    UPL_LANGUAGE_BTN = (By.XPATH, '//ytcp-form-select[contains(@class,"ytcp-form-language-input")]')
    UPL_LOCATION_INPUT=(By.XPATH,'id("location")/ytcp-form-autocomplete[@class="style-scope ytcp-form-location"]/ytcp-dropdown-trigger[@class="style-scope ytcp-form-autocomplete"]//input[@class="style-scope ytcp-form-autocomplete"]')
    UPL_LOCATION_BTN_CLICK=(By.XPATH,'//tp-yt-paper-item[contains(@test-id,"title")][1]')
    UPL_CATE_BTN=(By.XPATH,'//ytcp-form-select[@id="category"]')
    UPL_UPLOAD_PROGRESS=(By.XPATH,'//ytcp-video-upload-progress//span[contains(@class,"ytcp-video-upload-progress") and contains(text(),"Uploading")]')
    NEXT_BTN=(By.XPATH,'id("next-button")')
    PUBLIC_BTN = (By.NAME, 'PUBLIC')
    DONE_BTN = (By.XPATH, 'id("done-button")')
class LoginPageLocators(object):
    LANG_CHOOSE_BUTTON=(By.XPATH,"//div[@id=\"lang-chooser\"]")
    LANG_IT = (By.XPATH, "//*[@id=\"lang-chooser\"]/div[2]/div[@data-value=\"it\"]")
    LANG_EN = (By.XPATH, "//*[@id=\"lang-chooser\"]/div[2]/div[@data-value=\"en\"]")
    EMAIL_LOGIN=(By.ID,"identifierId")
    PASS_WORD_LOGIN=(By.NAME,"password")
    RECO_EMAIL_BUTTON = (By.XPATH, "//form//div[contains(text(),\"Confirm your recovery email\")]")
    EMAIL_RECO=(By.ID,"knowledge-preregistered-email-response")
    EMAIL_RECO2= (By.ID, "identifierId")
    PROFILE_INDENTIFIER=(By.XPATH,"//div[@id=\"profileIdentifier\" and contains(@data-email,\"@\")]")
    VERIFY_NEXT=(By.ID,"identifierNext")
    DONE_BUTTON=(By.XPATH,"//div[@role=\"button\" and contains(text(),\"Done\")]")
class EditPageLocators(object):
    PUBLISH_BUTTON=(By.XPATH, "//button[contains(@class,\"vm-video-publish\") and @data-video-id]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class,\"save-changes-button\")]")
class WatchPageLocators(object):
    SUBS_BUTTON=(By.XPATH,"//div[@id=\"subscribe-button\"]//yt-formatted-string[text()=\"Subscribe\"]");
class AboutMeLocators(object):
    FIRST_NAME=(By.XPATH,"//input[@aria-label=\"First\"]")
    LAST_NAME = (By.XPATH, "//input[@aria-label=\"Last\"]")
    SUR_NAME=(By.XPATH, "//input[@aria-label=\"Surname\"]")
    FULL_NAME=(By.XPATH, "//input[@aria-label=\"Name\"]")

    FIRST_NAME_ROLE = (By.XPATH, "(//*[@role=\"dialog\"]//input)[1]")
    LAST_NAME_ROLE = (By.XPATH, "(//*[@role=\"dialog\"]//input)[2]")

    OK_BUTTON=(By.XPATH,"(//*[@role=\"dialog\"]//div[@role=\"button\"])[4]")
    CONFIRM_BUTTON=(By.XPATH,"(//*[@role=\"dialog\"]//div[@role=\"button\"])[4]")