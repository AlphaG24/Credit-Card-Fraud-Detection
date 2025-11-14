# -----------------------------
# 1. Base Image
# -----------------------------
FROM python:3.12-slim

# -----------------------------
# 2. Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# 3. Install system dependencies
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 4. Copy project files
# -----------------------------
COPY requirements.txt .
COPY app/ app/
COPY src/ src/
COPY model/ model/
COPY frontend/ frontend/
COPY data/ data/

# -----------------------------
# 5. Install Python packages
# -----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 6. Expose port
# -----------------------------
EXPOSE 8000

# -----------------------------
# 7. Start FastAPI
# -----------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
