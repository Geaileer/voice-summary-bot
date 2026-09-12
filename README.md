# Telegram Voice Summarizer

## Overview

A Telegram bot that turns 1–10 voice messages into a short summary, key
points, and a full transcript. Send your voice notes, tap **Done**, and get
back the essence of what was said — in whatever language you spoke it in,
regardless of the bot's interface language.

Built as a small, honest MVP: no accounts, no history, no database — just
a simple pipeline from voice to text to summary.

## Features

- 🎤 Accepts 1–10 voice messages per session (up to ~10 minutes each), in order
- 🌍 Automatic language detection per voice message (speech recognition
  never depends on the chosen interface language)
- 🧠 AI-generated summary + key points (decisions, tasks, dates, names,
  agreements) — never invented, only what's actually in the audio
- 📝 Full transcript, always in the original recording order
- 🇷🇺 🇬🇧 Russian/English interface, chosen once with `/start`
- 🗑️ No accounts, no history, no database — session state is temporary and
  in-memory only, and voice audio is never written to disk
- 💸 Runs entirely on free API tiers (see [Limitations](#limitations))

## Architecture

```
Telegram (voice messages)
        │
        ▼
 aiogram handlers            (app/handlers/*)
   - collect voice file_ids in FSM memory, in order
   - "Done" triggers the pipeline
        │
        ▼
 audio.py                    (app/services/audio.py)
   - downloads each voice message from Telegram straight into memory
        │
        ▼
 transcription.py            (app/services/transcription.py)
   - Groq Whisper API, one call per voice message, auto language detection
        │
        ▼
 summarization.py            (app/services/summarization.py)
   - Groq LLM chat completion, structured JSON output
        │
        ▼
 formatting.py + Telegram reply (app/utils/formatting.py)
   - splits long text safely under Telegram's 4096-char message limit
```

The Telegram layer never talks to Groq directly — handlers call
`app/services/pipeline.py`, which calls the transcription and
summarization services. Swapping either AI provider/model later means
editing exactly one file (`transcription.py` or `summarization.py`);
nothing else needs to change.

## Tech Stack

- **Python 3.12**
- **[aiogram 3](https://docs.aiogram.dev/)** — async Telegram Bot framework
- **[Groq API](https://console.groq.com/)** — both speech-to-text
  (`whisper-large-v3-turbo`) and summarization (`llama-3.3-70b-versatile`),
  free tier
- **In-memory FSM storage** (aiogram's built-in `MemoryStorage`) — no
  database
- **Docker** + **Railway** for deployment

## Setup

### 1. Prerequisites

- [Python 3.12+](https://www.python.org/downloads/) installed
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A free API key from [Groq Console](https://console.groq.com/keys)

### 2. Clone and install (Windows)

```bash
git clone https://github.com/<your-username>/voice-summary-bot.git
cd voice-summary-bot

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

On macOS/Linux, activate with `source .venv/bin/activate` instead.

### 3. Configure environment variables

```bash
copy .env.example .env
```

(macOS/Linux: `cp .env.example .env`)

Open `.env` and fill in:

```
BOT_TOKEN=your-telegram-bot-token
GROQ_API_KEY=your-groq-api-key
```

**Never commit your real `.env` file** — it's already listed in
`.gitignore`, and it contains secrets that must not end up on GitHub.

### 4. Run the bot

```bash
python -m app.bot
```

You should see `Bot started, polling for updates...` in the console.
Open your bot in Telegram and send `/start`.

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `BOT_TOKEN` | Yes | — | Telegram bot token from @BotFather |
| `GROQ_API_KEY` | Yes | — | Free API key from console.groq.com |
| `STT_MODEL` | No | `whisper-large-v3-turbo` | Groq speech-to-text model |
| `SUMMARY_MODEL` | No | `llama-3.3-70b-versatile` | Groq chat model for summarization |
| `MAX_VOICES_PER_SESSION` | No | `10` | Max voice messages per batch |
| `MAX_VOICE_FILE_SIZE_MB` | No | `20` | Rejects voice messages above this size before download |
| `REQUEST_TIMEOUT_SECONDS` | No | `120` | Timeout for each Groq API call |
| `RATE_LIMIT_RETRY_DELAY_SECONDS` | No | `5` | Delay before the single automatic retry on a rate-limit error |

## Usage

1. Send `/start`, choose 🇷🇺 Русский or 🇬🇧 English.
2. Send 1–10 voice messages (any mix of languages/topics you like).
3. Watch the "Received: N/10" counter after each one.
4. Tap **Done**.
5. Get back 🧠 Summary, 🔑 Key points, and 📝 Transcript.
6. Send more voice messages any time to start a new batch — no need to
   run `/start` again unless you want to change the interface language.

## Project Structure

```
voice-summary-bot/
├── app/
│   ├── bot.py              # Entry point: creates Bot/Dispatcher, starts polling
│   ├── config.py           # Loads and validates environment variables
│   ├── states.py           # FSM states (choosing_language / collecting_voices / processing)
│   ├── handlers/
│   │   ├── start.py        # /start + language selection
│   │   ├── voice.py        # Incoming voice messages, per-state fallback replies
│   │   └── callbacks.py    # Language & "Done" button callbacks
│   ├── services/
│   │   ├── audio.py        # Downloads voice messages into memory
│   │   ├── transcription.py# Groq Whisper speech-to-text
│   │   ├── summarization.py# Groq LLM summary + key points (JSON output)
│   │   ├── pipeline.py     # Orchestrates the steps above, maps errors to messages
│   │   └── errors.py       # Exception types for user-facing error handling
│   ├── keyboards/
│   │   └── keyboards.py    # Inline keyboards (language choice, Done button)
│   └── utils/
│       ├── texts.py        # Russian/English interface strings
│       ├── formatting.py   # Splits long results under Telegram's message limit
│       ├── retry.py        # Single automatic retry on rate-limit errors
│       └── cleanup.py      # Clears in-memory session state after processing
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── railway.toml
└── README.md
```

## Deployment (GitHub → Railway)

1. Push this project to a GitHub repository (make sure `.env` is **not**
   included — check `git status` before your first commit).
2. In [Railway](https://railway.com/), create a new project and choose
   **Deploy from GitHub repo**, selecting your repository.
3. Railway will detect the `Dockerfile` and build the image automatically
   (via `railway.toml`).
4. In the Railway project's **Variables** tab, add `BOT_TOKEN` and
   `GROQ_API_KEY` (and any optional variables you want to override).
5. Deploy. Check the **Logs** tab for `Bot started, polling for updates...`.

The bot uses long polling, not webhooks, so no public URL or port
configuration is needed on Railway.

Note: Railway's free usage tier and its terms change over time — this
project is simply Railway-compatible; check Railway's current pricing
before relying on it long-term.

## Limitations

Being upfront about what "free" actually means here:

- **Groq free tier limits** (subject to change — check
  [Groq's docs](https://console.groq.com/docs) for the current numbers):
  - Whisper (STT): ~20 requests/min, ~2,000 requests/day, 28,800
    audio-seconds/day, 25 MB max file size.
  - `llama-3.3-70b-versatile` (summarization): ~30 requests/min, ~1,000
    requests/day, 100,000 tokens/day.
  - If a limit is hit, the bot retries once automatically after a short
    delay, then shows a clear "try again later" message — it never
    fails silently or shows a stack trace.
- **Telegram's 20 MB bot download limit** governs in practice, even
  though Groq allows up to 25 MB — a bot can't download a file larger
  than 20 MB through the standard Bot API. In practice a 10-minute voice
  message is typically only 1–2 MB, so this is rarely an issue.
- **No database, no persistence.** Session state (chosen language,
  collected voice messages) lives only in memory. Restarting the bot
  (e.g. a redeploy) clears everyone's in-progress session.
- **Single-process polling.** This MVP is not designed for horizontal
  scaling or very high concurrent load — it's sized for personal/small-
  scale use.
- **Summary quality** depends on transcription quality, which in turn
  depends on audio clarity (background noise, overlapping speakers,
  heavy accents can reduce accuracy).

## Future Improvements

- Optional export of the transcript as a `.txt`/`.docx` file for long recordings
- Configurable summary length/style per user
- A lightweight per-user rate limiter to protect the shared free API quota
- Pluggable STT/summarization providers selectable via `.env` (the
  architecture already supports this — see `transcription.py` and
  `summarization.py`)
