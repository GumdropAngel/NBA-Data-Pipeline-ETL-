import urllib.request
import json
import time

def create_connector(url, data):
    req = urllib.request.Request(url, method='POST')
    req.add_header('Content-Type', 'application/json')
    data_bytes = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req, data=data_bytes) as response:
            print(f" -> Success! Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f" -> Failed: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f" -> Error: {e}")

#debezium configuration (PostgreSQL -> Kafka)
source_config = {
  "name": "postgres-source-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "admin",
    "database.password": "password",
    "database.dbname": "basketball_db",
    "topic.prefix": "pg-server", 
    "plugin.name": "pgoutput"
  }
}

#sink configuration (Kafka -> Elasticsearch)
sink_config = {
  "name": "elasticsearch-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "connection.url": "http://elasticsearch:9200",
    "tasks.max": "1",
    "topics.regex": "pg-server.public.(.*)",
    "key.ignore": "true",
    "schema.ignore": "true"
  }
}

print("1. Activating Debezium Source Connector...")
create_connector('http://localhost:8083/connectors', source_config)

print("Waiting 5 seconds for Debezium to be ready...")
time.sleep(5)

print("\n2. Activating Elasticsearch Sink Connector...")
create_connector('http://localhost:8083/connectors', sink_config)
print("\nDone! Please check your terminal.")