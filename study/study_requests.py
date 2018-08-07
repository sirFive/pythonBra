#ccoding=utf-8
import requests

class tieba_p(object):
    def __init__(self,tieba_name):
        self.url = "http://tieba.baidu.com/f?kw={}".format(tieba_name)
        self.header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'}

    def get_data(self,url):
        response = requests.get(url,headers=self.header)
        print(response.content)
        return response.content

    def run(self):
        url = self.url
        data = self.get_data(url)

if __name__ == '__main__':
    tieba = tieba_p('校花吧')
    tieba.run()