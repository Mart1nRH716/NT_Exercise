## NTGROUP Exercise:

Este asignación es una aplicación web desarrollada en Django, diseñada para ejecutar cada uno de las tareas directamente desde la aplicación.
Este proyecto implementa un proceso ETL (Extract, Transform, Load) usando  Pandas y MySQL. Todo esto en un contenedor  Docker.

### Características principales
* **Creación de esquemas y vistas:** El usuario por medio de la ruta 'crear-esquemas/' puede crear las tablas y la vista solicitada de la asignación
* **Almacenamiento de archivos:** La aplicación puede crear y almacenar en el proyecto los archivos generados.
* **Carga de archivo:** La aplicación puede cargar archivos csv para trabajar con es econjutno de datos a posterior.
* **Tranformar:** Una vez cargados los archivos, se puede transoformar los datos de acuerdo con las intrucciones de la asiganción
* **Población de los datos en la base de datos:** Después de realizar todas las actividades descritas, podemos poblar con los datos las tablas específicas.
* **Extracción de un número:** Puede extraer y calcular el número faltante.

### Requisitos del sistema
* **Docker Engine:** >= 20.10
* **Docker Compose** >= 2.17
* **Dependencias:** Las dependencias adicionales se listan en el archivo `requirements.txt`.

### Instalación
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Mart1nRH716/NT_Exercise.git
   
## Instrucciones de Configuración
2. **Crear un entorno virtual
```bash
python -m venv venv
venv\Scripts\activate     # En Windows
source venv/bin/activate   # En Linux/Mac
```

### 3. Crear el archivo de configuracion de las variables de entorno .env
Se debe de crear un archivo .env a la altura del manage.py, pero por fines prácticos, este repositorio ya cuenta con uno.

### 4. Ejecución de Docker
Una vez ubicados en la ruta ntgroup_test, ejecutar el siguiente comando:
```bash
docker-compose up --build
```
### 5.  Una vez iniciados los servicios, accede a:

App Django:
```bash
http://localhost:8000
http://0.0.0.0:8000/ 
```
EndPoints Disponibles:

* /cargar-csv/	GET	Carga datos iniciales desde CSV a MySQL
* /extraer-datos/	GET	Extrae datos y genera CSV
* /transformar-datos/	GET	Aplica transformaciones a los datos
* /cargar-datos-transformados/	GET	Carga datos transformados en esquema final
* app/<number>/ GET Extrae el número compartido en el argumento de la URL y calcula que número se ha extraído.


Contenedor de la base de datos:
```bash
docker exec -it [CONTAINER_ID_DB] mysql -uroot -p1234 ntgroup_test
```

### 6. Ejecución manual del flujo ETL


* 1.- Cargar datos iniciales:
```bash
http://localhost:8000/cargar-csv/
```
* 2.- Extraer datos:
```bash
http://localhost:8000/extraer-datos/
```
* 2.1.- Construir tablas y vista:
```bash
http://localhost:8000/crear-esquemas/
```
* 3.- Transformar datos:
```bash
http://localhost:8000/transformar-datos/
```
* 4.- Cargar estructura final:
**NOTA:** Esta ruta puede tardar un rato en ejecutarse.
```bash
http://localhost:8000/poblar/
```

### 6. Ejecución se query para la vista:
En la terminal conectada a la bd de docker ejecutar:
```bash
SELECT * FROM amount_company_perday;
```



