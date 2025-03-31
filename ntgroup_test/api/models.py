from django.db import models

class NumberSet(models.Model):
    def __init__(self):
        """Initialize a set of the first 100 natural numbers."""
        self.numbers = list(range(1, 101))
        self.extracted_number = None
    
    def extract(self, number):
        """
        Extract a specific number from the set.
        
        Args:
            number: The number to extract (must be between 1 and 100)
            
        Returns:
            bool: True if extraction was successful, False otherwise
        """
        if not isinstance(number, int):
            raise ValueError("Number must be an integer")
        
        if number < 1 or number > 100:
            raise ValueError("Number must be between 1 and 100")
        
        if number in self.numbers:
            self.numbers.remove(number)
            self.extracted_number = number
            return True
        return False
    
    def find_missing(self):
        """
        Find the missing number in the set.
        
        Returns:
            int: The missing number, or None if no number is missing
        """
        if len(self.numbers) == 100:
            return None
        
        # Calculate the sum of all numbers from 1 to 100
        expected_sum = 100 * 101 // 2  # Sum of arithmetic sequence
        actual_sum = sum(self.numbers)
        
        # The missing number is the difference between expected and actual sum
        return expected_sum - actual_sum
