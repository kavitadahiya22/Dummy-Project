# Penetration Testing Framework Dockerfile
# ========================================
# 
# This Dockerfile creates a comprehensive penetration testing environment
# with all necessary security tools pre-installed.

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Create app directory
WORKDIR /app

# Install system dependencies and security tools
RUN apt-get update && apt-get install -y \
    # Basic system tools
    curl \
    wget \
    git \
    unzip \
    build-essential \
    # Network tools
    nmap \
    nikto \
    dnsutils \
    netcat-traditional \
    # SSL/TLS tools
    openssl \
    # Web testing tools
    sqlmap \
    # Password tools
    hydra \
    john \
    # Additional security tools
    dirb \
    gobuster \
    # Development tools
    gcc \
    python3-dev \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Install additional security tools via pip
RUN pip install --no-cache-dir \
    scapy \
    paramiko \
    python-nmap \
    requests[security] \
    beautifulsoup4

# Install Ollama (for AI reasoning)
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from src directory
COPY ../src ./src

# Set Python path to include src directory
ENV PYTHONPATH=/app/src

# Create directories for logs and data
RUN mkdir -p /app/logs /app/data

# Create non-root user for security
RUN groupadd -r pentester && useradd -r -g pentester pentester
RUN chown -R pentester:pentester /app
USER pentester

# Expose port for FastAPI
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - run from src directory
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]