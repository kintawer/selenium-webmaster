import json
import requests
from dateutil import parser


class Data:

    OAUTH_TOKEN = 'YOUR_TOKEN'
    AUTH_HEADER = {
        'Authorization': 'OAuth %s' % OAUTH_TOKEN
    }

    SESSION = requests.Session()
    SESSION.headers.update(AUTH_HEADER)

    API_VERSION = 'v3.1'
    API_BASE_URL = 'https://api.webmaster.yandex.net'
    API_URL = API_BASE_URL + '/' + API_VERSION

    def __init__(self):

        self.user_id = self.get_user_id()

        self.domains = []
        with open('domains1acc.txt', "r") as f:
            for line in f:
                self.domains.append(line.strip())

    def get_user_id(self):
        r = self.SESSION.get(self.API_URL + '/user/')
        c = json.loads(r.text)

        return c['user_id']


    def parse(self):

        for domain in self.domains:
            # f.write(domain + ':' + '\n')
            host_id = "https:" + domain + ".rozarioflowers.ru:443"

            # Инфа о количестве ошибок
            path = '/user/' + str(self.user_id) + '/hosts/' + host_id + '/summary/'
            response = self.SESSION.get(self.API_URL + path)
            content = json.loads(response.text)
            problems = ['FATAL', 'CRITICAL', 'POSSIBLE_PROBLEM', 'RECOMMENDATION']
            for problem in problems:
                # Название пробемы problem, количество проблем count
                try:
                    site_problems = content['site_problems']
                    count = site_problems[problem]
                except:
                    count = 0
                finally:
                    print(problem + ' ' + str(count))

            # Инфа по sitemap (last_access_date = последняя дата проверки)
            path = '/user/' + str(self.user_id) + '/hosts/' + host_id + '/sitemaps/'
            response = self.SESSION.get(self.API_URL + path)
            content = json.loads(response.text)
            for sitemap in content['sitemaps']:
                if sitemap['sitemap_url'] == 'https://' + domain + '.rozarioflowers.ru/sitemap.xml':
                    last_access_date = sitemap['last_access_date']
                    last_access_date = parser.parse(last_access_date)
                    last_access_date = last_access_date.strftime("%Y-%m-%d")
                    print("Последняя дата проверки sitemap: " + last_access_date)
                    break

            # Инфа по страницам, находящихся в поиске (дата и количество страниц)
            host_id = "https:" + domain + ".rozarioflowers.ru:443"
            path = '/user/' + str(self.user_id) + "/hosts/" + host_id + "/indexing-history/?indexing_indicator=SEARCHABLE"
            response = self.SESSION.get(self.API_URL + path)
            content = json.loads(response.text)
            position = len(content['indicators']['SEARCHABLE']) - 1
            info = content['indicators']['SEARCHABLE'][position]
            date = info['date']
            value = info['value']
            print("%-30s%4d%15s" % (domain, value, date[:10]))
