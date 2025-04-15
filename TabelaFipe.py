from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
from datetime import datetime

import json

navegador = webdriver.Chrome()
navegador.get("http://veiculos.fipe.org.br/")
navegador.maximize_window()

# //*[@id="front"]/div[1]/div[2]/ul/li[1]/a/div[2]
time.sleep(0.5)
elemento = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((
    By.XPATH,'//*[@id="front"]/div[1]/div[2]/ul/li[1]/a/div[2]'))).click()

carros = {}
numero_carro = 0

time.sleep(1)

def move_tela(times):
    for time in range(0, times):
        navegador.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_UP)

def seleciona_mes_ano():
    navegador.find_element(By.XPATH,'//*[@id="selectTabelaReferenciacarro_chosen"]/a/div/b').click()
    options_mes_ano = navegador.find_elements(By.XPATH, '//*[@id="selectTabelaReferenciacarro_chosen"]/div/ul')
    return options_mes_ano[0].find_elements(By.CSS_SELECTOR, 'li')

def seleciona_marca(indice):
    element_click = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectMarcacarro_chosen"]/a/div/b'))).click()
    # navegador.find_element(By.XPATH,'//*[@id="selectMarcacarro_chosen"]/a/div/b').click()
    options_marca = navegador.find_elements(By.XPATH, '//*[@id="selectMarcacarro_chosen"]/div/ul')
    lista_marca = options_marca[0].find_elements(By.CSS_SELECTOR, 'li')
    lista_marca[indice].click()


def seleciona_modelo():
    navegador.find_element(By.XPATH,'//*[@id="selectAnoModelocarro_chosen"]/a/div/b').click()
    options_ano_modelo = navegador.find_elements(By.XPATH, '//*[@id="selectAnoModelocarro_chosen"]/div/ul')
    return options_ano_modelo[0].find_elements(By.CSS_SELECTOR, 'li')

# time.sleep(1)

def seleciona_ano_modelo():
    navegador.find_element(By.XPATH,'//*[@id="selectAnocarro_chosen"]/a/div/b').click()
    options_ano_carro = navegador.find_elements(By.XPATH, '//*[@id="selectAnocarro_chosen"]/div/ul')
    return options_ano_carro[0].find_elements(By.CSS_SELECTOR, 'li')

start = datetime.now()

lista_mes_ano = seleciona_mes_ano()
for mes_ano in range(0,1):
    lista_mes_ano[mes_ano].click()
    seleciona_marca(0)
    lista_modelos = seleciona_modelo()
    for modelo in range(0, len(lista_modelos)):
        lista_modelos[modelo].click()

        lista_ano_modelo = seleciona_ano_modelo()

        for ano_modelo in range(0, len(lista_ano_modelo)):
            lista_ano_modelo[ano_modelo].click()

            time.sleep(0.5)
            navegador.find_element(By.LINK_TEXT, 'Pesquisar').click()
            time.sleep(0.5)
            tabela = navegador.find_elements(By.XPATH, '//*[@id="resultadoConsultacarroFiltros"]/table/tbody')
            time.sleep(0.5)
            linhas = tabela[0].find_elements(By.CSS_SELECTOR, 'td')

            carro = {}

            for item in range(0,len(linhas)-1, 2):
                carro[linhas[item].text] = linhas[item+1].text

            carros[numero_carro] = carro
            print(f'Carro: {carros[numero_carro]}')
            numero_carro +=1
            time.sleep(0.5)

            move_tela(3)
            time.sleep(0.5)

            lista_ano_modelo = seleciona_ano_modelo()

        move_tela(7)
        time.sleep(0.5)
        seleciona_marca(1)

        time.sleep(0.5)

        seleciona_marca(0)
        time.sleep(0.5)
        lista_modelos = seleciona_modelo()
    move_tela(7)
    time.sleep(0.5)

    seleciona_marca(1)
    time.sleep(0.5)
    lista_mes_ano = seleciona_mes_ano()

end = datetime.now()
print(end)
navegador.close()

# print(carro)

object_json = json.dumps(carros, indent = 2, ensure_ascii = False)
with open('carroAcura.json', 'w') as file:
    file.write((object_json))

