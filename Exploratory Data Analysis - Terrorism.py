
# ## Author :- Maulik Mangukiya 

# ### Exploratory Data Analysis - Terrorism
# 
# -Problem Statement: Perform ‘Exploratory Data Analysis’ on dataset ‘Global Terrorism’
# 
# -As a security/defense analyst, try to find out the hot zone of terrorism.
# 
# -What all security issues and insights you can derive by EDA?

# **Import libraries**

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

d = pd.read_csv("C:/Users/shree/Desktop/Charfarm/DATASET.csv",encoding="latin1")


# In[3]:


d.head()


# In[4]:


d.info()


# In[5]:


d.describe()


# In[6]:


d.corr()


# In[7]:


d.columns


# ### **Destructive Feature of data**

# In[8]:


print("Country with the most attacks:",d['country'].value_counts().idxmax())
print("City with the most attacks:",d['city'].value_counts().index[1]) 
print("Region with the most attacks:",d['region'].value_counts().idxmax())
print("Year with the most attacks:",d['iyear'].value_counts().idxmax())
print("Month with the most attacks:",d['imonth'].value_counts().idxmax())
print("Group with the most attacks:",d['gname'].value_counts().index[1])
print("Most Attack Types:",d['weaptype1_txt'].value_counts().idxmax())


# ### **Number of Terrorist Activities each Year**
# 

# In[9]:


x_year = d['iyear'].unique()
y_count_years = d['iyear'].value_counts(dropna = False).sort_index()
plt.figure(figsize = (20,10))
sns.barplot(x = x_year,y = y_count_years,palette = 'rocket')
plt.xticks(rotation = 45)
plt.xlabel('Attack Year')
plt.ylabel('Number of Attacks each year')
plt.title('Attack_of_Years')
plt.show()


# ### **Terrorist Activities by Region in each Year through Area Plot**
# 

# In[9]:


pd.crosstab(d.iyear, d.region).plot(kind='area',figsize=(15,6))
plt.title('Terrorist Activities by Region in each Year')
plt.ylabel('Number of Attacks')
plt.show()


# In[10]:


d['nwound'] =d['nwound'].fillna(0).astype(int)
d['nkill'] = d['nkill'].fillna(0).astype(int)
d['casualities'] = d['nkill'] + d['nwound']


# Values are sorted by the top 40 worst terror attacks as to keep the heatmap simple and easy to visualize

# In[11]:


terror1 = d.sort_values(by='casualities',ascending=False)[:40]


# In[12]:


heat=terror1.pivot_table(index='country_txt',columns='iyear',values='casualities')
heat.fillna(0,inplace=True)


# In[13]:


heat.head()


# In[14]:


import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
colorscale = [[0, '#edf8fb'], [.3, '#00BFFF'],  [.6, '#8856a7'],  [1, '#810f7c']]
heatmap = go.Heatmap(z=heat.values, x=heat.columns, y=heat.index, colorscale=colorscale)
data = [heatmap]
layout = go.Layout(
    title='Top 40 Worst Terror Attacks in History from 1982 to 2016',
    xaxis = dict(ticks='', nticks=20),
    yaxis = dict(ticks='')
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='heatmap',show_link=False)


# ### **Death and Injuries at all time.**

# In[15]:



d.plot(kind='scatter',x='nkill',y='nwound',alpha=0.5,color = 'purple',figsize=(10,10),fontsize=15)
plt.xlabel('Kills',fontsize=15)
plt.ylabel('Wound',fontsize=15)
plt.title('Kill-wound scatter plot')
plt.show()


# In the majority of acts of terrorism, the mortality rate and injuries were low, but a small number of actions led to too many deaths and injuries.

# ### **Frequency of Terrorist Actions in Customized Region**
# 
# 

# In[16]:


plt.subplots(figsize=(15,6))
sns.barplot(d['country_txt'].value_counts()[:15].index,d['country_txt'].value_counts()[:15].values,palette='Blues_d')
plt.title('Top Countries Affected')
plt.xlabel('Countries')
plt.ylabel('Count')
plt.xticks(rotation= 90)
plt.show()


# Terrorist attacks have increased in recent years.

# ### **Total Number of people killed in terror attack**

# In[17]:


killData = d.loc[:,'nkill']
print('Number of people killed by terror attack:', int(sum(killData.dropna())))


# 
# ### **look at what types of attacks these deaths were made of.**

# In[18]:


attackData = d.loc[:,'attacktype1':'attacktype1_txt']
typeKillData = pd.concat([attackData, killData], axis=1)


# In[19]:


typeKillFormatData = typeKillData.pivot_table(columns='attacktype1_txt', values='nkill', aggfunc='sum')
typeKillFormatData


# In[20]:


typeKillFormatData.info()


# In[21]:


labels = typeKillFormatData.columns.tolist() 
transpoze = typeKillFormatData.T 
values = transpoze.values.flatten()
fig, ax = plt.subplots(figsize=(8, 10), subplot_kw=dict(aspect="equal"))
plt.pie(values, startangle=90, autopct='%0.2f%%')
plt.title('Types of terrorist attacks that cause deaths')
plt.legend(labels, loc='upper right', bbox_to_anchor = (1.5, 0.9), fontsize=10) 
plt.show()


# In[22]:


countryData = d.loc[:,'country':'country_txt']

countryKillData = pd.concat([countryData, killData], axis=1)


# In[23]:


countryKillFormatData = countryKillData.pivot_table(columns='country_txt', values='nkill', aggfunc='sum')
countryKillFormatData


# In[24]:


countryKillFormatData.info()


# In[25]:


fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size


# In[26]:


labels = countryKillFormatData.columns.tolist()
labels = labels[:50] 
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[:50]
values = [int(i[0]) for i in values] 
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange']  
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=15)
plt.xticks(index, labels, fontsize=12, rotation=90)
plt.title('Number of people killed by countries')

plt.show()


# In[27]:


labels = countryKillFormatData.columns.tolist()
labels = labels[50:101]
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[50:101]
values = [int(i[0]) for i in values]
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange']
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=15)
plt.xticks(index, labels, fontsize=12, rotation=90)
plt.title('Number of people killed by countries')
plt.show()


# In[28]:


labels = countryKillFormatData.columns.tolist()
labels = labels[152:206]
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[152:206]
values = [int(i[0]) for i in values]
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange']
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=15)
plt.xticks(index, labels, fontsize=12, rotation=90)
plt.title('Number of people killed by countries')
plt.show()


# Terrorist acts in the Middle East and northern Africa have been seen to have fatal consequences. The Middle East and North Africa are seen to be the places of serious terrorist attacks. In addition, even though there is a perception that Muslims are supporters of terrorism, Muslims are the people who are most damaged by terrorist attacks. If you look at the graphics, it appears that Iraq, Afghanistan and Pakistan are the most damaged countries. All of these countries are Muslim countries.

# ### ***THANK YOU***
