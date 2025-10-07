import csv
from collections import Counter

class DataProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()
    
    def _load_data(self):
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def count_rows(self):
        # BUG 1: Off-by-one error
        # This returns one less!
        return len(self.data) - 1
    
    def summarize(self):
        if not self.data:
            return {}
        
        numeric_fields = []
        for key in self.data[0].keys():
            try:
                float(self.data[0][key])
                numeric_fields.append(key)
            except ValueError:
                pass
        
        summary = {}
        for field in numeric_fields:
            values = [float(row[field]) for row in self.data]
            summary[field] = {
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values)
            }
        
        return summary
    
    def get_top_values(self, column, n=10):
        # BUG 2: Edge case - no handling if column is missing
        # This will crash with KeyError if the column is absent!
        values = [row[column] for row in self.data]
        counter = Counter(values)
        return counter.most_common(n)
    
    def filter_by_value(self, column, value):
        return [row for row in self.data if row[column] == value]