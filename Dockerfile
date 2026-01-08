FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (git is required for GitPython)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create temp workspace directory
RUN mkdir -p /tmp

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "app.main"]
