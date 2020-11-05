# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


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


