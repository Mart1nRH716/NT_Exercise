import pandas as pd
import mysql.connector
from datetime import datetime


df = pd.read_csv("csv/transformed_data.csv")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ntgroup_test"
)
cursor = conn.cursor()


df = df.dropna(subset=['company_id'])
df['company_name'] = df['company_name'].fillna('')

companies = df[['company_id', 'company_name']].drop_duplicates()

for _, row in companies.iterrows():
    try:
        cursor.execute(
            "INSERT INTO companies (company_id, company_name) VALUES (%s, %s)",
            (row['company_id'], row['company_name'])
        )
    except mysql.connector.Error as err:
        print(f"Error inserting company {row['company_id']}: {err}")


for _, row in df.iterrows():
    try:
        updated_at = None if pd.isna(row['updated_at']) else row['updated_at']
        
        cursor.execute(
            "INSERT INTO charges (charge_id, company_id, amount, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (row['id'], row['company_id'], row['amount'], row['status'], row['created_at'], updated_at)
        )
    except mysql.connector.Error as err:
        print(f"Error inserting charge {row['id']}: {err}")


conn.commit()
conn.close()