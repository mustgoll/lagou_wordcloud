import requests
import time
from bs4 import BeautifulSoup
def info_detail(url):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            "Cookie": 'user_trace_token=20170811131717-57a752e4-7e54-11e7-99fe-525400f775ce;LGUID=20170811131717-57a75947-7e54-11e7-99fe-525400f775ce;X_HTTP_TOKEN=278a2734cca1ebed9c576aa0b3d7ea3b;index_location_city=%E5%85%A8%E5%9B%BD;TG-TRACK-CODE=index_search;SEARCH_ID=b5b3f46b937e4b2784de5f01009b86f9;JSESSIONID=ABAAABAABEEAAJAD35661A9FEA6059A10D42671E555B5F2;PRE_UTM=;PRE_HOST=;PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fhangzhou-zhaopin%2Fhtml51%2F;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3365337.html;_gid=GA1.2.265403905.1502428643;_gat=1;_ga=GA1.2.1418184215.1502428643;LGSID=20170811170830-a49da512-7e74-11e7-9b35-525400f775ce;LGRID=20170811171800-f8d557b9-7e75-11e7-854e-5254005c3644;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502428644,1502428651;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502443087',
            }
    html=requests.get(url,headers=header).text
    soup=BeautifulSoup(html,'lxml')
    div=soup.select('#job_detail > dd.job_bt > div > p')
    if div:
        str=''
        for i in div:
            str+=i.get_text()
        return str
    else:
        print(url,'获取失败，等待重试.....')
        return
if __name__=='__main__':
    for i in range(10):
        print(i,info_detail('https://www.lagou.com/jobs/3452219.html'))#测试