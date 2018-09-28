from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException
from seleniumYandex import WebmasterTools, get_massive_from_file
import os

# подтверждение всех проверок в /diagnosis/checklist/#recommendation

# массив доменов domains
domains = get_massive_from_file("/home/dev/PycharmProjects/script-yandex/domainsWork.txt")
# domains = ['abakan']

# PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_2)
webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:rozarioflowers.ru:443/"
                                                                    "diagnosis/checklist/#recommendation")
webmasterTools.anti_captcha()

for item in domains:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" + item + ".rozarioflowers.ru:443/"
                                                                    "diagnosis/checklist/#recommendation")

        buttons = webmasterTools.driver.find_elements_by_xpath("//button[./span[contains(text(), 'Проверить')]]")

        if len(buttons) != 1:
            for button in buttons:
                try:
                    button.click()
                except WebDriverException:

                    continue
        else:
            try:
                buttons[0].click()
            except WebDriverException:
                pass
    except:
        webmasterTools.anti_captcha()
    finally:
        print(item + " отправлен")