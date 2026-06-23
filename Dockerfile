FROM python:3.12-slim

WORKDIR /workspace

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application logic into the image
COPY . .

# Expose the API gateway port
EXPOSE 8000

# Fire up the Uvicorn web server listening on all internal interfaces
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]