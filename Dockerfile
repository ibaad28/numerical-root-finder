FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install OS build dependencies and Python requirements
COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc g++ gfortran libopenblas-dev liblapack-dev \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

# Expose port for Render (Streamlit default is 8501)
EXPOSE 8501

# Health check for Render
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit on port 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]