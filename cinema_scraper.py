# -*- coding: utf-8 -*-
## WEB SCRAPPING PÀGINA CINEMA ##

## Importem les libreries que farem servir
import requests
from bs4 import BeautifulSoup
import csv
import re
import datetime
import argparse

## ------ DEFINIM TOTES LES FUNCIONS AUXILIARS ----------------------------
def maxPags(links):
    """
    Funció que ens dirà el nombre màxim de pàgines a la web

    Parameters
    ----------
    links : ResultSet de soup.find_all()
        En aquest cas pasem una llista de links que corresponen a les pagines
        que es poden recórrer des de la primera

    Returns
    -------
    ENTER
        Retorna el número de pàgines que tenim.

    """
    pags = []
    ## Iterem per obtenir les llista de les pagines
    for link in links:
        pags.append(link.string) 
    del pags[-1] ## Llevem la darrera perquè es "SEGÜENT" i no un mumero
    pags = [int(i) for i in pags] #Convertim en llista
    return max(pags)



def fichaTecnica(url):
    """
    Funciò que explora la fitxa tècnica de les películes

    Parameters
    ----------
    url : String
        pàgina web de la fitxa tècnica de la pel·lícula que volem obtenir.

    Returns
    -------
    global_list : Llista
        Llista amb les dades de la pel·lícula: 
        Gènere','Director', 'Interprets', 'Guio',
       'Pais', 'Durada', 'Edat_recomanada', 'Distribuidora', 'Data_estrena'
       Algunes poden quedar buides
    """
    ficha = requests.get(url) ## Obtenim la pagina de la pelicula 
    soup = BeautifulSoup(ficha.content, 'html.parser')
    global_list = []
    reparto = []
    fichaTecnica = soup.find_all('span', {"class":"span_rojo"})
    ## Iterem sobre els elements span_rojo per obtenir les dades corresponents
    for elemento in fichaTecnica:
        if len(elemento) == 1:
            global_list.append(elemento.string)
        else:
            for elem in elemento:
                if elem != ", ":
                    reparto.append(elem.string)
            
            reparto_str = ', '.join(reparto)
            global_list.append(reparto_str)
            reparto = []


    ## Fem el mateix pels elements de span_negro 
    fichaTecnica = soup.find_all('span', {'class': 'span_negro'})
    for elemento in fichaTecnica:
        global_list.append(elemento.string)
    
    #Retornem la llista de les dades
    return global_list

def getDataPage(i, filename, valores):
    """
    Funció que ens escriura les dades de la pàgina web principal. 
    que conté la llista de pel·lícules.
    

    Parameters
    ----------
    i : Integer
        Número que simplement és un comptador per poder numerar les pelis.
    filename : String
        Nom de l'arxiu csv on escriurem les dades.
    Valores : ResultSet de soup.find_all()
        Resultat de la cerca de soup sobre la que treballarem.

    Returns
    -------
    i : Integer
        Valor del comptador al final d'escriure aquest CSV + 1, es a dir, 
        llest per escriure el sgüent.
    fecha : String
        Data de la darrera película cercada en format String.

    """
    #### Iterem sobre la llista de pelicules i fem la crida a la fichaTecnica
    #### per obtenir les dades de la película concreta
    
    for valor in valores:
        print(i) ## Imprimim el comptador per tenir sensació de progressió en el procés
        listaPeli = [i] ##Incloem el comptador
        
        ## Cerquem el link de la pelicula que està en la iteracio
        link = valor.find('a')
        url = link.get('href')
        a_list = fichaTecnica(url) #Obtenim les dades de la pelicula
        
        ##Obtenim la resta de dades i les afegim a la llista
        titulo = valor.find('h3').text.strip()
        puntos = valor.find('img')
        fecha = valor.find('p').text.strip()
        listaPeli.append(titulo)
        listaPeli.append(puntos.attrs['alt'])
        listaPeli.append(fecha)
        
        ##Afegim els elements de la fitxa tecnica
        for element in a_list:
            listaPeli.append(element)
        i += 1
        
        ## Afegim les dades al fitxer
        with open(filename, 'a', newline = '', encoding='utf-8' ) as file:
            writer = csv.writer(file)
            writer.writerow(listaPeli)
    return i, fecha

###------------------------------------------------------------------------------------------------------------
### PROCES PRINCIPAL

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
n = maxPags(links) ## Num de pagines disponibles sobre les que iterar

## Processem les dates introduides
fechaFinal = datetime.datetime.strptime(args.fechaFinal, "%d-%m-%Y")
maxDate = datetime.datetime(2014, 5, 9)

## Si la data es superior a la maxima possible ens quedarem amb la maxima
## Si es el cas ho informarem per pantalla
if fechaFinal.date() < maxDate.date():
    print("Fecha final superior al máximo")
    print("---- buscando hasta el dia 9-5-2014")
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
    number, fecha = getDataPage(number, 'DarreresEstrenes.csv', valores)
    fecha = datetime.datetime.strptime(fecha, "%d-%m-%Y")
    if fecha.date() <= maxDate.date():
        break ## En cas d'arribar a la data limit finalitzem el procés
