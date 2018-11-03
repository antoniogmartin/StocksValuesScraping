#!/usr/bin/env python
# coding: utf-8

# In[16]:


import requests
import lxml.html as lh
import pandas as pd


# In[17]:


url='http://www.infobolsa.es/acciones/ibex35'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')


# In[18]:


#Check the length of the first 12 rows
[len(T) for T in tr_elements[:15]]
tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    f'{i}:"{name}"'
    col.append((name,[]))


# In[19]:


#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=15:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


# In[34]:


[len(C) for (title,C) in col]

Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)
"\n\r".rstrip("\n\r")

df = df.replace('\n',' ', regex=True) 
df = df.replace('\r',' ', regex=True) 
df
       

    


# In[ ]:



