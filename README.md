# ELK Stack + Linear Regression Logging

End-to-end example of training a scikit-learn Linear Regression model and shipping its logs to an ELK (Elasticsearch, Logstash, Kibana) stack for visualization.

## Repository Structure

```
elk-lr-logging/
├── model/
│   └── train.py               # Model training script with logging
├── logstash/
│   └── pipeline.conf          # Logstash input/filter/output config
├── kibana/
│   └── dashboard_export.ndjson  # Importable Kibana dashboard
├── config/
│   └── elasticsearch.yml      # Elasticsearch config overrides
├── docker-compose.yml         # One-command ELK stack setup
├── requirements.txt
└── README.md
```

## Quick Start

### Option A — Docker (recommended)

```bash
git clone https://github.com/your-username/elk-lr-logging.git
cd elk-lr-logging
docker compose up -d
pip install -r requirements.txt
python model/train.py
```

Then open Kibana at http://localhost:5601.

### Option B — Manual install

See [Manual Setup](#manual-setup) below.

## Manual Setup

### 1. Prerequisites

- Java 11+ installed (`java -version`)
- Python 3.8+
- Elasticsearch 8.x, Logstash 8.x, Kibana 8.x — download from https://elastic.co/downloads

### 2. Configure Elasticsearch

Copy `config/elasticsearch.yml` to your Elasticsearch `config/` directory, then start it:

```bash
./bin/elasticsearch
```

Verify: http://localhost:9200

### 3. Start Kibana

```bash
./bin/kibana         # macOS / Linux
.\bin\kibana.bat     # Windows
```

Verify: http://localhost:5601

### 4. Start Logstash

```bash
bin/logstash -f /path/to/elk-lr-logging/logstash/pipeline.conf
```

### 5. Train the model

```bash
pip install -r requirements.txt
python model/train.py
```

Logs are written to `model/training.log` and automatically picked up by Logstash.

## Kibana Dashboard

1. Open Kibana → **Stack Management → Saved Objects**
2. Click **Import** and select `kibana/dashboard_export.ndjson`
3. Navigate to **Dashboards** and open **LR Training Dashboard**

## What Gets Logged

| Field | Description |
|---|---|
| `log_timestamp` | ISO 8601 timestamp of the event |
| `log_level` | INFO / WARNING / ERROR |
| `log_message` | Human-readable description |
| Embedded JSON | R² score, MSE, coefficients, intercept, sample counts |

## Requirements

See `requirements.txt`. Main dependencies: `scikit-learn`, `numpy`, `python-json-logger`.
