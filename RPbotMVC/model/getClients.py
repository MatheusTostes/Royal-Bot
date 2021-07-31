import time
import pandas as pd

def GetClients(planilha, sellerTab):
    print("Buscando clientes...", end = "\r")
    try:
        tabClients = planilha.worksheet(sellerTab)
        dataClients = tabClients.get_all_records()
        dfClients = pd.DataFrame(dataClients)
        print("Clientes encontrados.")
        return dfClients
    except Exception as e:
        print(e)
        print("Clientes não recebidos, tentando novamente...", end = "\r")
        time.sleep(3)
        GetClients(planilha, sellerTab)