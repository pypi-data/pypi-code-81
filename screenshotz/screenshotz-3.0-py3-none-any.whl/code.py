import pickle
from pathlib import Path

from PIL import Image
from selenium import webdriver


class Screenshotter(object):
    def __init__(
        self,
        base_url,
        cookies_file_path,
    ):
        self.cookies_file_path = cookies_file_path
        self.base_url = base_url
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=chrome_options)

        if Path(self.cookies_file_path).exists():
            cookies = pickle.load(open(self.cookies_file_path, "rb"))

            self.driver.get(self.base_url)

            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        else:
            print("No cookies file present - no cookies loaded.")

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(self.cookies_file_path, "wb"))

    def close_all(self):
        # close all open tabs
        if len(self.driver.window_handles) < 1:
            return
        for window_handle in self.driver.window_handles[:]:
            self.driver.switch_to.window(window_handle)
            self.driver.close()

    def do_shot(self, filename):
        d = Path("screenshots")
        d.mkdir(exist_ok=True)
        self.driver.save_screenshot(str(d / filename))

    def quit(self):
        self.save_cookies()
        self.close_all()
        self.driver.quit()


def crop(in_name, out_name, top, bottom, left, right):
    img = Image.open(in_name)
    width, height = img.size

    # crop
    # 10 pixels from the left
    # 20 pixels from the top
    # 30 pixels from the right
    # 40 pixels from the bottom

    cropped = img.crop((left, top, width - right, height - bottom))
    cropped.save(out_name)


# if __name__ == '__main__':
#     selenium_object = SeleniumDriver()
#     driver = selenium_object.driver

#     if is_logged_in(driver):
#         print("Already logged in")
#     else:
#         print("Not logged in. Please log in.")

#     sleep(120)

#     selenium_object.quit()
