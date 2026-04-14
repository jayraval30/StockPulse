from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.agent import run_stock_agent
from app.scheduler import scheduler
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="Stock Tracker Agent")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook/sms")
async def sms_webhook(From: str = Form(...), Body: str = Form(...)):
    """Handles both SMS and WhatsApp messages from Twilio."""
    reply = await run_stock_agent(Body.strip())
    response = MessagingResponse()
    response.message(reply)
    return Response(content=str(response), media_type="application/xml")


@app.post("/digest/trigger")
async def trigger_digest():
    """Manually trigger the daily digest."""
    from app.sms import send_sms
    results = []
    for ticker in settings.watchlist:
        insight = await run_stock_agent(
            f"Give me a daily update on {ticker}"
        )
        send_sms(to=settings.user_phone_number, body=insight)
        results.append({"ticker": ticker, "insight": insight})
    return {"status": "sent", "results": results}