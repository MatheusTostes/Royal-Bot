import gspread
import time
from google.oauth2 import service_account

def Login(location):
    pathCredentials = location + "\\data\\credentials.json"
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
    json_file = pathCredentials
    try:
        credentials = service_account.Credentials.from_service_account_file(
            json_file)
        scoped_credentials = credentials.with_scopes(scopes)
        gc = gspread.authorize(scoped_credentials)
        planilha = gc.open("Solicitação de teste RoyalPlace (Respostas)")
        return planilha, gc
    except Exception as e:
        print("Não foi possível logar no banco de dados, tentando novamente!")
        print(e)
        time.sleep(3)
        Login(location)