import re
import urllib.request

import bs4
from bs4 import BeautifulSoup
import json

data_list = []


# 获取文章详细内容
def get_content(url):
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    # cookie = "dcid=309752492b3944a6; uid=a53491f240a74a0092f444151669bac7; wdlast=1635924740"
    # headers = {"User-Agent": user_agent, "Cookie": cookie}
    request1 = urllib.request.Request(url)
    response1 = urllib.request.urlopen(request1)
    contents1 = response1.read()

    soup1 = BeautifulSoup(contents1, "html.parser")
    # print(soup1)
    tag = soup1.find('div', {'class': 'main-aticle'})
    if not isinstance(tag, bs4.element.Tag):
        tag = soup1.find('div', {'id': 'detail'})
    if not isinstance(tag, bs4.element.Tag):
        tag = soup1.find('div', {'id': 'contentMain'})
    content_str = tag.get_text()
    # for p_item in tag.find_all('p'):
    #     bef = p_item.get_text()
    #     if len(bef):
    #         content_str = content_str + bef
    return content_str


# 爬虫函数
def gydzf(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    cookie = "wdcid=309752492b3944a6; uid=a53491f240a74a0092f444151669bac7; fingerprint=9f5a71dd617f477d6a3a9862ab1e6dee; bfdid=87205254007bf95200000c1b0030c44261824cc5; bfd_g=87205254007bf95200000c1b0030c44261824cc5; tma=182794287.9250952.1635931073471.1635994355038.1636102454761.3; tmd=5.182794287.9250952.1635931073471.; wdlast=1637805389"
    headers = {"User-Agent": user_agent, "Cookie": cookie}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    contents = response.read()
    soup = BeautifulSoup(contents, "html.parser")
    soupStr = str(soup)
    pos1 = Index(soupStr, '(')
    pos2 = Index(soupStr, ')')
    soupStr = soupStr[pos1 + 1:pos2]
    result = json.loads(soupStr)
    for article in result['data']['list']:
        # 得到所有页面数
        article_url = article['LinkUrl']
        print(article_url)
        content = get_content(article_url).replace('\n', ' ').replace('\u3000', ' ')
        content_list = re.split("[，。；：！？]", content)
        print(content_list)
        length = len(content_list)
        # 处理引号
        rule1 = re.compile('^[”].*$')
        rule2 = re.compile('^[“].*$')
        for i in range(0, length):
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
            "title": article['Title'],
            "pubTime": article['PubTime'],
            "linkUrl": article['LinkUrl'],
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
                "title": article['Title'],
                "pubTime": article['PubTime'],
                "linkUrl": article['LinkUrl'],
                "before": content_list[j - 1].strip(),
                "content": content_list[j].strip(),
                "after": content_list[j + 1].strip(),
                "tag": ""
            }
            data_list.append(item)
            print(item)
            # 在最后的句子没有下一句
        lastItem = {
            "title": article['Title'],
            "pubTime": article['PubTime'],
            "linkUrl": article['LinkUrl'],
            "before": content_list[length - 2].strip(),
            "content": content_list[length - 1].strip(),
            "after": "",
            "tag": ""
        }
        data_list.append(lastItem)
        print(lastItem)


# 打包成json文件
def to_json(name):
    filename = "xinhua.json"
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
    while count <= 7:
        url = 'http://qc.wa.news.cn/nodeart/list?nid=11164946&pgnum=' + str(
            count) + '&cnt=20&attr=&tp=1&orderby=1&callback=jQuery112403709401163040411_1635928193289&_=163592819329' + str(
            count - 1)
        gydzf(url)
        count += 1
    to_json(data_list)
