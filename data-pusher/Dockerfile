# Dockerfile
FROM python:3.9-slim

WORKDIR /app


# 2. Copy all files into the container
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# 5. …and CMD is what you actually want to run once InfluxDB is up
CMD ["python", "push-to-db.py"]
