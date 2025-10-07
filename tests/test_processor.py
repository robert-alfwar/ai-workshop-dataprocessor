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