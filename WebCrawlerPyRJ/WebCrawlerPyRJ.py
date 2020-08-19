
from selenium  import webdriver
import requests, bs4
#lembrar de baixar o driver gecko
#browser = webdriver.Firefox()
#browser.get('https://inventwithpython.com')
#browser.get('http://doweb.rio.rj.gov.br/buscanova/#/p=1&q=material%20hospitalar&di=20100409&df=20100416')
#try:
#       elem = browser.find_element_by_class_name('cover-thumb')
#       print('Encontrei ' + len(elem) + ' igual a cover-thumb')
#except:
#    print('Não foi possível encontrar o elemento')


res = requests.get('http://doweb.rio.rj.gov.br/buscanova/#/p=1&q=material%20hospitalar&di=20100409&df=20100416')
res.raise_for_status()
noStarchSoup = bs4.BeautifulSoup(res.text,'html.parser')
elems = noStarchSoup.select("a", {"class":"link pdf-page"})
for i in range (len(elems)):
    print(str(elems[0]))
res = requests.get('http://doweb.rio.rj.gov.br/portal/edicoes/download/1124/34') 
'''
cria um objeto do tipo response a partir do arquivo encontrado na url, o site não possui certificado de segurança SSL/TSL
Então é necessário ignorar o certificado SSL ou utilizar apenas http ao invés de https
'''
res.raise_for_status()# caso tenha um status diferente de 200 em relação a conexão sobe um erro

print(len(res.text))
arquivoAberto = open('nomeDoArquivo.pdf','wb') #função que indica onde o arquivo pode ser encontrado e o que será feito, wb - write binary, rb- readbinary
#local onde está salvo C:/Users/mathe/source/repos/WebCrawlerPyRJ/WebCrawlerPyRJ/nomeDoArquivo.pdf
#obs: todo arquivo precisa ser considerado binário por mais que seja um txt a fim de poder preservar o unicode
for chunk in res.iter_content(10000): #Pra cada 100000 bytes restantes quebra o arquivo em 100000 bytes e salva
        arquivoAberto.write(chunk) #Função que salva no disco
'''
Utiliza um for pra iterar os dados do arquivo de forma que não fique muito pesado para a rede do servidor e nem para o processamento do PC
Funciona de forma semelhante a abertura e fechamento de arquivos em Java
'''
arquivoAberto.close()