import os
import json
import psycopg2
from pathlib import Path
from tqdm import tqdm

def connect_postgres(dbname="my_data_warehouse", user="postgres", password="your_password", host="localhost", port="5432"):
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

def create_raw_schema_and_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw;

        DROP TABLE IF EXISTS raw.telegram_messages;

        CREATE TABLE raw.telegram_messages (
            id TEXT PRIMARY KEY,
            channel TEXT,
            date DATE,
            file_path TEXT,
            raw_json JSONB
        );
        """)
    conn.commit()

def get_json_files(base_path: str):
    base_path = Path(base_path)
    return list(base_path.glob("**/*.json"))

def load_json_files_to_postgres(conn, json_files):
    with conn.cursor() as cur:
        for file_path in tqdm(json_files, desc="Inserting messages"):
            try:
                channel_name = file_path.parts[-2]
                date_str = file_path.parts[-3]

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for message in data:
                        message_id = message.get("id")
                        if message_id:
                            cur.execute("""
                                INSERT INTO raw.telegram_messages (id, channel, date, file_path, raw_json)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING;
                            """, (
                                str(message_id),
                                channel_name,
                                date_str,
                                str(file_path),
                                json.dumps(message)
                            ))
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse {file_path}: {e}")
    conn.commit()
