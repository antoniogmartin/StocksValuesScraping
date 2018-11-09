'''
Created on 31 oct. 2018

@author: aguzman
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.robotparser
from time import sleep


if __name__ == '__main__':
    str='http://www.infobolsa.es/divisas'

    i=0
    n_times=0
    c_res=[]
#     rp = urllib.robotparser.RobotFileParser()
#     rp.set_url("http://www.google.es/robots.txt")
#     rp.read()
#     print(rp)
#     rrate = rp.request_rate("*")
#     print("R: ",rp.can_fetch("*","https://www.google.es/search/about"))
#     print("R: ",rp.can_fetch("*","https://www.google.es/alerts/"))
#     
    while(n_times<=1):
        page = requests.get(str)
        soup = BeautifulSoup(page.content)
        c_name=soup.findAll("li", {"class": "titCurren01"})
        c_val = soup.findAll("li", {"class": "txtCurren_ult"})
        c_date= soup.find("span",{"class": "dataCurren01"})
        if (len(c_val)>=len(c_name)):        
            while(i<len(c_name)):
                c_pair=c_name[i].text.replace('\n','').split('/')
                
                c_res.append((c_pair[0],c_pair[1],c_val[i].text,c_date.text,c_date.previous_element ))
                i+=1
        else:
            while(i<len(c_val)):
                c_pair=c_name[i].text.replace('\n','').split('/')
                
                c_res.append((c_pair[0],c_pair[1],c_val[i].text,c_date.text,c_date.previous_element))
                i+=1
        n_times+=1
        i=0
        print(n_times)
        if(n_times<=1):
            sleep(0)
            
    labels = ['CURRENCY_1','CURRENCY_2', 'VALUE','DATE','HOUR']

    df=pd.DataFrame.from_records(c_res, columns=labels)
    print(df)
    df.to_csv("~/Escritorio/currencies_stock.csv", sep=',', encoding='utf-8')
