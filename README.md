# Selenium Docker Project

This project sets up a Docker environment to run Selenium with Chrome in headless mode. It includes a Python script that navigates to a specified webpage and searches for the text "Stories for you."

## Build the image

```sh
docker build -t selenium-python . -f Dockerfile.python
```

and run:

```sh
docker run -it --rm --shm-size=2g selenium-python --target types
```
