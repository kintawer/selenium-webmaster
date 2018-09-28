from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException
import codecs
import sys
from seleniumYandex import WebmasterTools, get_massive_from_file


# Указывание региональности

# массив регионов regions
regions = []
f = codecs.open("regions(all).txt", "r", "utf_8_sig")
for line in f:
    regions.append(line.strip())
f.close()

# массив доменов domens
domains = []
f = codecs.open("domains(all).txt", "r", "utf_8_sig")
for line in f:
    domains.append(line.strip())
f.close()

# массив доменов для региональности domens
domensReg = []
f = codecs.open("region_error_1", "r", "utf_8_sig")
for line in f:
    domensReg.append(line.strip())
f.close()

f = codecs.open("resultWork.txt", "a", "utf_8_sig")

PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_1)


code = 'авт. указан'
for item in domensReg:
    try:

        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" + item + ".rozarioflowers.ru:443/dashboard/")

        if "Сводка" in webmasterTools.driver.title:
            webmasterTools.driver.find_element_by_class_name("nav-menu__item-name_of_info").click()  # информация о сайте
            time.sleep(1)
            webmasterTools.driver.find_element_by_class_name("nav-menu__item-name_of_regions").click()  # региональность
            time.sleep(1)

            # регион не указан
            strRegionInfo = webmasterTools.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/div[2]/ul/li").text

            strRegion = regions[domains.index(item)]
            strRegion = strRegion.split(",")[0]  # переменная с названием региона

            if strRegionInfo == "регион сайта не задан" or (strRegion not in strRegionInfo):
                try:
                    webmasterTools.driver.find_element_by_class_name("regions-webmaster__edit-button").click()  # шестеренка вебмастера
                    time.sleep(1)

                    if strRegionInfo == "регион сайта не задан":
                        webmasterTools.driver.find_element_by_class_name("regions-select__add-button").click()  # добавить регион
                        time.sleep(1)

                    # название региона
                    webmasterTools.driver.find_element_by_xpath("(//input[@class='input__control'])[2]").send_keys(strRegion)
                    webmasterTools.driver.find_element_by_xpath("(//input[@class='input__control'])[2]").click()
                    time.sleep(2)
                    webmasterTools.driver.find_element_by_xpath("(//input[@class='input__control'])[2]").send_keys(Keys.ARROW_DOWN, Keys.ENTER)

                    # url контакты
                    webmasterTools.driver.find_element_by_xpath("(//input[@class='input__control'])[3]").send_keys(
                        'https://' + item + '.rozarioflowers.ru/page/contacts')
                    time.sleep(2)

                    # click сохранить
                    webmasterTools.driver.find_element_by_class_name("regions-webmaster__save-button").click()
                    code = 'указан'
                except ElementNotVisibleException:
                    # нет шестеренки
                    code = "заявка"
                    continue
                except WebDriverException:
                    # не кликнул на save
                    code = 'не опр регион'
                    continue
        else:
            # ошибка при заходе на домен
            code = "ошибка"
            f.write(item + ' ошибка\n')
            f.close()
            sys.exit()
    finally:
        print(item + " " + code)
        f.write(item + " " + code + '\n')
        code = 'авт. указан'

f.close()
