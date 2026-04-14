import json
from groq import AsyncGroq
from app.tools import get_stock_quote, get_stock_news
from app.config import settings


client = AsyncGroq(api_key=settings.groq_api_key)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_quote",
            "description": "Get the current price and daily % change for a stock ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol e.g. NVDA",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_news",
            "description": "Get recent news headlines for a stock ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol e.g. NVDA",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of headlines to fetch. Default 5.",
                    },
                },
                "required": ["ticker"],
            },
        },
    },
]


TOOL_MAP = {
    "get_stock_quote": get_stock_quote,
    "get_stock_news": get_stock_news,
}


SYSTEM_PROMPT = """You are a sharp, concise stock analyst delivered via SMS.

When asked about a stock:
1. Call get_stock_quote to get price and % change.
2. Call get_stock_news to get recent headlines.
3. Write ONE SMS-length message explaining WHY the stock moved.

Format rules:
- Start with ↑ if up, ↓ if down
- Then: TICKER +/-X.XX%
- Then: a dash and a plain English reason (specific, no fluff)
- Keep it under 160 characters total

Example: ↓ NVDA -1.89% — geopolitical risk in China, data center revenue miss, and fears the AI rally is overheating."""


async def run_stock_agent(user_message: str) -> str:
    """Run the agentic loop and return the final SMS reply."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    while True:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=200,
        )

        msg = response.choices[0].message

        # No tool calls means the agent has its final answer
        if not msg.tool_calls:
            return msg.content.strip()

        # Append assistant message with tool calls
        messages.append(msg)

        # Execute every tool the agent requested
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            tool_fn = TOOL_MAP.get(fn_name)
            if tool_fn is None:
                result = {"error": f"Unknown tool: {fn_name}"}
            else:
                result = await tool_fn(**fn_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })