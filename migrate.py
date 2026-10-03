import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import os

#fetching the nba.sqlite file located in the same directory as this script
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nba.sqlite")
sqlite_conn = sqlite3.connect(db_path)
pg_engine = create_engine('postgresql://admin:password@localhost:5433/basketball_db')

query_tables = "SELECT name FROM sqlite_master WHERE type='table';"
tables_df = pd.read_sql_query(query_tables, sqlite_conn)
tables = tables_df['name'].tolist()

print(f"Found {len(tables)} tables. Starting migration (Max 50,000 rows per table)...")

for table in tables:
    print(f"Migrating table: {table}...")
    
    #only fetching the first 50,000 rows (for computing safety as more rows will take more time and storage. You can adjust this number)
    query = f"SELECT * FROM {table} LIMIT 50000"
    df = pd.read_sql_query(query, sqlite_conn)
    
    #inserting into PostgreSQL
    df.to_sql(table, pg_engine, if_exists='replace', index=False)
    print(f"  -> {len(df)} rows successfully migrated!")

sqlite_conn.close()
print("\nDone! Sample data has been safely inserted into PostgreSQL.")