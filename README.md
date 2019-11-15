# reservations

Una empresa de viajes quiere integrar un sistema de recomendaciones de hoteles a su sistema de reservas de tickets. Para ello un equipo externo desarrollo una API que informa las últimas novedades de reservas.

API Reservas: https://brubank-flights.herokuapp.com/flight-reservations
Respuesta: array de reservas con su fecha de viaje, destino y ID

Restricciones de la API de Reservas:

* Cada llamada a la API retorna las nuevas reservas generadas desde la última petición
* La API utiliza un cache que expira luego de 10 minutos, por lo tanto si no son consumidas las reservas se pierden


El ejercicio consiste en crear una API REST con un solo endpoint que recibe como parámetro un "destino" y retorna un json con dos campos: 

* Lista de reservas (ID y fecha) para ese destino (ordenadas por fecha)
* Lista de hoteles de la ciudad destino (nombre y dirección).

Tener en cuenta que no se deben perder reservas y la API debe devolver la información de todas las reservas generadas en el tiempo

Para obtener un listado de hoteles en la ciudad destino se evaluó utilizar la API de FourSquare:

Documentación: 
https://developer.foursquare.com/docs/api/endpoints
https://developer.foursquare.com/docs/api/configuration/authentication

CLIENT_ID: HACVIHTUOMFKVK5HWQ0J0JCOKQAA2CSAVFS0LFQVN14EESS2 
CLIENT_SECRET: 50ITRVSKRB1GH2YWOBBQWZS5BEDVEIWN3Z2YABJEI454V2JZ

Ej: https://api.foursquare.com/v2/venues/search?near=buenos%20aires&intent=browse&query=hotel&client_id=HACVIHTUOMFKVK5HWQ0J0JCOKQAA2CSAVFS0LFQVN14EESS2&client_secret=50ITRVSKRB1GH2YWOBBQWZS5BEDVEIWN3Z2YABJEI454V2JZ&v=20190709


El ejercicio se puede realizar en cualquier lenguaje de programación, utilizar cualquier DB u otras herramientas siempre y cuando se especifiquen los pasos de instalación y ejecución del programa.

Entregables

- Repositorio de código y tests
- Archivo de documentación de la API
- Explicar como mejorar la arquitectura de la integración y el sistema si se pudiese modificar el sistema de reservas

Puntos extra

- Caching de la información localmente
- Explicación de decisiones a la hora de armar la API en el archivo de docs

## Requerimientos

Python 3.6.7 y virtual host
 ó
Docker y Docker-compose

### Instalación
#### En Ubuntu

 - Instalar drivers y pip
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
```

 - clonar este repositorio
 - ir a la carpeta de la aplicación
 - crear un nuevo virtual env
 - activar virtual env
 - instalar requirements de pip
 - crear local_settings.py en la carpeta /carpeta/del/proyecto/reservations/ usando uno de los local_settings_entornoadecuado.py
 - correr migraciones
```
git clone https://github.com/angdmz/reservations.git /carpeta/del/proyecto
cd /carpeta/del/proyecto
virtualenv -p python3 /carpeta/del/venv
source /carpeta/del/venv/bin/activate
pip install -U requirements.txt
cp reservations/local_settings_entornoadecuado.py reservations/local_settings.py 
python manage.py migrate
```

 - cronear python manage.py update_reservations a un tiempo deseado menor a 10 minutos
 - correr el servidor local (desarrollo solamente)

```
python manage.py runserver 127.0.0.1:8000
```

### Docker
#### Requisitos
Docker instalado y docker-compose instalado

#### Deploy
 - clonar este repositorio
 - ir a la carpeta de la aplicación
 - correr docker-compose
 - crear archivo de nombre .env con variables SECRET_KEY y POSTGRES_PASSWORD usando template .envexample
 - cronear la invocacion a container de upload_reservations
```
git clone https://github.com/angdmz/reservations.git /carpeta/del/proyecto
cd /carpeta/del/proyecto
docker-compose -d up
docker exec recommendations-app python manage.py update_reservations
```


#### Para desarrollo
 - clonar este repositorio
 - ir a la carpeta de la aplicación
 - Buildear imagen
 - Correr docker-compose
 - crear local_settings.py en la carpeta /carpeta/del/proyecto/reservations/ usando uno de los local_settings_entornoadecuado.py
 - correr migraciones
 - iniciar servidor
 - cronear comando de django

```
git clone https://github.com/angdmz/reservations.git /carpeta/del/proyecto
cd /carpeta/del/proyecto
docker build -t reservations:dev -f Dockerfile.dev .
docker-compose -f Dockerfile.dev up &
docker run -it -v $(pwd):/opt/project --rm --name migraciones reservations:dev python manage.py migrate
docker run -d -v $(pwd):/opt/project --rm -p algunPuerto:8000 --name aplicacion reservations:dev python manage.py runserver 0.0.0.0:8000
docker run -d -v $(pwd):/opt/project --rm --name update reservations:dev python manage.py update_reservations
```

## API Docs

- GET /recommendations
    -  destination -> str : required. Es el nombre de una ciudad o pais, es *case insensitive* 
    
    Devuelve diccionario con clave *results* que a su vez su significado es otro diccionario con claves *hotels* y *reservations*, que tienen los hoteles y las reservaciones ordenadas por fecha respectivamente
    
La documentación de la API se puede ver en Swagger también, endpont /v1/docs

## Decisiones tomadas

La aplicación está desarrollada sobre Python 3.6.7 y Django 2.2.6, Python porque es una herramienta de desarrollo flexible y robusta, y Django porque es un framework de desarrollo bastante rápido, fácil de usar, y con la mayoría de los features necesarios para proyectos que tienen que entregarse en período de tiempo corto

La idea para encarar el problema es desarrollar primero una API que exponga el servicio que se pide,
 y un daemon o cron que cada cierto tiempo traiga las nuevas reservaciones y las persista en DB, esto fue decidido así 
 en lugar de lazy loading porque como las reservaciones se limpian regularmente, en caso de que no se invoque el servicio durante ese tiempo entonces queda una inconsistencia entre los datos a exponer.
 Además en este comando, para cada destino de cada reservacion, se buscan hoteles y se los persiste en DB también, esto se hace así porque es más fácil hacer búsquedas sobre DB que una cache tipo clave=>valor si no tengo la clave exacta, que es el caso de buscar destinos sin usar el término standarizado

Este cron, que ejecutará el comando Django upload_reservations, traerá todas las reservaciones, y en el momento también buscará los hoteles de las locaciones de cada una, entonces en el momento de consumir la API, no se dependerá de ningún servicio externo y el overhead único será sobre la DB de la aplicación



## Mejores a la aplicacion

Ahora, la aplicacion usa como persistencia Postgres, y las busquedas de las ciudades y paises se hace con %, lo cual puede ser ineficiente a largo plazo, deberia cambiarse por ElasticSearch que es mejor para búsqueda de texto

El comando que actualiza las reservaciones en la aplicación debería buscar los hoteles de forma asincrónica para tardar menos en la ejecución

Si se pudiera modificar el sistema de reservas, haria que exponga un servicio para buscar reservaciones por destino, al igual que funciona esta API. Asi no tendria que tener un cron o daemon que levante las reservaciones nuevas regularmente, y se pueden obtener de forma lazy y cachearse normalmente