# -*- coding: utf-8 -*-
## WEB SCRAPPING PÀGINA CINEMA ##

## Importem les libreries que farem servir
import requests
from bs4 import BeautifulSoup
import csv
import re
import datetime
import argparse

## ------ CRIDEM LES FUNCIONS AUXILIARS QUE NECESSITEM----------------------------

import maxPags

import getData

###------------------------------------------------------------------------------------------------------------


## Processem els arguments

parser = argparse.ArgumentParser()
parser.add_argument("--fechaFinal", help = "Introduce la fecha final del intervalo")
args = parser.parse_args()

## Obrim l'arxiu i posem la primera fila que és el nom dels camps.

with open('DarreresEstrenes.csv', 'w', newline = '', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Titol', 'Valoracio', 'Data_critica', 'Gènere','Director', 'Interprets', 'Guio',
                    'Pais', 'Durada', 'Edat_recomanada', 'Distribuidora', 'Data_estrena'])
    file.close()

## Anem a la pagina principal per cercar el nombre maxim de pagines sobre les que iterar
page = requests.get('https://cinemania.20minutos.es/criticas/')
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.find_all('a', href = re.compile('^https://cinemania.20minutos.es/criticas/page/'))
n = maxPags.maxPags(links) ## Num de pagines disponibles sobre les que iterar

## Processem les dates introduides
fechaFinal = datetime.datetime.strptime(args.fechaFinal, "%d-%m-%Y")
maxDate = datetime.datetime(2014, 6, 30)

## Si la data es superior a la maxima possible ens quedarem amb la maxima
## Si es el cas ho informarem per pantalla
if fechaFinal.date() < maxDate.date():
    print("Fecha final superior al máximo")
    print("---- buscando hasta el dia 30-6-2014")
else:
    maxDate = fechaFinal

###Comencem el proces de cerca definint la pagina de les critiques i comencem per la pagina 1
url ='https://cinemania.20minutos.es/criticas/?paged='
number = 1

## Anirem pagina a pagina fins arribar a la data
##En cada iteracio fem la crida a la funcio getDataPage
for i in range(n):
    url_new = url+str(i+1)
    page = requests.get(url_new)
    soup = BeautifulSoup(page.content, 'html.parser')
    valores = soup.find_all('div', {'class': "cuerpo"})
    number, fecha = getData.getDataPage(number, 'DarreresEstrenes.csv', valores)
    fecha = datetime.datetime.strptime(fecha, "%d-%m-%Y")
    if fecha.date() <= maxDate.date():
        break ## En cas d'arribar a la data limit finalitzem el procés
