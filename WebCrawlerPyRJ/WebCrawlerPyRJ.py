
from selenium  import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, pathlib

def definicao_categorias_buscadas(nome_arquivo_txt):
    """ Função responsável pela leitura de arquivos e criação de lista de itens a serem pesquisados no site

    Função que recebe o local de leitura de um arquivo txt com um formato específico (exemplificado abaixo) 
    para fazer a busca dos PDF no site http://doweb.rio.rj.gov.br, essa função tem como utilidade a pesquisa de novos
    títulos sem a necesidade de fazer alteração no código.

    @Param Recebe como string o local do txt para ser lido com a lista de informações de pesquisa
    @Return retorna uma lista de listas de strings com 3 itens, sendo eles:
        - itens[0] = Produto a ser pesquisado
        - itens[1] = Data de início da pesquisa
        - itens[2] = Data de fim da pesquisa
    Padrão do formato - nome_produto, di=aaaaMMdd, df=aaaaMMdd
    """

    arquivo = open(nome_arquivo_txt, "r")
    lista_itens_pesquisar = []
    num_linhas = sum(1 for line in open(nome_arquivo_txt))
    for i in range (num_linhas):
        linha_arquivo = arquivo.readline()
        itens = linha_arquivo.split(", ")
        itens[0] = substituicao_espaco_padrao_url(itens[0])
        lista_itens_pesquisar.append(itens)
    arquivo.close()
    return lista_itens_pesquisar

def substituicao_espaco_padrao_url(str):
    """ Função que padroniza nomes que possuem espaço para busca na url

    Por padrão a URL do site http://doweb.rio.rj.gov.br encara espaços como %20 na hora de pesquisar algum item, 
    portanto é necessário fazer a transformação caso o item procurado seja uma palavra composta, isso é formada por 
    mais de uma palavra e consequentemente conter espaço (" ")
    @Param String pra ser validada
    @Return String formatada de forma adequada

    """
    if " " not in str:
        return str
    else:
        return str.replace(" ", "%20")
 
def acessar_site(url_pesquisa, lista_itens):
    """ Função que busca link dos PDFs para download por meio de selenium

    A função utiliza o selenium para abrir um browser firefox e fazer buscas no site http://doweb.rio.rj.gov.br para
    coletar os links para baixar os PDFs dos diários oficiais relacionados ao tema de pesquisa, ele realiza um loop para
    acessar todas as páginas de determinado item sendo que na primeira iteração ele não necessita recarregar a página porque
    já foi carregada anteriormente para definir o número de iterações do loop.

    LEMBRAR DE BAIXAR O DRIVER GECKO (ponte entre o firefox e o selenium) E COLOCAR NO SEU PATH
    @Param url_pesquisa - String formada pela url de pesquisa montada previamente para já poder definir o número de iterações
    @Param lista_itens - informações necessárias para montar as novas URLs que devem ser acessadas
    @Return links - Uma lista de lista de strings contendo as URLs para download dos arquivos

    """
    #
    browser = webdriver.Firefox()
    browser.get(url_pesquisa)
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropup')))
        #Necessário esperar o site executar uma ação Ajax para carregas os itens da página

        maxPage = browser.find_element_by_class_name("mostrador-paginas")
        total_pag = define_num_pag(maxPage)
        links = []
        i = 1
        while i < (total_pag+1):
            if (i != 1):
                url_iteracao = montador_url(lista_itens, i)
                browser.get(url_iteracao)
                wait = WebDriverWait(browser, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropup')))
                for elem in browser.find_elements_by_class_name('dropup'):
                     if (elem.text == "  Download"):
                         elem.click()
                         pdfLinks = browser.find_elements_by_css_selector("a[class = 'link pdf-page']")
                         links.append([pdfLink.get_attribute('href') for pdfLink in pdfLinks])
                         break
                i = i + 1
            else:
                  for elem in browser.find_elements_by_class_name('dropup'):
                     if (elem.text == "  Download"):
                         elem.click()
                         pdfLinks = browser.find_elements_by_css_selector("a[class = 'link pdf-page']")
                         links = ([pdfLink.get_attribute('href') for pdfLink in pdfLinks])
                         break
                  i = i + 1   
    finally:
        browser.quit()
        return links


def define_num_pag(elem_pag):
    """ Função responsável po pegar a string que define o número de páginas da pesquisa

    A função recebe a string encontrada no site contendo o número de páginas que compõe aquela pesquisa.
    O formato é: página 1 de x. X sendo o número de páginas máximas, portanto eu inverto a string isolando
    o número final, separo ele pelo espaço e depois inverto novamente para evitar problemas do tipo 12 se tornar 21
    @Param elem_pag - objeto de retorno do selenium quando se busca um objeto na página
    @Return total_pag - Inteiro contendo o valor total de páginas

    """
    str_pag = str(elem_pag.text)#resgata texto falando quantas páginas de resultados foram encontradas
    str_pag = str_pag[::-1] #inverte a string
    list_separada_str_pag = (str_pag.split(" ",1))#Pega o número final de páginas, separado por um  espaço (" ")
    list_separada_str_pag[0] = list_separada_str_pag[0][::-1]
    total_pag = int(list_separada_str_pag[0])
    return total_pag

def downloader(lista_links, assunto, nome_pdf):
    """ Função responsável por utilizar requests para baixar uma lista de PDFs

    A função cria um novo arquivo binário baseado nos links que recebe
    """
    for i in range (len(lista_links)):
        res = requests.get(lista_links[i], verify=False)
        res.raise_for_status()
        nome_pdf = '/Download/'+str(nome_pdf).zfill(3)
        nome_pdf = assunto+numPDF+'.pdf'
        arquivo_aberto = open(nome_pdf, 'wb')
        for chunk in res.iter_content(10000):
            arquivoAberto.write(chunk)
        arquivo_aberto.close()

def montador_url(lista_itens, num_int):
    """ Função responsável por montar url seguindo os padrões de pesquisa do site https://doweb.rio.rj.gov.br/

    @Param lista_itens - recebe a lista de itens necessárias para montar a url sendo:
        - lista_itens[0] = Produto a ser pesquisado
        - lista_itens[1] = Data de início da pesquisa
        - lista_itens[2] = Data de fim da pesquisa
    @Param num_int - Inteiro que indica qual número da página pra ser procurada
    @Return url_montada - URL para pesquisa

    """
    url_base = 'http://doweb.rio.rj.gov.br/buscanova/#/p='
    url_montada = url_base+str(num_int)+"&q="+lista_itens[0]+"&"+lista_itens[1]+"&"+lista_itens[2]
    return url_montada


lista_itens_pesquisar = definicao_categorias_buscadas('arquivo_busca_pdf.txt')
for i in range (len(lista_itens_pesquisar)):
    url_pesquisar = montador_url(lista_itens_pesquisar[i],1)
    list = acessar_site(url_pesquisar,lista_itens_pesquisar[i])
    for i in range (len(list)):
        print (str(len(list)))
        if len(list[i]) == 0 :
            print (list[i])
        else:
            for j in range (len(list[i])):
                print(list[i][j])

#local onde está salvo C:/Users/mathe/source/repos/WebCrawlerPyRJ/WebCrawlerPyRJ/nomeDoArquivo.pdf