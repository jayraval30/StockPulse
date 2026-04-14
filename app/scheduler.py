from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import settings

scheduler = AsyncIOScheduler(timezone="America/New_York")


async def daily_digest() -> None:
    """Push a morning briefing for every stock on the watchlist."""
    from app.agent import run_stock_agent
    from app.sms import send_sms
    for ticker in settings.watchlist:
        insight = await run_stock_agent(f"Give me a daily update on {ticker}")
        send_sms(to=settings.user_phone_number, body=insight)


scheduler.add_job(daily_digest, "cron", hour=9, minute=0)