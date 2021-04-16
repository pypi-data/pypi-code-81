from time import sleep
from selenium import webdriver
from helper import  send_clicker


# New Group Creator
def group_creator(group_list: list, group_name: str, driver: webdriver, text_dir: str = './group_names.txt'):

    if len(group_list) > 0:
        people_name = group_list
    else:
        try:
            people_name = open(text_dir, "r").read().split("\n")
        except:
            people_name = []
            pass
    triple_dot = driver.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[3]/div/span')
    triple_dot.click()
    sleep(1)

    new_grp = driver.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[3]/span/div/ul/li[1]/div')
    new_grp.click()

    for i in range(0, len(people_name)):
        contact_searcher = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div['
                                                        '1]/span/div/span/div/div/div[1]/div/div/input')
        contact_searcher.click()
        contact_searcher.send_keys(people_name[i])


        contact_clicker = driver.find_element_by_xpath('//span[@title="{}"]'.format(people_name[i]))

        contact_clicker.click()

    next_step = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div/span/div/span')
    next_step.click()

    grp_name = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div/div['
                                            '2]/div/div[2]/div/div[2]')
    grp_name.click()
    grp_name.send_keys(group_name)

    final_creator = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div['
                                                 '1]/span/div/span/div/div/span/div/div/span')
    final_creator.click()
    sleep(3)
    x=1
    while(x==1):
        try:
            exceptional_peeps = driver.find_element_by_xpath('//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]/div/div').click()
            sleep(1)
            exceptional_peeps = driver.find_element_by_xpath('//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div/span/div/span').click()
            sleep(0.5)
        except:
            x=0
            pass
