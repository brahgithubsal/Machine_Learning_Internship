# import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
import plotly.express as px 
import datetime
import haversine as hs
# function names
print("\033[1m\nthe available filtring functions are:\033[0m\n")
print("read_dataset")
print("get_time")
print("get_date")
print("get_time")
print("get_route")
print("data_filtering")
print("input_data_filtering")
print("segmentation")
print("filter_and_segment")
print("input_filter_and_segment")
print("process_dataset")
print("input_process_dataset")
print("\033[1m\nthe available visualization functions are:\033[0m\n")
print("map_with_marker")
print("map_with_segments")
# read and format dataset function
def read_dataset(file_name):
    df= pd.read_table(file_name,sep=",",header=0)
    df.columns = ['CIN','latitude','longitude','SPEED','ENGINE_RPM','ENGINE_LOAD','AmbientAirTemp','ThrottlePos','insFuel','valX','valY','valZ','zone','place','time']
    df['time'] = np.array(df['time'], dtype=np.datetime64)
    df['date'] = [d.date() for d in df['time']]
    df['hour'] = [d.time() for d in df['time']]
    return df
# filter and segment functions
## data prepare function
def data_prepare(df):
    df['AmbientAirTemp'] = df['AmbientAirTemp'].str.replace(r'\D+', '')
    df['AmbientAirTemp'] = pd.to_numeric(df['AmbientAirTemp'], errors='coerce').astype('float')
    df['ENGINE_RPM'] = pd.to_numeric(df['ENGINE_RPM'], errors='coerce').astype('float')    
    df['ENGINE_LOAD'] = df['ENGINE_LOAD'].str.replace(r'\D+', '')
    df['ENGINE_LOAD'] = pd.to_numeric(df['ENGINE_LOAD'], errors='coerce').astype('float')    
    df['ThrottlePos'] = df['ThrottlePos'].str.replace(r'\D+', '')
    df['ThrottlePos'] = pd.to_numeric(df['ThrottlePos'], errors='coerce').astype('float') 
    return df
## filter time function
def get_time(data,time_start_client, time_end_client):
    time_start_client_arr = time_start_client.split(':')
    heur_start = int(time_start_client_arr[0])
    minute_start = int(time_start_client_arr[1])
    second_start = int(time_start_client_arr[2])
    time_end_client_arr =time_end_client.split(':')
    heur_end = int(time_end_client_arr[0])
    minute_end = int(time_end_client_arr[1])
    second_end = int(time_end_client_arr[2])
    start_time = datetime.time(heur_start,minute_start,second_start)
    end_time = datetime.time(heur_end, minute_end, second_end)   
    condition = (data['hour'] >= start_time) & (data['hour'] <= end_time)
    data = data.loc[condition]
    return data
## filter date function
def get_date(data,start_date, end_date):
    start_date_new = start_date.split('-')
    year_start = int(start_date_new [0])
    month_start = int(start_date_new [1])
    day_start = int(start_date_new [2])
    end_date_new = end_date.split('-')
    year_end = int(end_date_new [0])
    month_end = int(end_date_new [1])
    day_end = int(end_date_new [2])
    start_data = datetime.date(year_start, month_start, day_start)
    end_data = datetime.date(year_end, month_end, day_end)     
    condition = (data['date'] >= start_data) & (data['date'] <= end_data)
    data = data.loc[condition]
    return data
## filter route function
def get_route(data,route):
    route
    h = data.loc[data['place'] == route]   
    return h
## data filtering function
def data_filtering(data,starting_time,ending_time,starting_date,ending_date,route):
    df = get_time(data,starting_time,ending_time)
    df= get_date(df,starting_date,ending_date)
    df= get_route(df,route)
    return df
## input data filtering function
def input_data_filtering(data):
    starting_time = input("please give your starting time in this form hh:mm:ss \n")
    ending_time = input("Now, please give your ending time in this form hh:mm:ss \n")
    starting_date = input("For the date, please give your starting date in this form yyyy-mm-dd \n")
    ending_date = input("Now, please give your ending date in this form yyyy-mm-dd \n")
    route= input("Finally, please select your route like this example: GP13 \n")
    try: 
        df= data_filtering(data,starting_time,ending_time,starting_date,ending_date,route)
    except Exception:
        print("\033[1m\nPLEASE CHECK ENTRY VALUES, SOMETHING WENT WRONG\033[0m\n")
        df = None
    return df
## segmentation function
def segmentation(data, location):
    road = data[data['place']==location]
    road = road.dropna(subset=['place'])
    print("Cleaning data from Nan values in the place column")
    road = road.reset_index(drop=True)
    road['begin segments']=""
    road['end segments']=""
    list_distance,index_list, segments =[] ,[],[]
    for index1, index2 in zip(range(0,len(road)-1),range(1,len(road))):
        loc1 = (road['latitude'][index1],road['longitude'][index1])
        loc2 =(road['latitude'][index2],road['longitude'][index2])
        distance = hs.haversine(loc1,loc2,unit=hs.Unit.METERS)
        if distance >= 50 :
            segments.append(index1)
            segments.append(index2)
            road.loc[index1,'begin segments']="yes"
            road.loc[index2,'end segments']="yes"
        elif distance < 50:
            index_list.append(index1)
            list_distance.append(distance)
            somme = sum(list_distance)
            if somme >= 50:
                segments.append(index_list[0])
                segments.append(index2)
                road.loc[index_list[0],'begin segments'] ="yes"
                road.loc[index2,'end segments']= "yes"
                list_distance.clear()
                index_list.clear()
    road.loc[index1,'begin segments']= "yes"
    road.loc[len(road)-1,'end segments']= "yes"
    return road
## filter and segement function
def filter_and_segment(data,starting_time,ending_time,starting_date,ending_date,route):
    df = get_time(data,starting_time,ending_time)
    df= get_date(df,starting_date,ending_date)
    df= get_route(df,route)
    df= segmentation(df,route)
    return df
## input filter and segment function
def input_filter_and_segment(data):
    starting_time = input("please give your starting time in this form hh:mm:ss \n")
    ending_time = input("Now, please give your ending time in this form hh:mm:ss \n")
    starting_date = input("For the date, please give your starting date in this form yyyy-mm-dd \n")
    ending_date = input("Now, please give your ending date in this form yyyy-mm-dd \n")
    route= input("Finally, please select your route like this example: GP13 \n")
    try: 
        df= filter_and_segment(data,starting_time,ending_time,starting_date,ending_date,route)
    except Exception:
        print("\033[1m\nPLEASE CHECK ENTRY VALUES, SOMETHING WENT WRONG\033[0m\n")
        df = None
    return df
## process dataset function
def process_dataset(file_name,starting_time,ending_time,starting_date,ending_date,route):
    df = read_dataset(file_name)
    df_final = filter_and_segment(df,starting_time,ending_time,starting_date,ending_date,route)
    return df_final
## process dataset from input function
def input_process_dataset():
    file_name = input("please enter the name of the dataset file\n")
    data = read_dataset(file_name)
    df_final = input_filter_and_segment(data)
    return data

# visualization functions 
## visualize map with marker
def map_with_marker(data):
    n = folium.Map(location=[data.latitude.mean(), data.longitude.mean()], zoom_start=10)
    colors = ['green', 'blue', 'yellow', 'orange', 'red' ]
    for i in range(0,len(data)):
        html=f"""
            <h1> {data.iloc[i]['date']}</h1>
            <h1> {data.iloc[i]['hour']}</h1>
            <p>your location is road GP13:</p>
            """
        iframe = folium.IFrame(html=html, width=220, height=220)
        popup = folium.Popup(iframe, max_width=1000)
        if  data.iloc[i]['SPEED'] < 30:
            folium.Marker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
            popup=popup, tooltip=data.iloc[i]['place'], icon=folium.Icon(color=colors[0])).add_to(n)
        elif data.iloc[i]['SPEED'] > 30 and data.iloc[i]['SPEED']  < 50:
            folium.Marker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
            popup=popup, tooltip=data.iloc[i]['place'], icon=folium.Icon(color=colors[1])).add_to(n)
    return n
## visualize map with segments
def map_with_segments(data,vitesse1=30,vitesse2=50,vitesse3=90,vitesse4=120,marker_type='line'):
    m5 = folium.Map(location=[data.latitude.mean(), data.longitude.mean()])
    colors = ['darkred', 'orange', 'red', 'green']
    loc1, loc2, loc3, loc4 = [], [], [], [] 
    begin_segment_index = []
    end_segment_index = []
    for i in range(0,len(data)):
        if data.iloc[i]['begin segments']=="yes":
            begin_segment_index.append(i)
        if data.iloc[i]['end segments']=="yes":
            end_segment_index.append(i)
    for i in range(0,len(begin_segment_index)):
        segment_speed = data.iloc[begin_segment_index[i]:end_segment_index[i]]["SPEED"].mean()
        if segment_speed < vitesse1:
            loc1.append((data["latitude"][begin_segment_index[i]],data["longitude"][begin_segment_index[i]]))
            loc1.append((data["latitude"][end_segment_index[i]],data["longitude"][end_segment_index[i]]))
            if marker_type == 'circle':
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[0]).add_to(m5)
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[0]).add_to(m5)
            elif marker_type =='line':
                folium.PolyLine(loc1, color=colors[0], tooltip=data['place'][0]).add_to(m5)
            loc1.clear()
        elif segment_speed > vitesse1 and segment_speed < vitesse2:
            loc2.append((data["latitude"][begin_segment_index[i]],data["longitude"][begin_segment_index[i]]))
            loc2.append((data["latitude"][end_segment_index[i]],data["longitude"][end_segment_index[i]]))
            if marker_type == 'circle':
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[1]).add_to(m5)
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[1]).add_to(m5)
            elif marker_type == 'line':
                folium.PolyLine(loc2, color=colors[1], tooltip=data['place'][0]).add_to(m5)
            loc2.clear()
        elif segment_speed > vitesse2 and segment_speed < vitesse3:
            loc3.append((data["latitude"][begin_segment_index[i]],data["longitude"][begin_segment_index[i]]))
            loc3.append((data["latitude"][end_segment_index[i]],data["longitude"][end_segment_index[i]]))
            if marker_type == 'circle':
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[2]).add_to(m5)
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[2]).add_to(m5)
            elif marker_type == 'line':
                folium.PolyLine(loc3, color=colors[2], popup=data['place'][0]).add_to(m5)
            loc3.clear()
        elif segment_speed > vitesse3 and segment_speed < vitesse4:
            loc4.append((data["latitude"][begin_segment_index[i]],data["longitude"][begin_segment_index[i]]))
            loc4.append((data["latitude"][end_segment_index[i]],data["longitude"][end_segment_index[i]]))
            if marker_type == 'circle':
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[3]).add_to(m5)
                folium.CircleMarker(location=[data.iloc[begin_segment_index[i]]['latitude'], data.iloc[begin_segment_index[i]]['longitude']], tooltip=data['place'][0], popup=data['place'][0], color=colors[3]).add_to(m5)
            elif marker_type =='line':
                folium.PolyLine(loc4, color=colors[3], popup=data['place'][0]).add_to(m5)
            loc4.clear()
        return m5
 