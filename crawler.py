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
    browser = webdriver.PhantomJS(executable_path='phantomjs.exe')
    browser.get(cdairport_url)
    # print("2")
    html_text = browser.page_source
    # print(html_text)
    return html_text


# 解析html源码页面得到关键数据
def parse_html(cdairport_html):
    cdairport_html = etree.HTML(cdairport_html)
    air_list = cdairport_html.xpath("//div[@class='container--wrap bg-navy-4 table-container col hide-mobile' and position()>1]")

    for air_item in air_list:
        item = {
            'pageUrl': air_item.xpath(".//div[@class='sorted-table__header']//a[@class='header-link']/@href"),
            '标题': air_item.xpath(".//div[@class='sorted-table__header']//a[@class='header-link']/text()"),
        }
        # all_list.append(item['标题'][0])
        table_list = air_item.xpath(".//table[@id='sortable_table_world']")
        # table_list = air_item.xpath(".//div[@class='dataTables_scrollBody']")

        for table_item in table_list:
            td_list = len(table_item.xpath(".//tr[position()>2]"))+1
            for i in range(td_list):
                confirmed_len = len(table_item.xpath(".//tr[@class='odd' or 'even']/td[2]//span"))
                confirmed = str(table_item.xpath(".//tr[@class='odd' or 'even']/td[2]//span[1]/text()")[i+1]).strip()
                if confirmed_len == 2:
                    confirmed = confirmed + str(table_item.xpath(".//tr[@class='odd' or 'even']/td[2]//span[2]/text()")[i+1]).strip()
                span_len = len(table_item.xpath(".//tr[@class='odd' or 'even']/td[4]//span"))
                deceased = str(table_item.xpath(".//tr[@class='odd' or 'even']/td[4]//span[1]/text()")[i+1]).strip()
                if span_len == 2:
                    deceased = deceased + str(table_item.xpath(".//tr[@class='odd' or 'even']/td[4]//span[2]/text()")[i+1]).strip()
                item = {
                    "name": str(table_item.xpath(".//tr[@class='odd' or 'even']/td[1]//span[2]/text()")[i]).strip(),
                    "Confirmed":
                        confirmed,
                    "Per Million1":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[3]/text()")[i+1]).strip(),
                    "Deceased":
                        deceased,
                    "Per Million2":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[5]/text()")[i+1]).strip(),
                    "Tests":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[6]//span[1]/text()")[i+1]).strip(),
                    "Active":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[7]/text()")[i+1]).strip(),
                    "Recovered":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[8]//span[1]/text()")[i+1]).strip(),
                    "Per Million3":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[9]/text()")[i+1]).strip(),
                    "Vaccinated":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[10]/text()")[i+1]).strip(),
                    "Population":
                        str(table_item.xpath(".//tr[@class='odd' or 'even']/td[11]/text()")[i+1]).strip(),
                    }
                print(item)
                all_list.append(item)

        # print(item)
        # cdairport_list.append(item)
    # print(cdairport_list)



# 打包成json文件
def to_json(cdairport):
    filename = "cdairport.json"
    with open(filename, 'w', encoding='utf-8') as file_obj:
        json.dump(cdairport, file_obj, ensure_ascii=False)


if __name__ == '__main__':
    # 爬取网页地址
    base_url = "https://ncov2019.live/data"
    # 每天定时爬取

    # 清空JSON文件
    json_file = open('cdairport.json', 'w', encoding='utf-8')
    json_file.truncate()
    # 初始化爬取记录总数
    cdairport_data = 0

    # 得到所有页面数
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
    print("\n" + "爬取完成！本次共爬取数据数为：" + str(cdairport_data))
        # 每天定时爬取
        # time.sleep(86400)
