import os
from pathlib import Path
import psycopg2
from tqdm import tqdm
from PIL import Image

def connect_postgres(dbname="my_data_warehouse", user="postgres", password="your_password", host="localhost", port="5432"):
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

def create_images_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw;
        CREATE TABLE IF NOT EXISTS raw.telegram_images (
            id SERIAL PRIMARY KEY,
            channel TEXT,
            date TEXT,
            file_path TEXT UNIQUE,
            width INTEGER,
            height INTEGER,
            file_size_kb REAL,
            format TEXT,
            mode TEXT
        );
        """)
    conn.commit()

def extract_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            format = img.format
            mode = img.mode
        file_size_kb = os.path.getsize(image_path) / 1024  # Convert bytes to KB
        return width, height, file_size_kb, format, mode
    except Exception as e:
        print(f"❌ Error reading image {image_path}: {e}")
        return None

def load_image_metadata(conn, base_path):
    base_path = Path(base_path)
    image_files = list(base_path.glob("**/*.jpg")) + list(base_path.glob("**/*.png"))

    print(f"📸 Found {len(image_files)} images.")
    with conn.cursor() as cur:
        for file_path in tqdm(image_files, desc="Loading image metadata"):
            try:
                date = file_path.parts[-3]      # e.g. 2025-07-11
                channel = file_path.parts[-2]   # e.g. CheMed123

                metadata = extract_image_metadata(file_path)
                if metadata is None:
                    continue
                width, height, size_kb, format, mode = metadata

                cur.execute("""
                    INSERT INTO raw.telegram_images (
                        channel, date, file_path,
                        width, height, file_size_kb,
                        format, mode
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (file_path) DO NOTHING;
                """, (
                    channel, date, str(file_path),
                    width, height, size_kb,
                    format, mode
                ))
            except Exception as e:
                print(f"❌ Failed to insert {file_path}: {e}")
    conn.commit()

if __name__ == "__main__":
    conn = connect_postgres(password=os.getenv("DB_PASSWORD"))
    create_images_table(conn)
    load_image_metadata(conn, base_path="../data/raw/telegram_images")
    conn.close()
    print("✅ Done loading image metadata.")
