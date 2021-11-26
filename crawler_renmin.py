import urllib.request
import re
from bs4 import BeautifulSoup
import codecs
import csv
import json

data_list = []


# 获取文章详细内容
def get_content(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    cookie = "__jsluid_h=86a123201aaef7d0fba887feeba1e857; wdcid=3643bc4051ff327b; ci_session=s01ahq412c4b5mm3jgf03e7noirqraiu; wdses=2dc90c70610e77f3; wdlast=1637807287"
    headers = {"User-Agent": user_agent, "Cookie": cookie}
    request1 = urllib.request.Request(url, headers=headers)
    response1 = urllib.request.urlopen(request1)
    contents1 = response1.read()
    soup1 = BeautifulSoup(contents1, "html.parser")
    tag = soup1.find('div', {'class': 'd2txt_con clearfix'})
    content_str = tag.get_text()
    # print(tag.get_text())
    # for p_item in tag.find_all('p'):
    #     bef = p_item.get_text()
    #     if len(bef):
    #         content_str = content_str + bef
    return content_str


# 爬虫函数
def gydzf(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    cookie = "__jsluid_h=86a123201aaef7d0fba887feeba1e857; wdcid=3643bc4051ff327b; ci_session=qtsqiu3bs9n7qqp2j6i0geaj4enl8ksp; wdses=2aedb863df0ae120; wdlast=1636340857"
    headers = {"User-Agent": user_agent, "Cookie": cookie}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    contents = response.read()
    soup = BeautifulSoup(contents, "html.parser")
    soupStr = str(soup)
    pos = Index(soupStr, '}')
    soupStr = soupStr[0:pos + 1]
    start = soupStr.find('pages')
    end = soupStr.find('curPage')
    soupStr = soupStr[0:start - 1] + soupStr[end - 1:]
    result = json.loads(soupStr)
    for article in result['list']:
        item = {
            "title": article['title'],
            "inputDate": article['input_date'],
            "articleId": article['article_id'],
            "publishDate": article['publishdate'],
            "publishDep": article['publishdep'],
            "origin": article['origin_name'],
            "content": "",
            "tag": ""
        }
        # 得到所有页面数
        article_url = "http://jhsjk.people.cn/article/"+item['articleId']
        item['content'] = get_content(article_url).replace('\n', ' ').replace('\u3000', ' ')
        data_list.append(item)
        print(item)


# 打包成json文件
def to_json(name):
    filename = "renmintext.json"
    with open(filename, 'w', encoding='utf-8') as file_obj:
        json.dump(name, file_obj, ensure_ascii=False)


# 对获取到的json数据找到 } 最后出现的位置
def Index(str1, c):
    i = 0
    result = 0
    for char in str1:
        if char == c:
            result = i
        i += 1
    return result


# 主函数
if __name__ == '__main__':
    count = 1
    while count <= 63:
        url = 'http://jhsjk.people.cn/testnew/result?keywords=&isFuzzy=0&searchArea=0&year=0&form=706&type=0&page=' + str(count) + '&origin=%E5%85%A8%E9%83%A8&source=2'
        gydzf(url)
        count += 1
    to_json(data_list)