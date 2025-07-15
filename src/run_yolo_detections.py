# run_yolo_detections.py

import os
import psycopg2
from ultralytics import YOLO
from tqdm import tqdm

def connect_postgres(dbname="my_data_warehouse", user="postgres", password="your_password", host="localhost", port="5432"):
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

def create_detections_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.image_detections (
            id SERIAL PRIMARY KEY,
            image_id INTEGER REFERENCES raw.telegram_images(id),
            detected_class TEXT,
            confidence_score REAL
        );
        """)
    conn.commit()

def run_yolo_detections(conn, model_path="yolov8n.pt"):
    model = YOLO(model_path)

    with conn.cursor() as cur:
        cur.execute("SELECT id, file_path FROM raw.telegram_images;")
        images = cur.fetchall()

        for image_id, file_path in tqdm(images, desc="Running YOLO"):
            if not os.path.exists(file_path):
                print(f"⚠️ Missing: {file_path}")
                continue

            try:
                results = model(file_path)
                boxes = results[0].boxes

                for box in boxes:
                    cls = model.names[int(box.cls[0])]
                    score = float(box.conf[0])

                    cur.execute("""
                        INSERT INTO raw.image_detections (image_id, detected_class, confidence_score)
                        VALUES (%s, %s, %s);
                    """, (image_id, cls, score))
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")

    conn.commit()

if __name__ == "__main__":
    conn = connect_postgres(password=os.getenv("DB_PASSWORD"))  # Or replace with hardcoded password
    create_detections_table(conn)
    run_yolo_detections(conn)
    conn.close()
    print("✅ YOLO detections saved.")
