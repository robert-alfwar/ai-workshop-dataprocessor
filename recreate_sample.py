#!/usr/bin/env python3
"""
Script to recreate the sample.csv file in the data directory.
"""

import os
import csv

def recreate_sample_csv():
    """Recreate the sample CSV file with test data."""
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    # Sample data
    data = [
        ['id', 'value', 'category', 'amount'],
        ['1', '100', 'A', '50.5'],
        ['2', '200', 'B', '75.0'],
        ['3', '150', 'A', '60.5'],
        ['4', '300', 'C', '90.0'],
        ['5', '120', 'B', '55.5'],
        ['6', '180', 'A', '70.0'],
        ['7', '250', 'C', '85.5'],
        ['8', '140', 'B', '65.0'],
        ['9', '220', 'A', '80.5'],
        ['10', '160', 'C', '72.0']
    ]

    # Write to CSV file
    with open('data/sample.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    print("Recreated data/sample.csv with sample data")

if __name__ == "__main__":
    recreate_sample_csv()