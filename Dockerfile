# Use the official Python image as the base
FROM python:3.9.19-slim

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y wget unzip \
    && apt-get install -y chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Selenium
RUN pip install --no-cache-dir selenium webdriver-manager

# Download and install ChromeDriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver-linux64.zip

# Set display port to avoid crashes
ENV DISPLAY=:99

# Set the working directory
WORKDIR /app

# Copy your Selenium test scripts or other files into the container
COPY scrap.py scrap.py

# Default command to run Selenium tests
CMD ["python", "scrap.py"]

