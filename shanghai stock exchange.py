
# coding: utf-8

# In[1]:


import requests
import pandas as pd


# In[2]:


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cookie': 'yfx_c_g_u_id_10000042=_ck18080215111213778485731307677; VISITED_MENU=%5B%2210015%22%5D; yfx_f_l_v_t_10000042=f_t_1533193872365__r_t_1533193872365__v_t_1533194207054__r_c_0',
    'Host': 'query.sse.com.cn',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'http://www.sse.com.cn/disclosure/credibility/supervision/change/',
}
url = 'http://query.sse.com.cn/commonQuery.do?&isPagination=true&sqlId=COMMON_SSE_XXPL_CXJL_SSGSGFBDQK_S&pageHelp.pageSize=25&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1533198126869'
response = requests.get(url,headers=headers).json()


# In[6]:


response['result']


# In[3]:


list_all = []
for i in range(1,746):
    url = 'http://query.sse.com.cn/commonQuery.do?&isPagination=true&sqlId=COMMON_SSE_XXPL_CXJL_SSGSGFBDQK_S&pageHelp.pageSize=25&pageHelp.pageNo={}&pageHelp.beginPage={}&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1533198126869'.format(i,i)
    response = requests.get(url,headers=headers).json()
    list_data = response['result']
    list_all += list_data


# In[5]:


df_sh = pd.DataFrame(list_all)


# In[6]:


df_sh.to_excel('E:/sh_new.xlsx')


# In[1]:


range(1,3)[0]

