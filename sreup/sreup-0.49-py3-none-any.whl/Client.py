from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil, requests, os, json
from sreup.selenium import page
from sreup.common import config, utils, Requests
import time, traceback
import multiprocessing
import threading
from gbackup import DriverHelper
import zipfile
class Client():
    def __init__(self, id, email, drive_config_url, timeout=150):
        self.timeout=timeout
        self.id = id
        self.email = email.strip()
        self.root_path = utils.get_dir('auto_browser')
        self.cookie_load_folder =os.path.join(self.root_path,self.email)
        self.driver = None
        self.cookie_cur_folder = self.cookie_load_folder
        self.drive_config_url=drive_config_url
        self.retries_upload=3
        self.is_stop=False
    def load_config(self):
        dh = DriverHelper()
        zip_file=dh.download_file(self.drive_config_url,ext="zip")
        self.folder_data = zip_file.replace(".zip", "")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.folder_data)
        try:
            os.remove(zip_file)
        except:
            os.system("rm -rf "+zip_file)
            pass
        config_path=os.path.join(self.folder_data,"config.txt")
        with open(config_path,'r') as rb:
            data=json.load(rb)
            self.video_path=os.path.join(self.folder_data,data['video_path'])
            self.title=data['title']
            self.description=data['description']
            self.tag=data['tag']
            self.language=data['language']
            self.country_name=data['country_name']
            self.category=data['category']
            self.thumb_path=os.path.join(self.folder_data,data['thumb_path'])

    def setup(self, root_folder="", version="52",ext=".exe"):
        ff_root_folder = os.getenv('FF_ROOT_FOLDER',root_folder)
        ff_version = os.getenv('FF_VERSION', version)
        ff_ext = os.getenv('FF_EXT', ext)
        firefox_binary = ff_root_folder+"FirefoxSetup"+ff_version+"/core/firefox"+ff_ext
        executable_path = ff_root_folder+"geckodriver_"+ff_version+ff_ext
        mail_server = os.getenv("MAIL_SERVER", config.ServerAdress.MAIL_SERVER)
        email_obj = requests.post(f"{mail_server}/automail/api/mail/get/", json={"gmail": self.email}).json()
        if "gmail" not in email_obj:
            return False
        self.pass_word = email_obj["pass_word"]
        self.reco_email = email_obj["recovery_email"]
        utils.load_cookie(self.cookie_load_folder, self.email)
        profile = webdriver.FirefoxProfile(self.cookie_load_folder)
        set_preference=profile.set_preference
        set_preference("dom.webdriver.enabled", False)
        set_preference("webdriver_enable_native_events", False)
        set_preference("webdriver_assume_untrusted_issuer", False)
        set_preference("media.peerconnection.enabled", False)
        set_preference("media.navigator.permission.disabled", False)
        self.driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=firefox_binary,
                                        executable_path=executable_path)
        self.cookie_cur_folder = self.driver.capabilities.get('moz:profile')
        return True

    def check_login(self):
        self.driver.get("https://www.youtube.com/upload")
        login_page = page.LoginPage(self.driver)
        if login_page.is_login():
            try:
                login_page.change_language()
            except:
                pass
            try:
                login_page.click_next_verify()
            except:
                pass
            try:
                login_page.click_profile_indentifier()
            except:
                pass
            try:
                login_page.email_login = self.email+Keys.RETURN
                self.sleep(3)
            except:
                pass
            try:
                login_page.pass_word_login = self.pass_word+Keys.RETURN
                self.sleep(3)
            except:
                pass
            try:
                login_page.click_cofirm_reco(self.reco_email)
            except:
                pass
            try:
                login_page.click_done_button()
            except:
                pass
            self.sleep(5)
            self.driver.get("https://www.youtube.com/upload")
            login_page = page.LoginPage(self.driver)
            if login_page.is_login():
                print("Login  Fail")
                return False
        return True
    def change_yt_lang(self,hl='en',gl='US'):
        if not self.driver.find_element_by_xpath("//html").get_attribute("lang") == "en":
            self.driver.get(f"https://youtube.com/account?persist_gl=1&gl={gl}&persist_hl=1&hl={hl}")

    def sleep(self,t):
        if self.is_stop:
            return
        time.sleep(t)
    def upload(self):
        upload_page = page.UploadPage(self.driver)
        self.driver.get("https://www.youtube.com/upload?approve_browser_access=1")
        self.sleep(1)
        if not upload_page.is_upload_page():
            self.driver.get("https://www.youtube.com/upload?approve_browser_access=1")
            self.sleep(3)
        if upload_page.is_upload_page():
            if not upload_page.is_avail_upload():
                if(self.retries_upload>0):
                    self.retries_upload=self.retries_upload-1
                    return self.upload()
                else:
                    print("Don't have upload page")
                    Requests.log(self.id, "[Error]Don't have upload page")
                    return
            self.sleep(5)
            upload_page.upload_path_element = self.video_path
            self.sleep(5)
            upload_page.wait_title_input_avail()
            upload_page.set_title_vid(self.title)
            self.sleep(2)
            upload_page.description = self.description
            self.sleep(2)
            upload_page.thumb = self.thumb_path
            self.sleep(2)
            upload_page.click_no_kids_details()
            self.sleep(2)
            upload_page.set_tag_vid(self.tag)
            self.sleep(2)
            upload_page.set_vid_lang(self.language)
            self.sleep(2)
            upload_page.set_vid_loc(self.country_name)
            self.sleep(2)
            upload_page.set_vid_cate(self.category)
            self.sleep(2)
            upload_page.wait_vid_progress()
            video_link = upload_page.video_link
            upload_page.publish()
            print("videoLink: "+video_link)
            Requests.log(self.id, "[Success]Video_link:" + video_link)
        else:
            print("Don't have upload page")
            Requests.log(self.id, "[Error]Don't have upload page")
    def execute(self):
        #load 52 ff
        try:
            Requests.status(self.id, 2)
            self.load_config()
            next = True
            if not self.setup(root_folder=config.Client.ROOT_FOLDER, version="52", ext=config.Client.EXT):
                Requests.log(self.id, "[Error]Can't Init")
                next = False
                return
            if  not self.check_login():
                Requests.log(self.id, "[Error]Login Fail")
                next = False
            if next:
                self.change_yt_lang()
                self.upload()
        except Exception as e:
            Requests.log(self.id, "[Error] Except: "+str(e))
            traceback.print_exc()
            pass
        self.close()
    def start(self):
        self.processx = threading.Thread(target=self.execute)
        self.processx.start()
    def wait(self):
        self.processx.join(self.timeout)
        if self.processx.is_alive():
            Requests.log(self.id, "[Error]Timeout Process")
            self.close()

    def close(self):
        self.is_stop = True
        if self.driver:
            try:
                utils.save_cookie(self.cookie_cur_folder, self.email)
            except:
                traceback.print_exc()
                pass
            try:
                self.driver.close()
            except:
                pass
            try:
                self.driver.quit()
            except:
                pass
            try:
                shutil.rmtree(self.cookie_cur_folder)
            except:
                pass
            try:
                shutil.rmtree(self.cookie_load_folder)
            except:
                pass
            try:
                shutil.rmtree(self.folder_data)
            except:
                pass
            try:
                os.system(f"pkill -f \"{self.cookie_cur_folder}\"")
                os.system(f"rm -rf \"{self.cookie_cur_folder}\"")
            except:
                pass
            self.driver=None





