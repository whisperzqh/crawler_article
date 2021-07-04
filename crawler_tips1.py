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
    air_list = cdairport_html.xpath(".//div[@id='endtext']/p/text()")

    for air_item in air_list:
        if str(air_item[0]) == '【':
            continue

        item = {
            'content': air_item
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
    base_url = "http://m.yipinjuzi.com/yangsheng/2020-02-19/27808.html"

    # 清空JSON文件
    json_file = open('cdairport.json', 'w', encoding='utf-8')
    json_file.truncate()

    # 解析页面
    html = get_html(base_url)
    parse_html(html)


    # 输出成json文件
    to_json(all_list)
    print("OK")
