import os

def SellerData(login, password, dfSellers):
    valid = ''
    state = ''
    ExpireDate = ''
    Business = ''
    user = ''

    if login in dfSellers["User"].to_list():
        for i in dfSellers["User"]:
            if login == i:
                id = (dfSellers[dfSellers['User']
                      == login].index.values)[0]
                if password == dfSellers["Password"][id]:
                    user = dfSellers["User"][id]
                    Business = dfSellers["Business"][id]
                    ExpireDate = dfSellers["ExpireDate"][id]
                    Online = dfSellers["Online"][id]
                    state = dfSellers['Estado'][id]
                    
                    macSeller = dfSellers['Mac'][id]
                    phoneSeller = dfSellers['Telefone'][id]
                    valid = "valido"
                    print('Usuário: '+ state +'. Data de expiração: '+ ExpireDate)
                    return valid, state, ExpireDate, Business, user, Online, id, macSeller, phoneSeller
                else:
                    #print("Senha inválida")
                    valid = "invalido"
                    print("Usuário e/ou senha incorreto/os")
                    os._exit(0)
            else:
                valid = "invalido"
    else:
        #print("Usuário Inválido")
        valid = "invalido"
        state = "desativado"
        print("Usuário e/ou senha incorreto/os")
        os._exit(0)