#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests 
from geopy.geocoders import Nominatim   
import folium                           
from folium import plugins              
import openrouteservice                 
from openrouteservice import convert
import geopy.distance                   
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


ride_data = pd.read_csv('final_data_volume.csv')


# In[3]:


ride_data.info()


# In[4]:


pd.set_option('display.max_columns', 500)


# In[5]:


ride_data.count()


# In[6]:


def generate_map(map_location, map_style, start_lat_col, start_long_col, start_color, end_lat_col, end_long_col, end_color):
      
    folium_map = folium.Map(location=map_location,
                            zoom_start=11,
                            tiles=map_style)
    
    for index, row in ride_data.iterrows():  
        
        folium.CircleMarker(location=(row[start_lat_col],
                                      row[start_long_col]),
                            color=start_color,
                            radius=5,
                            weight=1,
                            fill=True).add_to(folium_map)
        
        folium.CircleMarker(location=(row[end_lat_col],
                                      row[end_long_col]),
                            color=end_color,
                            radius=5,
                            weight=1,
                            fill=True).add_to(folium_map)
        
    return folium_map


# In[7]:


ride_data = ride_data[np.isfinite(ride_data['pla'])]
ride_data = ride_data[np.isfinite(ride_data['plo'])]

ride_data = ride_data[np.isfinite(ride_data['dla'])]
ride_data = ride_data[np.isfinite(ride_data['dlo'])]

ride_data = ride_data[np.isfinite(ride_data['maplat'])]
ride_data = ride_data[np.isfinite(ride_data['maplong'])]


# In[8]:


generate_map([40.7128, -74.008],"cartodbpositron","pla", "plo",'#0A8A9F',"maplat", "maplong",'#f68e16')


# In[10]:


def get_paths(df):
    
    path_list = []
    
    for index, row in df.iterrows():
        
            coords = [(row['plo'],row['pla']),(row['maplong'],row['maplat'])]
            print(coords)
            
            client = openrouteservice.Client(key='5b3ce3597851110001cf6248c196e442e9f148a9a1863fa5c168e7bc') 
            geometry = client.directions(coords)['routes'][0]['geometry']
            decoded = convert.decode_polyline(geometry)
            reverse = [(y,x) for x,y in decoded['coordinates']]        
            path_list.append(reverse)
            print(index)
    
        
    return path_list
    


# In[12]:


routes = get_paths(ride_data)


# In[13]:


def plot_paths(paths,map_data):
    
    for path in paths:
        
        line = folium.PolyLine(
            path,
            weight=1,
            color='#0A8A9F'
        ).add_to(map_data)
    
    return map_data


# In[14]:


map_data = generate_map([40.7128, -74.008],"cartodbpositron","pla","plo",'#0A8A9F',"maplat","maplong",'#f68e56')


# In[73]:


plot_paths(routes, map_data)


# In[ ]:




