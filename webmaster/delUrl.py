from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from seleniumYandex import WebmasterTools
import seleniumYandex
from selenium.common.exceptions import NoSuchElementException

# Удаляем все домены аккаунта
# с i-ой страницы

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_1)

i=2

while i <= 9:
    webmasterTools.driver.get("https://webmaster.yandex.ru/sites/?hostnameFilter=&page=" + str(i))
    time.sleep(0.5)
    urls = webmasterTools.driver.find_elements_by_class_name("sites-item__hostname")
    for item in urls:
        try:
            hover = ActionChains(webmasterTools.driver).move_to_element(item).click(webmasterTools.driver.
                    find_element_by_class_name("button_delete_yes")).pause(0.5)
            hover.perform()

            hover = ActionChains(webmasterTools.driver).click(webmasterTools.driver.find_element_by_class_name(
                "confirm__confirm"))
            hover.perform()
            print(item.text + ' удален')

        except:
            print(item.text + " ошибка")
            continue
    i +=1
