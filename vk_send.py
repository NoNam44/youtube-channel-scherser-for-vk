import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import VK_TAGS
import time
import os
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
seleniumLogger.setLevel(logging.WARNING)


def info():
    print('         Поиск каналов v 1.0')
    print('_____________________________________\n')
    print('програма была сделана для бесплатного использования \nесли ты купил ее то ты лох :(')
    print()
    print('Создатель : vk.com/happyn4ss')
    print('_____________________________________')



def user_profile():

    if os.path.isfile('profile.txt'):
        with open('profile.txt', 'r') as profile:
            accounts = profile.readlines()

        while True:
            if os.path.isfile('profile.txt'):
                with open('profile.txt', 'r') as profile:
                    accounts = profile.readlines()
            try:
                cls()
                info()
                accountDisplay(accounts)
                ac_index = int(input('Какой аккаунт использовать? если создать новый напиши 0: '))
                if ac_index == 0:
                    create_profile()
                else:


                    ac_index = ac_index - 1
                    account = str(accounts[ac_index]).split(':')

                    print('Рандомное слово или свое? для выбора рандомного слова види цифру 0 если хочеш свое напиши свое')
                    word = input('СЛОВО: ')
                    try:
                        if word == '0':
                            return account, True
                        else:
                            return account, word
                        break
                    except:
                        pass
            except:
                    print('Неправильный номер аккаунта')

    else:

        accounts = create_profile()
        if os.path.isfile('profile.txt'):
            with open('profile.txt', 'r') as profile:
                accounts = profile.readlines()
        while True:
            try:
                cls()
                accountDisplay(accounts)
                ac_index = int(input('Какой аккаунт использовать? : '))
                ac_index = ac_index - 1
                account = str(accounts[ac_index]).split(':')

                print('Рандомное слово или свое? для выбора рандомного слова види цифру 0 если хочеш свое напиши свое')
                word = input('СЛОВО: ')
                try:
                    if word == '0':
                        return account, True
                    else:
                        return account, word
                    break
                except:
                    pass
            except:
                print('Неправильный номер аккаунта')




def accountDisplay(accounts):

    counter= 1
    for ac in accounts:
        ac.replace("\n","")
        print(f'{counter}. {ac}' )
        counter = counter + 1


def create_profile():
    cls()
    info()
    print('\nСоздать новый аккаунт')
    print('-------------------------------------')

    try:
        account = []
        username = str(input('Логин: '))
        u_password = str(input('Пароль: '))

        profile = open('profile.txt', 'a')
        profile.write((username + ':' + u_password+'\n'))
        profile.close()



        while True:
                print('---')
                add = (input('Добавить еще один аккаунт? \nда/нет : ')).lower()
                try:
                    if add == 'да':
                        create_profile()
                        break
                    elif add == 'нет':
                        break
                    else:
                        print('Там же сука русскими буквами написано да или нет ')
                except:
                    pass
    except:
        print('что то не так :(')
        print("у тебя логин или пароль на русском")

    return account


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def webDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    return driver


def login():
    driver = webDriver()
    accountData, word = user_profile()
    driver.get("https://vk.com/login")
    # EMAIL    
    MONTH_TAG_element = driver.find_element_by_xpath(VK_TAGS.EMAIL_TAG)
    MONTH_TAG_element.click()
    MONTH_TAG_element.send_keys(accountData[0])

    # PASSWORD
    PASSWORD_element = driver.find_element_by_xpath(VK_TAGS.PASSWORD_TAG)
    PASSWORD_element.click()
    PASSWORD_element.send_keys(accountData[1])

    # LOGIN
    try:
        LOGIN_element = driver.find_element_by_xpath(VK_TAGS.LOGIN_IN_TAG)
        LOGIN_element.click()
    except:
        pass
    return driver,word


def pageHandle(vk_link, driver):
    time.sleep(2)
    driver.get(vk_link)
    time.sleep(2)
    try:
        SEND_MESSAGE_PAGE(driver)
    except:
        try:
            SEND_ADD_FRIEND_MESSAGE(driver)
        except:
            SEND_GROUP_MESSAGE(driver)
    return driver


def SEND_MESSAGE_PAGE(driver):
    # SEND MASSAGE
    SEND_MESSAGE_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, VK_TAGS.SEND_MESSAGE)))
    SEND_MESSAGE_element.click()
    time.sleep(2)

    SEND_MESSAGE_BOX_element = driver.find_element_by_xpath(VK_TAGS.SEND_MESSAGE_BOX)
    SEND_MESSAGE_BOX_element.send_keys(VK_TAGS.MESSAGE_TYPE)
    time.sleep(2)

    SEND_MESSAGE_BOX_element = driver.find_element_by_xpath(VK_TAGS.SEND_BUTTOM_MESSAGE)
    SEND_MESSAGE_BOX_element.click()
    time.sleep(2)


def SEND_ADD_FRIEND_MESSAGE(driver):
    MONTH_TAG_element = driver.find_element_by_xpath(VK_TAGS.ADD_TO_FREIND)
    MONTH_TAG_element.click()
    time.sleep(2)

    MONTH_TAG_element = driver.find_element_by_xpath(VK_TAGS.SEND_MESSAGE_MENU)
    MONTH_TAG_element.click()
    time.sleep(2)

    MONTH_TAG_element = driver.find_element_by_xpath(VK_TAGS.SEND_MESSAGE2)
    MONTH_TAG_element.click()
    MONTH_TAG_element.send_keys(VK_TAGS.MESSAGE_TYPE)
    time.sleep(2)

    MONTH_TAG_element = driver.find_element_by_xpath(VK_TAGS.SEND_MESSAGE2_BOX)
    MONTH_TAG_element.click()
    MONTH_TAG_element.send_keys(VK_TAGS.MESSAGE_TYPE)
    time.sleep(2)

    MONTH_TAG_element = driver.find_element_by_xpath(VK_TAGS.SEND_BUTTOM_MESSAGE2)
    MONTH_TAG_element.click()
    time.sleep(2)


def SEND_GROUP_MESSAGE(driver):
    time.sleep(2)
    # SEND GROUP MASSAGE
    driver.find_element_by_xpath(VK_TAGS.GROUP_SEND_MESSAGE).click()

    time.sleep(2)

    SEND_MESSAGE_BOX_element = driver.find_element_by_xpath(VK_TAGS.GROUP_SEND_MESSAGE_BOX)
    SEND_MESSAGE_BOX_element.send_keys(VK_TAGS.MESSAGE_TYPE)
    time.sleep(2)

    SEND_MESSAGE_BOX_element = driver.find_element_by_xpath(VK_TAGS.GROUP_SEND_MESSAGE_BUTTOM)
    SEND_MESSAGE_BOX_element.click()
    time.sleep(2)
