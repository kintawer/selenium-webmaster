from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from seleniumYandex import WebmasterTools, get_massive_from_file
import os

# переобход файла sitemap.xml в /indexing/sitemap/

# массив доменов domains
domains = get_massive_from_file("domainsWork.txt")

# PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_1)
webmasterTools.driver.get('https://webmaster.yandex.ru/site/https:rozarioflowers.ru:443/indexing/sitemap/')
webmasterTools.anti_captcha()
code = 1
for item in domains:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" + item + ".rozarioflowers.ru:443/"
                                                                                     "indexing/sitemap/")

        urls = webmasterTools.driver.find_elements_by_class_name("sitemap-item__recrawl")

        if len(urls) != 1:
            for url in urls:
                try:
                    url.click()
                except:
                    webmasterTools.anti_captcha()
                    continue

        else:
            try:
                urls[0].click()
            except:
                webmasterTools.anti_captcha()
                urls[0].click()

        # webmasterTools.driver.find_element_by_name("sitemapUrl").send_keys(
        #     "https://"+item+".rozarioflowers.ru/sitemap.xml")
        #
        # webmasterTools.driver.find_element_by_class_name("one-line-submit__submit").click()
        time.sleep(1)
    except:
        webmasterTools.anti_captcha()
        print(item + " капча")
        continue
    finally:
        print(item + " отправлен")