from operator import le
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



options = Options()
options.add_argument("start-maximized")
DRIVER_PATH = os.path.abspath(os.getcwd())+'/src/chromedriver'
driver = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)



lista_lojas = ['magazine-luiza-loja-online','americanas-com-loja-online', ]

lista_dados = []

for loja in lista_lojas:
  
    driver.get(f'https://www.reclameaqui.com.br/empresa/{loja}/')


    """ driver.find_element_by_class_name("form-control").send_keys(loja)
   
    driver.find_element_by_class_name('btn-blue-dark').click()
    

    time.sleep(3)
    print('Chegou aqui')
    """
    try:

        driver.find_element_by_id('onetrust-accept-btn-handler').click()
    except:
        pass
    try:
        driver.find_element_by_class_name('_hj-OO1S1__styles__openStateToggle').click()
    except:
        pass
    
    """ driver.find_element_by_class_name('wrapper-item').click()
    time.sleep(5) """
    time.sleep(3)

    texto = driver.find_element_by_class_name('description')
    print(texto.text)

    
    informacao = {'Nome Da Loja': loja, 'Reclamações' : 1}
    lista_dados.append(informacao)
time.sleep(5)
print(lista_dados)
