from lxml import html
from selenium import webdriver
import json
import time

etree = html.etree
# 记录爬取的数据列表，每天都刷新一次
cdairport_list = []
page_list = []
all_list = []
# 记录每次爬取的数据总数
cdairport_data = 0

pageUrl = ""


# 获取爬取页面源码
def get_html(cdairport_url):
    browser = webdriver.PhantomJS(executable_path='phantomjs.exe')
    browser.get(cdairport_url)
    html_text = browser.page_source
    return html_text


def get_eachPage(cdairport_html):
    cdairport_html = etree.HTML(cdairport_html)
    air_list = cdairport_html.xpath(".//div[@class='history']/ul/li")

    print(air_list)

    for air_item in air_list:
        if len(air_item):
            air_str = str(air_item.xpath("./a/@href")[0])
            if air_str:
                if air_str[0:4] != "http":
                    air_str = "http://jhsjk.people.cn/" + air_str
            page_list.append(air_str)


# 解析html源码页面得到关键数据
def parse_html(cdairport_html):
    cdairport_html = etree.HTML(cdairport_html)
    air_list = cdairport_html.xpath(".//div[@class='word']/p")

    # 标题
    title = cdairport_html.xpath(".//div[@class='title']/h1[@class='big_title']/text()")
    # print(title[1])

    # 时间
    # time = cdairport_html.xpath(".//div[@class='pages-date']/text()")
    # print('time'+time)

    # 合成文章
    air_str = ''
    for air_item in air_list:
        bef = air_item.xpath("./text()")
        if len(bef):
            air_str = air_str + air_item.xpath("./text()")[0]

    item = {
        'title': title[1],
        # 'time': time[0].strip(),
        'content': air_str.strip()
    }
    print(item)
    all_list.append(item)


# 打包成json文件
def to_json(cdairport):
    filename = "dangyuan.json"
    with open(filename, 'w', encoding='utf-8') as file_obj:
        json.dump(cdairport, file_obj, ensure_ascii=False)


if __name__ == '__main__':
    # 爬取网页地址
    base_url = "https://www.12371.cn/special/xxzd/jh/"
    # 每天定时爬取

    # 清空JSON文件
    json_file = open('renmin.json', 'w', encoding='utf-8')
    json_file.truncate()

    # 得到所有页面数
    html = get_html(base_url)
    get_eachPage(html)
    # print(page_list)
    for page_url in page_list:
        html = get_html(page_url)
        parse_html(html)
    # html = get_html(page_list[0])
    # parse_html(html)

    # 输出成json文件
    to_json(all_list)