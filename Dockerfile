FROM python:3.8.10-slim

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --ignore-installed PyYAML ptyprocess --no-deps -r requirements.txt

ENV PROJECT_ROOT /weather-bot
ENV PYTHONPATH "${PYTHONPATH}:${PROJECT_ROOT}"
WORKDIR /weather-bot

CMD ["python", "weather_bot/bot.py"]