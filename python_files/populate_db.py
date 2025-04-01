import pandas as pd
import mysql.connector
from datetime import datetime

# 4.- Cuarto punto de la asignación: Craga de los datos transoformados a la base de datos.
"""
Se debe de utilizar una base de datos MySQL, Postgres, MongoDB, etc. 
En esta base se va a crear un esquema estructurado basado en el ejercicio anterior, pero debemos de crear una tabla 
llamada charges donde tendremos la información de las transacciones y otra llamada companies donde incluiremos la
información de las compañias. Estas tablas deberán de estar relacionadas. 
Cargaremos la información del dataset en estas dos tablas.

Incluye el diagrama de base de datos resultado de este ejercicio.

"""

#Cargamos el archivo CSV que ya hemos transformado
df = pd.read_csv("csv/transformed_data.csv")

# Creamos un motor de conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ntgroup_test"
)
#Creamos un cursor para tratar fila por fila
cursor = conn.cursor()
companies = df[['company_id', 'company_name']].drop_duplicates()

companies = companies.drop_duplicates(subset='company_id', keep='first')

print (companies.head())

#Recorremos el dataframe y vamos insertando los datos en la tabla companies
for _, row in companies.iterrows():
    try:
        cursor.execute(
            "INSERT INTO companies (company_id, company_name) VALUES (%s, %s)",
            (row['company_id'], row['company_name'])
        )
    except mysql.connector.Error as err:
        print(f"Error inserting company {row['company_id']}: {err}")

#Recorremos el dataframe y vamos insertando los datos en la tabla charges
for _, row in df.iterrows():
    try:
        updated_at = None if pd.isna(row['updated_at']) else row['updated_at']
        
        cursor.execute(
            "INSERT INTO charges (charge_id, company_id, amount, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (row['id'], row['company_id'], row['amount'], row['status'], row['created_at'], updated_at)
        )
    except mysql.connector.Error as err:
        print(f"Error inserting charge {row['id']}: {err}")

# Finalizamos y confirmamos los cambios en la base de datos
conn.commit()
conn.close()