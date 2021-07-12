print("========================== RP Bot ==========================")

import pandas as pd
import re
import time
import gspread
from google.oauth2 import service_account

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

pd.set_option('display.max_rows', 350)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 100)

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
        
    return planilha

planilha = login() 

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
    return validar, estado, ExpireDate, Business, user

pathGecko = location + "\\data\\geckodriver.exe"

def loginBlessed(driver):
    driver.find_element_by_id('username').send_keys("royalplacebot")
    driver.find_element_by_id('password').send_keys('996317547')
    driver.find_element_by_class_name("gradient").click()
    time.sleep(3)

def abrirBlessed():
    print("Abrindo painel Blessed")
    try:
        os.system('taskkill /IM "Firefox.exe" /F')
    except:
        pass
    try:
        blessed = "http://blessedserver.net/"

        option = Options()
        option.headless = True
        driver = webdriver.Firefox(executable_path=pathGecko, options=option) 
        driver.maximize_window()
        driver.get(blessed)
        time.sleep(3)
        try:
            print("Logando na conta bot da Blessed")
            loginBlessed(driver)
        except:
            time.sleep(3)
            print("Não foi possível logar na conta bot, tentando novamente!")
            loginBlessed()
    except: 
        print("Não foi possível abrir o painel, tentando novamente!")
        driver.close()
        time.sleep(3)
        abrirBlessed()
    return driver

pathChrome = location + "\\data\\chromedriver.exe"
userDataDir = "user-data-dir=" + location + "\\data"

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

def dadosBlessed():
    print("Recebendo dados Blessed")
    try: 
        dadosNovoTeste = driver.find_element_by_class_name("fast-message").text
    except: 
        print("Não foi possível receber os dados Blessed, tentando novamente!")
        print("Verifique a disponibilidade do servidor de teste!")
        try:
            driver.find_element_by_xpath("/html/body/div[2]/div/nav/div/div[1]/ul/li[12]/ul/li[6]/a").click();
        except:
            time.sleep(3)
            dadosBlessed()
    time.sleep(3)
    return dadosNovoTeste

def criarTesteBlessed():
    print("Criando teste")
    try:
        driver.find_element_by_xpath("/html/body/div[2]/div/nav/div/div[1]/ul/li[12]/a").click();
        print('---menu lateral aberto---')
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[2]/div/nav/div/div[1]/ul/li[12]/ul/li[6]/a").click();
        print('---pagina de teste aberto---')
        time.sleep(5)
        try: 
            dadosNovoTeste = dadosBlessed()
            print(dadosNovoTeste)

            usuario = re.findall(r'acesso:\nUsuario: (.+?)\nSenha: ', dadosNovoTeste)
            senha = re.findall(r'\nSenha: (.+?)\nLista M3U: ', dadosNovoTeste)
            listaM3u = re.findall(r'\nLista M3U: (.+?)\nDNS STB ', dadosNovoTeste)
            DNS = re.findall(r'\nDNS STB (.+?)\nDNS PRINCIPAL', dadosNovoTeste)
            DNSprincipal = re.findall(r'\nDNS PRINCIPAL\n(.+?)\nSSIPTV:', dadosNovoTeste)
            SSIPTV = re.findall(r'\nSSIPTV:(.+?)\nWeb player:', dadosNovoTeste)
            webPlayer = re.findall(r'\nWeb player:\n(.+?)/\n\nLink epg:', dadosNovoTeste)
            epg = re.findall(r'/\n\nLink epg:(.+?)\n\n', dadosNovoTeste)
            vcapp = re.findall(r'\n\n(.+?)\nObrigado Por Ser Nosso Cliente', dadosNovoTeste)

            driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/button[3]").click();

            if len(usuario) < 1:
                print(usuario)
                print("Dados não obtidos")
                print("DADOS DO TESTE: ", dadosNovoTeste)
                time.sleep(2)
                criarTesteBlessed() 
        except:
            time.sleep(3)
            dadosNovoTeste = dadosBlessed()    
    
    except:
        print("Não foi possível criar teste, tentando novamente!")
        #driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/button[3]").click();
        driver.quit()
        abrirBlessed()
        time.sleep(3)
        criarTesteBlessed()
    return usuario, senha, listaM3u, DNS, DNSprincipal, SSIPTV, webPlayer, epg, vcapp

def enviar():
    print("Enviando mensagem")
    try:
        driver2.find_element_by_class_name("_4sWnG").click()
    except:
        print("Não foi possível enviar a mensagem, tentando novamente!")
        time.sleep(3)
        enviar()
        
def ativarSSIPTV():
    try:    
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\Mathe\Desktop\RPbot teste\data")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        ativarSs = webdriver.Chrome(
        pathChrome, chrome_options=options)
        ativarSs.get("http://ss-iptv.com/en/users/playlist")

        ativarSs.find_element_by_id("inptConnectionCodeInput").send_keys("E6ZZQC")
        ativarSs.find_element_by_id("btnAddDevice").click()
    except:
        time.sleep(3)
        ativarSSIPTV()
    return ativarSs

def mensagemPadrao(i, mensagem, telefone):
    print("Gerando mensagem padrão")
    try:
        linkWhats = ('https://web.whatsapp.com/send?phone=55' + str(telefone) + '&text=' + mensagem)
        print(linkWhats)
        driver2.get(linkWhats)
        time.sleep(5)
        enviar()
        time.sleep(3)
        relogio =  driver2.find_elements_by_css_selector('[aria-label=" Pendente "]')
        print(relogio)
        if len(relogio) > 1:        
            print("O WhatsApp pode estar desconectado, tentando novamente!")
            mensagemPadrao(i, mensagem, telefone)
    except:
        print("Não foi possível gerar mensagem padrão, tentando novamente!")
        mensagemPadrao(i, mensagem, telefone)
    
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

def repetirTeste():
    try:
        textoCliente = criarTesteBlessed()
    except:
        time.sleep(3)
        abrirBlessed()
        textoCliente = criarTesteBlessed()
    
    return textoCliente

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
            return validar, estado, ExpireDate, Business, user

        validar = validar(login, senha, dfVendedores)
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
                        textoCliente = repetirTeste()
                        print('textoCliente: ', textoCliente)
                        print("--criado texto cliente")

                        hour = time.strftime('%H', time.localtime())
                        hour = int(hour)
                        hour = hour+3
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

                        if dfClientes.iloc[i][colAparelho] == 'Smart - Samsung 4K':                       
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'Duplex Play'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na *Samsung modelo 4K* é o *Duplex Play*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Baixe o Aplicativo Duplex Play na sua Smart TV_ %0a*Passo 2:* _Abra o aplicativo, anote o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 3:* _Por meio de *qualquer dispositivo* entre no site: https://edit.duplexplay.com/_ %0a _acesse com o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 4:* _Clique no botão "Add playlist" e insira nos respectivos campos:_ %0a _*Playlist name =>* ROYAL PLACE - BRONZE_ %0a _*Playlist Url (.M3U or .M3U8) =>* ' +textoCliente[2][0]+ '_ %0a _*Marque a caixa* "Não sou um robô"_ %0a _*Clique em SAVE*_ %0a%0aRealizadas estas etapas, basta clicar em Refresh ou Atualizar o seu Duplex Play %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO seu teste acaba às: *' +dataEndTest+ '*'
                            mensagem = mensagem.replace( " ","+" )
                            try:
                                mensagemPadrao(i, mensagem, telefone)
                                time.sleep(3)
                            except:
                                print("Erro ao enviar mensagem Padrao")
                        
                        if dfClientes.iloc[i][colAparelho] == 'Smart - Samsung antiga':                       
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'STB'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na *Samsung modelo antigo* é o *Smart STB*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Ligue a TV e abra a janela "Configurações" pressionando o botão "Configurações" no controle remoto da TV._ %0a*Passo 2:* _Vá para a guia Geral e selecione Rede na lista de opções._ %0a*Passo 3:* _Você pode verificar se a TV está conectada à Internet em "Status da rede"._ %0a*Passo 4:* _Selecione as configurações de IP e vá para as configurações de DNS._ %0a*Passo 5:* _Você deve alterar as configurações de DNS de entrada manualmente._ %0a*Passo 6:* _Na configuração DNS você verá o servidor DNS atual, altere para 198.50.224.145_ %0a*Passo 7:* _Abra o Aplicativo STB Smart e utilize os dados a seguir:_ %0a%0a*Login:* ' +textoCliente[0][0]+ '%0a*Senha:* ' +textoCliente[1][0]+ ' %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                            mensagem = mensagem.replace( " ","+" )
                            try:
                                mensagemPadrao(i, mensagem, telefone)
                                time.sleep(3)
                            except:
                                print("Erro ao enviar mensagem Padrao")
                        
                        if dfClientes.iloc[i][colAparelho] == 'Smart - LG 4K' or dfClientes.iloc[i][colAparelho] == 'Smart - LG antiga':                       
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'Smarters Players ou Duplex'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na *LG modelo 4K* é o *Duplex Play* ou Smarters Players, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Smarters Players* %0aROYAL PLACE - BRONZE %0a*Login :* ' +textoCliente[0][0]+ ' %0a*Senha :* ' +textoCliente[1][0]+ ' %0a*URL:* http://nplay.top %0a%0a*Duplex Play* %0a*Passo 1:* _Baixe o Aplicativo Duplex Play na sua Smart TV_ %0a*Passo 2:* _Abra o aplicativo, anote o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 3:* _Por meio de *qualquer dispositivo* entre no site: https://edit.duplexplay.com/_ %0a _acesse com o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 4:* _Clique no botão "Add playlist" e insira nos respectivos campos:_ %0a _*Playlist name =>* ROYAL PLACE - BRONZE_ %0a _*Playlist Url (.M3U or .M3U8) =>* textoCliente[2][0]_ %0a _*Marque a caixa* "Não sou um robô"_ %0a _*Clique em SAVE*_ %0a%0aRealizadas estas etapas, basta clicar em Refresh ou Atualizar o seu Duplex Play %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                        
                            mensagem = mensagem.replace( " ","+" )
                            try:
                                mensagemPadrao(i, mensagem, telefone)
                                time.sleep(3)
                            except:
                                print("Erro ao enviar mensagem Padrao")

                        if dfClientes.iloc[i][colAparelho] == 'Smart - Philco, Philips, Sony, Panasonic':                       
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'SSIPTV'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar na sua *Smart TV* é o *SSIPTV*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Abra o aplicativo SSIPTV > Configurações > Obter código_ %0a*Passo 2:* _Acesse o site http://ss-iptv.com/en/users/playlist_ %0a*Passo 3:* _Digite o seu código e clicar em Adicionar dispositivo (ADD DEVICE)_ %0a*Passo 4:* _External Playlists > ADD ITEM_ %0a*Displayed Name:* _ROYAL PLACE - BRONZE_ %0a*Source:* ' +textoCliente[2][0]+ ' %0a*OK* %0a%0a*Passo 5:* _SAVE_ %0a*Passo 6:* _Clique em Atualizar no seu aplicativo SSIPTV e abra a pasta ROYAL PLACE - BRONZE_ %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'                
                            mensagem = mensagem.replace( " ","+" )
                            try:
                                mensagemPadrao(i, mensagem, telefone)
                                time.sleep(3)
                            except:
                                print("Erro ao enviar mensagem Padrao")

                        if dfClientes.iloc[i][colAparelho] == 'TV BOX' or dfClientes.iloc[i][colAparelho] == 'Celular Android':                       
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'Royal Place ou Smarters Players'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar no seu aparelho é o *Royal Place*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Link direto Play Store: https://play.google.com/store/apps/details?id=com.royalplcnew.ml* %0a*Link downloads site: https://www.royalplace.com.br/download*%0a%0a*Passo 1:* Abra o aplicativo *Royal Place* e selecione a opção *BRONZE* %0a*Passo 2:* Insira os dados a seguir: %0a*Usuário:* ' +textoCliente[0][0]+ ' %0a*Senha:* ' +textoCliente[1][0]+ ' %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                            mensagem = mensagem.replace( " ","+" )
                            try:
                                mensagemPadrao(i, mensagem, telefone)
                                time.sleep(3)
                            except:
                                print("Erro ao enviar mensagem Padrao")

                        if dfClientes.iloc[i][colAparelho] == 'Chromecast':                       
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'GSE IPTV'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar no seu *Chromecast* é o *GSE IPTV*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* Abra o aplicativo *Chromecast* e adicione uma nova lista com os dados a seguir: %0a*Playlist Name:* Royal Place - Bronze %0a*Description:* Teste %0a*http://...:* ' +textoCliente[2][0]+ ' %0a*Pressione OK* %0a*Passo 2:* Selecione a nova lista e aguarde o carregamento. %0a*passo 3:* Conecte o celular à televisão %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'                 
                            mensagem = mensagem.replace( " ","+" )
                            try:
                                mensagemPadrao(i, mensagem, telefone)
                                time.sleep(3)
                            except:
                                print("Erro ao enviar mensagem Padrao")

                        if dfClientes.iloc[i][colAparelho] == 'iPhone':                       
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'Smarters Players'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aO aplicativo indicado pra utilizar no *iPhone* é o Smarters Players, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Smarters Players* %0aROYAL PLACE - BRONZE %0a*Login :*' +textoCliente[0][0]+ ' %0a*Senha :*' +textoCliente[1][0]+ ' %0a*URL:* http://nplay.top %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' +dataEndTest+ '*'
                        
                            mensagem = mensagem.replace( " ","+" )
                            try:
                                mensagemPadrao(i, mensagem, telefone)
                                time.sleep(3)
                            except:
                                print("Erro ao enviar mensagem Padrao")

                        if dfClientes.iloc[i][colAparelho] == 'Android TV' or dfClientes.iloc[i][colAparelho] == 'Outro':
                            nome = dfClientes.iloc[i]["Nome"]
                            aplicativo = 'Smarters Players'
                            print(nome, aplicativo)
                            
                            mensagem = 'Olá *'+ nome +'*! %0aResponda a esta mensagem e aguarde o atendimento.'              
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
    except Exception as e:
        print("Confira sua conexão com a internet e contate o suporte técnico!")
        print(e)
        application(ultimoCliente)

login = str(input("Usuario vendedor: "))
senha = str(input("Senha vendedor: "))

validar = validar(login, senha, dfVendedores)

ExpireDate = validar[2]
Business = validar[3].title()
Name = validar[4].title()

if validar[0] == "valido":
    if validar[1] == "ativado":
        print("bem-vindo "+ Name + " ("+Business+")")
        print("Assinatura expira em: ", ExpireDate)
        driver = abrirBlessed()
        driver2 = abrirWhats()
        wpAberto = input("APERTE 'ENTER' CASO O WHATS APP WEB JÁ ESTEJA NA TELA DE CONVERSAS")
        colAparelho = "Qual o seu aparelho?"
        numeroWhats = "Número de WhatsApp com DDD (Exemplo: 27 998851972)"
        ultimoCliente = 0
        
        application(ultimoCliente)
    else:
        print(validar[0])
else:
    print("Usuário ou senha inválido")

