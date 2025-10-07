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