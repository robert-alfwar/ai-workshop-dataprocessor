# DataProcessor API

A simple data processing API.

## Setup

```bash
uv pip install -r requirements.txt
```

## Recreate Sample Data

If the sample CSV file gets deleted during testing, recreate it with:

```bash
uv run python recreate_sample.py
```

## Run

```bash
# CLI
uv run python main.py data/sample.csv

# API
uv run python api.py
```

## API Endpoints

- `GET /health` - Health check
- `POST /process` - Process CSV data

## API Testing

### Health Check

**PowerShell:**
```powershell
curl.exe http://localhost:5000/health
```

**Bash:**
```bash
curl http://localhost:5000/health
```

### Process CSV Data

**PowerShell:**
```powershell
curl.exe -X POST -F "file=@data/sample.csv" http://localhost:5000/process
```

**Bash:**
```bash
curl -X POST -F "file=@data/sample.csv" http://localhost:5000/process
```