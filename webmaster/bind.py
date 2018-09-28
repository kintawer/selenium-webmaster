from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import codecs
from seleniumYandex import WebmasterTools, get_massive_from_file

# добавление сайтов на аккаунт из файла input.txt

# массив доменов domens
domens = get_massive_from_file("domains2acc.txt")

PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_1)

code = 'добавлен или уже добавлен'
for item in domens:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/sites/add/")

        webmasterTools.driver.find_element_by_name("hostName").send_keys('https://' + item + '.rozarioflowers.ru')  # url
        time.sleep(1)
        webmasterTools.driver.find_element_by_class_name("one-line-submit__submit").click()  # добавить
        time.sleep(3)

        try:  # поиск ответа с поддоменом
            webmasterTools.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/'
                                                        'form/div[2]/div/div[2]/div[2]/span[2]'
                                                        '/span').click()
            time.sleep(3)
            code = 'добавлен с индексацией'
        except:
            code = 'добавлен или уже добавлен'
    finally:
        print(item + " " + code)
        code = 'добавлен или уже добавлен'
