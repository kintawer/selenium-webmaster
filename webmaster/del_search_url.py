from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from seleniumYandex import WebmasterTools, get_massive_from_file

# добавление в важные страницы доменов из файла domain.txt без удаления

## массив доменов domains
domains = get_massive_from_file("work2.txt")

# PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_2)

# # массив urls
# urls = get_massive_from_file("urlWork.txt")

urls = ["category/korziny-s-tsvetami/"]

webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:avalon.rozarioflowers.ru:443/"
                                                                             "tools/del-url/")

for item in domains:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" + item + ".rozarioflowers.ru:443/"
                                                                                     "tools/del-url/")

        for url in urls:
            webmasterTools.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]/div/div/div[2]/"
                                                        "div[1]/form/span/span/div/div[3]/div/div/div[2]/div/div"
                                                        "[3]").click()

            ActionChains(webmasterTools.driver).send_keys("https://" + item + ".rozarioflowers.ru/"
                                                          + url).perform()
        time.sleep(2)
        webmasterTools.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div[1]/"
                                                    "form/div[2]/button").click()

    except:
        webmasterTools.anti_captcha()
    finally:
        print(item + ' ссылки добавлены в важное')

