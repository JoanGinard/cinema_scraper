# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import re
import datetime
import argparse


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
    for link in links:
        pags.append(link.string) 
    del pags[-1]
    pags = [int(i) for i in pags]
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
    ficha = requests.get(url)
    soup = BeautifulSoup(ficha.content, 'html.parser')
    global_list = []
    reparto = []
    fichaTecnica = soup.find_all('span', {"class":"span_rojo"})
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



    fichaTecnica = soup.find_all('span', {'class': 'span_negro'})
    for elemento in fichaTecnica:
        global_list.append(elemento.string)
    
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
    
    for valor in valores:
        print(i)
        listaPeli = [i] ##Incloem el comptador
        link = valor.find('a')
        url = link.get('href')
        a_list = fichaTecnica(url)
        titulo = valor.find('h3').text.strip()
        puntos = valor.find('img')
        fecha = valor.find('p').text.strip()
        listaPeli.append(titulo)
        listaPeli.append(puntos.attrs['alt'])
        listaPeli.append(fecha) ## S'ha d'incloure aquesta data????? Al final de la fitxa tècnica tenim una altra
        for element in a_list:
            listaPeli.append(element)
        i += 1
        #print(listaPeli) ## La llista de dades de la pelicula
        with open(filename, 'a', newline = '', encoding='utf-8' ) as file:
            writer = csv.writer(file)
            writer.writerow(listaPeli)
    return i, fecha

### PROCES PRINCIPAL

parser = argparse.ArgumentParser()
parser.add_argument("--fechaFinal", help = "Introduce la fecha final del intervalo")
args = parser.parse_args()

with open('DarreresEstrenes.csv', 'w', newline = '', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Titol', 'Valoracio', 'Data_critica', 'Gènere','Director', 'Interprets', 'Guio',
                    'Pais', 'Durada', 'Edat_recomanada', 'Distribuidora', 'Data_estrena'])
    file.close()

page = requests.get('https://cinemania.20minutos.es/criticas/')
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.find_all('a', href = re.compile('^https://cinemania.20minutos.es/criticas/page/'))
n = maxPags(links)

fechaFinal = datetime.datetime.strptime(args.fechaFinal, "%d-%m-%Y")
maxDate = datetime.datetime(2014, 5, 9)

if fechaFinal.date() < maxDate.date():
    print("Fecha final superior al máximo")
    print("---- buscando hasta el dia 9-5-2014")
else:
    maxDate = fechaFinal

url ='https://cinemania.20minutos.es/criticas/?paged='
number = 1
for i in range(n):
    url_new = url+str(i+1)
    page = requests.get(url_new)
    soup = BeautifulSoup(page.content, 'html.parser')
    valores = soup.find_all('div', {'class': "cuerpo"})
    number, fecha = getDataPage(number, 'DarreresEstrenes.csv', valores)
    fecha = datetime.datetime.strptime(fecha, "%d-%m-%Y")
    if fecha.date() <= maxDate.date():
        break
