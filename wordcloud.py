
# coding: utf-8

# In[3]:


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS 
import wordcloud
import jieba 
from scipy.misc import imread


# In[5]:


text = open('E:/SH600887.txt',encoding='GB2312', errors='ignore').read() 
cut_text = " ".join(jieba.cut(text))


# In[17]:


stopwords = set()
# stopwords = set(STOPWORDS) 
# STOPWPRD自带的是英文停用词，所以在制作中文词云要自己添加或者调用nltk库的stopword，nltk这里不做介绍
# stopwords.add("然而") # 单项添加
stopwords.update(["然而","这样","另一方面","但是","因此","我们","一个","如果",
                  '它们','具有','人们','可以','这个','这种','不能','因为',
                  '或者','没有','这些','一种','非常','可能','他们','而且',
                  '所有','也许','就是','认为','正如','必须','确定','所以',
                  '任何','发生','甚至','能够','过去','对于','知道','这是',
                  '现在','不同','并且','似乎','那样','其他','什么','不是',
                  '那么','一点','已经','之间','如何','仍然','伊利','伊利股份',
                  '企业','中国','股份','公司'])


# In[18]:


# 查看词频，方便重新增加停用词
process_word = WordCloud.process_text(wc, cut_text)
# 下面是字典排序
sort = sorted(process_word.items(),key=lambda e:e[1],reverse=True) # sort为list
print(sort[:50])  # 输出前词频最高的前50个


# In[19]:


imagename= imread( "E:/hillhouse.jpg")


# In[20]:


wc = WordCloud(background_color="white", # 背景图片中不添加word的颜色
               max_words=2000, # 最大词个数
               mask=imagename, stopwords=stopwords,
               font_path = 'X:\Windows\Fonts\simfang.ttf',
               # 设置字体格式，如不设置显示不了中文，而且字体名不能是中文
               max_font_size = 75, # 设置字体大小的最大值
               random_state = 42
               )
# generate word cloud 生成词云
wc.generate(cut_text)
# save to file
wc.to_file("E:/wordcloud.jpg")


# In[21]:


plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()

