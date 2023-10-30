#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime #### to handling the null values of date time
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# In[2]:


data = pd.read_csv(r"C:\Users\Ivin\OneDrive\Desktop\Airbnb_Open_Data.csv")


# In[3]:


data.head()


# In[4]:


data.shape


# In[5]:


data.info()


# In[6]:


data.columns


# In[7]:


data.isnull()


# In[8]:


data.isnull().sum()


# In[9]:


data.isnull().sum().sum()         ### is shows the totel number of null values


# In[10]:


data.isnull().sum()/len(data)


# In[11]:


data.isnull().sum()/len(data)*100


# In[12]:


###house_rules and license have more than 50% null values in the dataset 
###and last reviews and review per month more than 15% null values in dataset


# In[12]:


data["last review"].head()


# In[13]:


data["reviews per month"].head()


# In[14]:


data["house_rules"].head()


# In[15]:


data["license"].head()


# ### handing null values of reviews per month

# In[16]:


data["reviews per month"].mean()


# In[17]:


data["reviews per month"].median()


# In[18]:


data["reviews per month"].mode()


# In[19]:


data["reviews per month"]=data["reviews per month"].fillna(data["reviews per month"].median())


# In[20]:


data["reviews per month"]


# In[21]:


data.head()


# In[22]:


data.isnull().sum()/len(data)*100


# In[23]:


data["reviews per month"]


# ### handling null values of last reviews,house_rulesand license

# In[24]:


data.drop(["license"],axis=1,inplace=True)


# In[25]:


data.shape


# In[26]:


data.drop(["last review"],axis=1,inplace=True)


# In[27]:


pd.to_datetime("2020-01-01")


# In[28]:


data.shape


# In[29]:


data.drop(["house_rules"],axis=1,inplace=True)


# In[30]:


data.head()


# In[31]:


data.shape


# In[32]:


data.isnull().sum()/len(data)*100


# In[33]:


data.info()


# In[34]:


data.nunique()


# ### convert the price value into float from object

# In[35]:


data["price"]


# In[36]:


def clean_and_convert_price(price_str):
    try:
        price_str = price_str.replace('$', '').replace(',', '').replace(' ', '').replace('.', '').strip()
        return int(price_str)
    except:
        return None
    
data['price'] = data['price'].apply(clean_and_convert_price)
data['service fee'] = data['service fee'].apply(clean_and_convert_price)


# In[37]:


data["price"]


# In[38]:


data.info()


# ### mongodb

# In[39]:


from pymongo import MongoClient


# In[40]:


CloudClient = MongoClient("mongodb+srv://naveenaiyyappan:Rink@cluster0.od0r49h.mongodb.net/?retryWrites=true&w=majority")


# In[41]:


CloudClient.list_database_names()


# In[42]:


airbib=data.to_dict("records")


# In[43]:


airbib


# In[44]:


data_base=CloudClient["airbib_list"]


# In[45]:


air=data_base["hostlist"]


# In[46]:


air.insert_many(airbib)


# In[46]:


for i in air.find():
    print (i)


# In[47]:


air.find_one()


# In[48]:


for i in air.find({},{"_id":0}):
    print(i)                          ### project the data without the "_id"


# In[49]:


for i in air.find():
    print(i)


# In[50]:


data.head()


# In[51]:


get_ipython().system('pip install seaborn')


# In[52]:


construction_total_year =data.groupby("Construction year")["Construction year"].count() ### 1


# In[53]:


print(construction_total_year)


# In[54]:


bar=px.bar(construction_total_year,
           x=construction_total_year.index,
           y=construction_total_year.values,
           title="NUMBER OF CONSTRUCTION PER YEAR"
          )
bar.update_layout(font=dict(size=10,color="black",family="Avenir"))
bar.show()


# In[55]:


room_type=data.groupby("room type")["price"].median()   ### 2


# In[56]:


room_type


# In[57]:


room_price=px.bar(room_type,
                  x=room_type.index,
                  y=room_type.values,
                  title="Rooms Avg price",
                  labels={"x":"Room type","y":"Average price"},
                  color_discrete_sequence=px.colors.sequential.Bluyl,
                  template="plotly_dark"
                 )
room_price.update_layout(font=dict(size=12,color="white",family="Avenir"))
room_price.show()


# In[58]:


room_available=data["room type"].value_counts() ### 3


# In[59]:


room_available


# In[60]:


room=px.bar(room_available,
            x=room_available.index,
            y=room_available.values,
            color=room_available.index,
            text=room_available.values,
            color_discrete_sequence=px.colors.sequential.PuBuGn,
            title="ROOM TYPE",
            template="plotly_dark"
           )
room.update_layout(
    xaxis_title = "Room type",
    yaxis_title = "count",
    font=dict(size=10,color="white",family="Avenir"))
room.show()


# In[61]:


neighbourhood_count=data["neighbourhood group"].value_counts()   ###4


# In[62]:


neighbourhood_count


# In[63]:


plt.figure(figsize=(5,5))
plt.pie(neighbourhood_count,
        labels=neighbourhood_count.index,
        autopct='%1.1f%%',
        startangle=140
       )
plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
plt.title('Neighborhood Group Distribution')
plt.show()


# In[64]:


neighbourhood_service_fees=data.groupby("neighbourhood")["service fee"].mean()   ### 5


# In[65]:


neighbourhood_service_fees


# In[66]:


servicefees_neighbourhood=px.bar(neighbourhood_service_fees,
                                 x=neighbourhood_service_fees.index,
                                 y=neighbourhood_service_fees.values,
                                 labels={"x":"Neighbourhood","y":"Average_price"},
                                 title="Neighbourhood_Avg_service_fees",
                                 template="plotly_dark"
                                )
servicefees_neighbourhood.update_layout(
    xaxis_title ="neighbourhood",
    yaxis_title = "price",
    font=dict(size=16,color="white",family="Avenir"))
servicefees_neighbourhood.show()


# In[67]:


data.head()


# In[68]:


neighbourhood_group_availability=data.groupby("neighbourhood group")["availability 365"].mean() ### 6


# In[69]:


neighbourhood_group_availability


# In[70]:


data["neighbourhood group"].unique()


# In[71]:


days_availability_neighbour=px.bar(neighbourhood_group_availability,
                                   x=neighbourhood_group_availability.index,
                                   y=neighbourhood_group_availability.values,
                                   title="Days Availability Of Neighbour",
                                   labels={"x":"neighbourhood group","y":"availability 365"},
                                   template="plotly_dark"
                                  )
days_availability_neighbour.update_layout(
    xaxis_title ="neighbourhood group",
    yaxis_title = "availability 365",
    font=dict(size=16,color="white",family="Avenir"))
days_availability_neighbour.show()


# In[72]:


get_ipython().system('pip install wordcloud')


# In[73]:


from wordcloud import WordCloud , STOPWORDS


# In[74]:


host_names = data["host name"].values


# In[94]:


print (host_names)


# In[80]:


price_place = px.scatter_mapbox(data,           ### 7
                                lat="lat",
                                lon="long",
                                opacity = 0.3, 
                                hover_name="neighbourhood group",
                                hover_data=["neighbourhood group", "price"],
                                color="price",
                                color_discrete_sequence=px.colors.sequential.PuBuGn,
                                title = "Price comparing to the place",
                                template = "plotly_dark",
                                zoom=20
                               )
price_place.update_layout(mapbox_style="open-street-map")
price_place.update_layout(margin={"r":0,"t":0,"l":0,"b":0},font = dict(size=17,family="Franklin Gothic"))
price_place.show()


# In[81]:


room_type_present = px.scatter_mapbox(data,                    ### 8
                                      lat="lat",
                                      lon="long",
                                      opacity = 0.3,
                                      hover_name="neighbourhood group",
                                      hover_data=["neighbourhood group", "room type"],
                                      color="room type",
                                      color_discrete_sequence=px.colors.qualitative.Dark24,
                                      title = "Price comparing to the place",
                                      template = "plotly_dark",
                                      zoom=10
                                     )
room_type_present.update_layout(mapbox_style="open-street-map")
room_type_present.update_layout(margin={"r":0,"t":0,"l":0,"b":0},font = dict(size=17,family="Franklin Gothic"))
room_type_present.show()


# In[82]:


data.dtypes


# In[83]:


cancellation_counts = data['cancellation_policy'].value_counts()        ### 9


# In[84]:


cancellation_counts


# In[85]:


plt.figure(figsize=(5,5))
plt.pie(cancellation_counts, 
        labels=cancellation_counts.index,
        autopct='%1.1f%%', 
        startangle=140
       )
plt.axis('equal')
plt.title('Cancellation Policy Distribution')
plt.show()

