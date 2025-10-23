"""
TWAP (Time-Weighted Average Price) Strategy
Executes multiple small orders over a set duration.
"""

import argparse
import sys
import os
import time
from typing import Optional, List, Dict
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ..utils import (
    make_request,
    validate_symbol,
    validate_side,
    validate_quantity,
    get_current_price,
    setup_logger,
)

logger = setup_logger("twap")
ORDER_ENDPOINT = "/fapi/v1/order"

class TWAPOrder:
    def __init__(self):
        self.executed_orders: List[Dict] = []

    def execute_twap(self, symbol: str, side: str, total_quantity: float, intervals: int, duration_seconds: int, order_type: str = "MARKET", limit_price: Optional[float] = None, position_side: str = "BOTH") -> Optional[List[Dict]]:
        if not (validate_symbol(symbol) and validate_side(side) and validate_quantity(total_quantity)):
            return None
        if intervals <= 0 or duration_seconds <= 0:
            logger.error("Invalid intervals or duration")
            return None

        qty_per_order = total_quantity / intervals
        delay = duration_seconds / intervals
        logger.info(f"Executing TWAP: {intervals} orders of {qty_per_order} {symbol} every {delay:.2f}s")

        for i in range(intervals):
            params = {
                "symbol": symbol.upper(),
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": qty_per_order,
                "positionSide": position_side.upper(),
            }
            if order_type.upper() == "LIMIT" and limit_price:
                params["price"] = limit_price
                params["timeInForce"] = "GTC"

            try:
                order = make_request("POST", ORDER_ENDPOINT, params, signed=True)
                self.executed_orders.append(order)
                logger.info(f"TWAP order {i+1}/{intervals} placed: {order.get('orderId')}")
            except Exception:
                logger.exception(f"TWAP order {i+1} failed")

            if i < intervals - 1:
                time.sleep(delay)

        return self.executed_orders if self.executed_orders else None

    def get_summary(self) -> Dict:
        total_qty = sum(float(o.get("executedQty", 0)) for o in self.executed_orders)
        avg_price = (
            sum(float(o.get("avgPrice", 0) or 0) * float(o.get("executedQty", 0)) for o in self.executed_orders)
            / total_qty
            if total_qty
            else 0
        )
        return {"orders": len(self.executed_orders), "total_quantity": total_qty, "average_price": avg_price}

def main():
    parser = argparse.ArgumentParser(description="Execute TWAP strategy")
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL", "buy", "sell"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("--intervals", type=int, default=10)
    parser.add_argument("--duration", type=int, default=300)
    parser.add_argument("--limit-price", type=float)
    parser.add_argument("--position-side", default="BOTH", choices=["BOTH", "LONG", "SHORT"])
    args = parser.parse_args()

    order_type = "LIMIT" if args.limit_price else "MARKET"
    print(f"\n⚠️  TWAP will place {args.intervals} {order_type} orders over {args.duration}s.")
    confirm = input("Proceed? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("Cancelled.")
        sys.exit(0)

    twap = TWAPOrder()
    result = twap.execute_twap(args.symbol, args.side, args.quantity, args.intervals, args.duration, order_type, args.limit_price, args.position_side)
    if result:
        summary = twap.get_summary()
        print("\n✅ TWAP Execution Completed")
        print(f"Total Orders: {summary['orders']}")
        print(f"Total Quantity: {summary['total_quantity']}")
        print(f"Average Price: {summary['average_price']}")
    else:
        print("❌ TWAP execution failed. Check bot.log for details.")

if __name__ == "__main__":
    main()
