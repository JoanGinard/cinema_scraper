# -*- coding: utf-8 -*-



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