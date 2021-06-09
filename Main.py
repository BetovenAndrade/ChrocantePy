from typing import Text
import requests
import os
from winreg import *
from xml.dom import minidom
import wget

# Baixando lista de drivers
URL_drivers= "https://chromedriver.storage.googleapis.com/"

response = requests.get(URL_drivers)

with open('temp/ListaDrives.xml', 'wb') as file:
    file.write(response.content)

# Capturando a versão do Chrome no registro do Windows
key= OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Google\Chrome\BLBeacon", 0, KEY_READ)
g_version= QueryValueEx(key, 'version')[0]
print(g_version)

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
print(f'A versão {link} foi baixada para...')
wget.download(link, 'ChromeDriver.zip')