import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from getmac import get_mac_address as gma
from google.oauth2 import service_account
import gspread
import time
import pandas as pd
import pyautogui
from datetime import datetime

print("========================== RP Bot ==========================")

versionAtual = '1.1.7'

location = os.getcwd()
print(location)
pathCredentials = location + "\\data\\credentials.json"

scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
json_file = pathCredentials

def screenshotError():
    capturar = pyautogui.screenshot()
    capturar.save('erro.png')

def login():
    print("Logando no banco de dados")
    try:
        credentials = service_account.Credentials.from_service_account_file(
            json_file)
        scoped_credentials = credentials.with_scopes(scopes)
        gc = gspread.authorize(scoped_credentials)
        planilha = gc.open("Solicitação de teste RoyalPlace (Respostas)")
    except Exception as e:
        print("Não foi possível logar no banco de dados, tentando novamente!")
        print(e)
        time.sleep(3)
        # login()

    return planilha, gc

funcLogin = login()
planilha = funcLogin[0]
gc = funcLogin[1]

def receberVendedores(planilha):
    try:
        abaVendedores = planilha.worksheet("Sellers")
        dadosVendedores = abaVendedores.get_all_records()
        dfVendedores = pd.DataFrame(dadosVendedores)
    except Exception as e:
        print(e)
        print("Vendedores não encontrados, tentando novamente!")
    return dfVendedores

def receberClientes(planilha, NomeAba):
    try:
        abaClientes = planilha.worksheet(NomeAba)
        dadosClientes = abaClientes.get_all_records()
        dfClientes = pd.DataFrame(dadosClientes)
    except Exception as e:
        print(e)
        print("Clientes não recebidos, tentando novamente!")
    return dfClientes

dfVendedores = receberVendedores(planilha)

def validar(login, senha, dfVendedores):
    validar = ''
    estado = ''
    ExpireDate = ''
    Business = ''
    user = ''

    if login in dfVendedores["User"].to_list():
        for i in dfVendedores["User"]:
            if login == i:
                id = (dfVendedores[dfVendedores['User']
                      == login].index.values)[0]
                if senha == dfVendedores["Password"][id]:
                    user = dfVendedores["User"][id]
                    Business = dfVendedores["Business"][id]
                    ExpireDate = dfVendedores["ExpireDate"][id]
                    Online = dfVendedores["Online"][id]
                    print("Logado")
                    estado = dfVendedores['Estado'][id]
                    print(estado)
                    macSeller = dfVendedores['Mac'][id]
                    telefoneVendedor = dfVendedores['Telefone'][id]
                    validar = "valido"
                    return validar, estado, ExpireDate, Business, user, Online, id, macSeller, telefoneVendedor
                else:
                    #print("Senha inválida")
                    validar = "invalido"
                    print("Usuário e/ou senha incorreto/os")
                    os._exit(0)
            else:
                validar = "invalido"
                #print("Usuário e/ou senha incorreto/os")
    else:
        #print("Usuário Inválido")
        validar = "invalido"
        estado = "desativado"
        print("Usuário e/ou senha incorreto/os")
        os._exit(0)

def obterHora():
    seconds = time.strftime('%S', time.localtime())
    hour = time.strftime('%H', time.localtime())
    hour = int(hour)
    hour = hour+6
    if hour >= 24:
        hour = hour - 24
    hour = str(hour)
    if len(hour) == 1:
        hour = '0' + hour
    elif len(hour) == 0:
        hour = '00'
    minute = str(time.strftime('%M', time.localtime()))
    if len(minute) == 1:
        minute = '0' + minute
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
        # driver2.maximize_window()
    except:
        print("Não foi possível abrir o WhatsApp Web, tentando novamente!")
        time.sleep(3)
        abrirWhats()
    return driver2

def loginFive(driver):
    try:
        print("Atualize a pagina do painel e aguarde a tela de Login")
        f = open('fiveLP.txt', 'r')
        fiveLogin = f.readline()
        fivePwd  = f.readline()
        if len(fiveLogin) < 1:
            fiveLogin = input("Digite o login da five: ")
            fivePwd = input("Digite a senha da five: ")
            f = open('fiveLP.txt', 'w')
            conteudo = [fiveLogin + '\n' + fivePwd]
            f.writelines(conteudo)
        print('fiveLogin:', fiveLogin)
        print('fivePwd:', fivePwd)
        #f.close('fiveLP.txt')
        
        driver.find_element_by_name('username').send_keys(fiveLogin.strip())
        driver.find_element_by_name('password').send_keys(fivePwd.strip())
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/div/div/div/form/div[4]/div/button').click()

        time.sleep(1)
    except Exception as e:
        # print(e)
        screenshotError()
    # input("Verifique a tela de login do painel")""
        # loginFive(driver)
        pass

def abrirFive():
    try:
        options = webdriver.ChromeOptions()
        # ua = UserAgent()
        # userAgent = ua.random
        # print(userAgent)    
        # options.add_argument(f'user-agent={userAgent}')
        options.add_argument(userDataDir2)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(pathChrome2, options=options)
        driver.get("http://painel.c-pro.site/auth/sign-in")
        time.sleep(1)
        input("Pressione ENTER quando a Five estiver na tela de login")
        loginFive(driver)
    except:
        screenshotError()
    return driver

pathChrome = location + "\\data\\chromedriver.exe"
pathChrome2 = location + "\\data\\chromedriver2.exe"
userDataDir = "user-data-dir=" + location + "\\data"
userDataDir2 = "user-data-dir2=" + location + "\\data"

def dadosFive(texto):
    texto = texto.replace("username: ", "")
    texto = texto.replace("Senha: ", "")
    texto = texto.split(" | ")
    # print(texto)
    return texto

def enviarVendedor():
    try:
        driver2.find_element_by_class_name("_4sWnG").click()
        time.sleep(5)
    except:
        time.sleep(2)
        enviarVendedor()
        print("Não foi possível enviar a mensagem ao revendedor!")

def criarTesteFive():
    try:
        horarioTeste = obterHora()
        hour = horarioTeste[1]
        minute = horarioTeste[2]
        seconds = horarioTeste[3]
        try:
            driver.get("http://painel.c-pro.site/users/add_trial")
            time.sleep(2)
            driver.find_element_by_xpath(
                '//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/form/div[1]/div[1]/input').send_keys("rp"+hour+minute+seconds)
            driver.find_element_by_xpath(
                '//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/form/div[1]/div[2]/input').send_keys("p2pgold")
            time.sleep(1)
            driver.find_element_by_xpath(
                '//*[@id="react-select-2-input"]').send_keys("TESTE 6H COMPLETO", Keys.ENTER)
            time.sleep(1)
            driver.find_element_by_xpath(
                '//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/form/div[2]/div/button[2]').click()
            time.sleep(2)
            print("Capturando dados")
            texto = driver.find_element_by_id('swal2-content').text

            if 'username' not in texto and 'Senha' not in texto:
                criarTesteFive()

            time.sleep(2)
            
        except:
            mensagem = Name + ', verifique se o painel Five se encontra online'
            contatoVendedor = 'https://web.whatsapp.com/send?phone=55' + str(telefoneVendedor) + '&text=' + mensagem
            driver2.get(contatoVendedor)
            time.sleep(5)
            enviarVendedor()
            loginFive(driver)
            application(ultimoCliente)
            criarTesteFive()
        # print(texto)
        
        textoCliente = dadosFive(texto)
        linkM3U = "http://5ce.co/get.php?username=" + \
            textoCliente[0]+"%26password="+textoCliente[1] + \
            "%26type=m3u_plus%26output=ts"
        linkSSIPTV = "http://ss.5ce.co/get.php?username=" + \
            textoCliente[0]+"%26password=" + \
            textoCliente[1]+"%26type=ss%26output=ts"
        linkHLS = "http://5ce.co/get.php?username=" + \
            textoCliente[0]+"%26password="+textoCliente[1] + \
            "%26type=m3u_plus%26output=m3u8"
        textoCliente.append(linkM3U)
        textoCliente.append(linkSSIPTV)
        textoCliente.append(linkHLS)
    except Exception as e:
        print(e)
        time.sleep(2)
        criarTesteFive()
    return textoCliente

def enviar(i):
    print("Enviando mensagem")
    try:
        driver2.find_element_by_class_name("_4sWnG").click()
    except:
        print("Não foi possível enviar a mensagem, tentando novamente!")

        try:
            erro = driver2.find_element_by_xpath(
                '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[1]').text
            print(erro)
            if "O número de telefone compartilhado através de url é inválido." in erro:
                setErroDeAtendido(i)
                application(ultimoCliente)
        except Exception as e:
            #print(e)
            pass

        time.sleep(3)
        enviar(i)

def mensagemPadrao(i, mensagem, telefone):
    print("Gerando mensagem padrão")
    try:
        linkWhats = ('https://web.whatsapp.com/send?phone=55' +
                     str(telefone) + '&text=' + mensagem)
        # print(linkWhats)

        driver2.get(linkWhats)
        time.sleep(5)
        enviar(i)
        time.sleep(3)
        relogio = driver2.find_elements_by_css_selector(
            '[aria-label=" Pendente "]')
        # print(relogio)
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
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[3]/button[1]').click()
    time.sleep(2)
    driver.find_element_by_xpath(
        '//*[@id="datatabled"]/tbody/tr[1]/td[10]/div/button[2]/i').click()
    time.sleep(2)
    driver.find_element_by_xpath(
        '//*[@id="datatabled"]/tbody/tr[1]/td[10]/div/div/a[2]').click()

def setAtendido(i):
    setAtendido = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet(NomeAba)
    coord = 'E'+str(i+2)
    setAtendido.update_acell(coord, 'sim')

def setErroDeAtendido(i):
    setAtendido = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet(NomeAba)
    coord = 'E'+str(i+2)
    setAtendido.update_acell(coord, 'erro')

def application(ultimoCliente):
    try:
        print("Iniciando o bot")
        dfVendedores = receberVendedores(planilha)

        def validar(login, senha, dfVendedores):
            validar = ''
            estado = ''
            ExpireDate = ''
            Business = ''
            user = ''

            if login in dfVendedores["User"].to_list():
                for i in dfVendedores["User"]:
                    if login == i:
                        id = (dfVendedores[dfVendedores['User'] == login].index.values)[
                            0]
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
                # Adicionar logica para reconhecer se o cliente é sim ou não na coluna atendido
                dfClientes = receberClientes(planilha, NomeAba)
                print("Buscando clientes...")
                for i in range(ultimoCliente, len(dfClientes)):
                    if dfClientes.iloc[i]['Atendido'] != 'sim' and dfClientes.iloc[i]['Atendido'] != 'erro':
                        print("------Cliente:"+str(i)+"------")
                        
                        # chamar função pra preencher coluna com sim no id+2
                        #setErroDeAtendido(i)
                        telefone = str(dfClientes.iloc[i][numeroWhats])
                        telefone = telefone.replace("+", "")
                        telefone = telefone.replace(" ", "")
                        telefone = telefone.replace("-", "")
                        if telefone.isdecimal() == False:
                            setErroDeAtendido(i)
                            telefone = ""
                        if telefone[:2] == "55":
                            telefone = telefone[2:]
                        if len(telefone) == 11 or len(telefone) == 10:
                            ultimoCliente = definirUltCliente(ultimoCliente, i)

                            horarioTeste = obterHora()
                            dataEndTest = horarioTeste[0]

                            try:
                                textoCliente = criarTesteFive()
                            except Exception as e:
                                print (e)
                                pass
                            # print('textoCliente: ', textoCliente)
                            print("--criado teste do cliente")

                            nome = str(dfClientes.iloc[i]["Nome"])
                            try:
                                nome = nome.capitalize()
                            except:
                                pass
                            
                            print(telefone, nome)

                            if dfClientes.iloc[i][colAparelho] == 'Smart - Samsung 4K':
                                aplicativo = 'Duplex Play'
                                print(aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO aplicativo indicado pra utilizar na *Samsung modelo 4K* é o *Duplex Play*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Baixe o Aplicativo Duplex Play na sua Smart TV_ %0a*Passo 2:* _Abra o aplicativo, anote o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 3:* _Por meio de *qualquer dispositivo* entre no site: https://edit.duplexplay.com/_ %0a _acesse com o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 4:* _Clique no botão "Add playlist" e insira nos respectivos campos:_ %0a _*Playlist name =>* ROYAL PLACE - GOLD_ %0a _*Playlist Url (.M3U or .M3U8) =>* ' + textoCliente[
                                    2] + '_ %0a _*Marque a caixa* "Não sou um robô"_ %0a _*Clique em SAVE*_ %0a%0aRealizadas estas etapas, basta clicar em Refresh ou Atualizar o seu Duplex Play %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO seu teste acaba às: *' + dataEndTest + '*'
                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            elif dfClientes.iloc[i][colAparelho] == 'Smart - Samsung antiga':
                                aplicativo = 'STB'
                                print(nome, aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO aplicativo indicado pra utilizar na *Samsung modelo antigo* é o *Smart STB*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Ligue a TV e abra a janela "Configurações" pressionando o botão "Configurações" no controle remoto da TV._ %0a*Passo 2:* _Vá para a guia Geral e selecione Rede na lista de opções._ %0a*Passo 3:* _Você pode verificar se a TV está conectada à Internet em "Status da rede"._ %0a*Passo 4:* _Selecione as configurações de IP e vá para as configurações de DNS._ %0a*Passo 5:* _Você deve alterar as configurações de DNS de entrada manualmente._ %0a*Passo 6:* _Na configuração DNS você verá o servidor DNS atual, altere para 212.102.61.85_ %0a*Passo 7:* _Abra o Aplicativo STB Smart e utilize os dados a seguir:_ %0a%0a*Login:* ' + \
                                    textoCliente[0] + '%0a*Senha:* ' + textoCliente[1] + \
                                    ' %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' + dataEndTest + '*'
                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            elif dfClientes.iloc[i][colAparelho] == 'Smart - LG 4K' or dfClientes.iloc[i][colAparelho] == 'Smart - LG antiga':
                                aplicativo = 'Smarters Players ou Duplex'
                                print(nome, aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO aplicativo indicado pra utilizar na *LG* é o *Duplex Play* ou *Smarters Players*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Smarters Players* %0aROYAL PLACE - GOLD %0a*Login :* ' + textoCliente[0] + ' %0a*Senha :* ' + textoCliente[1] + ' %0a*URL:* http://smart.cms-central.ovh %0a%0a*Duplex Play* %0a*Passo 1:* _Baixe o Aplicativo Duplex Play na sua Smart TV_ %0a*Passo 2:* _Abra o aplicativo, anote o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 3:* _Por meio de *qualquer dispositivo* entre no site: https://edit.duplexplay.com/_ %0a _acesse com o *DEVICE ID* e *DEVICE KEY*_ %0a*Passo 4:* _Clique no botão "Add playlist" e insira nos respectivos campos:_ %0a _*Playlist name =>* ROYAL PLACE - GOLD_ %0a _*Playlist Url (.M3U or .M3U8) =>* ' + textoCliente[
                                    2] + '_ %0a _*Marque a caixa* "Não sou um robô"_ %0a _*Clique em SAVE*_ %0a%0aRealizadas estas etapas, basta clicar em Refresh ou Atualizar o seu Duplex Play %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' + dataEndTest + '*'

                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            elif dfClientes.iloc[i][colAparelho] == 'Smart - Philco, Philips, Sony, Panasonic':
                                aplicativo = 'SSIPTV'
                                print(nome, aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO aplicativo indicado pra utilizar na sua *Smart TV* é o *SSIPTV*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* _Abra o aplicativo SSIPTV > Configurações > Obter código_ %0a*Passo 2:* _Acesse o site http://ss-iptv.com/en/users/playlist_ %0a*Passo 3:* _Digite o seu código e clicar em Adicionar dispositivo (ADD DEVICE)_ %0a*Passo 4:* _External Playlists > ADD ITEM_ %0a*Displayed Name:* _ROYAL PLACE - GOLD_ %0a*Source:* ' + textoCliente[
                                    3] + ' %0a*OK* %0a%0a*Passo 5:* _SAVE_ %0a*Passo 6:* _Clique em Atualizar no seu aplicativo SSIPTV e abra a pasta ROYAL PLACE - GOLD_ %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' + dataEndTest + '*'
                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            elif dfClientes.iloc[i][colAparelho] == 'TV BOX' or dfClientes.iloc[i][colAparelho] == 'Celular Android':
                                aplicativo = 'Royal Place ou Smarters Players'
                                print(nome, aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO aplicativo indicado pra utilizar no seu aparelho é o *Royal Place P2P*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Link direto Play Store: https://play.google.com/store/apps/details?id=nd.ndapps.royalplacep2p%26hl=pt_BR%26gl=US* %0a*Link downloads site: https://www.royalplace.com.br/download*%0a%0a*Passo 1:* Abra o aplicativo *Royal Place P2P* %0a*Passo 2:* Insira os dados a seguir: %0a*Usuário:* ' + \
                                    textoCliente[0] + ' %0a*Senha:* ' + textoCliente[1] + \
                                    ' %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' + dataEndTest + '*'
                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                                print("Alterando tipo de lista de IPTV para P2P")
                                alterarListaP2P(driver)

                            elif dfClientes.iloc[i][colAparelho] == 'Chromecast':
                                aplicativo = 'GSE IPTV'
                                print(nome, aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO aplicativo indicado pra utilizar no seu *Chromecast* é o *GSE IPTV*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Passo 1:* Abra o aplicativo *Chromecast* e adicione uma nova lista com os dados a seguir: %0a*Playlist Name:* Royal Place - GOLD %0a*Description:* Teste %0a*http://...:* ' + \
                                    textoCliente[4] + ' %0a*Pressione OK* %0a*Passo 2:* Selecione a nova lista e aguarde o carregamento. %0a*Passo 3:* Conecte o celular à televisão %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' + dataEndTest + '*'
                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            elif dfClientes.iloc[i][colAparelho] == 'iPhone':
                                aplicativo = 'Smarters Players'
                                print(nome, aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO aplicativo indicado pra utilizar no *iPhone* é o *Smarters Players*, siga o passo a passo pra ativar o seu sinal de teste grátis! %0a%0a*Smarters Players* %0aROYAL PLACE - GOLD %0a*Login:* ' + \
                                    textoCliente[0] + ' %0a*Senha:* ' + textoCliente[1] + \
                                    ' %0a*URL:* http://smart.cms-central.ovh %0a%0aCaso tenha dúvidas responda a essa mensagem e aguarde um de nossos atendentes entrar em contato! %0a%0aO Seu teste acaba às: *' + dataEndTest + '*'

                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            elif dfClientes.iloc[i][colAparelho] == 'Android TV' or dfClientes.iloc[i][colAparelho] == 'Outro':
                                aplicativo = 'Smarters Players'
                                print(nome, aplicativo)

                                mensagem = 'Olá *' + nome + '*! %0aO seu dispositivo necessita de atendimento especializado, por favor responda a esta mensagem e aguarde um atendente. %0a%0aCaso tenha algum aplicativo instalado no dispositivo pode tentar inserir alguns destes dados se requisitado: %0a%0a*Usuário:* ' + \
                                    textoCliente[0] + ' %0a*Senha:* ' + textoCliente[1] + '%0a*Link .M3U:* ' + textoCliente[2] + \
                                    '%0a*Url:* http://cms-central.co:80 %0a%0aEm caso de dúvida, aguarde o suporte.'
                                mensagem = mensagem.replace(" ", "+")
                                try:
                                    mensagemPadrao(i, mensagem, telefone)
                                    time.sleep(3)
                                    setAtendido(i)
                                except:
                                    print("Erro ao enviar mensagem Padrao")

                            time.sleep(2)
                            print("---------------------")
                        else:
                            setErroDeAtendido(i)
                            print("Número de telefone inválido: ",
                                  telefone, dfClientes.iloc[i]["Nome"])
                            print("---------------------")
                    
                time.sleep(10)
                application(ultimoCliente)
            else:
                print("Sua assinatura expirou! Contate o suporte.")
        else:
            print("A sua conta foi acessada em outra sessão")
    except Exception as e:
        print("Confira sua conexão com a internet e contate o suporte técnico!")
        print(e)
        application(ultimoCliente)

news = gc.open("Solicitação de teste RoyalPlace (Respostas)").worksheet('news')
versionNew = news.acell('B2').value

print("====================== Versão: ",
      versionAtual, " =====================")

def verificarAtt(versionAtual, versionNew):
    vAtual = int(versionAtual.replace(".", ""))
    vNew = int(versionNew.replace(".", ""))

    if vAtual < vNew:
        print("Há uma nova atualização disponível (v"+versionNew +
              "). Para obte-la feche o bot e execute o arquivo update.exe")

verificarAtt(versionAtual, versionNew)

login = str(input("Usuario vendedor: "))
senha = str(input("Senha vendedor: "))

validar = validar(login, senha, dfVendedores)

UserAndPass = validar[0]
ExpireDate = validar[2]
Business = validar[3].title()
Name = validar[4].title()
Online = validar[5]
id = validar[6]
macSeller = validar[7]
# print(macSeller)
telefoneVendedor = validar[8]

macAddress = gma()

def definirMac(macAddress):
    plVendedores = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'G'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, macAddress)

def desconectarConta(id):
    plVendedores = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'F'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, 'não')

def horas():
    # day = 
    # month = 
    # hour = time.strftime('%H', time.localtime())
    # minute = time.strftime('%M', time.localtime())
    # seconds = time.strftime('%M', time.localtime())

    horas = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return horas

def conectarConta(id):
    plVendedores = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'F'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, 'sim ' + horas)

def iniciar():
    print("bem-vindo " + Name + " ("+Business+")")
    print("Assinatura expira em: ", ExpireDate)
    driver = abrirFive()
    driver2 = abrirWhats()
    input("Aperte ENTER caso o whatsapp já esteja na tela de conversas!")

    return driver, driver2

def obterNomeAba(id):
    NomeAba = dfVendedores["NomeAba"][id]
    return NomeAba

def guardarVersao(id):
    plVendedores = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'I'+str(id+2)
    # print("coord :", coord)
    plVendedores.update_acell(coord, versionAtual)

ultimoCliente = 0
colAparelho = "Qual o seu aparelho?"
numeroWhats = "Número de WhatsApp com DDD (Exemplo: 27 998851972)"

if UserAndPass == "valido":
    if validar[1] == "ativado": 
        if len(str(macSeller)) < 3:
            definirMac(macAddress)
            macSeller = macAddress
            pass
        else:
            pass
        if macAddress == macSeller:
            if Online == 'não':
                guardarVersao(id)
                horas = horas()
                print(horas)
                conectarConta(id)
                NomeAba = obterNomeAba(id)
                #dfClientes = receberClientes(planilha, NomeAba)
                iniciar = iniciar()
                driver = iniciar[0]
                # loginFive(driver)
                input()
                driver2 = iniciar[1]
                
                guardarVersao(id)
                application(ultimoCliente)
            else:
                print("Sua conta já se encontra conectada a outra sessão!")
                forceDC = str(
                    input("Deseja forçar a desconexão? Digite 1 para 'sim' ou 2 para 'não: "))
                if forceDC == '1':
                    guardarVersao(id)
                    desconectarConta(id)
                    horas = horas()
                    conectarConta(id)
                    NomeAba = obterNomeAba(id)
                    iniciar = iniciar()
                    driver = iniciar[0]
                    driver2 = iniciar[1]
                    application(ultimoCliente)
                else:
                    print("Não é possível executar duas sessões na mesma conta!")
        else:
            print(
                "Máquina não reconhecida, contate o Suporte. Por segurança, a sessão será finalizada.")
    else:
        print("Sua conta expirou em: ", ExpireDate)
else:
    print("Usuário ou senha inválido")
