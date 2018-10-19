
# coding: utf-8

# In[1]:


import requests
from lxml import etree
import pandas as pd
from functools import reduce
import time
import datetime


# In[2]:


# Define the time-adjustment function.
def time_change(time_):
    if "分钟前" in time_:
        time_ = time_.replace("分钟前","")
        now = datetime.datetime.now()
        endnow = now + datetime.timedelta(minutes = (-int(time_)))
        endnow = str(endnow.strftime('%Y-%m-%d %H:%M'))
        time_use = datetime.datetime.strptime(endnow,'%Y-%m-%d %H:%M')
        return time_use
    elif "秒前" in time_:
        now = datetime.datetime.now()
        endnow = now
        endnow = str(endnow.strftime('%Y-%m-%d %H:%M'))
        time_use = datetime.datetime.strptime(endnow,'%Y-%m-%d %H:%M')
        return time_use
    elif "今天" in time_:
        time_ = time_.replace("今天","")
        now = datetime.datetime.now()
        endnow = now
        endnow = str(endnow.strftime('%Y-%m-%d')) + time_
        time_use = datetime.datetime.strptime(endnow,'%Y-%m-%d %H:%M')
        return time_use
    elif len(time_) == 11:
        time_ = time_
        now = "2018-"
        endnow = now + time_
        time_use = datetime.datetime.strptime(endnow,'%Y-%m-%d %H:%M')
        return time_use
    else:
        endnow = time_
        time_use = datetime.datetime.strptime(endnow,'%Y-%m-%d %H:%M')
        return time_use


# In[3]:


headers = {
    'x-udid':'ACAnU6qc0g2PToU22fbdVomjcZ5nbZg5Py4=',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'cookie':'_ga=GA1.2.911796492.1529645539; device_id=88c064c391ab04c4de2045294ab0aa38; s=er1259sufj; __utmz=1.1529980363.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); bid=4e52568e8166ce6b949541317316c791_jizdfhow; _gid=GA1.2.853318031.1530240081; aliyungf_tc=AQAAADGAwnZ1fwQAgkLBfAM+Rt9iiDJd; Hm_lvt_1db88642e346389874251b5a1eded6e3=1530098265,1530151272,1530240072,1530254522; snbim_minify=true; __utma=1.911796492.1529645539.1530240072.1530254647.7; __utmc=1; __utmt=1; xq_a_token=7443762eee8f6a162df9eef231aa080d60705b21; xq_a_token.sig=3dXmfOS3uyMy7b17jgoYQ4gPMMI; xq_r_token=9ca9ab04037f292f4d5b0683b20266c0133bd863; xq_r_token.sig=6hcU3ekqyYuzz6nNFrMGDWyt4aU; u=471530255026209; __utmb=1.2.10.1530254647; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1530255097; _gat_gtag_UA_16079156_4=1',
    'X-Requested-With':'XMLHttpRequest'
}

# Define the function of scrabing articles.
def get_article(target):
    url = str(target)
    r = requests.get(url,headers=headers).text
    s = etree.HTML(r)
    text = s.xpath('//*[@class="article__bd__detail"]//text()')
    if len(text) == 0:
        t = text
    elif len(text) == 1:
        t = text
    else:
        t = reduce(lambda x, y:str(x)+str(y),text)
    return t


# In[4]:


# Main function.
def get_info(id):
    url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page=1&user_id='+str(id)
    maxPage = requests.get(url,headers=headers).json()['maxPage']
    list_all = []
    for n in range(maxPage):
        url_page =  ('https://xueqiu.com/v4/statuses/user_timeline.json?page={}&user_id='+str(id)).format(n+1)
        count = len(requests.get(url_page,headers=headers).json()['statuses'])
        for i in range(count):
            response = requests.get(url_page,headers=headers,).json()['statuses'][i]
            target =  "https://xueqiu.com" + response['target']
            info = {"screen_name": response['user']['screen_name'],
                    "user_id": int(response['user_id']),
                    "timeBefore": time_change(response['timeBefore']),
                    "target": target,
                    "article": get_article(target)}
            list_all.append(info)
            time.sleep(0.01)
        print("loading")
    df = pd.DataFrame(list_all)
    df.to_excel('C:/Users/IndyW/OneDrive/桌面/高瓴资本/文本/%s文本.xls'%str(id),encoding='utf-8')

