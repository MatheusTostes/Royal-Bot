import time
import pandas as pd

def GetClients(planilha, NomeAba):
    print("Buscando vendedores...", end = "\r")
    try:
        tabClients = planilha.worksheet(NomeAba)
        dataClients = tabClients.get_all_records()
        dfClients = pd.DataFrame(dataClients)
        print("Vendedores encontrados.")
        return dfClients
    except Exception as e:
        print(e)
        print("Clientes não recebidos, tentando novamente...", end = "\r")
        time.sleep(3)
        GetClients(planilha, NomeAba)