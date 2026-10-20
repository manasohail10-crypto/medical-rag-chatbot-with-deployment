# Base image: a small Linux with Python
FROM python:3.12-slim

# Python settings: no .pyc files, and print logs at once
# CHANGED: HF_HOME is the place where the embedding model is saved
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  HF_HOME=/opt/hf_cache

# Work folder inside the container
WORKDIR /app

# System tools that some Python libraries need
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# CHANGED: CPU-only torch (much smaller, you have no GPU in Docker)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Step A: install libraries first (this layer is saved and reused)
# CHANGED: no setup.py in this project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# CHANGED: download the embedding model now, so the app does not download it at start
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('abhinand/MedEmbed-base-v0.1')"

# CHANGED: install the web server (placed here so Docker reuses the saved steps above)
RUN pip install --no-cache-dir gunicorn

# Step B: copy your code
# CHANGED: removed "pip install -e ." because there is no setup.py
COPY . .

# CHANGED: Flask runs on port 5000
EXPOSE 5000

# Start the app
# CHANGED: gunicorn runs the Flask app (app/application.py, object named "app")
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "120", "app.application:app"]