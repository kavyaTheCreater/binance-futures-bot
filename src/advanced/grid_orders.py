"""
Grid Trading Module
Automatically places multiple buy/sell limit orders across price levels to profit from volatility.
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
from ..config import GRID_LEVELS, GRID_PROFIT_PERCENTAGE

logger = setup_logger("grid_orders")
ORDER_ENDPOINT = "/fapi/v1/order"

def place_limit_order(symbol, side, quantity, price, time_in_force="GTC"):
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": time_in_force,
    }
    return make_request("POST", ORDER_ENDPOINT, params, signed=True)

def place_grid_orders(symbol: str, total_quantity: float, grid_levels: int = GRID_LEVELS, profit_percent: float = GRID_PROFIT_PERCENTAGE):
    """
    Create a symmetric grid of buy and sell limit orders.
    Example: 10 levels at ±0.5% intervals.
    """
    if not (validate_symbol(symbol) and validate_quantity(total_quantity)):
        return None
    if grid_levels <= 1:
        logger.error("Grid levels must be > 1")
        return None

    current_price = get_current_price(symbol)
    if not current_price:
        logger.error("Unable to fetch current price")
        return None

    qty_per_order = total_quantity / (grid_levels * 2)
    price_step = current_price * (profit_percent / 100)

    logger.info(f"Placing {grid_levels} BUY and {grid_levels} SELL grid orders around {current_price}")
    results = []

    # Buy Orders (below current price)
    for i in range(1, grid_levels + 1):
        price = current_price - i * price_step
        if price <= 0:
            continue
        try:
            res = place_limit_order(symbol, "BUY", qty_per_order, round(price, 2))
            results.append(res)
            logger.info(f"BUY Grid {i}: {price}")
        except Exception:
            logger.exception(f"Failed to place BUY grid {i}")

    # Sell Orders (above current price)
    for i in range(1, grid_levels + 1):
        price = current_price + i * price_step
        try:
            res = place_limit_order(symbol, "SELL", qty_per_order, round(price, 2))
            results.append(res)
            logger.info(f"SELL Grid {i}: {price}")
        except Exception:
            logger.exception(f"Failed to place SELL grid {i}")

    return results

def main():
    parser = argparse.ArgumentParser(description="Execute Grid Trading Strategy on Binance Futures")
    parser.add_argument("symbol")
    parser.add_argument("total_quantity", type=float)
    parser.add_argument("--levels", type=int, default=GRID_LEVELS)
    parser.add_argument("--profit-percent", type=float, default=GRID_PROFIT_PERCENTAGE)
    args = parser.parse_args()

    print(f"\nCreating {args.levels}x2 grid orders for {args.symbol}...")
    results = place_grid_orders(args.symbol, args.total_quantity, args.levels, args.profit_percent)
    if results:
        print(f"✅ {len(results)} grid orders placed successfully. Check bot.log for details.")
    else:
        print("❌ Grid strategy failed. Check bot.log for errors.")

if __name__ == "__main__":
    main()
