# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import codecs

#获取每条链接的内容
def getnewsdetail(newsUrl):
    #另类的http://dangjian.gmw.cn/2017-08/17/content_25688708.htm
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
    links = []
    res = requests.get(linksUrl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    for newshref in soup.select('.channel-newsGroup a')[:-1]:
        links.append(newshref['href'])   #获取a标签中的href内容
    return links

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
    specialUrl1 = 'http://dangjian.gmw.cn/2017-08/17/content_25688708.htm'
    specialUrl2 = 'http://dangjian.gmw.cn/2017-07/21/content_25157101.htm'
    specialUrl3 = 'http://survey.5icomment.com/jq/12228641.aspx'
    specialUrl4 = 'http://survey.5icomment.com/m/8863616.aspx?plg_nld=1&udsid=386284&plg_uin=1&plg_auth=1&plg_usr=1&plg_dev=1&plg_vkey=1'
    specialUrl5 = 'http://news.gmw.cn/2016-06/23/content_20666989.htm'
    specialUrl6 = 'http://topics.gmw.cn/node_84146.htm'
    specialUrl7 = 'http://dangjian.gmw.cn/2016-03/16/content_19313561.htm'
    for url in linksNew:
        if url != specialUrl1 and url != specialUrl2 and url != specialUrl3 and url != specialUrl4 \
                and url != specialUrl5 and url != specialUrl6 and url != specialUrl7:
            print(url)
            result1 = getnewsdetail(url)
            oneListResult.append(result1)
    return oneListResult

if __name__ == '__main__':

    #linksUrl = 'http://dangjian.gmw.cn/node_11940.htm' #某页新闻地址
    #oneListResult = onePage(linksUrl)
    totalResult = []
    for x in range(1,11):
        url = ''
        if x == 1:
            url = 'http://dangjian.gmw.cn/node_11940.htm'  #第一页的没有规律
        else:
            url = 'http://dangjian.gmw.cn/node_11940_'+str(x)+'.htm'
        oneListResult = onePage(url)
        totalResult.append(oneListResult)
    #写入json文件
    f = codecs.open('file2.json', 'w', encoding='utf-8')
    f.write(json.dumps(totalResult, ensure_ascii=False))
    f.close()
