from operator import le
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from json import dump

options = Options()
options.add_argument("start-maximized")
DRIVER_PATH = os.path.abspath(os.getcwd())+'/src/chromedriver'
driver = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)

lista_lojas = ['americanas-com-loja-online', 'magazine-luiza-loja-online', 'carrefour-loja-online', 'casas-bahia-loja-online', 'amazon', 'extra-loja-online']

lista_dados = []

for loja in lista_lojas:
  
    driver.get(f'https://www.reclameaqui.com.br/empresa/{loja}/')
    try:

        driver.find_element_by_id('onetrust-accept-btn-handler').click()
    except:
        pass
    try:
        driver.find_element_by_class_name('_hj-OO1S1__styles__openStateToggle').click()
    except:
        pass
    
    time.sleep(3)
    driver.find_element_by_id('reputation-tab-5').click()

    indices = driver.find_elements_by_class_name('label')
    total_reclamacoes = driver.find_elements_by_class_name('stats')[1].find_element_by_tag_name('b')
    reclamacoesRespondidas = driver.find_elements_by_class_name('stats')[2].find_element_by_tag_name('b')
    reputacao = driver.find_elements_by_class_name('stats')[0].find_element_by_tag_name('b')


    percentualRespondidas = int(reclamacoesRespondidas.text)/int(total_reclamacoes.text)

    principaisProblemas = driver.find_elements_by_class_name('nvhcgi-2')

    driver.execute_script("document.querySelectorAll('.chu0q3-0.zUPSt.card-header')[3].click()")
    driver.execute_script("document.querySelectorAll('.chu0q3-0.zUPSt.card-header')[4].click()")
    driver.execute_script("document.querySelectorAll('.chu0q3-0.zUPSt.card-header')[5].click()")
    time.sleep(3)
    categorias = driver.find_elements_by_class_name('nvhcgi-1.jMSnzo')
    tiposDeProblemaSubCategoria = []
    produtosServicos = []
    problemasSubCategorias = []

    for nomeProblema in categorias[0].find_elements_by_tag_name('a'):
        nome  = nomeProblema.text.split("\n")[0] 
        valor = nomeProblema.text.split("\n")[1].replace('(','').replace(')','')
        tiposDeProblemaSubCategoria.append({nome: valor} )

    for nomeProblema in categorias[1].find_elements_by_tag_name('a'):
        nome  = nomeProblema.text.split("\n")[0] 
        valor = nomeProblema.text.split("\n")[1].replace('(','').replace(')','')
        produtosServicos.append({nome: valor} )

    for nomeProblema in categorias[2].find_elements_by_tag_name('a'):
        nome  = nomeProblema.text.split("\n")[0] 
        valor = nomeProblema.text.split("\n")[1].replace('(','').replace(')','')
        problemasSubCategorias.append({nome: valor} )        

    driver.execute_script("document.getElementById('box-complaints-read-more').click()")
    time.sleep(1)

    divsReclamacoes = driver.find_elements_by_class_name('bJdtis')
    
    print('divsReclamacoes: ')
    print(type(divsReclamacoes))
    print(divsReclamacoes)

    reclamacoes = list(map(lambda div: {
        'titulo': div.find_element_by_css_selector('a > h4').get_attribute('innerText'),
        'texto': div.find_element_by_tag_name('p').get_attribute('innerText')
    }, divsReclamacoes)) 

    informacao = {
                    'Nome Da Loja': loja,
                    'Total de reclamaçoes': total_reclamacoes.text,
                    'Reclamações Respondidas' : "{:.1f}%".format(percentualRespondidas * 100),
                    'Voltariam a fazer negogicio': indices[1].text,
                    'Indice de soluçao' : indices[2].text,
                    'Nota do consumidor' :indices[3].text,
                    'Reputação': reputacao.text,
                    'Percentual Principais Problemas': {
                                            principaisProblemas[0].find_element_by_tag_name('a').text.split('%')[1][1::]:f"{principaisProblemas[0].find_element_by_tag_name('a').text.split('%')[0]}%",
                                            principaisProblemas[1].find_element_by_tag_name('a').text.split('%')[1][1::]:f"{principaisProblemas[1].find_element_by_tag_name('a').text.split('%')[0]}%",
                                            principaisProblemas[2].find_element_by_tag_name('a').text.split('%')[1][1::]:f"{principaisProblemas[2].find_element_by_tag_name('a').text.split('%')[0]}%",
                    },
                    'Principais Problemas':{
                                            'Tipos de problemas': tiposDeProblemaSubCategoria,
                                            'Produtos e Servicos': produtosServicos,
                                            'Categorias': problemasSubCategorias
                    },
                    'Reclamacoes': reclamacoes,
        }
    lista_dados.append(informacao)
time.sleep(5)
for a in lista_dados:
    print(f'{a}\n')

caminho_arquivo = './data/dados.json'

arquivo = open(caminho_arquivo, 'w' if os.path.exists(caminho_arquivo) else 'x')
dump(lista_dados, arquivo)
arquivo.close()
