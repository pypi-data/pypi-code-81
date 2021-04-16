from selenium import webdriver
from time import sleep
from helper import txt_to_audio_converter, message_writer, send_clicker, chat_selector


# Function to send "all media" only When needed
def document_sender(name: list, files: list, file_dir: str, driver: webdriver, select: bool = True):
    if select:
        for j in range(len(name)):
            chat_selector(name[j], driver)
            for i in files:
                attachment_box = driver.find_element_by_xpath('//div[@title="Attach"]')
                attachment_box.click()
                image_box = driver.find_element_by_xpath(
                    '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[3]/button/input')
                image_box.send_keys(file_dir + "/" + i)
                sleep(1)
                send_clicker(driver)


# Function to send "all media" only When needed
def image_sender(name: list, files: list, file_dir: str, driver: webdriver, select: bool = True):
    if select:
        for j in range(len(name)):
            chat_selector(name[j], driver)
            for i in range(len(files)):
                attachment_box = driver.find_element_by_xpath('//div[@title="Attach"]')
                attachment_box.click()
                image_box = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,'
                                                         'video/quicktime"]')
                image_box.send_keys(file_dir + "/" + files[i])
                sleep(1)
                send_clicker(driver)


def text_sender(name: list, msg: str, driver: webdriver, select: bool = True):
    for j in range(len(name)):
        chat_selector(name[j], driver)
        message_writer(msg, select=select, driver=driver)
        sleep(1)


# Function to Send Audio only When needed
def audio_sender(name: list, msg: str, file_name: str, driver: webdriver, file_dir: str, select: bool = True):
    if select:
        txt_to_audio_converter(msg=msg, file_name=file_name, audio_saving_dir=file_dir)
        for j in range(len(name)):
            chat_selector(name[j], driver)
            attachment_box = driver.find_element_by_xpath('//div[@title="Attach"]')
            attachment_box.click()
            image_box = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,'
                                                     'video/quicktime"]')
            image_box.send_keys(file_dir + "/" + file_name + ".mp3")
            sleep(1)
            # Code to Send Media Files
            send_media_box = driver.find_element_by_xpath(
                '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div/span')
            send_media_box.click()
        sleep(1)
