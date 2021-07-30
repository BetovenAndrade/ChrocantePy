from typing import Text
import requests
import os
from winreg import *
from xml.dom import minidom
import wget
import os
from datetime import date
from zipfile import ZipFile

# Baixando lista de drivers
URL_drivers= "https://chromedriver.storage.googleapis.com/"
response = requests.get(URL_drivers)

# Criando pasta para arquivo da lista de drivers
if not os.path.isdir('./temp'):
    os.mkdir('./temp')

# Gravando a lista de drivers
with open('temp/ListaDrives.xml', 'wb') as file:
    file.write(response.content)

# Capturando a versão do Chrome no registro do Windows
key= OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Google\Chrome\BLBeacon", 0, KEY_READ)
g_version= QueryValueEx(key, 'version')[0]
print(f'A versão do seu Chrome é: {g_version}')

documento : minidom.Document = minidom.parse('temp/ListaDrives.xml')

def link_mostSimilarVersion(documento : minidom.Document):
    
    # Percorrendo o XML dos drivers e procurando o mais atual
    for elemento in documento.getElementsByTagName('Contents'):
        elemento = elemento.getElementsByTagName('Key')[0]
        versaoNoXML = elemento.firstChild.data

        if(('zip' in versaoNoXML) and (not versaoNoXML.startswith('2')) and ('win' in versaoNoXML)):
            if(g_version[0:12] in versaoNoXML[0:12]):
                return r'https://chromedriver.storage.googleapis.com/'+versaoNoXML

            if(g_version[0:9] in versaoNoXML[0:9]):
                return r'https://chromedriver.storage.googleapis.com/'+versaoNoXML
            
            if(g_version[0:7] in versaoNoXML[0:7]):
                return r'https://chromedriver.storage.googleapis.com/'+versaoNoXML

            if(g_version[0:4] in versaoNoXML[0:4]):
                return r'https://chromedriver.storage.googleapis.com/'+versaoNoXML
            
            if(g_version[0:2] in versaoNoXML[0:2]):
                return r'https://chromedriver.storage.googleapis.com/'+versaoNoXML

link = link_mostSimilarVersion(documento) 

# Baixando
onde_baixar = os.path.expanduser('~\\Desktop\\DriverChrome_' + str(date.today()).replace('-', '_'))

if not os.path.isdir(onde_baixar):
    os.mkdir(onde_baixar)

path_completo_arquivo = wget.download(link, onde_baixar)
print(f'A versão {link} do driver foi baixada para {path_completo_arquivo}')

# Descompactando
zip_ = ZipFile(path_completo_arquivo, 'r')
zip_.extractall(onde_baixar)
zip_.close()

#Abrindo diretório
os.startfile(onde_baixar)