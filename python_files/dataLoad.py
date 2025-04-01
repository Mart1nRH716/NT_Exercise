import pandas as pd
from sqlalchemy import create_engine

# 1.- Primer punto de la asignación: Cargar el archivo CSV en una base de datos MySQL.
"""
La información proporcionada se debe de cargar en alguna base de datos. Puede ser estructurada o no estructurada.
Ejemplo: MySQL, Postgres, MongoDB, etc.
Incluye comentarios del por qué elegiste ese tipo de base de datos.
"""
#Leemos el archivo CSV
df = pd.read_csv('csv/data_prueba_tecnica.csv')
#Creamos la conexión a la base de datos MySQL
engine = create_engine('mysql://root:1234@localhost/ntgroup_test')
#Cargamos el DataFrame en la base de datos MySQL
df.to_sql('compania', engine, if_exists='replace', index=False)

"""
Elegí MySQL porque:
    *Ya lo tenía instalado.
    *Es compatible con Python y tiene una amplia variedad de bibliotecas para conectar con él.
    *Tiene una buena compatibilidad con Django.
    *Es una gestor de bases relacional, el cual es ideal para esta tarea.
"""