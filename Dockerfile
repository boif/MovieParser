FROM python:3.10

# Установка необходимых зависимостей для Firefox и geckodriver
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Установка geckodriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.30.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.30.0-linux64.tar.gz

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
