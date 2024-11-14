#automatizar (gestão de contratos)
#1 acessar o sei de teste____________________________________________________________ok
#2 identificar um processo___________________________________________________________ok
#2.1 buscar (CONTRATO Nº 306/2023)___________________________________________________ok
#2.2 deve ser espeficifcado um filtro para identificação do processoç_________________
#3 criar ou identificar acompanhamento especial referente ao grupo de processos______
#4 adicinar ao processo do item2 ao item 3
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
# Acesso ao sistema SEI TJPI
browser.get('https://www.tjpi.jus.br/pesquisas')
elem = browser.find_element(By.NAME, "user[username]")
elem.send_keys("wilker.silva")
elem = browser.find_element(By.NAME, "user[password]")
elem.send_keys("EAgames2019")
# clicar no botão Acessa
elem.send_keys(Keys.RETURN)

# Clicar no link pesquisas/surveys
elem = browser.find_element(By.LINK_TEXT, "147")

# Clicar no botão Pesquisar Admin pegar o xpath
#elem = browser.find_element(By.XPATH, "//a[@href='https://www.tjpi.jus.br/pesquisas/surveys']")


elem.click()






sleep(50)


#//*[@id="participant_unity"]