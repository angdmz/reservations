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