"""
OCO (One-Cancels-the-Other) Order Module
Places a take-profit and stop-loss pair — when one executes, the other cancels.
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

logger = setup_logger("oco")
ORDER_ENDPOINT = "/fapi/v1/order/oco"

def place_oco_order(symbol: str, side: str, quantity: float, take_profit_price: float, stop_price: float, stop_limit_price: float, time_in_force: str = "GTC"):
    """
    Create an OCO order with take-profit and stop-limit legs.
    """
    if not (validate_symbol(symbol) and validate_side(side) and validate_quantity(quantity)):
        return None
    if not (validate_price(take_profit_price) and validate_price(stop_price) and validate_price(stop_limit_price)):
        logger.error("Invalid prices for OCO order.")
        return None

    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "quantity": quantity,
        "price": take_profit_price,
        "stopPrice": stop_price,
        "stopLimitPrice": stop_limit_price,
        "stopLimitTimeInForce": time_in_force,
    }

    try:
        res = make_request("POST", ORDER_ENDPOINT, params, signed=True)
        logger.info(f"OCO order placed successfully: {res}")
        return res
    except Exception:
        logger.exception("Failed to place OCO order.")
        return None

def main():
    parser = argparse.ArgumentParser(description="Place OCO (One-Cancels-the-Other) order on Binance Futures")
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL", "buy", "sell"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("take_profit_price", type=float, help="Take-profit limit price")
    parser.add_argument("stop_price", type=float, help="Stop trigger price")
    parser.add_argument("stop_limit_price", type=float, help="Stop-limit execution price")
    parser.add_argument("--time-in-force", default="GTC", choices=["GTC", "IOC", "FOK"])
    args = parser.parse_args()

    print(f"\nPlacing OCO for {args.symbol}: side={args.side}, qty={args.quantity}, TP={args.take_profit_price}, SL={args.stop_price}")
    result = place_oco_order(args.symbol, args.side, args.quantity, args.take_profit_price, args.stop_price, args.stop_limit_price, args.time_in_force)

    if result:
        print("✅ OCO order placed successfully.")
    else:
        print("❌ OCO order failed. Check bot.log for details.")

if __name__ == "__main__":
    main()
