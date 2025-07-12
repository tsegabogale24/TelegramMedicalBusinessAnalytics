# Telegram Medical Business Analytics

This project builds a data pipeline to collect and transform data from Ethiopian medical business Telegram channels. The pipeline extracts raw messages and images, processes them, and loads them into a PostgreSQL data warehouse using staging and transformation models.

## 📁 Project Structure

TelegramMedicalBusinessAnalytics/
│
├── data/
│ └── raw/
│ ├── telegram_messages/ # JSON or CSV files of raw messages
│ └── telegram_images/ # Extracted image files by date/channel
│
├── telegram_warehouse/
│ ├── staging/ # Python scripts to create staging tables
│ ├── models/
│ │ └── staging/ # .sql files for staging models
│ └── init.py
│
├── notebooks/
│ └── data_modeling_and_transformation.ipynb
│
├── .env # Environment variables
├── requirements.txt
└── README.md


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TelegramMedicalBusinessAnalytics.git
cd TelegramMedicalBusinessAnalytics
2. Create and Activate a Virtual Environment
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Set Environment Variables
Create a .env file:
DB_PASSWORD=your_postgres_password
🛠️ Staging Models
We define staging models to clean and structure raw data. These are the intermediate step before building star schema or analytics models.

▶️ Refresh Staging Tables
In notebooks/data_modeling_and_transformation.ipynb, you can run:
from telegram_warehouse.staging.stg_telegram_messages import refresh_staging_telegram_messages
from telegram_warehouse.staging.stg_telegram_images import refresh_staging_telegram_images

refresh_staging_telegram_messages(conn)
refresh_staging_telegram_images(conn)
✅ Staging: stg_telegram_messages
Extracts fields like id, text, date, channel, etc.

Cleans up data types, nulls, and formatting.

✅ Staging: stg_telegram_images
Extracts metadata like:

file_path

width, height

file_size_kb

format (e.g., JPEG, PNG)

mode (RGB, etc.)

Useful for downstream object detection or image quality analysis.

🧪 Testing & Preview
You can preview staging table results with:

SELECT * FROM staging.stg_telegram_messages LIMIT 10;
SELECT * FROM staging.stg_telegram_images LIMIT 10;
