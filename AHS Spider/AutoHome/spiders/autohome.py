import re
import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from AutoHome.items import AutohomeItem
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--proxy-server=http://127.0.0.1:8080')


class AutohomeSpider(scrapy.Spider):
    name = 'autohome'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/config/spec/38695.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/43097.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/36000.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/40000.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/42000.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/28000.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/48000.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/30001.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/32001.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/10001.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/14001.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/16001.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/34001.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/38001.html#pvareaid=3454541',
                  'https://car.autohome.com.cn/config/spec/22001.html#pvareaid=3454541']

    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        super().__init__()

    def start_requests(self):
        with open('C:/Users/cq/Desktop/mess/vscode/Py/Scrapy/AutoHome/urls.txt', 'r') as f:
            for i in f.readlines():
                # time.sleep()
                response = scrapy.Request(i, callback=self.parse)
                yield response
        # for i in range(len(self.start_urls)):
        #     response = scrapy.Request(self.start_urls[i], callback=self.parse)
        #     yield response

    def close(self, spider):
        self.browser.quit()

    def parse(self, response):
        # 读取网页内容
        html = response.text

        # 存储映射表
        flag = -1
        confusions_baike = {}
        confusions_config = {}
        confusions_option = {}
        for index, string in re.compile(r'\[(\w+)]-&gt;{([\u4e00-\u9fa5]+)+}').findall(html):
            if index == '0':
                flag += 1
            if flag == 0:
                confusions_baike[index] = string
            elif flag == 1:
                confusions_config[index] = string
            else:
                confusions_option[index] = string

        # 查找该次爬取的class后缀
        suffix_baike = re.compile(r'''hs_kw[0-9]+_baike(\w+)''', re.IGNORECASE).search(html).groups()[0]
        suffix_config = re.compile(r'''hs_kw[0-9]+_config(\w+)''', re.IGNORECASE).search(html).groups()[0]
        suffix_option = re.compile(r'''hs_kw[0-9]+_option(\w+)''', re.IGNORECASE).search(html).groups()[0]

        # 根据映射表替换::before伪元素
        for key, value in confusions_baike.items():
            html = html.replace(r'''<span class="hs_kw{}_baike{}"></span>'''.format(key, suffix_baike), value)

        for key, value in confusions_config.items():
            html = html.replace(r'''<span class="hs_kw{}_config{}"></span>'''.format(key, suffix_config), value)

        for key, value in confusions_option.items():
            html = html.replace(r'''<span class="hs_kw{}_option{}"></span>'''.format(key, suffix_option), value)

        # 初始化
        item = AutohomeItem()
        soup = BeautifulSoup(html, 'html5lib')

        # 提取系列
        series = soup.find('div', class_='path').find_all('a')[3].string
        item.data['系列'] = str(series)
        #
        # 提取车型
        carbox = soup.find('div', class_='carbox').a.string
        item.data['车型'] = str(carbox)

        # 提取其他信息
        table_total_item = soup.find_all('table', class_='tbcs')[1:]
        for table_item in table_total_item[:-1]:
            for tr_item in table_item.find_all('tr'):
                th_item, td_item = tr_item.find('th'), tr_item.find('td')
                td_content = ''
                if td_item is not None:
                    if td_item.a is not None:
                        td_content = td_item.a.string
                    [s.extract() for s in td_item("a")]
                    [s.extract() for s in td_item("a")]
                    if td_item.string is not None:
                        td_content = td_item.string
                    if td_content is None:
                        td_content = '-'
                    elif td_content == '':
                        td_content = '-'
                    item.data[str(th_item.string)] = str(td_content)
                    # item.data['th_item.string'] = 'td_content'
        print(response.url)
        print(item.data)
        # print(len(item.data))
        # 返回数据
        yield item
        # for i, j in item.data.items():
        #     print(i + ': ' + j)
        # print(soup.prettify())
