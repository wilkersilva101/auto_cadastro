from time import sleep
from IPython.display import display
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configurar o Pandas para exibir todas as colunas
pd.set_option('display.max_columns', None)


def inicializar_navegador():
    # Configurações do Chrome para melhor estabilidade
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)
    return browser


def esperar_elemento(browser, by, valor, tempo=10):
    try:
        elemento = WebDriverWait(browser, tempo).until(
            EC.presence_of_element_located((by, valor))
        )
        return elemento
    except TimeoutException:
        print(f"Timeout esperando por elemento: {valor}")
        return None


def fazer_login(browser):
    try:
        browser.get('https://www.tjpi.jus.br/pesquisas')
        sleep(3)  # Espera inicial para carregamento completo

        username = esperar_elemento(browser, By.NAME, "user[username]")
        if username:
            username.send_keys("wilker.silva")

        password = browser.find_element(By.NAME, "user[password]")
        password.send_keys("EAgames2019")
        password.send_keys(Keys.RETURN)

        sleep(2)  # Espera após login
        return True
    except Exception as e:
        print(f"Erro no login: {str(e)}")
        return False


def navegar_para_formulario(browser):
    try:
        # Espera mais longa para o carregamento inicial
        sleep(5)

        link_147 = esperar_elemento(browser, By.LINK_TEXT, "147")
        if link_147:
            link_147.click()
            sleep(2)

        link_admin = esperar_elemento(browser, By.LINK_TEXT, "Admin")
        if link_admin:
            link_admin.click()
            sleep(2)

        # Corrigido o erro de sintaxe
        link_responder = esperar_elemento(browser, By.LINK_TEXT, "Responder Questionário") or esperar_elemento(browser, By.LINK_TEXT, "Responder novamente")
        if link_responder:
            link_responder.click()
            sleep(2)

        return True
    except Exception as e:
        print(f"Erro na navegação: {str(e)}")
        return False


def preencher_formulario(browser, dados_servidor):
    try:
        print("Iniciando preenchimento do formulário...")

        # Espera mais longa para o formulário carregar
        sleep(5)

        # Selecionar Unidade Global usando diferentes métodos
        try:
            select_unidade = Select(browser.find_element(By.NAME, "participant[unity]"))
            select_unidade.select_by_visible_text("* - Unidade Global")
        except:
            try:
                select_unidade = Select(browser.find_element(By.CSS_SELECTOR, "select[name='participant[unity]']"))
                select_unidade.select_by_visible_text("* - Unidade Global")
            except Exception as e:
                print(f"Erro ao selecionar unidade: {str(e)}")

        sleep(1)

        # Mapeamento dos campos com múltiplos seletores
        campos = {
            "E-mail": ["participant_replies_attributes_0_description"],
            "Telefone": ["participant_replies_attributes_1_description"],
            "Matrícula": ["participant_replies_attributes_2_description"],
            "Cargo": ["participant_replies_attributes_3_description"],
            "Função": ["participant_replies_attributes_4_description"],
            "Lotação": ["participant_replies_attributes_5_description"]
        }

        # Tentar preencher cada campo usando diferentes métodos
        for campo, seletores in campos.items():
            valor = str(dados_servidor[campo])
            print(f"Preenchendo {campo}: {valor}")

            for seletor in seletores:
                try:
                    # Tentar por ID
                    elemento = browser.find_element(By.ID, seletor)
                except:
                    try:
                        # Tentar por nome
                        elemento = browser.find_element(By.NAME, seletor)
                    except:
                        try:
                            # Tentar por CSS
                            elemento = browser.find_element(By.CSS_SELECTOR, f"input[id='{seletor}']")
                        except:
                            continue

                if elemento:
                    elemento.clear()
                    elemento.send_keys(valor)
                    sleep(1)  # Aumentar o tempo de espera para garantir que o campo seja preenchido corretamente
                    break

        # Tentar diferentes métodos para encontrar o botão Finalizar
        sleep(2)
        try:
            botao = browser.find_element(By.CLASS_NAME, "btn-success")
        except:
            try:
                botao = browser.find_element(By.XPATH, "//button[contains(text(), 'Finalizar')]")
            except:
                try:
                    botao = browser.find_element(By.CSS_SELECTOR, "button.btn-success")
                except Exception as e:
                    print(f"Erro ao encontrar botão Finalizar: {str(e)}")
                    return False

        if botao:
            browser.execute_script("arguments[0].scrollIntoView(true);", botao)
            sleep(1)
            botao.click()
            sleep(3)

            # Verificar se há mensagem de erro
            try:
                erro = browser.find_element(By.CLASS_NAME, "alert-danger")
                if erro.is_displayed():
                    print("Erro de validação encontrado!")
                    print(erro.text)
                    return False
            except:
                pass

            return True

    except Exception as e:
        print(f"Erro detalhado ao preencher formulário: {str(e)}")
        return False


def main():
    browser = None
    try:
        # Importar dados
        df = pd.read_csv("importar.csv", sep=",")
        print("Dados importados com sucesso:")
        display(df)

        # Inicializar navegador
        browser = inicializar_navegador()

        # Login e navegação inicial
        if not fazer_login(browser):
            print("Falha no login!")
            return

        if not navegar_para_formulario(browser):
            print("Falha na navegação!")
            return

        # Processar cada servidor
        sucessos = 0
        falhas = 0

        for index, servidor in df.iterrows():
            print(f"\nProcessando registro {index + 1}/{len(df)}")
            if preencher_formulario(browser, servidor):
                sucessos += 1
                print(f"Registro {index + 1} processado com sucesso!")
                sleep(6)  # Aguardar 6 segundos antes de processar o próximo registro
            else:
                falhas += 1
                print(f"Falha ao processar registro {index + 1}")

            # Voltar para o link "147" para preencher o formulário novamente
            if not navegar_para_formulario(browser):
                print("Falha ao voltar para o formulário!")
                break

        print(f"\nProcessamento concluído!")
        print(f"Sucessos: {sucessos}")
        print(f"Falhas: {falhas}")

    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

    finally:
        if browser:
            sleep(5)
            browser.quit()


if __name__ == "__main__":
    main()