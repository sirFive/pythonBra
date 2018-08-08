# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import codecs

#获取每条链接的内容
def getnewsdetail(newsUrl):
    #http://dangjian.gmw.cn/2018-07/28/content_30136870.htm
    result = {}
    res = requests.get(newsUrl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    ##获取标题
    title = soup.find(id='articleTitle').string
    title = title.strip()  # 去掉标题前后的空格
    #print(title)
    result['title'] = title

    ##获取时间
    time = soup.find(id='pubTime').string
    #print(time)
    result['time'] = time

    ##获取文章内容
    article = []
    for p in soup.select('#contentMain p')[:-1]:
        article.append(p.text.strip())
    content = ' '.join(article)  ##可以去掉由于数组引起多出的[]和‘’
    #print(content)
    result['content'] = content

    return result

#获取单页的所有新闻链接地址
def getliks(linksUrl):
    #http://dangjian.gmw.cn/node_11940.htm
    links = []
    res = requests.get(linksUrl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    for newshref in soup.select('.channel-newsGroup a')[:-1]:
        links.append(newshref['href'])   #获取a标签中的href内容
    return links

#一页的所有内容
def onePage(pageUrl):
    links = getliks(pageUrl) #单页的所有链接
    linksNew = []
    for link in links:  # 有些链接没有 http://news.gmw.cn/  这个前缀，要加上
        if (link.find('http')) < 0:
            addHttpLink = 'http://dangjian.gmw.cn/' + link
            linksNew.append(addHttpLink)
        else:
            linksNew.append(link)
    oneListResult = []  # 某一页的所有内容
    for url in linksNew:
        print(url)
        result1 = getnewsdetail(url)
        oneListResult.append(result1)
    return oneListResult
if __name__ == '__main__':
    pageUrl = 'http://dangjian.gmw.cn/node_11940.htm'
    oneListResult = onePage(pageUrl)
    # 写入json文件
    f = codecs.open('firstPage.json', 'w', encoding='utf-8')
    f.write(json.dumps(oneListResult, ensure_ascii=False))  #加ensure_ascii=False防止中文编码错误
    f.close()
