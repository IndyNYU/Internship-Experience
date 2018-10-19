
# coding: utf-8
IT Test by Yidi Wang 6/15/2018
start from: 2:00pm
finish at:  5:30pm
Work with Python pandas.
Step 1: Calculate the technical indicator according to the requirement.
Step 2: Get the trading signal.
Step 3: Calculate the return.
# In[1]:


# Work only with Python.pandas.
import pandas as pd

Step 1. Read the data, clean and calculate according to the technical signals.
# In[2]:


# Get the original data and slice what I want to use.
data = pd.read_excel('D:/杉树笔试-data.xlsx', header = 3, skiprows = 0, index_col = '时间')
data = data[['开盘','最高','最低','收盘','成交量']][1:]
# Calculate the RSI.
# Calculate the Ut and Dt.
data['Ut'] = np.maximum(data['收盘'].diff(1),0)
data['Dt'] = np.maximum(data['收盘'].diff(-1),0)
# Calculate the EMA.
data = data[1:len(data)-1]
data['EMA(Ut,2)'] = np.ones(len(data))
data['EMA(Ut,2)'][0] = (2/3) * data['Ut'][0]
for i in range(len(data)):
    data['EMA(Ut,2)'][i] = (2/3) * data['Ut'][i] + (1/3) * data['EMA(Ut,2)'][i-1]

    data['EMA(Dt,2)'] = np.ones(len(data))
data['EMA(Dt,2)'][0] = (2/3) * data['Dt'][0]
for i in range(len(data)):
    data['EMA(Dt,2)'][i] = (2/3) * data['Dt'][i] + (1/3) * data['EMA(Dt,2)'][i-1]


# In[3]:


# Calculate the RSI.
data['RSt'] = data['EMA(Ut,2)'] / data['EMA(Dt,2)']
data['RSI'] = 100 - 100 / (1 + data['RSt'])


# In[4]:


# Calculate the MA5 and MA30.
data['MA5'] = data['收盘'].rolling(window = 5).mean()
data['MA30'] = data['收盘'].rolling(window = 30).mean()
data = data.dropna()


# In[5]:


# Calculate the ADX.
# Calculat the TRt.
data['TRt'] = np.ones(len(data))
for i in range(len(data)):
    data['TRt'][i] = max((data['最高'][i] - data['最低'][i]),  
                         (abs(data['最高'][i] - data['收盘'][i-1])),
                         (abs(data['最低'][i] - data['收盘'][i-1])))


# In[6]:


# Calculate the HDt and LDt.
data['HDt'] = data['最高'].diff(1)
data['LDt'] = data['最低'].diff(-1)
data = data.dropna()


# In[7]:


# Calculate the DMP and DMM.
data['DMPsign'] = np.where(data['HDt']>0, 1, 0)
data['DMMsign'] = np.where(data['LDt']>0, 1, 0)

data['DMPsign'] = np.where(data['HDt'] > data['LDt'], data['DMPsign'], 0)
data['DMMsign'] = np.where(data['LDt'] > data['HDt'], data['DMMsign'], 0)

data['DMPproduct'] = data['DMPsign'] * data['HDt']
data['DMMproduct'] = data['DMMsign'] * data['LDt']

data['DMP'] = data['DMPproduct'].rolling(window = 14).mean()
data['DMM'] = data['DMMproduct'].rolling(window = 14).mean()

data = data.dropna()


# In[8]:


# Calculate the PDI and MDI.
data['PDIt'] = data['DMP'] * 100 / data['TRt']
data['MDIt'] = data['DMM'] * 100 / data['TRt']


# In[9]:


data['ADX'] = abs((data['MDIt']-data['PDIt'])/(data['MDIt']+data['PDIt'])) * 100
data['ADX(14,14)'] = data['ADX'].rolling(window = 14).mean()

data = data.dropna()


# In[10]:


# Slice what I want to use to calculate the trading signal.
data = data[['开盘', '最高', '最低', '收盘', '成交量', 'RSI', 'ADX(14,14)', 'MA5', 'MA30']]

Step 2. Get the trading signal.
# In[11]:


data['Trading Signal'] = np.zeros(len(data))
for i in range(len(data)):
    if data['ADX(14,14)'][i] > 15:
        if data['MA5'][i] > data['MA30'][i]:
            data['Trading Signal'][i] = 1
        if data['MA5'][i] <= data['MA30'][i]:
            data['Trading Signal'][i] = -1
    if data['ADX(14,14)'][i] <= 15:
        if data['RSI'][i] < 5:
            data['Trading Signal'][i] = 1
        if data['RSI'][i] > 95:
            data['Trading Signal'][i] = -1

Step 3. Calculate the trading return.
# In[12]:


data['moving'] = data['收盘'].diff(1)
data['Daily Return'] = data['moving'] * data['Trading Signal'] * (0.98)
data['Total Return'] = data['Daily Return'].cumsum()


# In[13]:


data.to_excel('D:\Yidi Wang.xlsx')

