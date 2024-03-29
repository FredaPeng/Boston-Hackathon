#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from google.colab import drive
drive.mount('/content/gdrive/')

get_ipython().system('pip install tabula-py')

get_ipython().system('pip install git+https://github.com/pdftables/python-pdftables-api.git')

import tabula
import pdftables_api
import pandas as pd
import os

path = '/content/gdrive/MyDrive/Colab Notebooks/Syllabus/'
file = os.listdir(path)[0]
print(file)

def main():
    """the main interaction loop"""
    convert_to_CSV(path + file) 
    
def convert_to_CSV(file):
    # Read a PDF File
    print(dir(tabula))
    df = tabula.read_pdf(file, pages='all')[0]
    # convert PDF into CSV
    tabula.convert_into(file, "syllabus.csv", output_format="csv", pages='all')

main()

import pandas as pd
df = pd.read_csv('syllabus.csv')
df = df.drop(df.iloc[:, 0:1],axis = 1)
df = df.dropna(how = "any")
df = df[df["topics, exams, assignments, and special dates"].str.contains('due|Midterm')==True]
df.to_csv("cleaned_sy.csv", index = False)

from datetime import date
df = pd.read_csv('cleaned_sy.csv')
today = date.today()
year = today.year

s = df["lecture dates"].apply(lambda x: str(x)+"/"+str(year))# insert year later

date = pd.to_datetime(s, infer_datetime_format=True) 

df.drop('lecture dates', 1, inplace=True)

df['Start date'] = date

df = df.rename(columns={df.columns[0]: 'Subject',df.columns[1]: 'Start date' })

df.to_csv(str(file) + ".csv", index = False)

shortened_name = file.split(' ')[0]
renamed_file = str(shortened_name) + ".csv"
path = f'/content/gdrive/MyDrive/Colab Notebooks/AfterClean/{renamed_file}'

with open(path, "w", 100, 'utf-8-sig') as f:
  df.to_csv(f)

