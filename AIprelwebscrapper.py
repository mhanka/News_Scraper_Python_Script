import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

import pandas as pd
import numpy as np

from datetime import datetime

#Getting URL and making request to server
url="https://venturebeat.com/category/ai/" 
page=requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# Extracting all articles
weblinks = soup.find_all("div",attrs={'class':'story-river MainBlock__river'})[0].find_all('article')

# Empty datasets
pagelinks=[]
title=[]
imglinks=[]
datetime=[] 
authorlinks=[]

#Extracting datasets from articles
for link in weblinks:
   pagelink=link.find("a",attrs={'class':'ArticleListing__title-link'})
   pagelinker=pagelink.get('href')
   pagelinks.append(pagelinker)
   titlelink=pagelink.get_text()
   title.append(titlelink)
   authorlink=link.find("a",attrs={'class':'ArticleListing__author'})
   author=authorlink.get_text()
   authorlinks.append(author)
   imglink=link.find("img",attrs={'class':'ArticleListing__image wp-post-image'})
   img=imglink.get('src')
   imglinks.append(img)
   datetimelinks=link.find("time",attrs={'class':'ArticleListing__time'})
   dateandtime=datetimelinks.get_text()
   datetime.append(dateandtime)

#Reading oldDatasets from excel file
#NOTE: Replace the absolute hardcoded filepath with a relative filepath for running the cron job for the script
olddata=pd.read_excel('C:\\Users\\sailajamon\\Documents\\Python_Web_Scraper\\AI_Datasets1.xlsx', engine='openpyxl')
data={'Title':title,'Author':authorlinks,'DateOfPublication':datetime,'ArticleLink':pagelinks,'imgLink':imglinks}
#Creating dataframes from exracted data
news=pd.DataFrame(data=data)
cols=['Title','Author','DateOfPublication','ArticleLink','imgLink']
news=news[cols]

currentNews=olddata.append(news)
# Drop duplicate news which contains older news articles and replace with new articles
currentNews.drop_duplicates(subset='Title', keep=False, inplace=True)
currentNews.reset_index(inplace=True)
currentNews.drop(labels='index', axis=1, inplace=True)

# Similiarly also replace this file path with a relative file path for the cron job for running the script
filename= 'C:\\Users\\sailajamon\\Documents\\Python_Web_Scraper\\AI_Datasets1.xlsx'
wks_name= 'Data'

# Writing datasets onto the excel
writer=pd.ExcelWriter(filename)
currentNews.to_excel(writer, wks_name, index=False)

writer.save()

     
      
  
    
       

    
