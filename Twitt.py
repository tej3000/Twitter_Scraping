import streamlit as st
import pandas as pd
import numpy as np
import snscrape.modules.twitter as snstwl
import pymongo
from datetime import datetime

st.sidebar.title("Welcome! Let me help you to do some Twitter scraping :smile:")                   #Heading for the Web Application

with st.form(key = 'Twitter_form'):
    search_keyword = st.text_input('What do you want to search for?',value = 'teja')
    number = st.number_input('How many tweets do you want to get',1,100000,step=5)
    start_date = st.date_input('Enter the start date for scraping')
    end_date = st.date_input('Enter the End date for scraping')
    data_base = st.radio('Do you want to upload the above data into Database ?',['Yes','No'])
    download = st.radio('And also do you want to download the above data in CSV or JSON format?',['Yes','No'])
    submit_button = st.form_submit_button(label = 'Scrap the data')
    
    if submit_button:
        tweets_data = []
        for i, tweets in enumerate(snstwl.TwitterSearchScraper('{} since:{} until:{}'.format(search_keyword,start_date,end_date)).get_items()):
            if i >= number:
                break
            tweets_data.append([tweets.date, tweets.id, tweets.content, tweets.user.username, tweets.replyCount, tweets.retweetCount, tweets.lang.upper(), tweets.source, tweets.likeCount])
        tw_data = pd.DataFrame(tweets_data, 
                            columns = ('Date','ID','Content','Username','Reply_Count','Retweet_Count','Language','Source','Like_Count'))
    
        st.table(tw_data)
        
        if data_base == 'Yes':
            data_dic = []
            for i in range(len(tw_data.index)):
                col_data = {}
                for j in range(len(tw_data.columns)):
                    if type(tw_data.iloc[i,j]) == np.int64:
                        col_data[tw_data.columns[j]] = int(tw_data.iloc[i,j])
                    elif type(tw_data.iloc[i,j]) == str:
                        col_data[tw_data.columns[j]] = str(tw_data.iloc[i,j])
                    else:
                        col_data[tw_data.columns[j]] = tw_data.iloc[i,j]
                data_dic.append(col_data)
                
            client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
            mydb = client['Twitter']
            my_col = mydb['Twi_scr_da']
            m = {}
            m[search_keyword+'@'+str(datetime.now())]= data_dic
            my_col.insert_one(m)
            st.text('Data Successfully uploaded into database')
            
if download == 'Yes':
    tweets_data = []
    for i, tweets in enumerate(snstwl.TwitterSearchScraper('{} since:{} until:{}'.format(search_keyword,start_date,end_date)).get_items()):
        if i >= number:
            break
        tweets_data.append([tweets.date, tweets.id, tweets.content, tweets.user.username, tweets.replyCount, tweets.retweetCount, tweets.lang.upper(), tweets.source, tweets.likeCount])
    tw_data = pd.DataFrame(tweets_data, 
                            columns = ('Date','ID','Content','Username','Reply_Count','Retweet_Count','Language','Source','Like_Count'))

    st.download_button('Download CSV File',tw_data.to_csv(),file_name = 'scraped_data.csv',mime = 'text/csv')
    st.download_button('Download Json File',tw_data.to_csv(),file_name = 'scraped_data.json',mime = 'application/json')
