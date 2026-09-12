\# 🎙️ Voice Summary Bot



> An AI-powered Telegram bot that transforms voice messages into structured, concise text summaries.
## 🎬 Demo

A short demonstration of the Voice Summary Bot in action.

[▶️ Watch the demo](./demo%201.mp4)


Voice Summary Bot is a Telegram-based AI application designed to process spoken information and turn it into useful written notes.



Users can send one or multiple voice messages, finish the session, and receive an automatically generated \*\*summary, key points, and full transcript\*\*.



The project combines asynchronous Telegram bot development, speech-to-text technology, large language models, API integration, error handling, and deployment configuration into a single practical application.



\---



\## ✨ Features



\* 🎙️ \*\*Voice message processing\*\*

\* 🔢 Supports up to \*\*10 voice messages per session\*\*

\* 📝 Automatic \*\*speech-to-text transcription\*\*

\* 🧠 AI-generated \*\*2–4 sentence summary\*\*

\* 🔑 Extraction of \*\*3–5 key points\*\*

\* 📄 Complete \*\*full transcript\*\*

\* 🌍 Automatic detection of the \*\*spoken language\*\*

\* 🇷🇺 Russian and 🇬🇧 English interface

\* 🔄 Voice messages are processed \*\*in their original order\*\*

\* ⚡ Asynchronous processing with `aiogram`

\* 🛡️ API keys stored securely using environment variables

\* 🚫 No database and no permanent storage of voice recordings

\* 🔁 Automatic retry for temporary API rate-limit errors

\* 📦 Docker and Railway deployment configuration



\---



\## 🧠 How It Works



The processing pipeline is divided into several stages:



```text

Telegram User

&#x20;     │

&#x20;     ▼

Voice Messages

&#x20;     │

&#x20;     ▼

Telegram Bot

&#x20;     │

&#x20;     ▼

Audio Download

&#x20;     │

&#x20;     ▼

Whisper Speech-to-Text

&#x20;     │

&#x20;     ▼

Combined Transcript

&#x20;     │

&#x20;     ▼

Large Language Model

&#x20;     │

&#x20;     ├── Summary

&#x20;     ├── Key Points

&#x20;     └── Full Transcript

&#x20;     │

&#x20;     ▼

Telegram Response

```



\### Example



A user sends several voice messages:



```text

Voice 1 → Voice 2 → Voice 3 → Done

```



The bot:



1\. Downloads the voice messages.

2\. Transcribes each message separately.

3\. Preserves their original order.

4\. Combines the transcripts.

5\. Sends the text to the language model.

6\. Generates a concise summary and key points.

7\. Returns the final result to the user.



\---



\## 🤖 AI Stack



\### Speech-to-Text



\*\*Whisper Large V3 Turbo\*\*



Used to convert Telegram voice messages into text.



The bot sends each voice message separately for transcription and then combines the results in the correct order.



\### Language Model



\*\*OpenAI GPT-OSS 120B via Groq\*\*



Used to analyze the combined transcript and generate:



\* a concise summary;

\* key points;

\* a structured final response.



\### AI Architecture



The application separates transcription from text generation:



```text

Audio

&#x20; ↓

Whisper

&#x20; ↓

Transcript

&#x20; ↓

LLM

&#x20; ↓

Structured Result

```



This separation makes the system easier to maintain and allows individual AI components to be replaced independently.



\---



\## 🏗️ Architecture



The project follows a modular service-oriented structure.



```text

app/

├── bot.py

├── config.py

├── states.py

│

├── handlers/

│   ├── start.py

│   ├── voice.py

│   └── callbacks.py

│

├── keyboards/

│   └── keyboards.py

│

├── services/

│   ├── audio.py

│   ├── errors.py

│   ├── pipeline.py

│   ├── summarization.py

│   └── transcription.py

│

└── utils/

&#x20;   ├── cleanup.py

&#x20;   ├── formatting.py

&#x20;   ├── retry.py

&#x20;   └── texts.py

```



\### Main Components



\*\*Handlers\*\*



Responsible for Telegram updates, commands, voice messages, and button callbacks.



\*\*Services\*\*



Contain the main application logic:



\* audio processing;

\* transcription;

\* summarization;

\* pipeline orchestration;

\* error handling.



\*\*Keyboards\*\*



Contains Telegram inline/reply keyboard definitions.



\*\*Utils\*\*



Contains reusable helpers for:



\* text formatting;

\* cleanup;

\* retries;

\* localized texts.



\*\*Configuration\*\*



Loads environment variables and application settings without hardcoding secrets.



\---



\## 🛠️ Technology Stack



| Technology             | Purpose                    |

| ---------------------- | -------------------------- |

| Python 3.12            | Main programming language  |

| aiogram 3              | Telegram Bot API framework |

| Groq API               | AI inference               |

| Whisper Large V3 Turbo | Speech recognition         |

| GPT-OSS 120B           | Text summarization         |

| python-dotenv          | Environment configuration  |

| Docker                 | Containerization           |

| Railway                | Deployment configuration   |

| Git / GitHub           | Version control            |



\---



\## 🔐 Security \& Privacy



The project follows several basic security principles.



\### Environment Variables



Sensitive credentials are not stored directly in the source code.



Required secrets are provided through environment variables:



```env

BOT\_TOKEN=your\_telegram\_bot\_token

GROQ\_API\_KEY=your\_groq\_api\_key

SUMMARY\_MODEL=openai/gpt-oss-120b

```



The `.env` file is excluded from Git using `.gitignore`.



A `.env.example` file is provided so that the required configuration is clear without exposing real credentials.



\### Data Handling



The bot does not use a database and does not maintain permanent voice-message history.



Voice files are processed in memory and are not intentionally written to disk by the application.



\---



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Geaileer/voice-summary-bot.git

cd voice-summary-bot

```



\### 2. Create a virtual environment



Windows:



```powershell

python -m venv .venv

.venv\\Scripts\\activate

```



Linux / macOS:



```bash

python3 -m venv .venv

source .venv/bin/activate

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file based on `.env.example`:



```env

BOT\_TOKEN=your\_telegram\_bot\_token

GROQ\_API\_KEY=your\_groq\_api\_key

SUMMARY\_MODEL=openai/gpt-oss-120b

```



\### 5. Run the bot



```bash

python -m app.bot

```



The bot should start polling Telegram for updates.



\---



\## 🐳 Docker



The project also includes a `Dockerfile` for containerized deployment.



Build the image:



```bash

docker build -t voice-summary-bot .

```



Run the container:



```bash

docker run --env-file .env voice-summary-bot

```



\---



\## ☁️ Deployment



The repository includes configuration for deployment using Railway.



The application is designed to run as a long-running Telegram polling service.



Deployment configuration is provided through:



```text

railway.toml

Dockerfile

```



\---



\## ⚠️ Current Limitations



The current version intentionally keeps the architecture simple.



\* Maximum of 10 voice messages per session.

\* Individual voice messages are limited by the configured processing constraints.

\* Telegram's Bot API imposes a file download limit.

\* No user accounts or persistent history.

\* No database.

\* Processing depends on external AI APIs.

\* AI-generated summaries may occasionally contain inaccuracies.



\---



\## 🚀 Future Improvements



Possible future versions could include:



\* 📚 Persistent conversation history

\* 👤 User accounts and profiles

\* 🗂️ Saved transcripts

\* 📤 Export to PDF / Markdown / TXT

\* 🔎 Search through previous transcripts

\* ⏱️ Automatic processing without pressing "Done"

\* 🎯 Custom summary styles

\* 📊 Usage statistics

\* 🌐 Web interface

\* 🔐 More advanced privacy controls

\* 🧪 Automated test suite and CI/CD pipeline



\---



\## 📚 What I Learned



Building this project helped me practice several areas of software and AI engineering:



\* Designing modular Python applications

\* Building asynchronous Telegram bots

\* Working with external APIs

\* Integrating speech-to-text models

\* Integrating large language models

\* Managing environment variables and secrets

\* Handling API failures and rate limits

\* Designing multi-step AI processing pipelines

\* Structuring a project for maintainability

\* Using Git and GitHub for version control

\* Preparing applications for Docker-based deployment



The main goal was not simply to connect an AI model to Telegram, but to build a complete application around the AI components.



\---



\## 🎓 Portfolio Context



This project demonstrates my interest in \*\*Artificial Intelligence, Computer Science, and software engineering\*\*.



It combines:



```text

Programming

&#x20;    +

AI / Machine Learning APIs

&#x20;    +

Software Architecture

&#x20;    +

API Integration

&#x20;    +

Deployment

```



The project was developed as a practical example of how modern AI models can be integrated into an end-user application.



\---



\## 📌 Project Status



\*\*Status:\*\* Active / Working Prototype



The core voice-to-text and AI summarization pipeline is functional and tested with multiple voice messages.



\---



\## 👨‍💻 Author



\*\*Sanjar Inomaliev\*\*



Interested in:



\* Artificial Intelligence

\* Computer Science

\* Software Engineering

\* Machine Learning

\* Technology \& Entrepreneurship



GitHub:

https://github.com/Geaileer



\---



\## 📄 License



This project is intended primarily as a personal educational and portfolio project.



