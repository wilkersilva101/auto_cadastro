from time import sleep
from IPython.display import display
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar o Pandas para exibir todas as colunas
pd.set_option('display.max_columns', None)

browser = webdriver.Chrome()
# Acesso ao sistema SEI TJPI
browser.get('https://www.tjpi.jus.br/pesquisas')

# Esperar até que o campo de usuário esteja presente
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.NAME, "user[username]"))
)

elem = browser.find_element(By.NAME, "user[username]")
elem.send_keys("wilker.silva")
elem = browser.find_element(By.NAME, "user[password]")
elem.send_keys("EAgames2019")

# Clicar no botão Acessa
elem.send_keys(Keys.RETURN)

# Esperar até que o link "147" esteja presente
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "147"))
)

elem = browser.find_element(By.LINK_TEXT, "147")
elem.click()

# Esperar até que o link "Admin" esteja presente
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Admin"))
)

elem = browser.find_element(By.LINK_TEXT, "Admin")
elem.click()

# Esperar até que o link "Responder novamente" esteja presente
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Responder novamente"))
)

elem = browser.find_element(By.LINK_TEXT, "Responder novamente")
elem.click()

# Importar a lista de servidores
servidores = pd.read_csv("importar.csv", sep=",")

# Montar o dataframe
df = pd.DataFrame(servidores)
display(df)

sleep(50)