# Use the official Python image as the base
FROM python:3.9.19-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files first to leverage Docker cache
COPY scrape-playwright.py ./



# Install Playwright browsers and dependencies
RUN pip install playwright python-dotenv
RUN playwright install
RUN playwright install-deps

COPY session ./
COPY .env ./

ENTRYPOINT ["python", "scrape-playwright.py"]
