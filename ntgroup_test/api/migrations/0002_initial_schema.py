# apps/mi_app/migrations/0002_initial_schema.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'), 
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS companies ( 
                company_id VARCHAR(64) NOT NULL PRIMARY KEY, 
                company_name VARCHAR(130) NULL
            );

            CREATE TABLE IF NOT EXISTS charges (
                charge_id VARCHAR(64) NOT NULL PRIMARY KEY,
                company_id VARCHAR(64) NOT NULL,
                amount DECIMAL(16,2) NOT NULL,
                status VARCHAR(30) NOT NULL, 
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NULL,
                FOREIGN KEY (company_id) REFERENCES companies(company_id)
            );
            """
        ),
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW amount_company_perday AS (
                SELECT 
                    ch.company_id, 
                    c.company_name, 
                    SUM(ch.amount) AS total_amount, 
                    DATE(ch.created_at) AS transaction_day 
                FROM charges ch 
                INNER JOIN companies c ON ch.company_id = c.company_id
                GROUP BY ch.company_id, DATE(ch.created_at)
            );
            """
        )
    ]