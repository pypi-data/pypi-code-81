from os import system, path, makedirs
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import json
import getpass



def createNew():
    filePath = "D:/bookWater"
    fileName = "D:/bookWater/user.json"
    userMessage = {}
    if not path.exists(filePath):
        makedirs(filePath)
    if not path.exists(fileName):
        print("第一次使用要输入相关信息")
        userName = input("输入校园网账号:")
        password = getpass.getpass("输入密码:")
        number = int(input("输入宿舍号(如13401):"))
        userMessage["userName"], userMessage["password"], userMessage["number"] = userName, password, number
        with open(fileName, "w") as fp:
            json.dump(userMessage, fp,indent=4)
        return True
    return False


def hasUserMessage():
    createNew()
    with open("D:/bookWater/user.json", "r") as fp:
        temp = json.load(fp)
        return temp["userName"], temp["password"], temp["number"]


def begin(url):
    userName, password, number = hasUserMessage()
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(userName)
    driver.find_element_by_xpath('//*[@id="casPassword"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[3]/div[4]/div/div/div/div/ul[2]/li[1]/div/div[1]').click()
    sleep(2)
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div/div[5]/button').click()
    sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/form/div/div[1]/div[4]/div[2]/div/div/div[1]/div').click()
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/div/div/ul/li[1]').click()

    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/form/div/div[1]/div[4]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div').click()
    driver.find_element_by_xpath(
        '/html/body/div[3]/div/div/div/ul/li[1]').click()

    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/form/div/div[1]/div[4]/div[2]/div/div/div[3]/div/div[2]/div/div/div/div/div').click()
    sleep(2)
    driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div/ul/li[%d]' % (number/1000)).click()

    driver.find_element_by_xpath('//*[@id="room_number"]').send_keys(number)
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/form/div/div[1]/div[5]/div[2]/div/div[1]/div[2]/div/button').click()
    sleep(2)
    driver.find_element_by_xpath(
        '/html/body/div[6]/div/div[2]/div/div[1]/div[3]/button[2]').click()
    sleep(2)
    driver.find_element_by_xpath(
        '/html/body/div[7]/div/div[2]/div/div[1]/div[2]/div/div[7]/button').click()


def exit():
    system.exit()


def bookWater():
    url = "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/ehall/state/home.html"
    begin(url)


def updateUserName():
    if createNew():
        return
    temp = ""
    userName = input("输入修改后的用户名:")
    with open("D:/bookWater/user.json", "r") as fp:
        temp = json.load(fp)
    temp["userName"] = userName
    with open("D:/bookWater/user.json", "w") as fp:
        json.dump(temp, fp)


def updateNumber():
    if createNew():
        return
    temp = ""
    number = input("输入修改后的宿舍号:")
    with open("D:/bookWater/user.json", "r") as fp:
        temp = json.load(fp)
    temp["number"] = number
    with open("D:/bookWater/user.json", "w") as fp:
        json.dump(temp, fp)


def updatePaswword():
    if createNew():
        return
    temp = ""
    password = getpass.getpass("输入修改后的密码:")
    with open("D:/bookWater/user.json", "r") as fp:
        temp = json.load(fp)
    temp["password"] = password
    with open("D:/bookWater/user.json", "w") as fp:
        json.dump(temp, fp,indent=4)


def main():
    chooseOperators = (exit,bookWater,updateUserName, updatePaswword, updateNumber)
    while True:
        system("cls")
        print("\t\t\t1、订水")
        print("\t\t\t2、修改用户名")
        print("\t\t\t3、修改密码")
        print("\t\t\t4、修改宿舍号")
        print("\t\t\t0、退出")
        choose = int(input("\t\t\t选择:"))
        chooseOperators[choose]()


if __name__ == "__main__":
    main()
