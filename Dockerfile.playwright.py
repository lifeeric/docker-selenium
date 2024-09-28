# Use the official Python image as the base
FROM python:3.9.19-slim

# Set the working directory
WORKDIR /app


# Install Playwright browsers and dependencies
RUN pip install playwright python-dotenv
RUN playwright install
RUN playwright install-deps

COPY session ./
COPY .env ./
COPY scrape-playwright.py ./

ENTRYPOINT ["python", "scrape-playwright.py"]
