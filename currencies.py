
# coding: utf-8

# In[112]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    str='http://www.infobolsa.es/divisas'
    page = requests.get(str)
    soup = BeautifulSoup(page.content)
    c_name=soup.findAll("li", {"class": "titCurren01"})
    c_val = soup.findAll("li", {"class": "txtCurren_ult equal"})
    c_date= soup.find("span",{"class": "dataCurren01"})
    print(c_date.text)
    i=0
    c_res=[]
    while(i<len(c_name)):
        c_pair=c_name[i].text.replace('\n','').split('/')
        c_res.append((c_pair[0],c_pair[1],c_val[i].text,c_date.text ))
        i+=1
    print(c_res)
    labels = ['CURRENCY_1','CURRENCY_2', 'VALUE','DATE']


pd.DataFrame.from_records(c_res, columns=labels)

