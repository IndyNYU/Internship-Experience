
# coding: utf-8

# In[1]:


from snownlp import SnowNLP
import pandas as pd


# In[2]:


df = pd.read_excel('E:/SH600887.xls')


# In[3]:


list_sentiment = []
for i in range(len(df)):
    text = df['article'][i]
    s = SnowNLP(text)
    score = s.sentiments
    list_sentiment.append(score)


# In[4]:


df['sentiment'] = list_sentiment


# In[5]:


df_sentiment = df[['timeBefore','sentiment']]


# In[6]:


list_day = []
for i in range(len(df_sentiment)):
    day = str(df_sentiment['timeBefore'][i])[0:10]
    list_day.append(day)


# In[7]:


df_sentiment['day'] = list_day


# In[8]:


df_sentiment = df_sentiment[['day','sentiment']]


# In[9]:


df_sentiment.median()


# In[10]:


df_analysis = df_sentiment.groupby('day').mean()
df_analysis['sentiment'].describe()


# In[11]:


list_price = [27.64, 27.64, 27.14, 27.55, 27.55, 
              27.55, 27.59, 28.02, 27.54, 26.97, 
              26.92, 26.92, 26.92, 26.69, 26.44]
df_analysis['price'] = list_price


# In[12]:


df_analysis


# In[13]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[14]:


x = list(df_analysis.index)
y1 = df_analysis['price']
y2 = df_analysis['sentiment']


# In[15]:


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x, y1,'r',label="price");
ax1.legend(loc=1)
ax1.set_ylabel('price');
ax2 = ax1.twinx() # this is the important function
ax2.plot(x, y2, 'g',label = "sentiment")
ax2.legend(loc=2)
ax2.set_ylabel('sentiment');
plt.show()


# In[1]:


from aip import AipNlp
import codecs
APP_ID = '11617425'
API_KEY = 'UYQM5DIx14BxCU1w47WG2rdM'
SECRET_KEY = 'SLWzBVKHCT9bW4C5Cq0oDKofDkGs5wEL'

def get_sentiment(text):
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    sitems=client.sentimentClassify(text)['items'][0]#情感分析
    positive=sitems['positive_prob']#积极概率
    confidence=sitems['confidence']#置信度
    sentiment=sitems['sentiment']#0表示消极，1表示中性，2表示积极
    return(positive,confidence,sentiment)


# In[ ]:


list_

