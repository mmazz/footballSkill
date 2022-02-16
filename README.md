# DataBase Premier league


### Pre-requisitos 📋

Estos scrips fueron corridos con Python 3.9.

Los requerimientos de los diferentes modulos usados se encuentran en el requirement.txt.
Para instalarlos:

```
$ pip install -r requirements.txt
```

### Descarga de base de datos 🔧
El repositorio cuenta con un Makefile que descarga y depura la base de datos.
Para ello se corre *$ make data*.
El orden es el siguiente, primero descargamos los datos de todos los torneos.
En el tendremos la informacion para luego escrapear la información de los
jugadores como tambien la de los estadios.
Este último tiene algunos datos incompletos los cuales son completados a "mano"
por medio de otro script.

```
python3 WF_scraper.py
python3 dataBase.py
```

De forma simultanea podemos correr lo siguiente.
Por un lado:

```
python3 WF_scraper_stadium.py
python3 WF_stadium_null_completion.py
```
y por el otro lado:

```
python3 WF_scraper_players.py
```

Por ultimo unificamos todo y depuramos algunas cosas:

```
python3 WF_game_purify.py

```
Esto nos generara los csv necesarios para el analisis.

## Tiempos
Se deja los tiempos de corrida como estimativo sin nignun tipo de analisis de complejidad.
Fue corrido en una maquina virtual con las siguientes especificaciones:...
Makefile: 2.5 dias

WF_scraper.py: 33h
WF_scraper_players.py: 12h
WF_scraper_stadium.py: 10m

## Autores ✒️

* **Matias Mazzanti** - *Doctorando* - [mmazz](https://github.com/mmazz)
* **Esteban Mocskos** - *Director* -

## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles
(en proceso)


