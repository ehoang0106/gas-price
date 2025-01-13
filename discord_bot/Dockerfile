FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV DISCORD_TOKEN=${DISCORD_TOKEN}
ENV DISCORD_CHANNEL_ID=${DISCORD_CHANNEL_ID}

CMD ["python", "bot.py"]