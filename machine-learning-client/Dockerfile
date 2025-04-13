FROM python:3.9-slim

WORKDIR /app

# Install dependencies with increased timeout and retries
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=100 --retries=10 -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]