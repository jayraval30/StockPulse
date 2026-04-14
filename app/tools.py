import httpx
from app.config import settings


async def get_stock_quote(ticker: str) -> dict:
    """Fetch current price and daily % change for a ticker."""
    url = "https://finnhub.io/api/v1/quote"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={
                "symbol": ticker.upper(),
                "token": settings.finnhub_api_key,
            },
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

    if data["c"] == 0:
        return {"error": f"No data found for ticker: {ticker.upper()}"}

    change_pct = round(((data["c"] - data["pc"]) / data["pc"]) * 100, 2)

    return {
        "ticker": ticker.upper(),
        "current_price": data["c"],
        "previous_close": data["pc"],
        "change_pct": change_pct,
        "high": data["h"],
        "low": data["l"],
        "direction": "up" if change_pct >= 0 else "down",
    }


async def get_stock_news(ticker: str, limit: int = 5) -> list[dict]:
    """Fetch recent news headlines for a stock."""
    url = "https://newsapi.org/v2/everything"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={
                "q": ticker.upper(),
                "sortBy": "publishedAt",
                "pageSize": limit,
                "language": "en",
                "apiKey": settings.news_api_key,
            },
            timeout=10.0,
        )
        response.raise_for_status()
        articles = response.json().get("articles", [])

    if not articles:
        return [{"title": "No recent news found", "source": "N/A"}]

    return [
        {
            "title": article["title"],
            "source": article["source"]["name"],
        }
        for article in articles
    ]