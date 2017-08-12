from datetime import datetime
from urllib.parse import urlencode
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import time
from itertools import product
import json
import random
from lagou_wordcloud.conf import *
from lagou_wordcloud.sqlmysq import *
from urllib.request import quote
from lagou_wordcloud.lagouinfo import *
def download(url,pn,addr,kd):
    data={
            'first': 'true',
            'pn': pn,
            'kd': kd
         }
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            #'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'Referer':'https://www.lagou.com/jobs/list_'+quote(kd)+'?city='+quote(addr)+'&cl=false&fromSearch=true&labelWords=&suginput=',
            'Host':'www.lagou.com',
            'Connection':'keep-alive',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            "Cookie": 'user_trace_token=20170811131717-57a752e4-7e54-11e7-99fe-525400f775ce;LGUID=20170811131717-57a75947-7e54-11e7-99fe-525400f775ce;index_location_city=%E5%85%A8%E5%9B%BD;TG-TRACK-CODE=index_search;SEARCH_ID=b5b3f46b937e4b2784de5f01009b86f9;JSESSIONID=ABAAABAABEEAAJAD35661A9FEA6059A10D42671E555B5F2;PRE_UTM=;PRE_HOST=;PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fchengdu-zhaopin%2Fhtml51%2F;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3365337.html;X_HTTP_TOKEN=278a2734cca1ebed9c576aa0b3d7ea3b;_gid=GA1.2.265403905.1502428643;_gat=1;_ga=GA1.2.1418184215.1502428643;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502428644,1502428651;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502443905;LGSID=20170811170830-a49da512-7e74-11e7-9b35-525400f775ce;LGRID=20170811173138-e03e7308-7e77-11e7-8551-5254005c3644',
            }#若服务器拒绝爬虫访问多半是cookie用多了被封的愿意，重新替换cookie即可
    pro=[
        'http://190.122.20.85:53281',#该处代理感觉用了像没用一样，所以通过第58行代码增加时间来解除屏蔽
        'http://113.247.88.81:3128',
        'http://71.41.27.245:8080'
    ]
    response=requests.post(url,data=data,headers=headers,timeout=10)
    return response.text

def get_content(html):
    info=json.loads(html)
    result=info['content']['positionResult']['result']
    for item in result:
        link_url='https://www.lagou.com/jobs/'+str(item['positionId'])+'.html'
        detail_link=info_detail(link_url)
        # print(detail_link)
        yield {
            'name': item['positionName'],
            'city':item['city'],
            'createTime':item['createTime'],
            'company':item['companyFullName'],
            'salary':item['salary'],
            'fuli':item['positionAdvantage'],
            'workyear':item['workYear'],
            'edu':item['education'],
            'link':link_url,
            'fied':item['industryField'],
            'onlyid':item['positionId'],
            'detail':detail_link
        }
def main(args):
    Url = 'https://www.lagou.com/jobs/positionAjax.json?city=*&needAddtionalResult=false&isSchoolJob=0'
    url=Url.replace('*',args[0])
    for pn in list(range(1,TOTLE_PAGE+1)):
        # time.sleep(random.randint(1,5))
        init_time=0
        wait_time=False
        html=''
        while not wait_time:
            # time.sleep(init_time)#若被屏蔽，每次增加10秒
            html=download(url,pn,args[0],args[1])
            print('%s----%s,第%s页' %(args[0],args[1],pn))
            isTure=json.loads(html)
            wait_time=isTure['success']
            print(isTure)
            if wait_time:
                if isTure['content']['pageNo'] == 0 or isTure['content']['pageNo']==TOTLE_PAGE:#该情况是采集完成或者是地区名字输入错误
                    print('已完成(%s,%s)的采集' %(args[0],args[1]))
                    return 0
                data=get_content(html)
                for i in data:
                    addinfo(i)
            else:
                # init_time=init_time+10
                date = datetime.now()
                date = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
                print(isTure['msg'],date)

if __name__=='__main__':
    args=product(ADDRESS,KEYWORDS)
    pool=Pool(10)
    pool.map(main,args)
    pool.close()
    pool.join()
    # for i in args:
    #     pool.apply_async(func=main,args=(i,))
    # pool.close()
    # pool.join()
    # for i in args:
    #     main(i)