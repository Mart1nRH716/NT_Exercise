from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NumberSet
import json

def extract_number(request, number):
    """API endpoint to extract a number from the URL path and find the missing one."""
    if request.method == 'GET':
        try:
            # Validate input
            if not isinstance(number, int):
                return JsonResponse({'error': 'Number must be an integer'}, status=400)
            
            if number < 1 or number > 100:
                return JsonResponse({'error': 'Number must be between 1 and 100'}, status=400)
            
            # Create number set and extract number
            number_set = NumberSet()
            number_set.extract(number)
            
            # Find the missing number
            missing_number = number_set.find_missing()
            
            return JsonResponse({
                'extracted_number': number,
                'missing_number': missing_number,
                'success': True
            })
            
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)