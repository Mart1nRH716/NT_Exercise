import pandas as pd
from sqlalchemy import create_engine

# 2.- Segundo punto de la asignación: Extracción de los datos.
"""
Se debe de realizar un procedimiento de extracción de la información anterior por medio de algún lenguaje de programación 
que permita procesarlo. El formato final de la información extraída puede ser CSV, Avro, parquet o el que se considere
más adecuado.
Agrega comentarios acerca del por qué tuviste que utilizar el lenguaje y el formato que elegiste. 
También platicamos si te encontraste con algún reto a la hora de extraer la información.

"""
# Creamos la conexión a la base de datos MySQL
engine = create_engine('mysql://root:1234@localhost/ntgroup_test')

# Realizamos la consulta para extraer los datos y lo guardamos en un DataFrame
query = "SELECT * FROM compania"
extracted_data = pd.read_sql(query, engine)

# Guardamos el DataFrame en un archivo CSV
extracted_data.to_csv('csv/extracted_data.csv', index=False)

"""
Decidí guardarlo en csv debido a que:
    - Los datos son tabulares y pueden ser facilmente leídos y manipulados con pandas.
    - La estructura de los datos es relativamente simple y no requiere de ninguna transformación adicional.
    - Son faciles de leer con cualquier gestor de bases de datos.
Con respecto al lenguaje Python:
Es el lenguaje por excelencia para la manipualción de datos, además, contiene muchas bibliotecas para la 
manipulacion de datos y conexión con gestores de bases de datos.
Además, es el lenguaje de programación que se solicitó usar para esta tarea.
Con respecto a los retos, no tuve problemas para extraer la información
"""