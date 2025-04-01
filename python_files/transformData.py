import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# 3.- Tercer punto de la asignación: Transformación de los datos.
"""
Realiza las transformaciones necesarias para que la información extraída cumpla con el esquema. 
Puedes realizarlas con el lenguaje de programación de tu preferencia.

Incluye comentarios acerca de que transformaciones tuviste que realizar y que retos te encontraste en la 
implementación de estos mecanismos de transformación.

"""
def format_amount(value):
    try:
        # Convertir a float y redondear a 2 decimales
        amount = round(float(value), 2)
        return amount
    except (ValueError, TypeError):
        return 0.00  # Valor por defecto para los errores


# Cargamos el archivo CSV que extraimos en el paso anterior
df = pd.read_csv("csv/extracted_data.csv")

# Renombramos las columnasdel data Frame
df = df.rename(columns={'name': 'company_name', 'paid_at': 'updated_at'})

#Eliminamos duplicados y manejamos valores nulos para que no tengamos errores en la poblacion de los datos
df = df.dropna(subset=['company_id'])
df = df.dropna(subset=['id'])
# Aplicar la función a la columna amount
df['amount'] = df['amount'].apply(format_amount)

# df['created_at'] = pd.to_datetime(df['created_at'], format='%d-%m-%Y')
# Convertimos las columnas de fechas a su formato datetime
df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')
df['updated_at'] = pd.to_datetime(df['updated_at'], format='mixed')

# A la columa de updated_at cuando venga vacio, le asigamos un valor de nulo
df['updated_at'] = df['updated_at'].fillna(pd.NaT)
#Los campos nulos vamos a rellenarlos con un string vacio
df['company_name'] = df['company_name'].fillna('')

#quitamos el id con *
df = df[df['company_id'] != '*******']


#Guardamos el dataframe transformado en un nuevo archivo CSV
df.to_csv("csv/transformed_data.csv", index=False)

"""
Tuve que renombrar los nombres de las columnas debido  aque asi lo solicitaba en la asignación.
Para el caso de los campos de fecha, tuve que convertirlos a un formato datetime para poder apegarme al esquema solicitado.
Los problemas aparecieron cuando los campos de fecha venían vacios, por lo que tuve que usar el formato 'mixed' para poder 
convertirlos a datetime sin tantos probelmas. Lo que me daba más felixibilidad al tratrar dichos datos
También tuve bastantes problemas con los valores nulos en el campo de company_name y con las compañias que anda mas causaban ruido
A su vez, la longitud de algunos valores del mount yambien hacía que tronara el código.
"""