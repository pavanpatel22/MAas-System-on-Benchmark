"""
Temporal Reasoning Agent for MaAS
Handles date/time calculations and temporal logic
Author: Pavan Patel
"""

from datetime import datetime, timedelta
import re
from typing import Dict, Any, Optional, Tuple

class TemporalReasoningAgent:
    """Agent for temporal reasoning tasks"""
    
    def __init__(self):
        self.name = "TemporalReasoningAgent"
        self.description = "Handles date calculations, time intervals, and temporal logic"
        self.supported_operations = [
            "date_addition",
            "date_subtraction",
            "age_calculation",
            "time_interval",
            "day_of_week",
            "leap_year_check"
        ]
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process temporal reasoning query"""
        
        query = input_data.get("query", "")
        context = input_data.get("context", {})
        
        # Identify temporal operation
        operation = self._identify_operation(query)
        
        # Execute operation
        result = self._execute_operation(operation, query, context)
        
        return {
            "agent": self.name,
            "operation": operation,
            "result": result,
            "confidence": self._calculate_confidence(query, result)
        }
    
    def _identify_operation(self, query: str) -> str:
        """Identify which temporal operation is needed"""
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['age', 'born', 'birth']):
            return "age_calculation"
        elif any(word in query_lower for word in ['later', 'after', 'next', 'add']):
            return "date_addition"
        elif any(word in query_lower for word in ['before', 'ago', 'subtract']):
            return "date_subtraction"
        elif any(word in query_lower for word in ['between', 'interval', 'duration']):
            return "time_interval"
        elif any(word in query_lower for word in ['day of week', 'weekday']):
            return "day_of_week"
        elif 'leap year' in query_lower:
            return "leap_year_check"
        else:
            return "date_addition"  # Default
    
    def _execute_operation(self, operation: str, query: str, context: Dict) -> Any:
        """Execute the identified operation"""
        
        try:
            if operation == "age_calculation":
                return self._calculate_age(query)
            elif operation == "date_addition":
                return self._add_to_date(query)
            elif operation == "date_subtraction":
                return self._subtract_from_date(query)
            elif operation == "time_interval":
                return self._calculate_interval(query)
            elif operation == "day_of_week":
                return self._find_day_of_week(query)
            elif operation == "leap_year_check":
                return self._check_leap_year(query)
            else:
                return None
                
        except Exception as e:
            return f"Error in temporal operation: {str(e)}"
    
    def _calculate_age(self, query: str) -> str:
        """Calculate age from birth date"""
        
        # Extract dates using regex
        date_pattern = r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b'
        dates = re.findall(date_pattern, query)
        
        if len(dates) >= 2:
            birth_date = datetime(int(dates[0][2]), int(dates[0][1]), int(dates[0][0]))
            target_date = datetime(int(dates[1][2]), int(dates[1][1]), int(dates[1][0]))
            
            # Calculate age
            age = target_date.year - birth_date.year
            
            # Adjust if birthday hasn't occurred yet
            if (target_date.month, target_date.day) < (birth_date.month, birth_date.day):
                age -= 1
            
            return f"{age} years"
        
        return "Could not extract dates for age calculation"
    
    def _add_to_date(self, query: str) -> str:
        """Add days/months/years to a date"""
        
        # Extract base date
        date_match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', query)
        if not date_match:
            return "No date found in query"
        
        day, month, year = map(int, date_match.groups())
        base_date = datetime(year, month, day)
        
        # Extract duration to add
        duration_match = re.search(r'(\d+)\s+(day|month|year)s?', query.lower())
        if not duration_match:
            return "No duration specified"
        
        amount = int(duration_match.group(1))
        unit = duration_match.group(2)
        
        # Add duration
        if unit == 'day':
            new_date = base_date + timedelta(days=amount)
        elif unit == 'month':
            # Simple month addition (doesn't handle edge cases perfectly)
            new_year = year + (month + amount - 1) // 12
            new_month = (month + amount - 1) % 12 + 1
            new_date = datetime(new_year, new_month, min(day, 28))
        elif unit == 'year':
            new_date = datetime(year + amount, month, min(day, 28))
        else:
            return f"Unknown unit: {unit}"
        
        return new_date.strftime("%B %d, %Y")
    
    def _subtract_from_date(self, query: str) -> str:
        """Subtract days/months/years from a date"""
        
        # Similar to _add_to_date but with subtraction
        # Implementation omitted for brevity
        pass
    
    def _calculate_interval(self, query: str) -> str:
        """Calculate interval between two dates"""
        
        date_pattern = r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b'
        dates = re.findall(date_pattern, query)
        
        if len(dates) >= 2:
            date1 = datetime(int(dates[0][2]), int(dates[0][1]), int(dates[0][0]))
            date2 = datetime(int(dates[1][2]), int(dates[1][1]), int(dates[1][0]))
            
            delta = abs(date2 - date1)
            
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            
            parts = []
            if years > 0:
                parts.append(f"{years} year{'s' if years > 1 else ''}")
            if months > 0:
                parts.append(f"{months} month{'s' if months > 1 else ''}")
            if days > 0 or not parts:
                parts.append(f"{days} day{'s' if days > 1 else ''}")
            
            return ", ".join(parts)
        
        return "Could not extract two dates"
    
    def _find_day_of_week(self, query: str) -> str:
        """Find day of week for a given date"""
        
        date_match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', query)
        if date_match:
            day, month, year = map(int, date_match.groups())
            date_obj = datetime(year, month, day)
            return date_obj.strftime("%A")
        
        return "Could not extract date"
    
    def _check_leap_year(self, query: str) -> str:
        """Check if a year is a leap year"""
        
        year_match = re.search(r'\b(\d{4})\b', query)
        if year_match:
            year = int(year_match.group(1))
            is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            return f"{year} is {'a leap year' if is_leap else 'not a leap year'}"
        
        return "Could not extract year"
    
    def _calculate_confidence(self, query: str, result: Any) -> float:
        """Calculate confidence score for the result"""
        
        if result is None or "Error" in str(result) or "Could not" in str(result):
            return 0.0
        
        # Simple confidence calculation based on result completeness
        confidence = 0.7  # Base confidence
        
        # Increase confidence if result contains specific patterns
        if isinstance(result, str):
            if any(pattern in result for pattern in ['year', 'month', 'day', 'Monday', 'Tuesday']):
                confidence += 0.2
            if re.search(r'\d+', result):
                confidence += 0.1
        
        return min(confidence, 1.0)