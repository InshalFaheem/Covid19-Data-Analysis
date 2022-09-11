#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import all necessary libraries 


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import plotly
import plotly.express as px
import plotly.graph_objects as go

import plotly.offline as pyo
from plotly.offline import init_notebook_mode,plot,iplot

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

plt.rcParams['figure.figsize'] = 17,8


# In[2]:


data = pd.read_csv(r"E:\Data Analysis project jupyter lab\Covid 19 data analysis for Pakistan\Pakistan covid 19 dataset.csv")


# In[3]:


data.head()


# # Data Cleaning

# In[4]:


df = data.drop(['Country_Region', 'Case-Fatality_Ratio'], axis = 1)


# In[5]:


df.rename(columns = {'Last_Update':'Date'}, inplace = True)


# In[6]:


df


# # Active Cases in different province 

# In[7]:


f, ax = plt.subplots(figsize=(12, 7))
sns.despine(f)
sns.barplot(x="Province_State", y="Active_Cases", palette='Set1', ci = None,  data=df)


# ## Maximum Incidence_Rate in each province
# 

# In[8]:


df.groupby('Province_State')['Incidence_Rate'].sum().sort_values(ascending = False).to_frame()


# In[9]:


#sns.barplot(x="Province_State", y="Incidence_Rate", palette='Pastel1', ci = None,  data=data)
fig=go.Figure()
fig.add_trace(go.Bar(x=df['Province_State'],y=df['Incidence_Rate']))
fig.update_traces(marker_color='green')
fig.update_layout(title='Total Incidence Rate in different provinces of Pakistan',  xaxis=dict(title='Province_State'),yaxis=dict(title='Incidence Rate'), plot_bgcolor='#fff' )


# # Total Recovered Cases in different province  

# In[10]:


f, ax = plt.subplots(figsize=(12, 7))
sns.despine(f)
sns.barplot(x="Province_State", y="Recovered", palette='Set3', ci = None,  data=df)


# # Minimum Deaths in each province

# In[11]:


df.groupby('Province_State')['Deaths'].sum().sort_values(ascending = True)


# In[12]:


f, ax = plt.subplots(figsize=(12, 7))
sns.despine(f)
sns.barplot(x="Province_State", y="Deaths", palette='Set1', ci = None,  data=df)


# # Pakistan Coordinates

# In[13]:


Pak_Cord = pd.read_csv(r"E:\Data Analysis project jupyter lab\Covid 19 data analysis for Pakistan\Pak_Cordinates.csv")
Pak_Cord 


# In[14]:


Pak_Cord.rename(columns = {'Long_':'Long'}, inplace = True)


# In[40]:


df = df[df['Province_State'].notna()]


# # Merege two datasets

# In[41]:


data_full = pd.merge(Pak_Cord, df, on= 'Province_State')
data_full


# In[42]:


Punjab_Data = df[df.Province_State == 'Punjab']
Islamabad_Data = df[df.Province_State == 'Islamabad']
GB_Data = df[df.Province_State == 'Gilgit-Baltistan']

KPK_Data = df[df.Province_State == 'Khyber Pakhtunkhwa']
Balochistan_Data = df[df.Province_State == 'Balochistan']
Ajk_Data = df[df.Province_State == 'Azad Jammu and Kashmir']
Sindh_Data = df[df.Province_State == 'Sindh']


# # Comparing Total Confirm Cases in Different States of Pakistan

# In[43]:


from plotly.subplots import make_subplots


# In[44]:


fig = make_subplots(
    rows=3, cols=3,
    specs = [[{"secondary_y": True},{"secondary_y": True}, {"secondary_y": True}], [{"secondary_y": True},{"secondary_y": True}, {"secondary_y": True}], [{"secondary_y": True}, {"secondary_y": True},{"secondary_y": True}]],
    subplot_titles=("Punjab","Sindh","Khyber Pakhtunkhwa", "Islamabad","Gilgit-Baltistan", "Balochistan", "AJK"))

fig.add_trace(go.Bar(x=Sindh_Data['Date'],y=Sindh_Data['Total_Confirmed_Cases'],
                    marker=dict(color=Sindh_Data['Total_Confirmed_Cases'],coloraxis="coloraxis")),1,1)

fig.add_trace(go.Bar(x=Punjab_Data['Date'],y=Punjab_Data['Total_Confirmed_Cases'],
                    marker=dict(color=Punjab_Data['Total_Confirmed_Cases'],coloraxis="coloraxis")),1,2)

fig.add_trace(go.Bar(x=KPK_Data['Date'],y=KPK_Data['Total_Confirmed_Cases'],
                    marker=dict(color=KPK_Data['Total_Confirmed_Cases'],coloraxis="coloraxis")),1,3)

fig.add_trace(go.Bar(x=GB_Data['Date'],y=GB_Data['Total_Confirmed_Cases'],
                    marker=dict(color=GB_Data['Total_Confirmed_Cases'],coloraxis="coloraxis")),2,1)

fig.add_trace(go.Bar(x=Islamabad_Data['Date'],y=Islamabad_Data['Total_Confirmed_Cases'],
                    marker=dict(color=Islamabad_Data['Total_Confirmed_Cases'],coloraxis="coloraxis")),2,2)

fig.add_trace(go.Bar(x=Ajk_Data['Date'],y=Ajk_Data['Total_Confirmed_Cases'],
                    marker=dict(color=Ajk_Data['Total_Confirmed_Cases'],coloraxis="coloraxis")),2,3)

fig.add_trace(go.Bar(x=Balochistan_Data['Date'],y=Balochistan_Data['Total_Confirmed_Cases'],
                    marker=dict(color=Balochistan_Data['Total_Confirmed_Cases'],coloraxis="coloraxis")),3,1)

fig.update_layout(coloraxis=dict(colorscale='Bluered_r'),showlegend=False,title_text="Total Cases in 6 States",
                height=1000, width=1000 )


fig.update_layout(plot_bgcolor='rgb(230,230,230)')


# # Map Showing Total Confirm Cases, Death and Recovered Cases in Different States

# In[47]:


map = folium.Map(location=[20,70], zoom_start = 4, tiles='Stamenterrain', prefer_canvas=True)
for lat,long,value,name in zip(data_full['Lat'],data_full['Long'],data_full['Total_Confirmed_Cases'],data_full['Province_State']):
    folium.CircleMarker([lat,long],radius=value*0.8,popup=('<strong>State</strong>: '+str(name).capitalize()+'<br>''<strong>Total Cases</strong>: ' + str(value)+ '<br>'),color='red',fill_color='red',fill_opacity=0.3).add_to(map)
    


# In[46]:


fig=px.density_mapbox(data_full,lat="Lat",lon="Long",hover_name="Province_State",hover_data=["Total_Confirmed_Cases","Deaths","Recovered"],animation_frame="Date",color_continuous_scale="Portland",radius=7,zoom=0,height=700)
fig.update_layout(title='Corona Virus Cases in Pakistan')
fig.update_layout(mapbox_style="open-street-map",mapbox_center_lon=0)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# In[ ]:





# In[ ]:





# In[ ]:




