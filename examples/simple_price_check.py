# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class SimplePriceCheck(gl.Contract):
    """
    Minimal example: fetch and store one crypto price.
    Deploy in GenLayer Studio and call:
      check_price("bitcoin")
      check_price("ethereum")
    """
    token: str
    price_usd: str

    def __init__(self):
        self.token = ""
        self.price_usd = ""

    @gl.public.write
    def check_price(self, token_id: str) -> typing.Any:
        token_id = token_id.strip().lower()
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={token_id}&vs_currencies=usd"
        )

        def get_price() -> str:
            response = gl.nondet.web.get(url)
            data = json.loads(response.body.decode("utf-8"))
            if token_id not in data:
                return "error"
            return str(data[token_id]["usd"])

        price_str = gl.eq_principle.strict_eq(get_price)
        self.token = token_id
        self.price_usd = f"${price_str}"

    @gl.public.view
    def read_price(self) -> str:
        if self.token == "":
            return "No price fetched yet"
        return f"{self.token}: {self.price_usd}"
