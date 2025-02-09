# Use a stable and lightweight Python version
FROM python:3.13

# Set working directory
WORKDIR /app

# Install dependencies separately to optimize caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application files (after dependencies to avoid unnecessary rebuilds)
COPY . .

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Run the FastAPI server (without --reload in production)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
