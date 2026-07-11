# Use official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (if you have one)
COPY requirements.txt .

# Install dependencies (if you have requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL your project files into the container
COPY . .

# Run your main python file
CMD ["python", "main.py"]