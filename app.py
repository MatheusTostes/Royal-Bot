print("========================== RP Bot ==========================")

versionAtual = '1.1.1'

import pandas as pd
import time
import gspread
from google.oauth2 import service_account

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os
location = os.getcwd()
print(location)
pathCredentials = location + "\\data\\credentials.json"

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
        
    return planilha, gc

funcLogin = login()
planilha = funcLogin[0]
gc = funcLogin[1]

def receberPlanilhas(planilha):     
    try:
        abaClientes = planilha.worksheet("Respostas do Formulário 1")
        dadosClientes = abaClientes.get_all_records()
        dfClientes = pd.DataFrame(dadosClientes)
    except Exception as e:
        print(e)
        print("Clientes não recebidos, tentando novamente!")
        
    try:     
        abaAtendidos = planilha.worksheet("Folha2")
        dadosAtendidos = abaAtendidos.get_all_records()
        dfAtendidos = pd.DataFrame(dadosAtendidos)
        listaAtendidos = []
        for i in dfAtendidos["Atendidos"]:
            listaAtendidos.append(i)
    except:    
        print("Clientes atendidos não recebidos, tentando novamente!")
      
    try:
        abaVendedores = planilha.worksheet("Vendedores")
        dadosVendedores = abaVendedores.get_all_records()
        dfVendedores = pd.DataFrame(dadosVendedores)
    except Exception as e:
        print(e)
        print("Vendedores não encontrados, tentando novamente!")
        
    planilhaAtendidos = planilha.worksheet('Folha2')

    return dfClientes, listaAtendidos, dfVendedores, planilhaAtendidos   

planilhas = receberPlanilhas(planilha)
dfClientes = planilhas[0]
listaAtendidos = planilhas[1]
dfVendedores = planilhas[2]
planilhaAtendidos =  planilhas[3]

def validar(login, senha, dfVendedores):
    validar = ''
    estado = ''
    ExpireDate = ''
    Business = ''
    user = ''

    if login in dfVendedores["User"].to_list():
        for i in dfVendedores["User"]:
            if login == i:
                id = (dfVendedores[dfVendedores['User'] == login].index.values)[0]
                if senha == dfVendedores["Password"][id]:
                    user = dfVendedores["User"][id]
                    Business = dfVendedores["Business"][id]
                    ExpireDate = dfVendedores["ExpireDate"][id]
                    Online = dfVendedores["Online"][id]
                    print("Logado")                   
                    estado = dfVendedores['Estado'][id]
                    print(estado)
                    validar = "valido"
                    break
                else:
                    #print("Senha inválida")
                    validar = "invalido"
            else:
                validar = "invalido"
    else:
        #print("Usuário Inválido")
        validar = "invalido"
        estado = "desativado"
    return validar, estado, ExpireDate, Business, user, Online, id

pathGecko = location + "\\data\\geckodriver.exe"

def obterHora():
    seconds = time.strftime('%S', time.localtime())
    hour = time.strftime('%H', time.localtime())
    hour = int(hour)
    hour = hour+6
    if hour >= 24:
        hour = hour - 24
    hour = str(hour)
    if len(hour) == 1:
        hour = '0'+ hour
    elif len(hour) == 0:
        hour = '00'
    minute = str(time.strftime('%M', time.localtime()))
    if len(minute) == 1:
        minute = '0'+ minute
    elif len(minute) == 0:
        minute = '00'
    dataEndTest = str(hour) + ":" + minute

    return dataEndTest, hour, minute, seconds

def abrirWhats():
    print("Abrindo WhatsApp Web")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(userDataDir)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver2 = webdriver.Chrome(pathChrome, options=options)
        driver2.get("https://web.whatsapp.com/")
        #driver2.maximize_window()
    except:
        print("Não foi possível abrir o WhatsApp Web, tentando novamente!")
        time.sleep(3)
        abrirWhats()
    return driver2

def loginFive(driver):
  try:
    input("Pressione ENTER quando estiver na tela de login do painel")
    print('logando five')
    driver.find_element_by_name('username').send_keys("matheustostes")
    driver.find_element_by_name('password').send_keys('Matheus123')
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/div/div/div/form/div[4]/div/button').click()
    time.sleep(1)
  except Exception as e:
    print(e)
    input("Verifique a tela de login do painel")
    loginFive(driver)
    pass

def abrirFive():
    options = webdriver.ChromeOptions()
    options.add_argument(userDataDir2)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(pathChrome2, options=options)
    driver.get("http://painel.c-pro.site/auth/sign-in")
    time.sleep(1)

    loginFive(driver)
    return driver

pathChrome = location + "\\data\\chromedriver.exe"
pathChrome2 = location + "\\data\\chromedriver2.exe"
userDataDir = "user-data-dir=" + location + "\\data"
userDataDir2 = "user-data-dir2=" + location + "\\data"

def dadosFive(texto):
    texto = texto.replace("username: ", "")
    texto = texto.replace("Senha: ", "")
    texto = texto.split(" | ")
    #print(texto)
    return texto

def criarTesteFive():
    try:

        horarioTeste = obterHora()
        hour = horarioTeste[1]
        minute = horarioTeste[2]
        seconds = horarioTeste[3]

        driver.get("http://painel.c-pro.site/users/add_trial")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/form/div[1]/div[1]/input').send_keys("rp"+hour+minute+seconds)
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/form/div[1]/div[2]/input').send_keys("p2pgold")
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys("TESTE 6H COMPLETO", Keys.ENTER)         
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/form/div[2]/div/button[2]').click()
        time.sleep(2)
        print("Capturando dados")
        texto = driver.find_element_by_id('swal2-content').text
        #print(texto)
        if 'username' not in texto and 'Senha' not in texto:
            criarTesteFive()
        time.sleep(2)
        textoCliente = dadosFive(texto)
        linkM3U = "http://5ce.co/get.php?username="+textoCliente[0]+"%26password="+textoCliente[1]+"%26type=m3u_plus%26output=ts"
        textoCliente.append(linkM3U)
    except Exception as e:
        print(e)
        time.sleep(2)
        criarTesteFive()
    return textoCliente

def enviar():
    print("Enviando mensagem")
    try:
        driver2.find_element_by_class_name("_4sWnG").click()
    except:
        print("Não foi possível enviar a mensagem, tentando novamente!")
        time.sleep(3)
        enviar()

def mensagemPadrao(i, mensagem, telefone):
    print("Gerando mensagem padrão")
    try:
        linkWhats = ('https://web.whatsapp.com/send?phone=55' + str(telefone) + '&text=' + mensagem)
        #print(linkWhats)

        driver2.get(linkWhats)
        time.sleep(5)
        enviar()
        time.sleep(3)
        relogio =  driver2.find_elements_by_css_selector('[aria-label=" Pendente "]')
        #print(relogio)
        if len(relogio) > 1:        
            print("O WhatsApp pode estar desconectado, tentando novamente!")
            mensagemPadrao(i, mensagem, telefone)
    except Exception as e:
        print("Não foi possível gerar mensagem padrão, tentando novamente!")
        print(e)
        #mensagemPadrao(i, mensagem, telefone)
    
def adicionarAtendido(planilhaAtendidos, i):
    print("Adicionando status de atendido ao cliente")
    try:
        lista = [i]
        planilhaAtendidos.append_row(lista, value_input_option='USER_ENTERED')
    except:
        print("Não foi possivel adicionar o status de atendido ao cliente, tentando novamente!")
        adicionarAtendido(planilhaAtendidos, i)

def definirUltCliente(ultimoCliente, i):
    ultimoCliente = i
    return ultimoCliente

def alterarListaP2P(driver):
    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/button[1]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="datatabled"]/tbody/tr[1]/td[10]/div/button[2]/i').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="datatabled"]/tbody/tr[1]/td[10]/div/div/a[2]').click()

def application(ultimoCliente):
    try:
        print("Iniciando o bot")
        planilhas = receberPlanilhas(planilha)
        dfClientes = planilhas[0]
        listaAtendidos = planilhas[1]
        dfVendedores = planilhas[2]

        def validar(login, senha, dfVendedores):
            validar = ''
            estado = ''
            ExpireDate = ''
            Business = ''
            user = ''

            if login in dfVendedores["User"].to_list():
                for i in dfVendedores["User"]:
                    if login == i:
                        id = (dfVendedores[dfVendedores['User'] == login].index.values)[0]
                        if senha == dfVendedores["Password"][id]:
                            user = dfVendedores["User"][id]
                            Business = dfVendedores["Business"][id]
                            ExpireDate = dfVendedores["ExpireDate"][id]
                            Online = dfVendedores["Online"][id]
                            print("logado")                   
                            estado = dfVendedores['Estado'][id]
                            print(estado)
                            validar = "valido"
                            break
                        else:
                            #print("Senha inválida")
                            validar = "invalido"
                    else:
                        validar = "invalido"
            else:
                #print("Usuário Inválido")
                validar = "invalido"
                estado = "desativado"
            return validar, estado, ExpireDate, Business, user, Online, id

        validar = validar(login, senha, dfVendedores)

        if validar[5] == 'sim ' + horas:
            if validar[1] == "ativado":
                planilhaAtendidos =  planilhas[3]
                print("Buscando clientes...")
                for i in range(ultimoCliente, len(dfClientes)):  
                    if i not in listaAtendidos:  
                        adicionarAtendido(planilhaAtendidos, i)
                        telefone = str(dfClientes.iloc[i][numeroWhats])
                        print("telefone")
                        telefone = telefone.replace("+","")
                        telefone = telefone.replace(" ","")
                        telefone = telefone.replace("-","")
                        if telefone.isdecimal() == False:
                            telefone = ""
                        if telefone[:2] == "55":
                            telefone = telefone[2:]
                        if len(telefone) == 11 or len(telefone) == 10: 
                            ultimoCliente = definirUltCliente(ultimoCliente, i)
                            print("Cliente: ", i)       

                            horarioTeste = obterHora()
                            dataEndTest = horarioTeste[0]

                            textoCliente = criarTesteFive()
                            print('textoCliente: ', textoCliente)
                            print("--criado texto cliente")

                            nome = dfClientes.iloc[i]["Nome"]
                            nome = nome.capitalize()

                            if dfClientes.iloc[i][colAparelho] == 'Smart - Samsung 4K':                       
                                aplicativo = 'Duplex Play'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na *Samsung modelo 4K* é o *Duplex Play*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Baixe o Aplicativo Duplex Play na sua Smart TV_ %0a*Passo 2:* _Abra o aplicativo, anote o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 3:* _Por meio de *qualquer dispositivo* entre no site: https://edit.duplexplay.com/_ %0a _acesse com o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 4:* _Clique no botão "Add playlist" e insira nos respectivos campos:_ %0a _*Playlist name =>* ROYAL PLACE - GOLD_ %0a _*Playlist Url (.M3U or .M3U8) =>* ' +textoCliente[2]+ '_ %0a _*Marque a caixa* "Não sou um robô"_ %0a _*Clique em SAVE*_ %0a%0aRealizadas estas etapas, basta clicar em Refresh ou Atualizar o seu Duplex Play %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO seu teste acaba às: *' +dataEndTest+ '*'
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)                                
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")
                            
                            if dfClientes.iloc[i][colAparelho] == 'Smart - Samsung antiga':                       
                                aplicativo = 'STB'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na *Samsung modelo antigo* é o *Smart STB*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Ligue a TV e abra a janela "Configurações" pressionando o botão "Configurações" no controle remoto da TV._ %0a*Passo 2:* _Vá para a guia Geral e selecione Rede na lista de opções._ %0a*Passo 3:* _Você pode verificar se a TV está conectada à Internet em "Status da rede"._ %0a*Passo 4:* _Selecione as configurações de IP e vá para as configurações de DNS._ %0a*Passo 5:* _Você deve alterar as configurações de DNS de entrada manualmente._ %0a*Passo 6:* _Na configuração DNS você verá o servidor DNS atual, altere para 198.50.224.145_ %0a*Passo 7:* _Abra o Aplicativo STB Smart e utilize os dados a seguir:_ %0a%0a*Login:* ' +textoCliente[0]+ '%0a*Senha:* ' +textoCliente[1]+ ' %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")
                            
                            if dfClientes.iloc[i][colAparelho] == 'Smart - LG 4K' or dfClientes.iloc[i][colAparelho] == 'Smart - LG antiga':                       
                                aplicativo = 'Smarters Players ou Duplex'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na *LG modelo 4K* é o *Duplex Play* ou Smarters Players, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Smarters Players* %0aROYAL PLACE - GOLD %0a*Login :* ' +textoCliente[0]+ ' %0a*Senha :* ' +textoCliente[1]+ ' %0a*URL:* http://nplay.top %0a%0a*Duplex Play* %0a*Passo 1:* _Baixe o Aplicativo Duplex Play na sua Smart TV_ %0a*Passo 2:* _Abra o aplicativo, anote o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 3:* _Por meio de *qualquer dispositivo* entre no site: https://edit.duplexplay.com/_ %0a _acesse com o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 4:* _Clique no botão "Add playlist" e insira nos respectivos campos:_ %0a _*Playlist name =>* ROYAL PLACE - GOLD_ %0a _*Playlist Url (.M3U or .M3U8) =>* ' +textoCliente[2]+ '_ %0a _*Marque a caixa* "Não sou um robô"_ %0a _*Clique em SAVE*_ %0a%0aRealizadas estas etapas, basta clicar em Refresh ou Atualizar o seu Duplex Play %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                            
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            if dfClientes.iloc[i][colAparelho] == 'Smart - Philco, Philips, Sony, Panasonic':                       
                                aplicativo = 'SSIPTV'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na sua *Smart TV* é o *SSIPTV*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Abra o aplicativo SSIPTV > Configurações > Obter código_ %0a*Passo 2:* _Acesse o site http://ss-iptv.com/en/users/playlist_ %0a*Passo 3:* _Digite o seu código e clicar em Adicionar dispositivo (ADD DEVICE)_ %0a*Passo 4:* _External Playlists > ADD ITEM_ %0a*Displayed Name:* _ROYAL PLACE - GOLD_ %0a*Source:* ' +textoCliente[2]+ ' %0a*OK* %0a%0a*Passo 5:* _SAVE_ %0a*Passo 6:* _Clique em Atualizar no seu aplicativo SSIPTV e abra a pasta ROYAL PLACE - GOLD_ %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'                
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            if dfClientes.iloc[i][colAparelho] == 'TV BOX' or dfClientes.iloc[i][colAparelho] == 'Celular Android':                       
                                aplicativo = 'Royal Place ou Smarters Players'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar no seu aparelho é o *Royal Place P2P*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Link direto Play Store: https://play.google.com/store/apps/details?id=nd.ndapps.royalplacep2p%26hl=pt_BR%26gl=US* %0a*Link downloads site: https://www.royalplace.com.br/download*%0a%0a*Passo 1:* Abra o aplicativo *Royal Place P2P* %0a*Passo 2:* Insira os dados a seguir: %0a*Usuário:* ' +textoCliente[0]+ ' %0a*Senha:* ' +textoCliente[1]+ ' %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")
                                
                                print("Alterando tipo de lista de IPTV para P2P")
                                alterarListaP2P(driver)

                            if dfClientes.iloc[i][colAparelho] == 'Chromecast':                       
                                aplicativo = 'GSE IPTV'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar no seu *Chromecast* é o *GSE IPTV*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* Abra o aplicativo *Chromecast* e adicione uma nova lista com os dados a seguir: %0a*Playlist Name:* Royal Place - GOLD %0a*Description:* Teste %0a*http://...:* ' +textoCliente[2]+ ' %0a*Pressione OK* %0a*Passo 2:* Selecione a nova lista e aguarde o carregamento. %0a*passo 3:* Conecte o celular à televisão %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'                 
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            if dfClientes.iloc[i][colAparelho] == 'iPhone':                       
                                aplicativo = 'Smarters Players'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar no *iPhone* é o Smarters Players, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Smarters Players* %0aROYAL PLACE - GOLD %0a*Login :*' +textoCliente[0]+ ' %0a*Senha :*' +textoCliente[1]+ ' %0a*URL:* http://nplay.top %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                            
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            if dfClientes.iloc[i][colAparelho] == 'Android TV' or dfClientes.iloc[i][colAparelho] == 'Outro':
                                aplicativo = 'Smarters Players'
                                print(nome, aplicativo)
                                
                                mensagem = 'Olá *'+ nome +'*! %0aO seu dispositivo necessita de atendimento especializado, por favor responda a esta mensagem e aguarde um atendente. %0a%0aCaso tenha algum aplicativo instalado no dispositivo pode tentar inserir alguns destes dados se requisitado: %0a%0a*Usuário:* ' +textoCliente[0]+ ' %0a*Senha:* ' +textoCliente[1]+ '%0aLink .M3U:* ' +textoCliente[2]+ '. %0a%0aEm caso de dúvida, aguarde o suporte.'              
                                mensagem = mensagem.replace( " ","+" )
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            time.sleep(2)
                            print("Aguardando novos clientes")
                        else:
                            print("Número de telefone inválido: ", telefone, dfClientes.iloc[i]["Nome"])
                
                time.sleep(30)
                application(ultimoCliente)    
            else:
                print("Sua assinatura expirou! Contate o suporte.")
        else:
            print("A sua conta foi acessada em outra sessão")
    except Exception as e:
        print("Confira sua conexão com a internet e contate o suporte técnico!")
        print(e)
        application(ultimoCliente)

news = gc.open("Solicitação de teste RoyalPlace (Respostas)").get_worksheet(3)
versionNew = news.acell('B2').value

print("====================== Versão: ", versionAtual ," =====================")

def verificarAtt():
    if versionAtual != versionNew:
        print("Há uma nova atualização disponível. Para obte-la feche o bot e execute o arquivo update.exe")
verificarAtt()

login = str(input("Usuario vendedor: "))
senha = str(input("Senha vendedor: "))

validar = validar(login, senha, dfVendedores)

UserAndPass = validar[0]
ExpireDate = validar[2]
Business = validar[3].title()
Name = validar[4].title()
Online = validar[5]
id = validar[6]

def desconectarConta(id):
    plVendedores = gc.open("Solicitação de teste RoyalPlace (Respostas)").get_worksheet(2)
    # print("id: ", id)
    coord = 'F'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, 'não')

def horas():
    hour = time.strftime('%H', time.localtime())
    minute = time.strftime('%M', time.localtime())
    seconds = time.strftime('%M', time.localtime())
    horas = str(hour) + ":" + str(minute) + ":" + str(seconds)
    return horas

def conectarConta(id):
    plVendedores = gc.open("Solicitação de teste RoyalPlace (Respostas)").get_worksheet(2)
    # print("id: ", id)
    coord = 'F'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, 'sim ' + horas)

def iniciar():
    print("bem-vindo "+ Name + " ("+Business+")")
    print("Assinatura expira em: ", ExpireDate)
    driver = abrirFive()
    input("Aperte ENTER quando o painel da Five estiver logado na conta!")
    driver2 = abrirWhats()
    input("Aperte ENTER caso o whatsapp já esteja na tela de conversas!")

    return driver, driver2

ultimoCliente = 0
colAparelho = "Qual o seu aparelho?"
numeroWhats = "Número de WhatsApp com DDD (Exemplo: 27 998851972)"

if UserAndPass == "valido":
    if validar[1] == "ativado":
        if Online == 'não':
            horas = horas()
            print(horas)
            conectarConta(id)
            iniciar = iniciar()
            driver = iniciar[0]
            driver2 = iniciar[1]
            application(ultimoCliente)
        else:
            print("Sua conta já se encontra conectada a outra sessão!")
            forceDC = str(input("Deseja forçar a desconexão? Digite 1 para 'sim' ou 2 para 'não: "))
            if forceDC == '1':
                desconectarConta(id)
                horas = horas()
                conectarConta(id)
                iniciar = iniciar()
                driver = iniciar[0]
                driver2 = iniciar[1]
                application(ultimoCliente)
            else:
                print("Não é possível executar duas sessões na mesma conta!")
    else:
        print("Sua conta expirou em: ", ExpireDate)
else:
    print("Usuário ou senha inválido")

