import os
import pprint
import requests
from bs4 import BeautifulSoup
import time
from youtubesearchpython import ChannelsSearch
import json
import re
from urllib.parse import unquote
import vk_send

driver, word_status = vk_send.login()


def word_Generator():
    headers = {
        'Host': 'sanstv.ru',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sanstv.ru/randomWord/lang-en/strong-2/count-1/word-%3F%3F%3F%3F%3F%3F',
        'accept-language': 'en-US,en;q=0.9',
    }
    params = (
        ('ajax', '#result'),
        ('lang', 'ru'),
        ('strong', '2'),
        ('count', '1'),
        ('word', '??????'),
    )
    response = requests.get('https://sanstv.ru/randomWord/lang-en/strong-2/count-1/word-%3F%3F%3F%3F%3F%3F',
                            headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html5lib')
    word = soup.get_text()
    return word


def channel_Search():
    cls()
    print('Идет поиск ....')

    if word_status == True:
        word = word_Generator()
    else:
        word = word_status

    channelsSearch = ChannelsSearch(word, limit=50, region='RU')

    for x in range(100):
        try:
            channel_subscribers = str(channelsSearch.result()['result'][x]['subscribers']).replace(' subscribers',
                                                                                                   '').replace(
                ' subscriber', '')
            channel_Link = str(channelsSearch.result()['result'][x]['link'])

            if 'K' in str(channel_subscribers):
                channel_subscribers = int(float((channel_subscribers.replace('K', ''))))
                if channel_subscribers in range(1, 100):
                    urls = contact_link_search(channel_Link)

                    if not urls:
                        print(f"Начальника я нашел этот канал {channel_Link}")
                        print('Начальника  нет вк')

                        f = open('good_channels.txt', 'a')
                        f.write(str(channel_Link) + " : " + str(urls) + '\n')
                        f.close()
                    else:
                        print(f"Начальника я нашел этот канал {channel_Link}")

                        f = open('good_channels.txt', 'a')
                        f.write(str(channel_Link) + " : " + str(urls) + '\n')
                        f.close()
                        p = re.compile(r'https://vk.com/(.*)')
                        for url in urls:
                            match = p.match(url)
                            if match is not None:
                                url = match.group()
                                print('Начальника я нашел ' + url)
                                try:

                                    time.sleep(15)
                                    vk_send.pageHandle(url, driver)

                                except:
                                    pass


            else:
                pass
        except IndexError:
            time.sleep(20)

            print('Начальника я ищу')
            channel_Search()


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def contact_link_search(channel_link):
    response = requests.get(channel_link)
    soup = BeautifulSoup(response.text, "lxml")
    scripts = soup.find_all("script")
    for script in scripts:
        scriptTemplate = re.compile(r'var ytInitialData = {(.*?)}')
        try:
            result = scriptTemplate.match(script.string)
            if result:
                channel_data = str(script)[58:-10]
                channel_json_data = json.loads(channel_data)
                urls = links_getter(channel_json_data)
                res = []
                for i in urls:
                    if i not in res:
                        res.append(i)
                return res
        except:
            pass


def links_getter(channel_json_data):
    urls = []
    links_count = 0
    while True:
        try:
            urls.append(unquote(str(channel_json_data['header']
                                    ['c4TabbedHeaderRenderer']
                                    ['headerLinks']
                                    ['channelHeaderLinksRenderer']
                                    ['secondaryLinks'][links_count]
                                    ['navigationEndpoint']
                                    ['commandMetadata']
                                    ['webCommandMetadata']
                                    ['url']).split('=')[3]))

            links_count = links_count + 1
        except:
            break

    links_count = 0
    while True:
        try:
            urls.append(unquote(str(channel_json_data['header']
                                    ['c4TabbedHeaderRenderer']
                                    ['headerLinks']
                                    ['channelHeaderLinksRenderer']
                                    ['secondaryLinks'][links_count]
                                    ['navigationEndpoint']
                                    ['commandMetadata']
                                    ['webCommandMetadata']
                                    ['url']).split('=')[3]))

            links_count = links_count + 1
        except:
            break
    return urls


channel_Search()
