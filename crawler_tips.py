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
    # print("1")
    global browser
    browser = webdriver.PhantomJS(executable_path='phantomjs.exe')
    browser.get(cdairport_url)
    # print("2")
    html_text = browser.page_source
    # print(html_text)
    return html_text


# 解析html源码页面得到关键数据
def parse_html(cdairport_html):
    cdairport_html = etree.HTML(cdairport_html)
    air_list = cdairport_html.xpath(".//div[@class='news_txt']/text()")

    for air_item in air_list:
        tip_str = str(air_item)
        if tip_str and (tip_str[0] == '1' or tip_str[0] == '2' or tip_str[0] == '3' or tip_str[0] == '4' or tip_str[0] == '5' or tip_str[0] == '6' or tip_str[0] == '7' or tip_str[0] == '8' or tip_str[0] == '9'):
            item = {
                'istitle': False,
                'content': tip_str
            }
            print(item)
            all_list.append(item)
        if tip_str and tip_str[-1] == '！' and len(tip_str)<=15:
            item = {
                'istitle': True,
                'content': tip_str
            }
            print(item)
            all_list.append(item)



# 打包成json文件
def to_json(cdairport):
    filename = "cdairport.json"
    with open(filename, 'w', encoding='utf-8') as file_obj:
        json.dump(cdairport, file_obj, ensure_ascii=False)


if __name__ == '__main__':
    # 爬取网页地址
    base_url = "https://www.thepaper.cn/newsDetail_forward_10768667"

    # 清空JSON文件
    json_file = open('cdairport.json', 'w', encoding='utf-8')
    json_file.truncate()

    # 解析页面
    html = get_html(base_url)
    parse_html(html)

    # for cdairport_item in cdairport_list:
        # print(cdairport_item)
        # url = base_url + cdairport_item['pageUrl'][0]
        # print(url)
        # html = get_html(url)
        # all_list.append(cdairport_item['标题'][0])
        # parse_page(html)

        # print(url)
        # 解析每一个页


    # 输出成json文件
    to_json(all_list)
    print("OK")
