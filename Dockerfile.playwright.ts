# Use the official Node.js image
FROM node:18

# Set the working directory
WORKDIR /app

# Install necessary dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libglib2.0-0 \
    libnspr4 \
    libxss1 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy package.json and install Playwright


# Copy the application code
COPY tsconfig.json ./
COPY package*.json ./
COPY playwright.config.ts ./


RUN npm install
# Install Playwright browsers
RUN npx playwright install && npx playwright install-deps

COPY scrape-playwright.ts ./
COPY session ./
COPY .env ./

# Set the command to run your script
ENTRYPOINT ["npx","ts-node", "scrape-playwright.ts"]
