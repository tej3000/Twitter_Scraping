# Twitter_Scraping

This " #Twitter_Scraping " repository consists of a python file which was created to do Twitter data scraping (Web Scraping) web application.

For doing this we used a extensive modules which are listed below:

1. import streamlit as st
2. import pandas as pd
3. import numpy as np
4. import snscrape.modules.twitter as snstwl
5. import pymongo
6. from datetime import datetime

Firstly, required data collection from the user is done using 'Streamlit input' functions.

After receiving the inputs we will now scrape the twitter for data using keyword and tweet_count limit. For this 'snscrape module' and 'TwitterSearchScraper' function are used.

A DataFrame is created using 'pandas library' and the scraped data is stored in it. 

As per user's requirement data is uploaded into a database using 'MongoDB'. To upload the data into database first the raw_data which is in Series format needed to be converted into int or str. So, normal 'if... else....' condition is used.

To be able to access the file from database, unique key value like {“Search_keyword+current Timestamp” :}  is given everytime data is uploaded.

For downloading the data into a required file format 'download_button' from 'Streamlit' library is used.
