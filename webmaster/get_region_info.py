import time
from seleniumYandex import get_massive_from_file, WebmasterTools

'''
Проверяет почту уведомлений на наличие ошибок при выставлении региона
'''

f = open('region_error_2', 'a')

account_1 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}
account_2 = {'login': 'YOUR_LOGIN', 'passwd': 'YOUR_PASSWORD'}

webmaster_tools = WebmasterTools(account_2)

webmaster_tools.driver.get('https://webmaster.yandex.ru/notifications/1c3dcab0-b374-11e8-a13e-c97e56ade0aa-fb6852b87b7c2589/?critical=false&page=71')
date = webmaster_tools.driver.find_element_by_class_name("message__time").text
while '21.08.2018' not in date:
    date = webmaster_tools.driver.find_element_by_class_name("message__time").text
    button_next = webmaster_tools.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/div[3]/a[2]")

    title = webmaster_tools.driver.find_elements_by_class_name("message__title").pop().text
    if ("Запрос на изменение региона сайта" in title) and ("отклонён" in title):
        # title = title[34:]
        print(title[34:])
        f.write(title[34:] + '\n')
        button_next.click()
    else:
        button_next.click()
    time.sleep(1)