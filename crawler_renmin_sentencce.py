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
    cookie = "__jsluid_h=86a123201aaef7d0fba887feeba1e857; wdcid=3643bc4051ff327b; ci_session=mqe5degqc2kipp6hr1qlku03d82km8ot; wdlast=1637744006; wdses=4f2cb7c0fb420b44"
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
    cookie = "__jsluid_h=86a123201aaef7d0fba887feeba1e857; wdcid=3643bc4051ff327b; ci_session=mqe5degqc2kipp6hr1qlku03d82km8ot; wdlast=1637744006; wdses=4f2cb7c0fb420b44"
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
        # 得到所有页面数
        article_url = "http://jhsjk.people.cn/article/" + article['article_id']
        content = get_content(article_url).replace('\n', ' ').replace('\u3000', ' ')
        content_list = re.split("[，。；：！？]", content)
        print(content_list)
        length = len(content_list)
        # 处理引号
        rule1 = re.compile('^[”].*$')
        rule2 = re.compile('^[“].*$')
        for i in range(0,length):
            content_list[i] = content_list[i].strip()
            if rule1.match(content_list[i]) is not None:
                print(content_list[i])
                content_list[i] = content_list[i][1:].strip()
                print(content_list[i])
            if rule2.match(content_list[i]) is not None:
                count1 = content_list[i].count("“")
                count2 = content_list[i].count("”")
                if count1 == count2 + 1:
                    print(content_list[i])
                    content_list[i] = content_list[i][1:].strip()
                    print(content_list[i])
        print(content_list)
        # 还要添加每个句子的上一句和下一句
        # 第一个出现的句子没有上一句
        firstItem = {
            "title": article['title'],
            "inputDate": article['input_date'],
            "articleId": article['article_id'],
            "publishDate": article['publishdate'],
            "publishDep": article['publishdep'],
            "origin": article['origin_name'],
            "before": "",
            "content": content_list[0].strip(),
            "after": content_list[1].strip(),
            "tag": ""
        }
        data_list.append(firstItem)
        print(firstItem)
        # 在中间的句子同时拥有上一句和下一句
        for j in range(1, length - 1):
            item = {
                "title": article['title'],
                "inputDate": article['input_date'],
                "articleId": article['article_id'],
                "publishDate": article['publishdate'],
                "publishDep": article['publishdep'],
                "origin": article['origin_name'],
                "before": content_list[j - 1].strip(),
                "content": content_list[j].strip(),
                "after": content_list[j + 1].strip(),
                "tag": ""
            }
            data_list.append(item)
            print(item)
        # 在最后的句子没有下一句
        lastItem = {
            "title": article['title'],
            "inputDate": article['input_date'],
            "articleId": article['article_id'],
            "publishDate": article['publishdate'],
            "publishDep": article['publishdep'],
            "origin": article['origin_name'],
            "before": content_list[length - 2].strip(),
            "content": content_list[length - 1].strip(),
            "after": "",
            "tag": ""
        }
        data_list.append(lastItem)
        print(lastItem)


# 打包成json文件
def to_json(name):
    filename = "renmin.json"
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
        url = 'http://jhsjk.people.cn/testnew/result?keywords=&isFuzzy=0&searchArea=0&year=0&form=706&type=0&page=' + str(
            count) + '&origin=%E5%85%A8%E9%83%A8&source=2'
        gydzf(url)
        count += 1
    to_json(data_list)
