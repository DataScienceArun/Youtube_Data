from googleapiclient.discovery import build
import pandas as pd
import os





#function to call the api and retrive the trending video details based on the region code
def get_video(region):
    cat = pd.read_csv('category.csv',index_col ='id')

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

print(get_video('IN'))
#Let's map some of ISO 3166-1 alpha-2 country code with country names to use in the web app
location = pd.Series(data=['INDIA','USA','CANADA','AUSTRALIA','SOUTH AFRICA'],
                              index =['IN','US','CA','AU','ZA'])



#Code to get the category id and title. Since it is same for all the regions, we will be using this api

#call once and save the category details in a file to use it in filter
#request = youtube.videoCategories().list(
#        part="snippet",
#        regionCode="IN"
#    )
#response = request.execute()
#category =[]

#for item in response['items']:
#    cat = dict(id=item['id'],title = item['snippet']['title'])
#    category.append(cat)
#category = pd.DataFrame(category)
#category.to_csv('category.csv',index=False)


