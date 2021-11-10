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
    cookie = "dcid=309752492b3944a6; uid=a53491f240a74a0092f444151669bac7; wdlast=1635924740"
    headers = {"User-Agent": user_agent, "Cookie": cookie}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    contents = response.read()
    soup = BeautifulSoup(contents, "html.parser")
    soupStr = str(soup)
    pos1 = Index(soupStr, '(')
    pos2 = Index(soupStr, ')')
    soupStr = soupStr[pos1+1:pos2]
    result = json.loads(soupStr)
    for article in result['data']['list']:
        item = {
            "title": article['Title'],
            "pubTime": article['PubTime'],
            "linkUrl": article['LinkUrl'],
            "content": "",
            "tag": ""
        }
        # 得到所有页面数
        article_url = item['linkUrl']
        print(article_url)
        item['content'] = get_content(article_url).replace('\n', ' ').replace('\u3000', ' ')
        data_list.append(item)
        print(item)


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
        url = 'http://qc.wa.news.cn/nodeart/list?nid=11164946&pgnum='+str(count)+'&cnt=20&attr=&tp=1&orderby=1&callback=jQuery112403709401163040411_1635928193289&_=163592819329'+str(count-1)
        gydzf(url)
        count += 1
    to_json(data_list)
