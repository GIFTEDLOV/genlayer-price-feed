# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class PriceFeed(gl.Contract):
    """
    Fetches real-time cryptocurrency prices from CoinGecko API.
    No API key required. Supports any token listed on CoinGecko.
    Use CoinGecko ID (e.g., "bitcoin") not ticker (e.g., NOT "BTC").
    """
    prices: TreeMap[str, str]
    previous_prices: TreeMap[str, str]
    tokens: DynArray[str]
    token_count: u32

    def __init__(self):
        self.token_count = u32(0)

    @gl.public.write
    def fetch_price(self, token_id: str) -> typing.Any:
        token_id = token_id.strip().lower()
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={token_id}&vs_currencies=usd"
            f"&include_24hr_change=true"
            f"&include_market_cap=true"
        )

        def get_price() -> str:
            response = gl.nondet.web.get(url)
            data = json.loads(response.body.decode("utf-8"))
            if token_id not in data:
                return json.dumps({"error": f"Unknown token: {token_id}"})
            token_data = data[token_id]
            result = {
                "token": token_id,
                "usd": token_data.get("usd", 0),
                "usd_24h_change": token_data.get("usd_24h_change", 0),
                "usd_market_cap": token_data.get("usd_market_cap", 0),
            }
            return json.dumps(result)

        price_json = gl.eq_principle.strict_eq(get_price)

        # Store previous price before updating
        existing = self.prices.get(token_id, "")
        if existing != "":
            self.previous_prices[token_id] = existing

        self.prices[token_id] = price_json

        # Track token list
        already_tracked = False
        for t in self.tokens:
            if t == token_id:
                already_tracked = True
                break
        if not already_tracked:
            self.tokens.append(token_id)
            self.token_count = u32(self.token_count + 1)

    @gl.public.write
    def fetch_multiple_prices(self, token_ids_csv: str) -> typing.Any:
        token_ids = token_ids_csv.strip().lower()
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={token_ids}&vs_currencies=usd"
            f"&include_24hr_change=true"
        )

        def get_prices() -> str:
            response = gl.nondet.web.get(url)
            data = json.loads(response.body.decode("utf-8"))
            return json.dumps(data)

        raw_json = gl.eq_principle.strict_eq(get_prices)
        all_data = json.loads(raw_json)

        for tid, tdata in all_data.items():
            existing = self.prices.get(tid, "")
            if existing != "":
                self.previous_prices[tid] = existing

            entry = {
                "token": tid,
                "usd": tdata.get("usd", 0),
                "usd_24h_change": tdata.get("usd_24h_change", 0),
            }
            self.prices[tid] = json.dumps(entry)

            already_tracked = False
            for t in self.tokens:
                if t == tid:
                    already_tracked = True
                    break
            if not already_tracked:
                self.tokens.append(tid)
                self.token_count = u32(self.token_count + 1)

    @gl.public.write
    def fetch_price_in_currency(self, token_id: str, currency: str) -> typing.Any:
        token_id = token_id.strip().lower()
        currency = currency.strip().lower()
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={token_id}&vs_currencies={currency}"
        )

        def get_price() -> str:
            response = gl.nondet.web.get(url)
            data = json.loads(response.body.decode("utf-8"))
            if token_id not in data:
                return json.dumps({"error": f"Unknown token: {token_id}"})
            price_val = data[token_id].get(currency, 0)
            result = {"token": token_id, "currency": currency, "price": price_val}
            return json.dumps(result)

        price_json = gl.eq_principle.strict_eq(get_price)
        key = f"{token_id}_{currency}"
        self.prices[key] = price_json

    @gl.public.view
    def get_price(self, token_id: str) -> str:
        token_id = token_id.strip().lower()
        stored = self.prices.get(token_id, "")
        if stored == "":
            return f"No price data for '{token_id}'. Call fetch_price first."
        return stored

    @gl.public.view
    def get_all_prices(self) -> str:
        result = {}
        for t in self.tokens:
            stored = self.prices.get(t, "")
            if stored != "":
                data = json.loads(stored)
                result[t] = data.get("usd", 0)
        return json.dumps(result)

    @gl.public.view
    def get_price_change(self, token_id: str) -> str:
        token_id = token_id.strip().lower()
        current_raw = self.prices.get(token_id, "")
        previous_raw = self.previous_prices.get(token_id, "")

        if current_raw == "":
            return f"No current price for '{token_id}'"
        if previous_raw == "":
            return f"No previous price for '{token_id}'. Fetch again later to track changes."

        current = json.loads(current_raw)
        previous = json.loads(previous_raw)
        cur_usd = current.get("usd", 0)
        prev_usd = previous.get("usd", 0)

        if prev_usd > 0:
            change_pct = ((cur_usd - prev_usd) / prev_usd) * 100
        else:
            change_pct = 0

        result = {
            "token": token_id,
            "previous_usd": prev_usd,
            "current_usd": cur_usd,
            "change_percent": f"{change_pct:.2f}%",
            "direction": "up" if change_pct >= 0 else "down",
        }
        return json.dumps(result)

    @gl.public.view
    def get_tracked_tokens(self) -> str:
        result = [t for t in self.tokens]
        return json.dumps(result)
