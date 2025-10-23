"""
Limit Orders Module
Places orders at specific prices that execute when the market reaches that level.
"""

import argparse
from .utils import (
    make_request,
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    setup_logger,
)

logger = setup_logger("limit_orders")
ORDER_ENDPOINT = "/fapi/v1/order"

def place_limit_order(symbol: str, side: str, quantity: float, price: float, time_in_force: str = "GTC", position_side: str = "BOTH", post_only: bool = False, reduce_only: bool = False):
    if not (validate_symbol(symbol) and validate_side(side) and validate_quantity(quantity) and validate_price(price)):
        return None
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": time_in_force,
        "positionSide": position_side.upper(),
    }
    if post_only:
        params["newOrderRespType"] = "RESULT"
    if reduce_only:
        params["reduceOnly"] = "true"
    try:
        res = make_request("POST", ORDER_ENDPOINT, params, signed=True)
        logger.info(f"Limit order placed: {res}")
        return res
    except Exception:
        logger.exception("Failed to place limit order")
        return None

def main():
    parser = argparse.ArgumentParser(description="Place limit order on Binance Futures")
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL", "buy", "sell"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("price", type=float)
    parser.add_argument("--time-in-force", default="GTC", choices=["GTC", "IOC", "FOK", "GTX"])
    parser.add_argument("--position-side", default="BOTH", choices=["BOTH", "LONG", "SHORT"])
    parser.add_argument("--post-only", action="store_true")
    parser.add_argument("--reduce-only", action="store_true")
    args = parser.parse_args()
    result = place_limit_order(args.symbol, args.side, args.quantity, args.price, args.time_in_force, args.position_side, args.post_only, args.reduce_only)
    if result:
        print("✅ Limit order placed successfully:", result.get("orderId"))
    else:
        print("❌ Order failed. Check bot.log for details.")

if __name__ == "__main__":
    main()
