# Use Python 3.10 slim image for smaller size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY stock_screening_students_v8.py .
COPY AASTOCKS_Export_2025-7-13.xlsx .
COPY init.sh .

# Make init script executable
RUN chmod +x init.sh

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Create directories for output files and logs with proper ownership
RUN mkdir -p /app/output /app/logs \
    && chown -R app:app /app

USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Use init script as entrypoint
ENTRYPOINT ["./init.sh"]

# Default command
CMD ["python", "stock_screening_students_v8.py"]