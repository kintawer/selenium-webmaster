from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from seleniumYandex import WebmasterTools, get_massive_from_file

# добавление в важные страницы (url) доменов из файла domain.txt
# с удалением категории (/category/elitnye-bukety)

## массив доменов domains
domains = get_massive_from_file("domainsWork.txt")
# PROXY = "185.5.17.170:21231" # IP:PORT or HOST:PORT

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmasterTools = WebmasterTools(account_2)

# # массив urls
# urls = get_massive_from_file("urlWork.txt")

url = "category/shikarnye-bukety"
flag = 0
webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:rozarioflowers.ru:443/"
                                                                                     "indexing/url-tracker/")
webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:rozarioflowers.ru:443/dashboard/")

time.sleep(20)
for item in domains:
    try:
        webmasterTools.driver.get("https://webmaster.yandex.ru/site/https:" + item + ".rozarioflowers.ru:443/"
                                                                                     "indexing/url-tracker/")

        rows = webmasterTools.driver.find_elements_by_class_name("luna-table__row")[1:]
        for row in rows:
            try:
                if row.find_element_by_class_name('link_external_yes').text == '/category/elitnye-bukety':
                    button = row.find_element_by_class_name('button_delete_yes')
                    button.click()
                    time.sleep(1)
                    webmasterTools.driver.find_element_by_class_name('confirm__confirm').click()
                    time.sleep(1)
                    break
            except:
                continue

        webmasterTools.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/div[1]/div[1]/"
                                                    "form/span/span/div/div[3]/div/div/div[2]/div").click()

        ActionChains(webmasterTools.driver).send_keys(Keys.PAGE_DOWN, "https://" + item + ".rozarioflowers.ru/"
                                                      + url, Keys.ENTER).perform()

        ActionChains(webmasterTools.driver).send_keys(Keys.BACKSPACE).perform()
        webmasterTools.driver.find_element_by_class_name("form__submit_align_left").click()
        time.sleep(2)
    # except:
    #     webmasterTools.anti_captcha()
    except:
        flag = 1
    finally:
        if flag == 0:
            print(item + ' ссылки добавлены в важное')
        else:
            print(item + ' ошибка')
        flag = 0
