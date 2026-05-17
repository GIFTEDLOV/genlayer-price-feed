# GenLayer Price Feed

A reusable helper library for GenLayer Intelligent Contracts to fetch real-time cryptocurrency prices directly on-chain — no API keys, no oracles, no middlemen.

Built on [CoinGecko](https://www.coingecko.com/), the world's largest independent crypto data aggregator.

## Features

- **Single token prices** — fetch USD price for any of 14,000+ cryptocurrencies
- **Batch price fetching** — get multiple token prices in one call
- **Multi-currency support** — prices in USD, EUR, GBP, NGN, and more
- **Price change tracking** — compare current vs previous prices
- **Price alert system** — trigger actions when tokens cross thresholds
- **GenVM-lint compliant** — uses `TreeMap`, `DynArray`, and `u32` storage types
- **Consensus-friendly** — uses `gl.eq_principle.strict_eq` for validator agreement
- **No API key required** — CoinGecko's free public API

## Quick Start

1. Open [GenLayer Studio](https://studio.genlayer.com)
2. Copy `contracts/price_feed.py` into the editor
3. Click **Deploy**
4. Call `fetch_price` with a CoinGecko coin ID

```python
# Fetch Bitcoin price
fetch_price("bitcoin")

# Fetch multiple at once
fetch_multiple_prices("bitcoin,ethereum,solana")

# Read stored price
get_price("bitcoin")

# Track price changes (call fetch_price again later)
get_price_change("bitcoin")

# See all tracked tokens
get_tracked_tokens()
```

## Project Structure

```
genlayer-price-feed/
├── README.md
├── LICENSE
├── contracts/
│   └── price_feed.py              # Main contract (TreeMap + DynArray storage)
├── examples/
│   ├── simple_price_check.py      # Minimal single-price example
│   └── price_alert.py             # Price threshold alert example
└── utils/
    └── token_ids.py               # CoinGecko token ID reference
```

## Storage Types Used

| GenLayer Type | Replaces | Used For |
|---------------|----------|----------|
| `TreeMap[str, str]` | `dict` | Token prices (JSON-serialized) |
| `DynArray[str]` | `list` | List of tracked tokens |
| `u32` | `int` | Token count |
| `str` | `str` | Simple text fields |

## Use Cases

- **DeFi** — on-chain price feeds for lending and liquidation
- **Prediction markets** — resolve crypto price bets automatically
- **Portfolio tracking** — store valuations on-chain
- **Price alerts** — trigger actions at price thresholds

## Resources

- [GenLayer Docs](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [CoinGecko API](https://docs.coingecko.com/reference/introduction)
- [GenLayer Builder Program](https://portal.genlayer.foundation)

## License

MIT License — see [LICENSE](LICENSE)
