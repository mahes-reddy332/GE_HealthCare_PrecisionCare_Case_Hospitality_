FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Expose port
EXPOSE 8000

# Seed database and start uvicorn
CMD python app/scripts/seed_database.py && uvicorn app.main:app --host 0.0.0.0 --port 8000
