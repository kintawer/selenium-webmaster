from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from seleniumYandex import WebmasterTools, get_massive_from_file

# переобход доменов по urls из файла domainWork.txt в /indexing/reindex/

## массив доменов domains
domains = get_massive_from_file("domainsWork.txt")
## массив urls
# urls = get_massive_from_file("urlWork.txt")

urls = ["category/korobki-s-tsvetami", "category/shikarnye-bukety", "category/korziny-s-tsvetami",
        "category/101-roza", ""]

# PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_1)

for item in domains:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" + item + ".rozarioflowers.ru:443/"
                                                                                     "indexing/reindex/")

        textBlock = webmasterTools.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]"
                                                                "/div/form/span/span/div/div[3]/div/div/div[2]/div")

        for url in urls:
            webmasterTools.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]/div/"
                                                        "form/span/span/div/div[3]/div/div/div[2]/div/div[3]").click()
            ActionChains(webmasterTools.driver).send_keys(Keys.PAGE_DOWN, "https://" + item + ".rozarioflowers.ru/"
                                                          + url, Keys.ENTER).perform()

        ActionChains(webmasterTools.driver).send_keys(Keys.BACKSPACE).perform()
        webmasterTools.driver.find_element_by_class_name("form__submit").click()
        time.sleep(1)
    except:
        webmasterTools.anti_captcha()
    finally:
        print(item + ' ссылки добавлены')
