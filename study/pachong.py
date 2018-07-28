#coding:utf-8
import requests
from lxml import etree
import os,json,sys


class Tieba_P(object):
    def __init__(self,tieba_name):
        self.url = 'http://tieba.baidu.com/f?kw={}'.format(tieba_name)
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0) '
        }
        self.file = open('tieba.json','w')


    def get_data(self, url):
        response = requests.get(url,headers=self.headers)
        return response.content

    def parse_list_page(self,data):
        # 将源码转换成element对象
        html = etree.HTML(data.decode('utf-8'))
        print(html)

        # 获取节点列表
        node_list = html.xpath('//li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a')
        #print (len(node_list))

        # 构建返回数据的列表
        data_list = []

        # 遍历节点列表
        for node in node_list:
            temp = {}
            temp['title'] = node.xpath('./text()')[0]
            temp['url'] = 'http://tieba.baidu.com/' + node.xpath('./@href')[0]
            data_list.append(temp)

        # 获取下一页url
        try:
            next_url = 'http:' + html.xpath('//*[@id="frs_list_pager"]/a[last()-1]/@href')[0]
        except:
            next_url = None

        return data_list,next_url

    def parse_detail_page(self, data):
        html = etree.HTML(data)

        image_list = html.xpath('//cc/div/img/@src')

        return image_list

    def download(self,image_list):
        if not os.path.exists('image'):
            os.makedirs('image')

        for url in image_list:
            filename = 'image' + os.sep + url.split('/')[-1]
            data = self.get_data(url)
            with open(filename,'wb')as f:
                f.write(data)

    def save_data(self,data):
        str_data = json.dumps(data,ensure_ascii=False) + ',\n'
        self.file.write(str_data)



    def __del__(self):
        self.file.close()

    def run(self):
        # 构建url
        # 构建请求头
        next_url = self.url
        while True:
            # 发送请求获取响应
            data = self.get_data(next_url)
            # 从列表页面响应中，抽取详情页面数据列表，下一页url
            detail_list,next_url = self.parse_list_page(data)
            # 遍历详情页面列表
            for detail in detail_list:

                # 获取详情页面的响应
                detail_data = self.get_data(detail['url'])
                # 提取图片链接列表
                image_list = self.parse_detail_page(detail_data)
                # 下载图片
                self.download(image_list)
                # 保存数据
                detail['images'] = image_list
                self.save_data(detail)

if __name__ == '__main__':
    #tieba = Tieba_P(sys.argv[1])
    tieba = Tieba_P("校花")
    tieba.run()