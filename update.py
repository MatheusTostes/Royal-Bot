import pandas as pd
import time
import gspread
from google.oauth2 import service_account

import requests
import os
location = os.getcwd()
print(location)
pathCredentials = location + "\\app-main - Copia\\data\\credentials.json"

scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
json_file = pathCredentials

def login():
    print("Logando no banco de dados")
    try:
        credentials = service_account.Credentials.from_service_account_file(json_file)
        scoped_credentials = credentials.with_scopes(scopes)
        gc = gspread.authorize(scoped_credentials)
        planilha = gc.open("Solicitação de teste RoyalPlace (Respostas)")
    except Exception as e:
        print("Não foi possível logar no banco de dados, tentando novamente!") 
        print(e)
        time.sleep(3)
        login()
        
    return planilha

planilha = login() 

def receberPlanilhas(planilha):     
    try:
        abaNews = planilha.worksheet("news")
        dadosNews = abaNews.get_all_records()
        dfNews = pd.DataFrame(dadosNews)
    except Exception as e:
        print(e)
        print("Clientes não recebidos, tentando novamente!")

    return dfNews   

dfNews = receberPlanilhas(planilha)

try:
    os.remove(location + '\\att.zip')
except: 
    pass

url = dfNews["News"][0]

myfile = requests.get(url)

open(location + '/att.zip', 'wb').write(myfile.content)

import zipfile
with zipfile.ZipFile(location + '\\att.zip', 'r') as zip_ref:
    zip_ref.extractall(location)


