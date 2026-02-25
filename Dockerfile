FROM python:3.11-slim AS base

WORKDIR /app

# System deps for faiss-cpu, opencv, etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create runtime dirs
RUN mkdir -p vector_db cache uploads exports rag/logs

EXPOSE 5000 8000

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py", "--mode", "serve"]
