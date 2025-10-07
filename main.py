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