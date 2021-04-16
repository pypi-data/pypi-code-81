from gtts import gTTS
from time import sleep
from selenium import webdriver


def send_clicker(driver: webdriver):
    # Code to Send Files
    send_media_box = driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
    send_media_box.click()
    sleep(1)


def message_writer(msg: str, select: bool, driver: webdriver):
    if select:
        # Code To send text message
        message_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        message_box.send_keys(msg)

        # Code to CLick Send Button
        message_sender = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button/span')
        message_sender.click()


# Function select the person/group name
def chat_selector(person_name: str, driver: webdriver):
    # Opening New chat Option
    user = driver.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[2]/div/span')
    user.click()

    # Code to Find Element in the Search box
    search_box = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div['
                                              '1]/div/label/div/div[2]')
    search_box.click()
    search_box.send_keys(person_name)
    sleep(0.5)

    # Code to Click the Open first Chat box in Search Results
    opening_chat = driver.find_element_by_xpath('//span[@title="{}"]'.format(person_name))
    opening_chat.click()
    sleep(0.5)


# Text to Audio Converter using gTTs
def txt_to_audio_converter(msg: str, file_name: str, audio_saving_dir: str = './'):
    language = 'en'
    output = gTTS(text=msg, lang=language, slow=False)
    output.save(audio_saving_dir + "/" + file_name + ".mp3")
