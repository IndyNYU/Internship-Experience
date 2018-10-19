
# coding: utf-8

# In[1]:


import requests
from lxml import etree
import pandas as pd
from functools import reduce
import time
import datetime
import re


# In[2]:


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
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cookie': '_ga=GA1.2.911796492.1529645539; device_id=88c064c391ab04c4de2045294ab0aa38; s=er1259sufj; bid=4e52568e8166ce6b949541317316c791_jizdfhow; xq_a_token=584d0cf8d5a5a9809761f2244d8d272bac729ed4; xq_a_token.sig=x0gT9jm6qnwd-ddLu66T3A8KiVA; xq_r_token=98f278457fc4e1e5eb0846e36a7296e642b8138a; xq_r_token.sig=2Uxv_DgYTcCjz7qx4j570JpNHIs; Hm_lvt_1db88642e346389874251b5a1eded6e3=1534421223,1534421295,1534421302,1535080108; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1535080108; u=291535080107860; _gid=GA1.2.1988791929.1535080109; _gat_gtag_UA_16079156_4=1',
    'X-Requested-With': 'XMLHttpRequest'
}
url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SH600887&hl=0&source=all&sort=alpha&page=1&q='
response = requests.get(url,headers=headers,).json()


# In[4]:


def get_stock_info(symbol):
    list_all = []
    url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={}&hl=0&source=all&sort=alpha&page=1&q='.format(symbol)
    response = requests.get(url,headers=headers,).json()
    maxPage = response['maxPage']
    for n in range(maxPage):
        url_new = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={}&hl=0&source=all&sort=alpha&page={}&q='.format(symbol,n+1)
        response_new = requests.get(url_new,headers=headers).json()
        list_hot = response_new['list']
        for each in list_hot:
            text = each['text']
            article = re.sub("[A-Za-z\!\%\[\]\<\>\&\/\;\=]", "", text)
            article = article.replace(' ','')
            info = {
                "ticker":symbol,
                "screen_name":each['user']['screen_name'],
                "user_id":each['user_id'],
                "timeBefore":time_change(each['timeBefore']),
                "title":each['title'],
                "retweet_count":each['retweet_count'],
                "reply_count":each['reply_count'],
                "fav_count":each['fav_count'],
                "article":article,
                "link":"https://xueqiu.com"+each['target']
            }
            list_all.append(info)
            time.sleep(1.5)
        print("loading")
    df = pd.DataFrame(list_all)
    df.to_excel('C:/Users/IndyW/OneDrive/桌面/高瓴资本/伊利股份/{}.xls'.format(symbol),encoding='utf-8')


# In[5]:


list_ticker = ['SH600519','SZ000858','SZ000568','00220','02319','SH600429','SH600597']
for id_ in list_ticker:
    get_stock_info(id_)

