import os
import json
import psycopg2
from pathlib import Path
from tqdm import tqdm

# 🔌 PostgreSQL connection details
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 🏗️ Create schema and table
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id TEXT PRIMARY KEY,
    message_date DATE,
    channel TEXT,
    file_path TEXT,
    raw_json JSONB
);
""")

# 📂 Base directory
base_path = Path("../data/raw/telegram_messages")

# 🔍 Recursively find all JSON files under date/channel_name/
json_files = list(base_path.rglob("*.json"))

print(f"📄 Found {len(json_files)} JSON files.")

for file_path in tqdm(json_files, desc="Loading messages"):
    try:
        # Extract date and channel from path
        parts = file_path.parts
        date_index = parts.index("telegram_messages") + 1
        message_date = parts[date_index]
        channel_name = parts[date_index + 1]

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for message in data:
                message_id = message.get("id")
                if message_id:
                    cur.execute("""
                        INSERT INTO raw.telegram_messages (id, message_date, channel, file_path, raw_json)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """, (
                        str(message_id),
                        message_date,
                        channel_name,
                        str(file_path),
                        json.dumps(message)
                    ))
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

conn.commit()
cur.close()
conn.close()

print("✅ Done loading Telegram messages into PostgreSQL.")
