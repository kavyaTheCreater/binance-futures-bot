"""
Stop-Limit Orders Module
Triggers a limit order once the stop price is reached.
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ..utils import (
    make_request,
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    get_current_price,
    setup_logger,
)

logger = setup_logger("stop_limit")
ORDER_ENDPOINT = "/fapi/v1/order"

def place_stop_limit_order(symbol: str, side: str, quantity: float, price: float, stop_price: float, time_in_force: str = "GTC", position_side: str = "BOTH", reduce_only: bool = False, working_type: str = "CONTRACT_PRICE"):
    if not (validate_symbol(symbol) and validate_side(side) and validate_quantity(quantity) and validate_price(price) and validate_price(stop_price)):
        return None

    current = get_current_price(symbol)
    if current:
        logger.info(f"Current price: {current}")

    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "STOP",
        "quantity": quantity,
        "price": price,
        "stopPrice": stop_price,
        "timeInForce": time_in_force,
        "positionSide": position_side.upper(),
        "workingType": working_type,
    }
    if reduce_only:
        params["reduceOnly"] = "true"

    try:
        res = make_request("POST", ORDER_ENDPOINT, params, signed=True)
        logger.info(f"Stop-limit order placed: {res}")
        return res
    except Exception:
        logger.exception("Failed to place stop-limit order")
        return None

def main():
    parser = argparse.ArgumentParser(description="Place Stop-Limit order on Binance Futures")
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL", "buy", "sell"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("price", type=float)
    parser.add_argument("stop_price", type=float)
    parser.add_argument("--time-in-force", default="GTC", choices=["GTC", "GTX"])
    parser.add_argument("--position-side", default="BOTH", choices=["BOTH", "LONG", "SHORT"])
    parser.add_argument("--reduce-only", action="store_true")
    parser.add_argument("--working-type", default="CONTRACT_PRICE", choices=["CONTRACT_PRICE", "MARK_PRICE"])
    args = parser.parse_args()

    result = place_stop_limit_order(args.symbol, args.side, args.quantity, args.price, args.stop_price, args.time_in_force, args.position_side, args.reduce_only, args.working_type)
    if result:
        print("✅ Stop-limit order placed successfully:", result.get("orderId"))
    else:
        print("❌ Order failed. Check bot.log for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
