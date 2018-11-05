import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    str='http://www.infobolsa.es/divisas'
    page = requests.get(str)
    soup = BeautifulSoup(page.content)
    c_name=soup.findAll("li", {"class": "titCurren01"})
    c_val = soup.findAll("li", {"class": "txtCurren_ult"})
    c_date= soup.find("span",{"class": "dataCurren01"})
    i=0
    c_res=[]
    if (len(c_val)>=len(c_name)):
        while(i<len(c_name)):
            c_pair=c_name[i].text.replace('\n','').split('/')
            
            c_res.append((c_pair[0],c_pair[1],c_val[i].text,c_date.text ))
            i+=1
    else:
        while(i<len(c_val)):
            c_pair=c_name[i].text.replace('\n','').split('/')
            
            c_res.append((c_pair[0],c_pair[1],c_val[i].text,c_date.text ))
            i+=1
    labels = ['CURRENCY_1','CURRENCY_2', 'VALUE','DATE']

df=pd.DataFrame.from_records(c_res, columns=labels)
print(df)
