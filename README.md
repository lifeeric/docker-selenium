# Selenium Docker Project

This project sets up a Docker environment to run Selenium with Chrome in headless mode. It includes a Python script that navigates to a specified webpage and searches for the text "Stories for you."

# Selenium

pass a volume current `session` directory for persistent session

#### .env

create `.env` file in the root dir:

```
COMPANY_NAME=
EMAIL=
PASS=
```

#### Build the image

```sh
docker build -t selenium-python . -f Dockerfile.selenium
```

and run:

```sh
docker run -it --rm  selenium-python --target types
```

# Playwright

**NODE:**

#### Build the image

```sh
docker build -t dayforce.playwrightts . -f Dockerfile.playwright.ts
```

and run:

```sh
docker run -it --rm  dayforce.playwrightts run --target properties
```

**PY:**

#### Build the image

```sh
docker build -t dayforce.playwrightpy . -f Dockerfile.playwright.py
```

and run:

```sh
docker run -it --rm  dayforce.playwrightpy --target properties
```
