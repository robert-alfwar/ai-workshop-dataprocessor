# GitHub Project Specification: AI Workshop DataProcessor

**Repository:** `robert-alfwar/ai-workshop-dataprocessor`

A Python Flask API project with intentional bugs for AI-assisted debugging workshop.

## Project Overview

**Purpose:** A simple data processing API that reads CSV files and provides various analysis tools.

**Intentional issues for workshop:**
- 🐛 **Bug 1:** Off-by-one error in `count_rows()`
- 🐛 **Bug 2:** Missing edge case handling in `get_top_values()`
- 📝 Minimal documentation (no docstrings)
- ⚠️ Incomplete test suite

## Project Structure

```
ai-workshop-dataprocessor/
├── main.py                  # CLI interface
├── processor.py             # Data processing (WITH BUGS)
├── api.py                   # Flask API
├── utils.py                 # Utility functions
├── requirements.txt
├── README.md
├── data/
│   └── sample.csv
└── tests/
    └── test_processor.py    # Incomplete tests
```

---

## Files to Create

### 1. requirements.txt

```txt
flask==3.0.0
pytest==7.4.3
pandas==2.1.3
```

### 2. README.md

```markdown
# DataProcessor API

A simple data processing API.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# CLI
python main.py data/sample.csv

# API
python api.py
```

## API Endpoints

- `GET /health` - Health check
- `POST /process` - Process CSV data
```

### 3. main.py

```python
import sys
import json
from processor import DataProcessor

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <csv_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    processor = DataProcessor(filename)
    
    results = {
        "total_rows": processor.count_rows(),
        "summary": processor.summarize(),
        "top_values": processor.get_top_values("value", 5)
    }
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
```

### 4. processor.py (WITH BUGS!)

```python
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
```

### 5. utils.py

```python
import os

def validate_file_exists(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    return True

def validate_csv_structure(data):
    if not data:
        return False
    if not isinstance(data, list):
        return False
    if not isinstance(data[0], dict):
        return False
    return True

def format_number(num, decimals=2):
    return round(num, decimals)
```

### 6. api.py

```python
from flask import Flask, request, jsonify
from processor import DataProcessor
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    filepath = os.path.join('data', file.filename)
    file.save(filepath)
    
    try:
        processor = DataProcessor(filepath)
        results = {
            "total_rows": processor.count_rows(),
            "summary": processor.summarize()
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, port=5000)
```

### 7. tests/test_processor.py (INCOMPLETE)

```python
import pytest
from processor import DataProcessor
import os
import csv

@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'value', 'category'])
        writer.writeheader()
        writer.writerow({'id': '1', 'value': '100', 'category': 'A'})
        writer.writerow({'id': '2', 'value': '200', 'category': 'B'})
        writer.writerow({'id': '3', 'value': '150', 'category': 'A'})
    return str(csv_file)

def test_load_data(sample_csv):
    processor = DataProcessor(sample_csv)
    assert len(processor.data) == 3

def test_count_rows(sample_csv):
    processor = DataProcessor(sample_csv)
    count = processor.count_rows()
    # This test will FAIL due to off-by-one bug!
    assert count == 3

# TODO: Add tests for:
# - summarize()
# - get_top_values() with invalid column (should test edge case)
# - filter_by_value()
# - edge cases with empty data
```

### 8. data/sample.csv

```csv
id,value,category,amount
1,100,A,50.5
2,200,B,75.0
3,150,A,60.5
4,300,C,90.0
5,120,B,55.5
6,180,A,70.0
7,250,C,85.5
8,140,B,65.0
9,220,A,80.5
10,160,C,72.0
```

---

## Bugs for Students to Find

### 🐛 Bug 1: Off-by-one Error

**File:** `processor.py`  
**Method:** `count_rows()`  
**Line:** 18  
**Problem:** Returns `len(self.data) - 1` instead of `len(self.data)`

**Effect:**
- For a file with 10 rows, returns 9
- Test `test_count_rows()` fails

**Fix:**
```python
def count_rows(self):
    return len(self.data)  # Remove "- 1"
```

### 🐛 Bug 2: KeyError Edge Case

**File:** `processor.py`  
**Method:** `get_top_values()`  
**Line:** 40  
**Problem:** No handling if the column is missing (KeyError)

**Effect:**
- Crashes if a non-existent column is specified
- No error message or handling

**Fix:**
```python
def get_top_values(self, column, n=10):
    # Check if column exists
    if not self.data or column not in self.data[0]:
        return []
    
    values = [row[column] for row in self.data]
    counter = Counter(values)
    return counter.most_common(n)
```

---

## Setup and Running

### Test the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI (shows off-by-one bug)
python main.py data/sample.csv

# Run tests (test_count_rows will fail)
pytest tests/ -v

# Start API
python api.py
# Test with: curl http://localhost:5000/health
```

---

## Workshop Tasks for Students

1. **Clone the project**
   ```bash
   git clone https://github.com/robert-alfwar/ai-workshop-dataprocessor
   cd ai-workshop-dataprocessor
   pip install -r requirements.txt
   ```

2. **Run the tests** - Identify which ones fail
   ```bash
   pytest -v
   ```

3. **Use AI to find Bug 1**
   - Prompt: "This test is failing. Find the bug in count_rows()"
   - Fix the bug

4. **Use AI to identify Bug 2**
   - Prompt: "Add error handling for get_top_values() when column doesn't exist"
   - Implement the fix

5. **Complete the test suite**
   - Use AI to generate tests for:
     - `summarize()` method
     - `get_top_values()` with invalid columns
     - Edge cases with empty data

6. **Add docstrings**
   - Prompt: "Add Google-style docstrings to all methods in processor.py"
   - Apply to all files

7. **Improve README**
   - Prompt: "Improve README with usage examples and API documentation"

8. **Push improvements**
   ```bash
   git add .
   git commit -m "Fix bugs and improve documentation"
   git push
   ```

---

## Expected Outcome After Workshop

✅ All bugs fixed  
✅ Complete test suite (>90% coverage)  
✅ Docstrings for all functions and methods  
✅ Edge case handling implemented  
✅ Improved error handling  
✅ Updated and enhanced documentation  

---

## Learning Objectives

- Use AI for bug detection and debugging
- Read and understand errors in test output
- Improve code with AI assistance
- Write additional tests with pytest
- Document code effectively with AI-generated docstrings
- Proactively handle edge cases

---

## Notes

**This project is INTENTIONALLY incomplete and buggy!**

The project is designed to:
- Provide hands-on experience with AI-assisted debugging
- Show how AI can help improve existing code
- Demonstrate the importance of testing and documentation
- Provide hands-on experience with pytest and Flask

**Use AI tools (ChatGPT, Claude, GitHub Copilot) to:**
- Find and fix bugs
- Complete tests
- Improve documentation
- Add error handling
- Understand the codebase

**Good luck with the workshop! 🚀**