# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies (for some tools like Playwright, if needed)
RUN apt-get update && apt-get install -y \
    git curl unzip ffmpeg libglib2.0-0 libnss3 libgconf-2-4 libxss1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variable (default dev)
ENV ENV=dev

# Optional: expose port if using API later
# EXPOSE 8000

# Start app
CMD ["python", "app.py"]
