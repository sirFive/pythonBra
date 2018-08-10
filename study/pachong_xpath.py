#coding:utf-8
import requests
from lxml import etree
import os,json,sys
import codecs

class  Tieba_P():
    def __init__(self):
        #self.url = "http://dangjian.gmw.cn/2018-07/28/content_30136870.htm"
        self.url = 'http://dangjian.gmw.cn/node_11940.htm'
        self.headers={
            #"User-Agent":"Mozilla/4.0(compatible;MSIE 5.01;Windows  NT 5.0)"
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }   #构造一个浏览器
        self.file = open("temp.json","w")    #打开一个文件用于写入


    def get_data(self,url):
        response = requests.get(url, headers=self.headers) #发起一个http请求
        response.encoding = 'utf-8'
        #print(response.text)
        return response.content

    def parse_detail_page(self, data):
        html = etree.HTML(data)

        #title_list = html.xpath("//ul[@class='channel-newsGroup']/li[5]/span[@class='channel-newsTitle']/a/@href")   #用xpath提取目标元素,li[index]变化
        #title_list = html.xpath('/html/body/div[6]/div[1]/div[2]/ul[1]/li[1]/span[1]/a')  # 用xpath提取目标元素,li[index]变化
        title_list = html.xpath("/html/body/div[@class='channelMain']/div[@class='channelLeftPart']/div/ul[@class='channel-newsGroup']/li/span[@class='channel-newsTitle']/a/@href")
        print(title_list)
        print('================')
        return title_list
    def get_detail_message(self,urls):
        list_result = []  #存放所有链接的所有内容
        title_xpath = "/html/body/div[@class='contentWrapper']/div[@class='contentLeft']/h1[@id='articleTitle']/text()"
        time_xpath = "/html/body/div[@class='contentWrapper']/div[@class='contentLeft']/div[@id='contentMsg']/span[@id='pubTime']/text()"
        content_xpath = "/html/body/div[@class='contentWrapper']/div[@class='contentLeft']/div[@id='contentMain']/p/text()"
        urls_new = []  #得到全部正确的url
        for url in urls:  # 有些链接没有 http://news.gmw.cn/  这个前缀，要加上
            if (url.find('http')) < 0:
                addHttpLink = 'http://dangjian.gmw.cn/' + url
                urls_new.append(addHttpLink)
            else:
                urls_new.append(url)
        for link in urls_new:  #遍历每个链接中的 title，content，date
            result = {}
            data = self.get_data(link)
            html = etree.HTML(data)
            title_detail = html.xpath(title_xpath)
            time_detail = html.xpath(time_xpath)
            content_detail = html.xpath(content_xpath)
            result['title'] = title_detail[0].strip()
            result['time'] = time_detail[0].strip()
            result['content'] = []
            for n in content_detail:
                result['content'].append(n.strip())
            #print(result['title'])
            #print(result['time'])
            #print(result['content'])
            list_result.append(result)
        return list_result

    def run(self):
            url = self.url
            #print(url)
            data = self.get_data(url)
            urls = self.parse_detail_page(data)
            all_result = self.get_detail_message(urls)
            f = codecs.open('4567.json', 'w', encoding='utf-8')
            f.write(json.dumps(all_result, ensure_ascii=False))  # 加ensure_ascii=False防止中文编码错误
            f.close()


if __name__ == '__main__':
    tieba = Tieba_P()
    tieba.run()