from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import codecs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException
import os


class WebmasterTools:

    def __init__(self, account, proxy_str=None):
        self.account = account
        self.proxy_str = proxy_str
        self.driver = self.auth_webmaster()

    def auth_webmaster(self):
        # аутентификация
        if self.proxy_str is not None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % self.proxy_str)
        else:
            chrome_options = webdriver.ChromeOptions()

        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get("https://webmaster.yandex.ru")  # переход по ссылке
        driver.find_element_by_class_name("button_size_l").click()  # клик по кнопке войти

        driver.find_element_by_name("login").send_keys(self.account.get('login'))  # логин
        driver.find_element_by_name("passwd").send_keys(self.account.get('passwd'), Keys.ENTER)  # пароль

        return driver

    def anti_captcha(self, pause=30):  # еще не тестилось
        """
        Издает звук, и делает паузу на 30 секунд
        :param pause: время паузу
        :return:
        """
        duration = 1  # second
        freq = 740  # Hz
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))

        # время на ввод капчи
        time.sleep(pause)
        # забираем куки с пройденной капчей
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def add_urls(self, domains, path_result="result_add_urls.txt"):
        """
        Добавляет массив доменов на аккаунт
        :param domains: массив доменов, которые необходимо добавить на аккаунт
        :param path_result: путь файла с результатом выполнения функции
        :return:
        """
        f = codecs.open(path_result, "a", "utf_8_sig")
        code = 'добавлен или уже добавлен'
        for item in domains:
            try:
                self.driver.get("https://webmaster.yandex.ru/sites/add/")

                self.driver.find_element_by_name("hostName").send_keys(
                    'https://' + item + '.rozarioflowers.ru')  # url
                time.sleep(1)
                self.driver.find_element_by_class_name("one-line-submit__submit").click()  # добавить
                time.sleep(3)

                try:  # поиск ответа с поддоменом
                    self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/'
                                                                'form/div[2]/div/div[2]/div[2]/span[2]'
                                                                '/span').click()
                    time.sleep(3)
                    code = 'добавлен с индексацией'
                except NoSuchElementException:
                    code = 'добавлен или уже добавлен'
                finally:
                    print("test")
            finally:
                print(item + " " + code)
                f.write(item + " " + code+"\n")
                code = 'добавлен или уже добавлен'
        f.close()

    def delete_urls(self, pages):
        # необходимо протестить
        # удаление всех сайтов с webmaster'a с pages по 1ую страницы
        i = 1
        while i <= pages:
            self.driver.get("https://webmaster.yandex.ru/sites/?hostnameFilter=&page=" + str(pages - i + 1))
            time.sleep(0.5)
            urls = self.driver.find_elements_by_class_name("sites-item__hostname")
            urls = urls.reverse()
            for item in urls:
                try:
                    ActionChains(self.driver).move_to_element(item).click(self.driver.find_element_by_class_name(
                        "button_delete_yes")).pause(0.5).perform()

                    ActionChains(self.driver).click(self.driver.find_element_by_class_name("confirm__confirm")).\
                        perform()
                    print(item.text + ' удален')

                except:
                    print(item.text + " ошибка")
                    continue
            i += 1

    def set_regions(self, domains, regions, path_result="result_regions.txt"):
        """
        Функция задания региональности доменам

        :param domains: домены, которым проставляется региональность
        :param regions: массив всех регионов в алф. порядке по доменам
        :param path_result: путь файла с результатом
        """
        f = codecs.open(path_result, "a", "utf_8_sig")
        code = 'авт. указан'
        for item in domains:
            try:

                self.driver.get("https://webmaster.yandex.ru/site/https:" + item + ".rozarioflowers.ru:443/dashboard/")

                if "Сводка" in self.driver.title:
                    self.driver.find_element_by_class_name(
                        "nav-menu__item-name_of_info").click()  # информация о сайте
                    time.sleep(1)
                    self.driver.find_element_by_class_name(
                        "nav-menu__item-name_of_regions").click()  # региональность
                    time.sleep(1)

                    # регион не указан
                    str_region_info = self.driver.find_element_by_xpath(
                        "/html/body/div[2]/div/div[1]/div/div/div[2]/ul/li").text

                    str_region = regions[domains.index(item)]
                    str_region = str_region.split(",")[0]  # переменная с названием региона

                    if str_region_info == "регион сайта не задан" or (str_region not in str_region_info):
                        try:
                            self.driver.find_element_by_class_name(
                                "regions-webmaster__edit-button").click()  # шестеренка вебмастера
                            time.sleep(1)

                            if str_region_info == "регион сайта не задан":
                                self.driver.find_element_by_class_name(
                                    "regions-select__add-button").click()  # добавить регион
                                time.sleep(1)

                            # название региона
                            self.driver.find_element_by_xpath(
                                "(//input[@class='input__control'])[2]").send_keys(str_region)
                            self.driver.find_element_by_xpath("(//input[@class='input__control'])[2]").click()
                            time.sleep(2)
                            self.driver.find_element_by_xpath(
                                "(//input[@class='input__control'])[2]").send_keys(Keys.ARROW_DOWN, Keys.ENTER)

                            # url контакты
                            self.driver.find_element_by_xpath(
                                "(//input[@class='input__control'])[3]").send_keys(
                                'https://' + item + '.rozarioflowers.ru/page/contacts')
                            time.sleep(2)

                            # click сохранить
                            self.driver.find_element_by_class_name("regions-webmaster__save-button").click()
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
                    code = "сайт не привязан к аккаунту"
            finally:
                print(item + " " + code)
                f.write(item + " " + code + '\n')
                code = 'авт. указан'
        f.close()

def get_massive_from_file(path):
    # возврат массива из файла
    massive = []
    f = codecs.open(path, "r", "utf_8_sig")
    for line in f:
        massive.append(line.strip())
    f.close()
    return massive
