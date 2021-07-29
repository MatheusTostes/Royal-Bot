# def openFive():
#     try:
#         options = webdriver.ChromeOptions()
#         # ua = UserAgent()
#         # userAgent = ua.random
#         # print(userAgent)    
#         # options.add_argument(f'user-agent={userAgent}')
#         options.add_argument(userDataDir2)
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])

#         driver = webdriver.Chrome(pathChrome2, options=options)
#         driver.get("http://painel.c-pro.site/auth/sign-in")
#         time.sleep(1)
#         # input("Pressione ENTER quando a Five estiver na tela de login")
#         print("Bypass cloudflare")
#         # driver.set_window_size(5, 400);time.sleep(0.3)
#         driver.maximize_window();time.sleep(1)
#         pyautogui.keyDown('alt');time.sleep(0.5)
#         pyautogui.press('d')
#         pyautogui.press('enter')
#         pyautogui.keyUp('alt');time.sleep(0.5)
#         driver.minimize_window()
#         time.sleep(8)
#         # driver.set_window_size(5, 400);time.sleep(1)
#         # driver.set_window_size(5, 400);time.sleep(0.3)
#         driver.maximize_window();time.sleep(0.5)
#         pyautogui.keyDown('ctrl');time.sleep(0.5)
#         pyautogui.keyDown('w');time.sleep(0.5)
#         pyautogui.keyUp('w');time.sleep(0.5)
#         pyautogui.keyUp('ctrl');time.sleep(0.5)
#         driver.minimize_window()

#         loginFive(driver)
#     except Exception as e:
#         print(e)
#         # screenshotError()
#         pass
#     return driver