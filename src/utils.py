"""
Utility functions for Binance Futures Trading Bot
Includes request signing, validation, and logging setup
"""

import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode
from typing import Dict, Optional, Any
from .config import (
    API_KEY,
    API_SECRET,
    API_BASE_URL,
    REQUEST_TIMEOUT,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
    DEFAULT_RECV_WINDOW,
)

def setup_logger(name: str):
    """Configure and return a logger"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    return logger

logger = setup_logger("utils")

def _sign(params: Dict) -> Dict:
    """Add timestamp and signature to parameters"""
    params = params.copy()
    params["timestamp"] = int(time.time() * 1000)
    params["recvWindow"] = DEFAULT_RECV_WINDOW
    query = urlencode(params, doseq=True)
    if not API_SECRET:
        logger.warning("API_SECRET not set — request unsigned (test mode).")
        params["signature"] = ""
        return params
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    return params

def make_request(method: str, endpoint: str, params: Optional[Dict] = None, signed: bool = False) -> Dict[str, Any]:
    """Send HTTP request to Binance Futures API"""
    url = API_BASE_URL.rstrip("/") + endpoint
    params = params or {}
    headers = {"X-MBX-APIKEY": API_KEY} if signed else {}
    try:
        if signed:
            params = _sign(params)
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        else:
            response = requests.post(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Request successful: {method} {endpoint}")
        return data
    except Exception as e:
        logger.exception(f"API request failed: {method} {endpoint} -> {e}")
        raise

# -------- Validation Functions --------
def validate_symbol(symbol: str) -> bool:
    valid = isinstance(symbol, str) and symbol.isalnum()
    if not valid:
        logger.error(f"Invalid symbol: {symbol}")
    return valid

def validate_side(side: str) -> bool:
    valid = side.upper() in ("BUY", "SELL")
    if not valid:
        logger.error(f"Invalid side: {side}")
    return valid

def validate_quantity(qty: float) -> bool:
    try:
        return float(qty) > 0
    except Exception:
        logger.error(f"Invalid quantity: {qty}")
        return False

def validate_price(price: float) -> bool:
    try:
        return float(price) > 0
    except Exception:
        logger.error(f"Invalid price: {price}")
        return False

def get_current_price(symbol: str) -> Optional[float]:
    """Fetch current price of a symbol"""
    try:
        data = make_request("GET", "/fapi/v1/ticker/price", {"symbol": symbol.upper()})
        return float(data.get("price"))
    except Exception as e:
        logger.error(f"Failed to get current price: {e}")
        return None
