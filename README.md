#  Stock Tracker Agent

> AI-powered WhatsApp chatbot that tells you **why** your stocks moved — not just that they did.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal?style=flat-square&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=flat-square)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-red?style=flat-square&logo=twilio)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

##  What is this?

Most stock apps tell you a stock is **down 2%**. This tells you **why**.
You → WhatsApp "NVDA"
Bot → ↓ NVDA -1.89% — geopolitical risk in China, data center revenue miss, and fears the AI rally is overheating.

Built with a real agentic loop — the AI autonomously fetches live prices, pulls recent news, and synthesizes everything into one clean insight delivered straight to your WhatsApp.

---

##  Demo

| You send | You receive |
|----------|-------------|
| `NVDA` | ↑ NVDA +2.58% — expanded AI collaboration with Cadence driving optimism |
| `AAPL` | ↑ AAPL +0.00% — steady demand for iPhones and services, no major catalysts |
| `TSLA` | ↑ TSLA +0.97% — strong FSD v15 rollout and Ark Investment accumulation |

---

## 🏗️ Architecture

```
User (WhatsApp)
      │
      ▼
   Twilio
      │  webhook
      ▼
   FastAPI
      │
      ├──────────────────────────┐
      ▼                          ▼
AI Agent (Groq LLM)      Scheduler (9AM)
      │                          │
      ├──► Finnhub (price)        │
      ├──► NewsAPI (news)         │
      │                          │
      ▼                          ▼
   Insight ◄─────────────────────┘
      │
      ▼
User (WhatsApp)
```

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Backend | FastAPI |
| AI / LLM | Groq (Llama 3.3 70B) |
| Stock Data | Finnhub API |
| News | NewsAPI |
| Messaging | Twilio WhatsApp |
| Scheduler | APScheduler |
| Tunnel | ngrok |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/jayraval30/stock-tracker-agent.git
cd stock-tracker-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
```

### 4. Run the server
```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Start ngrok
```bash
ngrok http 8000
```

### 6. Connect Twilio WhatsApp Sandbox
Go to Twilio Console → Messaging → Try it out → WhatsApp → paste your ngrok URL:
https://your-ngrok-url.ngrok-free.dev/webhook/sms

### 7. Send a WhatsApp message
Save the Twilio sandbox number and send any stock ticker:
NVDA
AAPL
TSLA
GOOGL
---

## 📁 Project Structure

```
stock_tracker_agent/
├── app/
│   ├── agent.py        # Agentic loop with tool calling
│   ├── tools.py        # Finnhub + NewsAPI integration
│   ├── main.py         # FastAPI server + webhook handler
│   ├── sms.py          # Twilio WhatsApp helper
│   ├── scheduler.py    # Daily 9AM digest
│   └── config.py       # Pydantic settings
├── tests/
│   └── test_agent.py
├── .env.example
├── requirements.txt
└── README.md
```

##  Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key — free at console.groq.com |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Your Twilio number |
| `FINNHUB_API_KEY` | Finnhub API key — free at finnhub.io |
| `NEWS_API_KEY` | NewsAPI key — free at newsapi.org |
| `USER_PHONE_NUMBER` | Your WhatsApp number |
| `WATCHLIST` | Stocks for daily digest |

---

##  How the Agent Works

1. User sends a stock ticker via WhatsApp
2. FastAPI webhook receives the message
3. Agent calls `get_stock_quote()` → fetches live price and % change from Finnhub
4. Agent calls `get_stock_news()` → fetches latest headlines from NewsAPI
5. Groq LLM synthesizes price data and news into one clean insight
6. Twilio sends the insight back to the user's WhatsApp

The agent uses a **tool-calling loop** — it autonomously decides which tools to call, executes them, and only responds when it has enough context to generate a meaningful insight.

---

##  Daily Digest

Every morning at 9AM EST, the scheduler automatically sends insights for all stocks in your watchlist — no message needed.

---

##  License

MIT License — feel free to use, modify and distribute.

---


