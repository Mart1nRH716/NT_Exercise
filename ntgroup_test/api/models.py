from django.db import models

class NumberSet(models.Model):
    def __init__(self):
        """Iniciamos el listado de números con los primeros 100"""
        self.numbers = list(range(1, 101))
        self.extracted_number = None
    
    def extract(self, number):
        """
        Función: Extrae un número específico
        
        Recibe:
            Número comprendido entre 1-100
            
        Regresa:
            True en caso de que fue exitoso la extracción del número, False en caso contrario
        """
        # if not isinstance(number, int):
        #     raise ValueError("Debe ser númerico")
        
        # if number < 1 or number > 100:
        #     raise ValueError("El número debe de estar entre 1-100")
        
        if number in self.numbers:
            self.numbers.remove(number)
            self.extracted_number = number
            return True
        return False
    
    def find_missing(self):
        """
        Función: Encuentra el número perdido
        
        Regresa:
            El número perdido
        """
        if len(self.numbers) == 100:
            return None
        
        # Calculamos la suma que debe de tener la lista
        longitud = len(self.numbers) + 1
        suma_esp = (longitud * (longitud + 1)) // 2  # (n * (n + 1)) /2
        actual_sum = sum(self.numbers)
        
        #Retornamos la diferencia ya que ese va ser el número faltante
        return suma_esp - actual_sum
