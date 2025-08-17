FROM python:3.11-slim

WORKDIR /app

# Copy Linux-compatible requirements
COPY requirements_linux.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements_linux.txt

# Copy project files
COPY . .

# Optional: expose port if your app runs a server
 EXPOSE 8000

# Optional: default command
# CMD ["python", "main.py"]



# Default command: run FastAPI
CMD ["python", "main.py","uvicorn", "my_project.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
