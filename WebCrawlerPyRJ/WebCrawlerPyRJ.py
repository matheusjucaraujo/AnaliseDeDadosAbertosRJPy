
from selenium  import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests, bs4
#lembrar de baixar o driver gecko
browser = webdriver.Firefox()
#browser.get('https://inventwithpython.com')
browser.get('http://doweb.rio.rj.gov.br/buscanova/#/p=1&q=material%20hospitalar&di=20100409&df=20100416')
try:

    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropup')))
    #print(browser.page_source)
    maxPage = browser.find_element_by_class_name("mostrador-paginas")
    num_max = str(maxPage.text)
    num_max = num_max[::-1] #inverte a string
    print(num_max)
    lNum_max = num_max.split(" ",1)#Pega o número final de páginas, separado por um  espaço (" ")
    print(lNum_max[0])
    for elem in browser.find_elements_by_class_name('dropup'):
        print(elem.text)
        if (elem.text == "  Download"):
            elem.click()
            #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'link pdf-full')))
            #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ng-show")))
            pdfLinks = browser.find_elements_by_css_selector("a[class = 'link pdf-page']")
            links = [pdfLink.get_attribute('href') for pdfLink in pdfLinks]
            for i in range (len(links)):
                print (str(links[i]))
            #pdfLink = browser.find_element_by_tag_name()
            #pdfLink.click()
                
    #listaLinks = browser.find_elements_by_class_name('btn btn-default dropdown-toggle')
    #listaLinks2 = browser.find_element_by_partial_link_text('https://doweb.rio.rj.gov.br/portal/edicoes/download/')
    #for i in range (len(listaLinks)):
     #   print((listaLinks[i].text))
    #print('Encontrei ' + str(len(listaLinks)))
   #print('Encontrei ' + str(len(listaLinks2)))
       #elem = browser.find_element_by_class_name('dropup')
       #print('Encontrei ' + len(elem) + ' igual a cover-thumb')
finally:
    browser.quit()
#except:
#    print('Não foi possível encontrar o elemento')
#    print(browser.page_source)


#res = requests.get('http://doweb.rio.rj.gov.br/buscanova/#/p=1&q=material%20hospitalar&di=20100409&df=20100416')
#res.raise_for_status()
#noStarchSoup = bs4.BeautifulSoup(res.text,'html.parser')
#elems = noStarchSoup.select("a", {"class":"link pdf-page"})
#for i in range (len(elems)):
#    print(str(elems[0]))
#res = requests.get('http://doweb.rio.rj.gov.br/portal/edicoes/download/1124/34') 
'''
cria um objeto do tipo response a partir do arquivo encontrado na url, o site não possui certificado de segurança SSL/TSL
Então é necessário ignorar o certificado SSL ou utilizar apenas http ao invés de https
'''
#res.raise_for_status()# caso tenha um status diferente de 200 em relação a conexão sobe um erro

#print(len(res.text))
#arquivoAberto = open('nomeDoArquivo.pdf','wb') #função que indica onde o arquivo pode ser encontrado e o que será feito, wb - write binary, rb- readbinary
#local onde está salvo C:/Users/mathe/source/repos/WebCrawlerPyRJ/WebCrawlerPyRJ/nomeDoArquivo.pdf
#obs: todo arquivo precisa ser considerado binário por mais que seja um txt a fim de poder preservar o unicode
#for chunk in res.iter_content(10000): #Pra cada 100000 bytes restantes quebra o arquivo em 100000 bytes e salva
#        arquivoAberto.write(chunk) #Função que salva no disco
'''
Utiliza um for pra iterar os dados do arquivo de forma que não fique muito pesado para a rede do servidor e nem para o processamento do PC
Funciona de forma semelhante a abertura e fechamento de arquivos em Java
'''
#arquivoAberto.close()