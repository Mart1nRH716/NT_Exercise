import pandas as pd
from sqlalchemy import create_engine

# Connect to MySQL
engine = create_engine('mysql://root:1234@localhost/ntgroup_test')

# Extract data
query = "SELECT * FROM raw_data"
extracted_data = pd.read_sql(query, engine)

# Save to CSV
extracted_data.to_csv('csv/extracted_data.csv', index=False)

"""
Decidí guardarlo en csv debido a que:
    - Los datos son tabulares y pueden ser facilmente leídos y manipulados con pandas.
    - La estructura de los datos es relativamente simple y no requiere de ninguna transformación adicional.
    - Son faciles de leer con cualquier gestor de bases de datos.
Con respecto al lenguaje Python:
Es el lenguaje por excelencia para la manipualción de datos, además, contiene muchas bibliotecas para la manipulacion de datos y conexión con gestores de bases de datos.
"""