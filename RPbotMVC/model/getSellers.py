import time
import pandas as pd

def GetSellers(planilha):
    print("Buscando vendedores...", end = "\r")
    try:
        tabSellers = planilha.worksheet("Sellers")
        dataSellers = tabSellers.get_all_records()
        dfSellers = pd.DataFrame(dataSellers)
        print("Vendedores encontrados.")
        return dfSellers
    except Exception as e:
        print(e)
        print("Vendedores não encontrados, tentando novamente...", end = "\r")
        time.sleep(3)
        GetSellers(planilha)