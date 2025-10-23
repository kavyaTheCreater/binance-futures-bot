"""
Configuration file for Binance Futures Trading Bot
Handles API credentials, endpoints, and default parameters.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Binance API Configuration
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# API Endpoints
BASE_URL = "https://fapi.binance.com"  # Mainnet
TESTNET_URL = "https://testnet.binancefuture.com"  # Testnet

# Use Testnet by default (safety)
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() in ("1", "true", "yes")
API_BASE_URL = TESTNET_URL if USE_TESTNET else BASE_URL

# Logging Configuration
LOG_FILE = "bot.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Order Configuration
DEFAULT_RECV_WINDOW = 5000
REQUEST_TIMEOUT = 10  # seconds

# Risk Management
MAX_POSITION_SIZE = 1.0
MIN_ORDER_SIZE = 0.001

# Grid Trading Configuration
GRID_LEVELS = 10
GRID_PROFIT_PERCENTAGE = 0.5  # 0.5% profit per grid

# TWAP Configuration
TWAP_DEFAULT_INTERVALS = 10
TWAP_DEFAULT_DURATION = 300  # seconds
