import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

import pandas as pd
import numpy as np

from datetime import datetime

# Empty datasets
pagelinks=[]
title=[]
imglinks=[]
datetime=[] 
authorlinks=[]
PageContent=[]
content=[]
articletext=[]

for i in range (6,20):
   url="https://venturebeat.com/category/ai/entrepreneur/page/"+str(i)+"/"
   page=requests.get(url)
   soup = BeautifulSoup(page.content, 'html.parser')
   # Extracting all articles
   weblinks = soup.find_all("div",attrs={'class':'MainBlock'})[0].find_all('article')   

   for link in weblinks:
      pagelink=link.find("a",attrs={'class':'ArticleListing__title-link'})
      pagelinker=pagelink.get('href')
      pagelinks.append(pagelinker)
      titlelink=pagelink.get_text()
      title.append(titlelink)
      try:
        authorlink=link.find("a",attrs={'class':'ArticleListing__author'})
        author=authorlink.get_text()
      except:
         author='None'  
      authorlinks.append(author)
      imglink=link.find("img",attrs={'class':'ArticleListing__image wp-post-image'})
      img=imglink.get('src')
      imglinks.append(img)
      try:
        datetimelinks=link.find("time",attrs={'class':'ArticleListing__time'})
        dateandtime=datetimelinks.get_text()
      except:
         dateandtime='None'  
      datetime.append(dateandtime)
      
      url=pagelinker
      page=requests.get(url)
      soup=BeautifulSoup(page.text,'html.parser')
      paragraphcontent=soup.find("div",attrs={'class':'article-content'})
      maincontent=soup.find_all("p")[2:9]
      for p in maincontent:
        paragraphtext=p.get_text().strip()
        PageContent.append(paragraphtext)
      articletext.append(PageContent)    
      articlecontent = [''.join(article) for article in articletext]
      content.append(articlecontent)
      PageContent.clear()
      articletext.clear()
     
       
         
      data={'Title':title,'Author':authorlinks, 'DateTime':datetime,'Article':content, 'ArticleLink':pagelinks, 'imgLink':imglinks}
      news=pd.DataFrame(data=data)
      
      cols=['Title','Author','DateTime','Article','ArticleLink','imgLink']
      news=news[cols]

      filename="C:\\Users\\sailajamon\\Documents\\Python_Web_Scraper_funding_scrap\\PythonAIFundingDataset2.xlsx"
      wks_name="Data"

      writer=pd.ExcelWriter(filename)
      news.to_excel(writer, wks_name, index=False)
      writer.save()
   
    
      
