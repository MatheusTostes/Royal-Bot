from getmac import get_mac_address as gma

def SetMac(macAddress, gc):
    tabSellers = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'G'+str(id+2)
    # print("coord :", coord)
    tabSellers.update_acell(coord, macAddress)

def desconectarConta(id, gc):
    plVendedores = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'F'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, 'não')

def conectarConta(id, gc, horas):
    plVendedores = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'F'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, 'sim ' + horas)

def obterNomeAba(id, dfSellers):
    nameTab = dfSellers["NomeAba"][id]
    return nameTab

def ValidSeller(valid, state, macSeller, Online, user, Business, ExpireDate, gc):
    macAddress = gma()
    if valid == "valido":
        if state == "ativado":
            # print(macSeller , macAddress)
            if len(str(macSeller)) < 3:
                SetMac(macAddress)
                macSeller = macAddress
                pass
            else:
                pass
            if macAddress == macSeller:     
                try:
                  desconectarConta(id, gc)
                  conectarConta(id, gc)
                  nameTab = obterNomeAba(id)
                  print("bem-vindo " + user + " ("+Business+")")
                  print("Assinatura expira em: ", ExpireDate)
                  # five = openFive()
                  # five.minimize_window()
                  # whatsApp = openWhatsApp()
                  # input(
                  #     "Aperte ENTER caso o whatsapp já esteja na tela de conversas!")
                  # whatsApp.minimize_window()
                  # application(ultimoCliente)
                except Exception as e:
                  print(e)
                return nameTab
            else:
                print(
                    "Máquina não reconhecida, contate o Suporte. Por segurança, a sessão será finalizada.")
        else:
            print("Sua conta expirou em: ", ExpireDate)
    else:
        print("Usuário ou senha inválido")
