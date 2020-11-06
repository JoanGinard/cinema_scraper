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
1. Joan Ginard Illescas (té dos usuaris JoanGinard, creat per aquesta pràctica i Lordofthe0s, que era un usuari anterior i des del qual s'han pujat alguns arxius des del repositori local)
2. Miquel Piña Grau

## FITXERS DEL REPOSITORI

1. _.gitignore_ Arxiu en el que el git cerca els arxius que dels que no ha de fer el seguiment. En el nostre cas només n'hi ha un.
2. _DarreresEstrenes.csv_ Dataset en format csv amb les dades corresponents.
3. _Explicacio_practica.pdf_ Fitxer on s'explica el projecte i es responen als apartats plantejats a l'enunciat.

__Dins la carpeta codi__

4. _cinema_scraper.py_ Fitxer on trobem el codi Python "principal" per realitzar el web scraping. 
5. _ficha.py_ , _getData.py_, _maxPags.py_ Arxius on col·loquem les funcions auxiliars que fa servir el codi que es troba a cinema_scraper.py.  En realitat la funció que es troba a ficha.py només es crida des de getData.py i no des de cinema_scraper.py. La raó de separar el codi és per facilitar la lectura posterior.

## BRANCHES

Tenim dues __main__, la principal i __master__ on fem el "commit" des de local, per després fer el "merge" amb el main. Es podria esborrar en acabar i presentar el projecte.

## EXECUCIÓ DE L'SCRIPT

Per executar l'script hem d'incloure la data en que volem que acabi de cercar pel·lícules. Hi ha una data màxima (abans no havia una fitxa tècnica ben definida), i en cas d'indicar una data anterior a aquesta el web scraper finalitzarà en aquesta data "màxima".

Per tant per executar s'ha d'indicar (s'inclou una data a mode d'exemple)

```
python cinema_scraper.py --fechaFinal 03-09-2015

```

En aquest punt hem de citar la tasca de @rafoelhonrado i els seu codi a [foodPriceScraper](https://github.com/rafoelhonrado/foodPriceScraper) de la practica de tipologia que ens va donar la idea de procedir així.

Una vegada fet això l'scraper obri el csv i el preparara i accedeix a la web i comprova el màxim de pàgines disponibles a la web. Després comprova si la data final es posterior a la màxima per quedar-se amb una o altre segons el cas.

La pàgina està organitzada de tal manera que cada pàgina té una sèrie de pel·lícules, de les que podem veure algunes dades com el títol i la valoració però per obtenir la resta de dades hem de fer "clic" i entrar a la pàgina.

El nostre scraper accedirà a la pàgina i anirà a la primera pel·lícula i agafarà les dades (fent servir la funció que es troba a _getData.py_) i una vegada ha agafat aquestes dades, entrarà al link de la pel·lícula per agafar la resta de dades de la fitxa tècnica (amb la funció de _ficha.py_ que es troba dins _getData.py_). Així fins aconseguir totes les dades de totes les pel·lícules i després passarà a la següent pàgina i així fins arribar a la data indicada (o la màxima) o al màxim de pàgines, el que arribi primer.


## Zenodo DOI

10.5281/zenodo.4126260
<br/>
LINK: 
https://doi.org/10.5281/zenodo.4126260
