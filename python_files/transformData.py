import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

df = pd.read_csv("csv/extracted_data.csv")

df = df.rename(columns={'name': 'company_name', 'paid_at': 'updated_at'})

# df['created_at'] = pd.to_datetime(df['created_at'], format='%d-%m-%Y')
df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')
df['updated_at'] = pd.to_datetime(df['updated_at'], format='mixed')

df['updated_at'] = df['updated_at'].fillna(pd.NaT)

df.to_csv("csv/transformed_data.csv", index=False)
