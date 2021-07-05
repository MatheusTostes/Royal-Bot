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
    if login in dfVendedores["User"].to_list():
        for i in dfVendedores["User"]:
            if login == i:
                id = (dfVendedores[dfVendedores['User'] == login].index.values)[0]
                if senha == dfVendedores["Password"][id]:
                    print("logado")                   
                    estado = dfVendedores['Estado'][id]
                    print(estado)
                    validar = "valido"
                    break
                else:
                    validar = "invalido"
            else:
                validar = "invalido"
    else:
        validar = "invalido"
        estado = "desativado"
    return validar, estado

pathGecko = location + "\\data\\geckodriver.exe"

def loginBlessed(driver):
    driver.find_element_by_id('username').send_keys("royalplacebot")
    driver.find_element_by_id('password').send_keys('996317547')
    driver.find_element_by_class_name("gradient").click()
    time.sleep(3)

def abrirBlessed():
    print("Abrindo painel Blessed")
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
        driver.find_element_by_xpath("/html/body/div[2]/div/nav/div/div[1]/ul/li[12]/ul/li[6]/a").click();
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
        time.sleep(3)
        criarTesteBlessed()
    return usuario, senha, listaM3u, DNS, DNSprincipal, SSIPTV, webPlayer, epg, vcapp

def enviar():
    print("Enviando mensagem")
    try:
        driver2.find_element_by_class_name("_1E0Oz").click()
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

def application(ultimoCliente):
    print("Iniciando o bot")
    planilhas = receberPlanilhas(planilha)
    dfClientes = planilhas[0]
    listaAtendidos = planilhas[1]
    dfVendedores = planilhas[2]
    planilhaAtendidos =  planilhas[3]
    print("Buscando clientes...")
    for i in range(ultimoCliente, len(dfClientes)):        
        if i not in listaAtendidos:   
            ultimoCliente = definirUltCliente(ultimoCliente, i)
            print("Cliente: ", i)       
            adicionarAtendido(planilhaAtendidos, i)
            textoCliente = criarTesteBlessed()
            print('textoCliente: ', textoCliente)
            print("--criado texto cliente")
            telefone = dfClientes.iloc[i][numeroWhats]

            if dfClientes.iloc[i][colAparelho] == 'Samsung "comum"':                       
                nome = dfClientes.iloc[i]["Nome"]
                aplicativo = 'STB'
                print(nome, aplicativo)
                
                mensagem = 'Olá *' + nome + '*! %0aRecomendamos a você utilizar o aplicativo ' + aplicativo + '. %0a Aproveite o teste e fique à vontade para nos contatar em caso de dúvidas. %0a Usuário: ' + textoCliente[0][0] + '%0a Senha: ' + textoCliente[1][0] + '%0a dns: 51.222.117.4'                
                mensagem = mensagem.replace( " ","+" )
                try:
                    mensagemPadrao(i, mensagem, telefone)
                except:
                    print("Erro ao enviar mensagem Padrao")
            if dfClientes.iloc[i][colAparelho] == 'LG "comum"':                       
                nome = dfClientes.iloc[i]["Nome"]
                aplicativo = 'Smarters Players'
                print(nome, aplicativo)
                mensagem = 'Olá *' + nome + '*! %0aRecomendamos a você utilizar o aplicativo ' + aplicativo + '. %0a Aproveite o teste e fique à vontade para nos contatar em caso de dúvidas. %0a Usuário: ' + textoCliente[0][0] + '%0a Senha: ' + textoCliente[1][0] + '%0a url: http://nplay.top' 
                mensagem = mensagem.replace( " ","+" )
                try:
                    mensagemPadrao(i, mensagem, telefone)
                except:
                    print("Erro ao enviar mensagem Padrao")

            if dfClientes.iloc[i][colAparelho] == 'Samsung 4K' or dfClientes.iloc[i][colAparelho] ==  'LG 4K':            
                nome = dfClientes.iloc[i]["Nome"]
                aplicativo = 'Duplex'
                print(nome, aplicativo)
                mensagem = 'Olá *' + nome + '*! %0aRecomendamos a você utilizar o aplicativo ' + aplicativo + '. Seu link M3U é: .' + textoCliente[2][0] + '%0a Site para ativação duplex com ID e Key: https://edit.duplexplay.com/ %0a*(caso tenha dúvidas sobre a ativação responda a essa mensagem)* %0a Aproveite o teste e fique à vontade para nos contatar em caso de dúvidas.'
                mensagem = mensagem.replace( " ","+" )
                try:
                    mensagemPadrao(i, mensagem, telefone)
                except:
                    print("Erro ao enviar mensagem Padrao")

            if dfClientes.iloc[i][colAparelho] == 'Philips' or dfClientes.iloc[i][colAparelho] == 'Philco' or dfClientes.iloc[i][colAparelho] == 'Aoc' or dfClientes.iloc[i][colAparelho] == 'TCL "comum"' or dfClientes.iloc[i][colAparelho] == 'Panasonic':              
                nome = dfClientes.iloc[i]["Nome"]
                aplicativo = 'SSIPTV'
                print(nome, aplicativo) 
                try:
                    #ativarSSIPTV()
                    mensagem = 'Olá *' + nome + '*! %0aRecomendamos a você utilizar o aplicativo ' + aplicativo + '. %0aAproveite o teste e fique à vontade para nos contatar em caso de dúvidas.'
                    mensagem = mensagem.replace( " ","+" )
                    try:
                        mensagemPadrao(i, mensagem, telefone)
                    except:
                        print("Erro ao enviar mensagem Padrao")
                except:
                    mensagem = 'Olá *' + nome + '*! %0aRecomendamos a você utilizar o aplicativo ' + aplicativo + '. %0aInfelizmente nosso Bot não conseguiu realizar a ativação automática, por favor *responda esta mensagem para ser atendido(a) pelo suporte*.'
                    try:
                        mensagemPadrao(i, mensagem, telefone)
                    except:
                        print("Erro ao enviar mensagem Padrao")
                    
            if dfClientes.iloc[i][colAparelho] == 'TV modelo Android' or dfClientes.iloc[i][colAparelho] == 'TV BOX':
                nome = dfClientes.iloc[i]["Nome"]
                aplicativo = 'Royal Place'
                print(nome, aplicativo)
                mensagem = 'Olá *' + nome + '*! %0aRecomendamos a você utilizar o aplicativo ' + aplicativo + '%0aDisponível na playstore: https://play.google.com/store/apps/details?id=com.royalplcnew.ml %0a Aproveite o teste e fique à vontade para nos contatar em caso de dúvidas. %0a Usuário: ' + textoCliente[0][0] + '%0a Senha: ' + textoCliente[1][0]
                mensagem = mensagem.replace( " ","+" )
                try:
                    mensagemPadrao(i, mensagem, telefone)
                except:
                    print("Erro ao enviar mensagem Padrao")
                
            time.sleep(2)
            print("Aguardando novos clientes")
    
    time.sleep(30)
    application(ultimoCliente)    

login = input("Usuario vendedor: ")
senha = input("Senha vendedor: ")

validar = validar(login, senha, dfVendedores)

if validar[0] == "valido":
    print("bem-vindo")
    if validar[1] == "ativado":
        print("Sua assinatura está em dia")
        driver = abrirBlessed()
        driver2 = abrirWhats()
        wpAberto = input("APERTE 'ENTER' CASO O WHATS APP WEB JÁ ESTEJA NA TELA DE CONVERSAS")
        colAparelho = "Utiliza Smart TV, Chromecast ou TV Box?"
        numeroWhats = "Número de whatsapp (com DDD)"
        ultimoCliente = 0
        application(ultimoCliente)
    else:
        print(validar[0])
else:
    print("Usuário ou senha inválido")

