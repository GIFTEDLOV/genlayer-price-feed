"""
CoinGecko Token ID Reference
==============================
Use CoinGecko IDs, NOT ticker symbols.
Example: "bitcoin" not "BTC", "ethereum" not "ETH"

Usage in GenLayer Studio:
  fetch_price("bitcoin")
  fetch_multiple_prices("bitcoin,ethereum,solana")
"""

TOKEN_IDS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin",
    "Avalanche": "avalanche-2",
    "Chainlink": "chainlink",
    "Polygon": "matic-network",
    "Uniswap": "uniswap",
    "Aave": "aave",
    "Arbitrum": "arbitrum",
    "Optimism": "optimism",
    "Render": "render-token",
    "Pepe": "pepe",
}

FIAT_CURRENCIES = {
    "US Dollar": "usd",
    "Euro": "eur",
    "British Pound": "gbp",
    "Japanese Yen": "jpy",
    "Nigerian Naira": "ngn",
    "South African Rand": "zar",
}
