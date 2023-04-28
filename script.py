#This is Python web scraping and data analysis script that I developed in my previous workplace. 
#With it's aid I was able to streamline and perform data analysis work in a very short amount of time and saved many man hours.


#importing the necessary libraries and modules for the project

!sudo apt update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium
!pip install xlsxwriter

import requests
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta,date

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


 #Selenium's web driver object is initiated to query the website and download the data using the necessary parameters, inputted by the user.

from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("-headless")
options.add_argument("-no-sandbox")
options.add_argument("-disable-dev-shm-usage")

driver = webdriver.Chrome("chromedriver",options=options)

#Login information and sign in action is automated by uploading the login details.
driver.get('https://www.facebook.com/login/')
driver.find_element_by_name('email').send_keys('adminview')
driver.find_element_by_name('pass').send_keys('12345')
driver.find_element_by_name('signin').click()


#Start date of duration for which the data is to be retrieved.
start_date=input("Enter date in the form of YYYY-MM-DD")

#End date of duration for which the data is to be retrieved.
end_date=input("Enter date in the form of YYYY-MM-DD")


#Input the number of stores as No_of_stores = a
a=int(Input("Please give the count of stores"))
while a<28:

    #Creating Form element to interact with the options table and acquire the necessary data
    Form=Select(driver.find_element_by_xpath('/html/body/header/span[2]/form/select'))
    Form.select_by_index(a)

    #The driver requests data from the url, using the time period of the data necessary, with the added suffixes.
    driver.get("https://easysalonspasoftware.com/salon/itemised-report.php?sdate="+"start_date+"&edate="+"end_date")

    #The download data from page source is downloaded and interpreted, to download the first table as a dataframe.
    data=driver.page_source
    df= pd.read_html(data)[0]
    df.insert(loc=0, column='Store', value=stores[a])

    Workbook=Workbook.append(df,ignore_index=True)
    
    print(stores[a]+" 🗸 "+"\n")
    a=a+1



# Creating a dataframe with sales data based on transaction date and store billed in.
df1=Workbook.copy()
df1=df1.drop_duplicates(subset=['Store','Date of bill', 'Bill id',  'Contact','Paid']) 
df_sales=pd.pivot_table(df1,values='Paid',index='Store',columns='Date of bill', aggfunc='sum')
df_sales.reset_index(level=0, inplace=True)
print(dff1)

#Generating a list of odd numbers to map onto the stores in the dataframe df_sales
i=1
Odd_no_List=[]
while True:
  Odd_no_List.append(i)
  i+=2
  if i<a:
    break

df_sales['Index']=df_sales.assign(Odd_no_List)


# Creating a dataframe with Walkins data based on transaction date and store billed in.
#Note:

d2=Workbook.copy()
d2.insert(loc=11, column='Count', value=1)
df2=d2[~d2["Ser/Prod"].isin(["Membership"])]
df2=d2.drop_duplicates(subset=['Store','Date of bill', 'Client', 'Contact'])
df_walkins=pd.pivot_table(df2,values='Count',index='Store',columns='Date of bill', aggfunc='count')
df_walkins.reset_index(level=0, inplace=True)


#Generating a list of odd numbers to map onto the stores in the dataframe df_sales
i=0
Even_no_List=[]
while True:
  Odd_no_List.append(i)
  i+=2
  if i<a:
    break

df_walkins['Index']=df_walkins.assign(Even_no_List)


#Combining the sales and walkins dataframes for summarized sales and walkins data.
df=pd.concat([dff2,dff1])
print(dfo)
df.set_index("Index", inplace = True)
df_result=dfo.sort_index(axis = 0)

#Selecting customers that have Memberships
df_members=Workbook[Workbook["Ser/Prod"].isin(["Membership"])]


#Filtering customers who bought select Elevate products and summarizing their sales value.
options = ["Elevate hair cream","Elevate body lotion","Elevate hair spray"]

df3 = Workbook[Workbook['Ser/Prod.1'].isin(options)]
df3['Elevate Products'] = 1
df_elevate_sales=pd.pivot_table(df3,values='Elevate Products',index='Store',columns=['Ser/Prod.1','Date of bill'], aggfunc='count')


#Collating all the data into a Excel workbook using the xlsx writer module.
with pd.ExcelWriter("Itemized_report.xlsx") as writer: 
    da.to_excel(writer, sheet_name='Original',index=False)
    df_sales.to_excel(writer, sheet_name='Billings',index=False)
    df2_walkins.to_excel(writer, sheet_name='Walkins',index=False)
    df_members.to_excel(writer, sheet_name='Membership',index=False)
    df_elevate_sales.to_excel(writer, sheet_name='Elevate Product',index=False)


#Copy the Xlsx workbook to user's Google drive account. 
from google.colab import files
!cp /content/Itemized_report.xlsx /content/drive/MyDrive/sham
