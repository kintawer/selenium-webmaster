from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from seleniumYandex import WebmasterTools, get_massive_from_file


# Записываем все домены аккаунта
# в файл domains1acc.txt
# с количеством страниц pages

pages = 32

f = open("domains2accTest.txt", "w")

# PROXY = "78.138.142.198:53281" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_2)

for i in range(pages):
    webmasterTools.driver.get("https://webmaster.yandex.ru/sites/?hostnameFilter=&page=" + str(i+1))
    time.sleep(1)
    urls = webmasterTools.driver.find_elements_by_class_name("sites-item__hostname")
    for item in urls:
        domen = item.text
        domen = str(domen).replace('https://', '')
        domen = domen.replace('.rozarioflowers.ru', '')
        f.write(domen + '\n')
f.close()

