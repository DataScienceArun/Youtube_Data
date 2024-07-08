import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import os


location = pd.Series(data=['INDIA','USA','CANADA','AUSTRALIA','SOUTH AFRICA'],
                              index =['IN','US','CA','AU','ZA'])
cat = pd.read_csv('category.csv',index_col ='id')
def get_video(region):

#creating the trending video api service, for more information please refer https://developers.google.com/youtube/v3
    api_key = os.env['youtube_api_key']
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = build(api_service_name, api_version, developerKey=api_key)
    df_video=[]
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode=region,
        maxResults=10)
    response=request.execute()
    for item in response['items']:
        df = dict(video_id = item['id'],
              title = item['snippet']['title'],
              views = int(item['statistics']['viewCount']),
              likes = int(item['statistics']['likeCount']),
              comments = int(item['statistics']['commentCount']),
              region = 'Global' if region is None else region,
              category_id = int(item['snippet']['categoryId']),
              category = cat.loc[int(item['snippet']['categoryId'])]['title'],
              date = item['snippet']['publishedAt'],
              thumbnail = item['snippet']['thumbnails']['high']['url'],
              url = f"https://www.youtube.com/watch?v={item['id']}",
              channel_name = item['snippet']['channelTitle'],
              description = item['snippet']['description'])
        df_video.append(df)
    return pd.DataFrame(df_video)

#Caching the api data to avoid making api calls everytime user interacts with the app
@st.cache
def fetch_get_video(region_code):
    return get_video(region_code)


#creating a function to return like/view counts as k(kilo) and M(million)
def transform(counts):
    if counts < 1000:
        return counts
    elif counts < 1000000:
        return f"{round(counts/1000,1)}k"
    else:
        return f"{round(counts/1000000,1)}M"



st.title('Trending YouTube Videos')

region = st.sidebar.radio('Select Region',['Global','INDIA','USA','CANADA','AUSTRALIA','SOUTH AFRICA'])
category_filter = st.sidebar.multiselect('Filter by Category',cat['title'].tolist())
sort_by = (st.sidebar.radio('Sort by',['Trend','Date','Likes','Views']))
trending_videos = fetch_get_video(location.index[location == region][0] if region != 'Global' else None)


filter_videos = trending_videos.copy()

if category_filter:
    filter_videos = filter_videos[filter_videos['category'].isin(category_filter)]

if sort_by !='Trend':
    filter_videos = filter_videos.sort_values(by=sort_by.lower(),ascending=False)



col1,col2= st.columns([2,1])

for i,video in filter_videos.iterrows():
    with col1:
        st.image(video['thumbnail'],caption=f" {transform(video['views'])} Views  ❤️ {transform(video['likes'])}  ",width=450)
        st.write(f"[{video['title']}]({video['url']})")



