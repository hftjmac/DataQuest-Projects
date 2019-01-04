#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import matplotlib as plt
get_ipython().magic('matplotlib inline')

recent_grads = pd.read_csv('recent-grads.csv')
print(recent_grads.iloc[0])


# In[4]:


print(recent_grads.head())
print(recent_grads.tail())


# In[5]:


print(recent_grads.describe())


# In[6]:


recent_grads.shape


# In[7]:


recent_grads = recent_grads.dropna()


# In[8]:


recent_grads.shape


# In[9]:


recent_grads.plot(x='Sample_size', y='Median', kind = 'scatter')


# In[10]:


recent_grads.plot(x='Sample_size', y='Unemployment_rate', kind='scatter')


# In[11]:


recent_grads.plot(x='Full_time', y='Median', kind='scatter')


# In[12]:


recent_grads.plot(x='ShareWomen', y='Unemployment_rate', kind='scatter')


# In[13]:


recent_grads.plot(x='Men', y='Median', kind='scatter')


# In[14]:


recent_grads.plot(x='Women', y='Median', kind='scatter')


# It appears that there is a weak upward trend between unemployment_rate and ShareWomen.
# It also appears that Median salary is slightly higher the more men there are.
# 
# To answer the questions, major popularity does not appear to have an effect on median salary as the more popular majors all appear to fall in the middle of the median salaries.
# Students in majority female majors make less.
# There does not appear to be a trend between the number of full-time employees and median salary.

# In[15]:


recent_grads['Sample_size'].hist(bins=15, range=(0,3000))


# In[16]:


recent_grads['Median'].hist(bins=15, range=(20000,80000))


# In[17]:


recent_grads['Employed'].hist(bins=20, range=(0,200000))


# In[18]:


recent_grads['Full_time'].hist(bins=20, range=(0,200000))


# In[19]:


recent_grads['ShareWomen'].hist(bins=2)


# In[20]:


recent_grads['Unemployment_rate'].hist(bins=18)


# In[21]:


recent_grads['Men'].hist(bins=20,range=(0,200000))


# In[22]:


recent_grads['Women'].hist(bins=20,range=(0,200000))


# About 40% of the majors are predominantly male.  60% are predominantly female.
# 
# The most common median salary range is 32000-36000.

# In[23]:


from pandas.plotting import scatter_matrix
scatter_matrix(recent_grads[['Sample_size', 'Median']], figsize = (6,6))


# In[24]:


scatter_matrix(recent_grads[['Sample_size', 'Median', 'Unemployment_rate']], figsize = (9,9))


# In[25]:


scatter_matrix(recent_grads[['ShareWomen', 'Median']], figsize = (6,6))


# In[26]:


scatter_matrix(recent_grads[['Full_time', 'Median']], figsize = (6,6))


# In[27]:


recent_grads[:10].plot.bar(x='Major', y='ShareWomen', legend=False)


# In[28]:


recent_grads[163:].plot.bar(x='Major',y='ShareWomen',legend=False)


# In[29]:


recent_grads[:10].plot.bar(x='Major', y='Unemployment_rate', legend=False)


# In[30]:


recent_grads[163:].plot.bar(x='Major',y='Unemployment_rate',legend=False)


# In[39]:


MenSum = {}
WomenSum = {}
categories = recent_grads['Major_category'].unique()

for category in categories:
    selected_rows = recent_grads[recent_grads['Major_category'] == category]
    MenSum[category] = selected_rows['Men'].sum()
    WomenSum[category] = selected_rows['Women'].sum()
    
MenSumSeries = pd.Series(MenSum)
WomenSumSeries = pd.Series(WomenSum)

majorCategoriesSums = pd.DataFrame(MenSumSeries, columns=['Men'])
majorCategoriesSums['Women'] = WomenSumSeries
majorCategoriesSums.plot.bar(figsize = (10,10));


# In[46]:


recent_grads['Median'].plot.box(figsize = (8,8))


# In[45]:


recent_grads['Unemployment_rate'].plot.box(figsize = (8,8))


# In[56]:


recent_grads.plot.hexbin(x='Sample_size',y='Median',figsize = (10,10))


# In[57]:


recent_grads.plot.hexbin(x='Sample_size',y='Unemployment_rate',figsize = (10,10))


# In[59]:


recent_grads.plot.hexbin(x='Full_time',y='Median',figsize = (10,10))


# In[61]:


recent_grads.plot.hexbin(x='ShareWomen', y='Unemployment_rate',figsize = (10,10))


# In[ ]:




