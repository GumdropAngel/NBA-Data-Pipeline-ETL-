# NBA Data Pipeline (ETL) 

This project is an implementation of a Data Engineering (ETL) architecture that streams NBA basketball data from a SQLite database to PostgreSQL, captures it via Kafka Connect (Debezium) in *real-time*, and finally loads it into Elasticsearch to be visualized through Kibana.

## Architecture
1. **Source Database:** SQLite (`nba.sqlite`) & PostgreSQL
2. **Streaming & Connectors:** Zookeeper, Apache Kafka, Kafka Connect, Debezium
3. **Destination (Sink):** Elasticsearch
4. **Visualization:** Kibana

## Data Source
The NBA dataset used in this project can be downloaded from Kaggle at the following link:
**[\[KAGGLE DATASET LINK\]](https://www.kaggle.com/datasets/wyattowalsh/basketball)**

## Requirements
- Docker & Docker Compose
- Python 3.8+
- Python Libraries (can be installed from `requirements.txt`)

## How to Run (Step by Step)

### 1. Start the Docker Environment (Services)
Run the following command in your terminal within the project directory:
```bash
docker-compose up -d
```
*Note: Wait until all containers are fully up and running. Kafka Connect might take a little longer because it downloads plugins automatically.*

### 2. Setup Python Environment
Install all required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Data Migration (SQLite -> PostgreSQL)
Run the migration script to move the raw NBA data into PostgreSQL:
```bash
python migrate.py
```
This script will fetch a sample of 50,000 rows per table and automatically insert them into PostgreSQL.

### 4. Enable Kafka Connect (Debezium & Elasticsearch)
Activate the Source and Sink connectors by running:
```bash
python setup_connectors.py
```

### 5. Check Results in Kibana
Open your browser and access Kibana at:
[http://localhost:5601](http://localhost:5601)

You can directly create a *Data View* in the "Stack Management" section with the index pattern (`pg-server.public.*`) to view the data that has entered Elasticsearch.
