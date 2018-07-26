from urllib3 import *
import re
disable_warnings()


http = PoolManager()
def str2Header(file):
    headerDict = {}
    f = open(file, 'r', encoding='UTF-8')
    headerText = f.read()
    headers = re.split('\n', headerText)
    for header in headers:
        result = re.split(':', header, maxsplit=1)
        headerDict[result[0]] = result[1]
    f.close()
    return headerDict

headers = str2Header('headers.txt')

url ='https://rate.taobao.com/feedRateList.htm?auctionNumId=38621807169&userNumId=55010489&currentPageNum=1&pageSize=20&rateType=1&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098%23E1hvFQvRvPQvUvCkvvvvvjiPPsqZzjYEPLq91jYHPmPZQjtnP2cvgjt8RsLw1ji2RphvCvvvvvmCvpvZzPsNcXdNznswuEHftsbwKnAi7I45vpvhvvmv9IyCvvOUvvVvayVivpvUvvmvWiphYFetvpvIvvvvvhCvvvvvvUUdphvU79vv9krvpvQvvvmm86CvmVWvvUUdphvUOQyCvhQUE7vvCsuxfwLZd3OiHExr1RoK5zXRtW2IsCuOwlMXS47BhC3qVUcnDOmOVzIUDajxALwpEcqhljc6hX3kLixr1noK5kx%2F1nBldCV7vphvC9vhvvCvpvGCvvpvvPMMRphvCvvvvvmjvpvhvvpvv86CvvyvmR8Czrgv7Uvjvpvjzn147rMvFFyCvvpvvvvv&_ksTS=1532574745678_1118&callback=jsonp_tbcrate_reviews_list'
r = http.request('GET', url, headers=headers)
print(r.data.decode('UTF-8', 'ignore'))
#UTF-8 gbk gb2312 gb18030
