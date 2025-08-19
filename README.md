# Telegram Medical Analytics Dashboard

A full-stack data analytics platform to explore and analyze Ethiopian Telegram medical business channels. Combines a **FastAPI backend** for data retrieval and processing with a **Streamlit frontend** for interactive dashboards.

---

## Overview

This project allows monitoring Telegram channels for medical business activities. Users can:  
- Track daily message activity per channel  
- Identify top mentioned products  
- Search messages  
- View YOLO-detected objects from images  

**Stack:** FastAPI + SQLAlchemy + PostgreSQL + Streamlit + Plotly  

---

## Features

- **Channel Activity Analysis:** Daily messages, messages with images, average message length  
- **Top Products:** Extracted via whitelist, regex, and token frequency  
- **Message Search:** Search by keyword with metadata display  
- **YOLO Object Detections:** Count of detected objects in images  
- **Filters:** Date range and channel selection  

---

## Screenshots

> Replace the placeholders below with actual images

### Dashboard Overview

<img width="1352" height="625" alt="image" src="https://github.com/user-attachments/assets/02bd175e-b0e5-47c3-8afe-e88544ddd3c9" />


### KPIs

<img width="1362" height="650" alt="image" src="https://github.com/user-attachments/assets/16b3f60f-4d9d-4f50-8a04-6b82719286c7" />


### Search Messages

<img width="1363" height="632" alt="image" src="https://github.com/user-attachments/assets/f9d192fe-7491-4807-8041-ff2831016e26" />




---

## Folder Structure

TelegramMedicalBusinessAnalytics/
├─ app.py # Streamlit dashboard
├─ backend/
│ ├─ main.py # FastAPI app & endpoints
│ ├─ crud.py # Database queries
│ ├─ models.py # SQLAlchemy ORM models
│ ├─ schemas.py # Pydantic schemas for API
│ └─ database.py # DB engine & session
├─ raw/ # Raw data files (images, JSON)
├─ screenshots/ # Placeholder for dashboard screenshots
├─ docker-compose.yml # Optional: container deployment
├─ requirements.txt # Python dependencies
└─ .env # Environment variables (DB URL, API URL)


---

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/TelegramMedicalBusinessAnalytics.git
cd TelegramMedicalBusinessAnalytics
Create and activate virtual environment


python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
Install dependencies


pip install -r requirements.txt
Configure environment variables


DATABASE_URL=postgresql://username:password@host:port/dbname
API_URL=http://localhost:8000/api
Run FastAPI backend


uvicorn backend.main:app --reload
Run Streamlit dashboard


streamlit run app.py
Usage
Open dashboard (http://localhost:8501)

Select a date range and channels from the sidebar

View KPIs, activity charts, top products, search results, and detections

Switch between tabs for more insights

Future Improvements
Add /overview API endpoint for KPIs per channel

Integrate YOLO detections API fully

Support multiple channel selection in activity charts

Add user authentication for secure access

Author: Tsega Bogale Dessalegn
Email: tsegabogale92@gmail.com
