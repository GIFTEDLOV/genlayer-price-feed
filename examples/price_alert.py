# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class PriceAlert(gl.Contract):
    """
    Price threshold alert system.
    Set a target price and check if real data triggers it.

    Deploy in GenLayer Studio and try:
      set_alert("bitcoin", "100000", "above")
      check_alert("bitcoin")
      get_alert("bitcoin")
    """
    alerts: TreeMap[str, str]

    def __init__(self):
        pass

    @gl.public.write
    def set_alert(self, token_id: str, target_price: str, direction: str) -> typing.Any:
        token_id = token_id.strip().lower()
        alert = {
            "token": token_id,
            "target_usd": float(target_price),
            "direction": direction,
            "triggered": False,
            "current_price": None,
            "status": "watching",
        }
        self.alerts[token_id] = json.dumps(alert)

    @gl.public.write
    def check_alert(self, token_id: str) -> typing.Any:
        token_id = token_id.strip().lower()
        stored = self.alerts.get(token_id, "")
        if stored == "":
            return "No alert set for this token"

        alert = json.loads(stored)
        if alert["triggered"]:
            return "Alert already triggered"

        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={token_id}&vs_currencies=usd"
        )

        def get_price() -> str:
            response = gl.nondet.web.get(url)
            data = json.loads(response.body.decode("utf-8"))
            if token_id not in data:
                return "0"
            return str(data[token_id]["usd"])

        price_str = gl.eq_principle.strict_eq(get_price)
        current_price = float(price_str)

        alert["current_price"] = current_price
        if alert["direction"] == "above" and current_price >= alert["target_usd"]:
            alert["triggered"] = True
            alert["status"] = "TRIGGERED - price went above target"
        elif alert["direction"] == "below" and current_price <= alert["target_usd"]:
            alert["triggered"] = True
            alert["status"] = "TRIGGERED - price dropped below target"
        else:
            alert["status"] = "watching"

        self.alerts[token_id] = json.dumps(alert)

    @gl.public.view
    def get_alert(self, token_id: str) -> str:
        token_id = token_id.strip().lower()
        stored = self.alerts.get(token_id, "")
        if stored == "":
            return f"No alert for '{token_id}'"
        return stored
