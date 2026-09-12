# No system audio libraries (e.g. ffmpeg) are needed: voice messages are
# sent to Groq's Whisper API in their original Telegram .ogg/Opus format,
# with no local conversion or merging step.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["python", "-m", "app.bot"]
