"""
Market Orders Module
Executes immediate buy/sell orders at best available price.
"""

import argparse
from .utils import (
    make_request,
    validate_symbol,
    validate_side,
    validate_quantity,
    setup_logger,
)

logger = setup_logger("market_orders")
ORDER_ENDPOINT = "/fapi/v1/order"

def place_market_order(symbol: str, side: str, quantity: float, position_side: str = "BOTH", reduce_only: bool = False):
    if not (validate_symbol(symbol) and validate_side(side) and validate_quantity(quantity)):
        return None
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity,
        "positionSide": position_side.upper(),
    }
    if reduce_only:
        params["reduceOnly"] = "true"
    try:
        res = make_request("POST", ORDER_ENDPOINT, params, signed=True)
        logger.info(f"Market order placed: {res}")
        return res
    except Exception:
        logger.exception("Failed to place market order")
        return None

def main():
    parser = argparse.ArgumentParser(description="Place market order on Binance Futures")
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL", "buy", "sell"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("--position-side", default="BOTH", choices=["BOTH", "LONG", "SHORT"])
    parser.add_argument("--reduce-only", action="store_true")
    args = parser.parse_args()
    result = place_market_order(args.symbol, args.side, args.quantity, args.position_side, args.reduce_only)
    if result:
        print("✅ Market order placed successfully:", result.get("orderId"))
    else:
        print("❌ Order failed. Check bot.log for details.")

if __name__ == "__main__":
    main()
