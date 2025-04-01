from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NumberSet
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