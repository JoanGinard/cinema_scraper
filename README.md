<br/>
<br/>

# CINEMA SCRAPER. PRÀCTICA WEB SCRAPING

## PROJECTE
Aquest treball correspon a una pràctica de l'assignatura _Tipologia i cicle de vida de les dades_ de la __UOC__

L'objectiu de la pràctica és aplicar _web scraping_ a una web per tal d'obtenir un joc de dades que publicarem a _zenodo_
En el nostre cas hem triar construir un dataset de cinema, a partir de la web de [CINEMANIA](https://cinemania.20minutos.es/).

En concret en centrarem en l'apartat de crítiques i extreurem la valoració de les pel·lícules juntament amb les dades de la seva fitxa tècnica.


## MEMBRES DE L'EQUIP
(en ordre alfabètic)
1. Joan Ginard Illescas
2. Miquel Piña Grau

## FITXERS DEL REPOSITORI

1. _cinema_scraper.py_ Fitxer on trobem el codi Python per realitzar el web scraping
2. _DarreresEstrenes.csv_ Dataset en format csv amb les dades corresponents.
2. _Explicacio_practica.pdf_ Fitxer on s'explica el projecte i es responen als apartats plantejats a l'enunciat

## BRANCHES

Tenim dues __main__, la principal i __master__ on fem el commit des de local. Es podrà esborrar en acabar el projecte.

## EXECUCIÓ DE L'SCRIPT

Per executar l'script hem d'incloure la data en que volem que acabi de cercar pel·lícules. Hi ha una data màxima (abans no havia una fitxa tècnica ben definida), i en cas d'indicar una data anterior a aquesta el web scraper finalitzarà en aquesta data "màxima".

Per tant per executar s'ha d'indicar (s'inclou una data a mode d'exemple)

```
python cinema_scraper.py --fechaFinal 03-09-2015

```

En aquest punt hem de citar la tasca de @rafoelhonrado i els seu codi a [foodPriceScraper](https://github.com/rafoelhonrado/foodPriceScraper) de la practica de tipologia que ens va donar la idea de procedir així.



## Zenodo DOI

10.5281/zenodo.4126260
<br/>
LINK: 
https://doi.org/10.5281/zenodo.4126260
