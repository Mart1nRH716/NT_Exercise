import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


df = pd.read_csv('csv/data_prueba_tecnica.csv')

engine = create_engine('mysql://root:1234@localhost/ntgroup_test')

df.to_sql('compania', engine, if_exists='replace', index=False)

"""
Elegí MySQL porque:
    *Ya lo tenía instalado
    *Es compatible con Python y tiene una amplia variedad de bibliotecas para conectar con el
    *Tiene una buena compatibilidad con Django
"""