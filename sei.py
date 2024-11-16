from time import sleep
from IPython.display import display
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Configurar o Pandas para exibir todas as colunas
pd.set_option('display.max_columns', None)


def inicializar_navegador():
    browser = webdriver.Chrome()
    return browser


def fazer_login(browser):
    # Acessar o sistema
    browser.get('https://www.tjpi.jus.br/pesquisas')

    # Esperar até que o campo de usuário esteja presente
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "user[username]"))
    )

    # Preencher login
    elem = browser.find_element(By.NAME, "user[username]")
    elem.send_keys("wilker.silva")
    elem = browser.find_element(By.NAME, "user[password]")
    elem.send_keys("EAgames2019")
    elem.send_keys(Keys.RETURN)


def navegar_para_formulario(browser):
    # Navegar pelos links necessários
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "147"))
    )
    browser.find_element(By.LINK_TEXT, "147").click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Admin"))
    )
    browser.find_element(By.LINK_TEXT, "Admin").click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Responder novamente"))
    )
    browser.find_element(By.LINK_TEXT, "Responder novamente").click()


def preencher_formulario(browser, dados_servidor):
    try:
        # Esperar pelo select de unidade
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "Unidade"))
        )

        # Selecionar Unidade Global
        select_unidade = Select(browser.find_element(By.NAME, "Unidade"))
        select_unidade.select_by_visible_text("*- Unidade Global")

        # Preencher os campos
        campos = {
            "E-mail": (By.ID, "1"),
            "Telefone": (By.ID, "2"),
            "Matrícula": (By.ID, "3"),
            "Cargo": (By.ID, "4"),
            "Função": (By.ID, "5"),
            "Lotação": (By.ID, "6")
        }

        for campo, (by, selector) in campos.items():
            elemento = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((by, selector))
            )
            elemento.clear()
            elemento.send_keys(str(dados_servidor[campo]))
            sleep(0.5)

        # Clicar no botão Finalizar Respostas
        # Tentando diferentes seletores para garantir que encontremos o botão
        try:
            # Primeira tentativa: por texto
            botao = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Finalizar Respostas')]"))
            )
        except:
            try:
                # Segunda tentativa: por classe
                botao = browser.find_element(By.CLASS_NAME, "btn-success")
            except:
                # Terceira tentativa: por XPath mais específico
                botao = browser.find_element(By.XPATH,
                                             "//button[@class='btn btn-success' or contains(@class, 'finalizar')]")

        # Rolar até o botão para garantir que está visível
        browser.execute_script("arguments[0].scrollIntoView(true);", botao)
        sleep(1)  # Pequena pausa para garantir que a página terminou de rolar

        # Clicar no botão
        botao.click()

        # Esperar um pouco para o próximo registro
        sleep(2)
        return True

    except Exception as e:
        print(f"Erro ao preencher formulário: {str(e)}")
        return False


def main():
    try:
        # Importar dados
        df = pd.read_csv("importar.csv", sep=",")
        print("Dados importados com sucesso:")
        display(df)

        # Inicializar navegador
        browser = inicializar_navegador()

        # Login e navegação inicial
        fazer_login(browser)
        navegar_para_formulario(browser)

        # Processar cada servidor
        sucessos = 0
        falhas = 0

        for index, servidor in df.iterrows():
            print(f"\nProcessando registro {index + 1}/{len(df)}")
            if preencher_formulario(browser, servidor):
                sucessos += 1
                print(f"Registro {index + 1} processado com sucesso!")
            else:
                falhas += 1
                print(f"Falha ao processar registro {index + 1}")

        print(f"\nProcessamento concluído!")
        print(f"Sucessos: {sucessos}")
        print(f"Falhas: {falhas}")

    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

    finally:
        # Aguardar um pouco antes de fechar
        sleep(5)
        browser.quit()


if __name__ == "__main__":
    main()