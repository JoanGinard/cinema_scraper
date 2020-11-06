# -*- coding: utf-8 -*-



import csv



## Cridem les funcions auxiliars que necessitem.
import ficha

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
        a_list = ficha.fichaTecnica(url) #Obtenim les dades de la pelicula
        
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


