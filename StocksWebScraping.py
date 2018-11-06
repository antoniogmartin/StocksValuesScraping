import requests
import lxml.html as lh
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import datetime

def title_of_table( page ):
    page_content = BeautifulSoup(page.content)
    elem = page_content.find("a", attrs={"class":"textOverflow select"})
    text = elem.text
    text = text.replace('\n','') 
    text = text.replace('\r','') 
    text = text.replace(' ','')
    
    return text;
def writeInCSV( df, title ):
    now = datetime.datetime.now()
    current_date =now.strftime("%Y-%m-%d %H_%M")
    file_name = title + '_' + current_date + '.csv'
    df.to_csv(file_name)

    return file_name;

def get_table( url, size ):

    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    #Check the length of the first 12 rows
    [len(T) for T in tr_elements[:size]]

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
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]

        #If row is not of size 10, the //tr data is not from our table 
        if len(T)!=size:
            break

        #i is the index of our column
        i=0

        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 

            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1

            [len(C) for (title,C) in col]

    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    

    df = df.replace('\n',' ', regex=True) 
    df = df.replace('\r',' ', regex=True) 
    
    return transform_dataFrame(df);

def transform_dataFrame( df ):
    clean_dataFrame = pd.DataFrame(df['Nombre'])
    clean_dataFrame.columns = ['Hora']
    clean_dataFrame.columns = ['Stocks']
    clean_dataFrame.columns = ['Volumen']
    
    clean_dataFrame['Nombre'] = df['Nombre']
    clean_dataFrame['Hora'] = df['Hora']
    clean_dataFrame['Stocks'] = df['Último']
    clean_dataFrame['Volumen'] = df['Volumen']
    
    return clean_dataFrame;

url = ['http://www.infobolsa.es/acciones/ibex35', 'http://www.infobolsa.es/acciones/nasdaq' ]
size = [15,11]

for i in range(len(url)):    
    #to get the page
    page = requests.get(url[i])
    title = title_of_table( page )
    file_name = writeInCSV( get_table(url[i], size[i]), title )
