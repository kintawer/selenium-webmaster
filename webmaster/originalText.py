from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from seleniumYandex import WebmasterTools, get_massive_from_file

# добавление оригинальных текстов в domains

## массив доменов domains
domains = get_massive_from_file("domains1acc.txt")

urls = ["category/korobki-s-tsvetami", "category/elitnye-bukety", "category/korziny-s-tsvetami"]

# PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

text = ''

webmasterTools = WebmasterTools(account_1)
time.sleep(20)
f = open('original_text.txt', "r")
lines = f.readlines()
for line in lines:
    text = text + line.strip() + " "
f.close()

for domain in domains:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" + domain + ".rozarioflowers.ru:443/"
                                                                                     "info/original-texts/")
        textBlock = webmasterTools.driver.find_element_by_name("text")
        textBlock.send_keys(text)
        webmasterTools.driver.find_element_by_class_name("button_align_left").click()
        time.sleep(1)
    except:
        print("\033[96m=============================\033[0m")
        time.sleep(30)
    finally:
        print(domain + ' текст добавлен')
