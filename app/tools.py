import httpx
import yfinance as yf
from app.config import settings


INDIAN_SUFFIXES = [".BSE", ".NSE", ".BO", ".NS"]
CRYPTO_SYMS = ["BTC", "ETH", "SOL", "BNB", "USDT", "XRP", "ADA", "DOGE"]
INDEX_SYMS = ["^NSEI", "^BSESN", "^GSPC", "^IXIC", "^DJI", "^FTSE",
              "NIFTYBEES.BSE", "SETFNIF50.BSE", "SPY", "QQQ", "DIA", "ISF"]


def is_indian(ticker: str) -> bool:
    return any(ticker.upper().endswith(s) for s in INDIAN_SUFFIXES)


def is_crypto(ticker: str) -> bool:
    base = ticker.upper().replace("-USD", "").replace("USDT", "")
    return base in CRYPTO_SYMS


def is_index(ticker: str) -> bool:
    return ticker.upper() in INDEX_SYMS or ticker.startswith("^")


def use_yahoo(ticker: str) -> bool:
    return is_indian(ticker) or is_crypto(ticker) or is_index(ticker)


def to_yahoo_sym(ticker: str) -> str:
    """Convert our internal symbol to Yahoo Finance format."""
    t = ticker.upper()
    if t.endswith(".BSE"):
        return t.replace(".BSE", ".BO")
    if t.endswith(".NSE"):
        return t.replace(".NSE", ".NS")
    if "USDT" in t:
        return t.replace("USDT", "-USD")
    return t


async def get_stock_quote(ticker: str) -> dict:
    """
    Fetch quote using Finnhub for US stocks,
    Yahoo Finance for Indian stocks, crypto, and indices.
    """
    if use_yahoo(ticker):
        return await _yahoo_quote(ticker)
    return await _finnhub_quote(ticker)


async def _finnhub_quote(ticker: str) -> dict:
    """Fetch US stock quote from Finnhub."""
    url = "https://finnhub.io/api/v1/quote"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={"symbol": ticker.upper(), "token": settings.finnhub_api_key},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

    if data["c"] == 0:
        return {"error": f"No data found for: {ticker.upper()}"}

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


async def _yahoo_quote(ticker: str) -> dict:
    """Fetch quote from Yahoo Finance (Indian stocks, crypto, indices)."""
    sym = to_yahoo_sym(ticker)
    try:
        t = yf.Ticker(sym)
        info = t.fast_info
        current = round(float(info.last_price), 2)
        prev = round(float(info.previous_close), 2)
        change_pct = round(((current - prev) / prev) * 100, 2)
        return {
            "ticker": ticker.upper(),
            "current_price": current,
            "previous_close": prev,
            "change_pct": change_pct,
            "high": round(float(info.day_high), 2),
            "low": round(float(info.day_low), 2),
            "direction": "up" if change_pct >= 0 else "down",
        }
    except Exception as e:
        return {"error": f"Could not fetch {ticker}: {str(e)}"}


async def get_stock_news(ticker: str, limit: int = 5) -> list[dict]:
    """Fetch recent news headlines for a stock."""
    clean = ticker.replace(".BSE", "").replace(".NSE", "").replace(".BO", "").replace(".NS", "")
    url = "https://newsapi.org/v2/everything"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={
                "q": clean,
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
        {"title": a["title"], "source": a["source"]["name"]}
        for a in articles
    ]