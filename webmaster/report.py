import time
from seleniumYandex import WebmasterTools, get_massive_from_file

# добавление сайтов на аккаунт из файла input.txt

# массив доменов domains
# domains = get_massive_from_file("domains1acc.txt")
domains = ['abaza']
# PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_1)

webmasterTools.anti_captcha()

for item in domains:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" +
                                  item + ".rozarioflowers.ru:443/indexing/url-tracker/")

        urls = webmasterTools.driver.find_elements_by_class_name("luna-table__row")
        urls.pop(0)
        urls.pop()

        for url in urls:
            source = url.find_element_by_class_name("link_external_yes").text
            code = url.find_element_by_class_name("http-code-status").text
            print("%-35s %-5s" % (source, code))
    finally:
        print()
