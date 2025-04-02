from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NumberSet
from django.db import connection
import pandas as pd
from sqlalchemy import create_engine
from django.views import View
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)
import json

def extract_number(request, number):
    """Endpoint de la API para extraer un número, extraer el numero desde el arg de la url"""
    if request.method == 'GET':
        try:
            number = int(number)
                
            if number < 1 or number > 100:
                return JsonResponse({'error': 'El número debe de estar entre 1-100'}, status=400)
            
            #Extraemos el número
            number_set = NumberSet()
            number_set.extract(number)
            
            #Encontramos el número faltante
            missing_number = number_set.find_missing()
            
            return JsonResponse({
                'extracted_number': number,
                'missing_number': missing_number,
                'success': True
            })
            
        except ValueError as e:
            return JsonResponse({'error': 'La entrada debe ser numérica'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Ocurrio un error inseperado'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


class CargarCSVView(View):
    """
    Vista para cargar datos desde un CSV a MySQL
    Ejemplo de uso: /cargar-csv/
    """
    
    csv_path = os.path.join(settings.BASE_DIR, 'csv', 'data_prueba_tecnica.csv')
    tabla_name = 'compania'
    
    def get(self, request, *args, **kwargs):
        try:
            # 1. Leer archivo CSV
            df = self.leer_csv()
            
            # 2. Crear conexión a MySQL
            engine = self.crear_conexion()
            
            # 3. Cargar datos
            self.cargar_datos(df, engine)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Datos cargados exitosamente',
                'registros': len(df)
            })
            
        except FileNotFoundError as e:
            logger.error(f"Error de archivo no encontrado: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def leer_csv(self):
        """Lee el archivo CSV y retorna un DataFrame"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Archivo CSV no encontrado en: {self.csv_path}")
            
        return pd.read_csv(self.csv_path)

    def crear_conexion(self):
        """Crea la conexión a MySQL usando las configuraciones de Django"""
        db_config = settings.DATABASES['default']
        connection_string = (
            f"mysql://{db_config['USER']}:{db_config['PASSWORD']}"
            f"@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        )
        return create_engine(connection_string)

    def cargar_datos(self, df, engine):
        """Carga los datos del DataFrame a la base de datos"""
        df.to_sql(
            name=self.tabla_name,
            con=engine,
            if_exists='replace',
            index=False
        )
        logger.info(f"Datos cargados en tabla {self.tabla_name}")
        
class ExtraerDatosView(View):
    """
    Vista para extraer datos de MySQL y convertirlos a CSV
    URL: /extraer-datos/
    """
    
    def get(self, request, *args, **kwargs):
        try:
            df = self.extraer_datos()
            
            # Ruta donde se guardará (crea la carpeta 'outputs' primero)
            output_dir = os.path.join(settings.BASE_DIR, 'salidas')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'datos_extraidos.csv')
            
            df.to_csv(output_path, index=False)
            
            logger.info(f"Datos guardados en {output_path}")
            return JsonResponse({
                'status': 'success',
                'message': f"Archivo guardado en {output_path}",
                'path': output_path
            })
            
        except Exception as e:
            logger.error(f"Error al extraer datos: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def extraer_datos(self):
        """Extrae datos de MySQL y retorna un DataFrame"""
        # Usar configuración de Django para la conexión
        db_config = settings.DATABASES['default']
        connection_string = (
            f"mysql://{db_config['USER']}:{db_config['PASSWORD']}"
            f"@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        )
        
        engine = create_engine(connection_string)
        query = "SELECT * FROM compania"
        
        return pd.read_sql(query, engine)
    
class TransformarDatosView(View):
    """
    Vista para transformar datos según la asignación
    """
    
    def get(self, request, *args, **kwargs):
        try:
            # 1. Cargar datos
            input_path = os.path.join(settings.BASE_DIR, 'salidas', 'datos_extraidos.csv')
            df = self.cargar_datos(input_path)
            
            # 2. Aplicar transformaciones
            df_transformado = self.aplicar_transformaciones(df)
            
            # 3. Guardar resultado
            output_path = os.path.join(settings.BASE_DIR, 'salidas', 'datos_transformados.csv')
            df_transformado.to_csv(output_path, index=False)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Datos transformados exitosamente',
                'output_path': output_path,
                'registros_transformados': len(df_transformado)
            })
            
        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Archivo no encontrado: {str(e)}"
            }, status=404)
            
        except Exception as e:
            logger.error(f"Error transformando datos: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Error transformando datos: {str(e)}"
            }, status=500)

    def cargar_datos(self, file_path):
        """Carga el archivo CSV en un DataFrame"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo {file_path} no encontrado")
        return pd.read_csv(file_path)

    def aplicar_transformaciones(self, df):
        """Aplica todas las transformaciones necesarias"""
        # 1. Renombrar columnas
        df = df.rename(columns={
            'name': 'company_name',
            'paid_at': 'updated_at'
        })
        
        # 2. Eliminar filas con IDs nulos
        df = df.dropna(subset=['company_id', 'id'])
        
        # 3. Formatear montos
        df['amount'] = df['amount'].apply(self.format_amount)
        
        # 4. Convertir fechas
        df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')
        df['updated_at'] = pd.to_datetime(df['updated_at'], format='mixed', errors='coerce')
        
        # 5. Manejar valores nulos
        df['company_name'] = df['company_name'].fillna('')
        df['updated_at'] = df['updated_at'].fillna(pd.NaT)
        
        # 6. Filtrar IDs inválidos
        df = df[df['company_id'] != '*******']
        
        return df

    def format_amount(self, value):
        """Formatea el monto a 2 decimales"""
        try:
            return round(float(value), 2)
        except (ValueError, TypeError):
            logger.warning(f"Valor de monto inválido: {value}")
            return 0.00
        
class CargarDatosTransformadosView(View):
    """
    Vista para cargar datos transformados a las tablas companies y charges
    """
    
    def get(self, request, *args, **kwargs):
        try:
            # 1. Cargar archivo transformado
            file_path = os.path.join(settings.BASE_DIR, 'salidas', 'datos_transformados.csv')
            df = self.cargar_datos(file_path)
            
            # 2. Cargar datos en MySQL
            stats = self.cargar_en_bd(df)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Datos transformados cargados exitosamente',
                'stats': stats
            })
            
        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Archivo no encontrado: {str(e)}"
            }, status=404)
            
        except Exception as e:
            logger.error(f"Error cargando datos: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Error cargando datos: {str(e)}"
            }, status=500)

    def cargar_datos(self, file_path):
        """Carga el archivo CSV transformado"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        return pd.read_csv(file_path)

    def cargar_en_bd(self, df):
        """Carga los datos en las tablas MySQL"""
        stats = {
            'companies_insertadas': 0,
            'charges_insertados': 0,
            'errores_companies': 0,
            'errores_charges': 0
        }
        
        # Procesar companies
        companies = df[['company_id', 'company_name']].drop_duplicates(subset='company_id', keep='first')
        
        with connection.cursor() as cursor:
            # Insertar companies
            for _, row in companies.iterrows():
                try:
                    cursor.execute(
                        "INSERT INTO companies (company_id, company_name) VALUES (%s, %s)",
                        [row['company_id'], row['company_name']]
                    )
                    stats['companies_insertadas'] += 1
                except Exception as e:
                    logger.warning(f"Error insertando company {row['company_id']}: {str(e)}")
                    stats['errores_companies'] += 1
            
            # Insertar charges
            for _, row in df.iterrows():
                try:
                    updated_at = None if pd.isna(row['updated_at']) else row['updated_at']
                    cursor.execute(
                        """INSERT INTO charges 
                        (charge_id, company_id, amount, status, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        [row['id'], row['company_id'], row['amount'], 
                         row['status'], row['created_at'], updated_at]
                    )
                    stats['charges_insertados'] += 1
                except Exception as e:
                    logger.warning(f"Error insertando charge {row['id']}: {str(e)}")
                    stats['errores_charges'] += 1
            
            connection.commit()
        
        return stats
        
class EjecutarEsquemasView(View):
    """Vista para ejecutar los scripts SQL de esquemas"""
    
    def get(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                # Ejecutar scripts
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS companies ( 
                        company_id VARCHAR(64) NOT NULL PRIMARY KEY, 
                        company_name VARCHAR(130) NULL
                    );
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS charges (
                        charge_id VARCHAR(64) NOT NULL PRIMARY KEY,
                        company_id VARCHAR(64) NOT NULL,
                        amount DECIMAL(16,2) NOT NULL,
                        status VARCHAR(30) NOT NULL, 
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NULL,
                        FOREIGN KEY (company_id) REFERENCES companies(company_id)
                    );
                """)
                cursor.execute("""
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
                """)
                
            return JsonResponse({
                'status': 'success',
                'message': 'Esquemas y vista creados exitosamente'
            })
            
        except Exception as e:
            logger.error(f"Error creando esquemas: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
