FROM python:3.10-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies (Poppler + Tesseract for OCR)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr-eng \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port and run the app
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8080"]
