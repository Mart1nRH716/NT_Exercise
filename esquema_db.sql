CREATE DATABASE IF NOT EXISTS ntgroup_test;
USE ntgroup_test;
-- SELECT DISTINCT(created_at) FROM raw_data;

CREATE TABLE IF NOT EXISTS companies ( 
company_id VARCHAR(64) NOT NULL PRIMARY KEY, 
company_name VARCHAR(130) NULL
);

CREATE TABLE IF NOT EXISTS charges (
charge_id VARCHAR(64) NOT NULL PRIMARY KEY,
company_id VARCHAR(64) NOT NULL,
amount DECIMAL(16,2) NOT NULL,
status VARCHAR(30) NOT NULL, 
created_at TIMESTAMP NOT NULL ,
updated_at TIMESTAMP NULL,
FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Tabla donde cargamos la información transformada para que podamos ver el monto total transaccionado por día para las diferentes compañías
-- suma del monto por dia
-- agrupado por compañia y por dia 
CREATE VIEW amount_company_perday AS (
SELECT ch.company_id, c.company_name, SUM(ch.amount) AS total_amount, DATE(ch.created_at) AS transaction_day 
FROM charges ch INNER JOIN companies c ON ch.company_id = c.company_id
GROUP BY ch.company_id, DATE(ch.created_at)
);


