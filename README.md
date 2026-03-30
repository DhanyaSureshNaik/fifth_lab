# ELK Stack + Linear Regression Logging

End-to-end example of training a scikit-learn Linear Regression model and shipping its logs to an ELK (Elasticsearch, Logstash, Kibana) stack for visualization.

## Repository Structure

```
elk-lr-logging/
├── model/
│   └── train.py               
├── logstash/
│   └── pipeline.conf          
├── kibana/
│   └── dashboard_export.ndjson  
├── config/
│   └── elasticsearch.yml      
├── docker-compose.yml         
├── requirements.txt
└── README.md
```

## Quick Start

```bash
git clone https://github.com/your-username/elk-lr-logging.git
cd elk-lr-logging
docker compose up -d
```

That's it. Docker will:

1. Start Elasticsearch and wait until it is healthy
2. Start Kibana and Logstash once Elasticsearch is ready
3. Import the Kibana dashboard automatically
4. Run the model training script, which writes logs picked up by Logstash

Once complete, open Kibana at **http://localhost:5601**, go to **Dashboards**, and open **LR Training Dashboard**.

## What Gets Logged

| Field | Description |
|---|---|
| `log_timestamp` | ISO 8601 timestamp of the event |
| `log_level` | INFO / WARNING / ERROR |
| `stage` | Pipeline stage: data, preprocessing, training, evaluation, done |
| `r2_score` | R² score from the evaluation stage |
| `mse` / `rmse` | Mean squared error and root MSE |
| `coefficients` | Learned model weights |
| `intercept` | Learned bias term |
| `duration_ms` | Time taken to fit the model |
| `n_train` / `n_test` | Sample counts from the data split |

## Manual Setup (without Docker)

### Prerequisites

- Java 11+ (`java -version`)
- Python 3.8+
- Elasticsearch 8.x, Logstash 8.x, Kibana 8.x — download from https://elastic.co/downloads

### 1. Configure and start Elasticsearch

Copy `config/elasticsearch.yml` into your Elasticsearch `config/` directory, then:

```bash
./bin/elasticsearch
```

Verify at http://localhost:9200.

### 2. Start Kibana

```bash
./bin/kibana         # macOS / Linux
.\bin\kibana.bat     # Windows
```

Verify at http://localhost:5601.

### 3. Start Logstash

```bash
bin/logstash -f /path/to/elk-lr-logging/logstash/pipeline.conf
```

### 4. Install dependencies and train the model

```bash
pip install -r requirements.txt
python model/train.py
```

### 5. Import the Kibana dashboard

```bash
curl -X POST http://localhost:5601/api/saved_objects/_import?overwrite=true \
  -H 'kbn-xsrf: true' \
  --form file=@kibana/dashboard_export.ndjson
```

## Requirements

See `requirements.txt`. Main dependencies: `scikit-learn`, `numpy`, `python-json-logger`.
