# 📈 StockPulse

> Send a stock ticker on WhatsApp. Get back an AI-generated insight on why it moved.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal?style=flat-square&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=flat-square)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-red?style=flat-square&logo=twilio)

---

## Demo

You:  NVDA
Bot:  ↑ NVDA +2.58% — expanded AI collaboration with Cadence driving optimism

## Tech Stack
- **Backend** — Python, FastAPI
- **AI** — Groq LLM (Llama 3.3 70B)
- **Stock Data** — Finnhub API
- **News** — NewsAPI
- **Messaging** — Twilio WhatsApp
- **Scheduler** — APScheduler (daily 9AM digest)

## Setup
```bash
git clone https://github.com/jayraval30/stock-tracker-agent.git
cd stock-tracker-agent
pip install -r requirements.txt
cp .env.example .env  # fill in your keys
uvicorn app.main:app --reload --port 8000
```

## How it works
1. You send a ticker on WhatsApp
2. Agent fetches live price from Finnhub
3. Agent fetches latest news headlines
4. Groq LLM generates a one-line insight
5. You receive it instantly on WhatsApp

---

<div align="center">Built with ❤️ by <a href="https://github.com/jayraval30">Jay Raval</a></div>
