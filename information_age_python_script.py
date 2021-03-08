import requests
from bs4 import BeautifulSoup
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
articletext=[]
textcontent=[]


for i in range (11,21):
    url="https://www.information-age.com/topics/artificial-intelligence/page/"+str(i)+"/"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    weblinks=soup.find_all("div", attrs={'class':'container body-text'})
    for linkly in weblinks:
        linking=linkly.find_all("div", attrs={'class':'card h-100'})
        continue
    for link in linking:
        try:
           pagelink=link.find("div",attrs={'class':'story-body'}).find("a")
           linker=pagelink.get("href")
        except:
           linker="None"    
        try:   
           titlelink=link.find("h3",attrs={'class':'story-title'}).get_text().strip()
        except:
            titlelink="None"
        try:       
           datetimelink=link.find("span",attrs={'class':'p1_home-date'}).get_text().strip()
        except:
           datetimelink="None"
        try:       
           imglink=link.find("img",attrs={'img-fill divider'})
           img=imglink.get("src")
        except:
           img="None"   
        datetime.append(datetimelink)
        pagelinks.append(linker)
        title.append(titlelink)
        imglinks.append(img)

        url=linker
        try:   
           page=requests.get(url)
        except MissingSchema:
            continue   
        soup=BeautifulSoup(page.text,'html.parser')
        try:
           authordetail=soup.find("div",attrs={'class':'post-author'}).find("a").get_text().strip()
        except:
           authordetail="None"    
        authorlinks.append(authordetail)
        try:
           articlecontent=soup.find("div",attrs={'class':'col-md-6 post-story'}).find_all("p")
        except:
           articlecontent="None"    
        for p in articlecontent:
            try:
               paratext=p.get_text().strip()
            except:
               paratext="None"    
            textcontent.append(paratext)
        articletext.append(textcontent)
        pagedata= [''.join(article) for article in articletext]
        PageContent.append(pagedata)
        textcontent.clear()
        articletext.clear()    


        olddata=pd.read_excel('C:\\Users\\sailajamon\\Documents\\Information_age_Scraper\\Information_age_dataset_sample.xlsx', engine='openpyxl')
        data={'Title':title,'Author':authorlinks, 'DateTime':datetime,'Article':PageContent, 'ArticleLink':pagelinks, 'imgLink':imglinks}
        news=pd.DataFrame(data=data)
      
        cols=['Title','Author','DateTime','Article','ArticleLink','imgLink']
        news=news[cols]

        CurrentData=olddata.append(news)
        filename="C:\\Users\\sailajamon\\Documents\\Information_age_scraper\\Information_age_dataset_sample.xlsx"
        wks_name="Data"

        writer=pd.ExcelWriter(filename)
        news.to_excel(writer, wks_name, index=False)
        writer.save()