FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]