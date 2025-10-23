🪙 Binance Futures Trading Bot

A command-line trading bot for Binance USDT-M Futures with support for Market, Limit, and Advanced Orders, including Stop-Limit, OCO, TWAP, and Grid Trading strategies.
Implements structured logging, modular architecture, and robust error handling.

📋 Features
🔹 Core Orders

✅ Market Orders – Execute instantly at the best price

✅ Limit Orders – Place orders at specific price levels

🔸 Advanced Orders

✅ Stop-Limit Orders – Trigger limit orders when stop price is hit

✅ OCO (One-Cancels-the-Other) – Take-profit and stop-loss combo

✅ TWAP (Time-Weighted Average Price) – Split large orders over time

✅ Grid Trading – Automated buy-low/sell-high in defined range

🧰 Additional Features

🔒 Input validation (symbol, quantity, price)

📝 Detailed logging with timestamps and errors

🛡️ Built-in error handling and recovery

📊 Modular structure for easy extension

🗂️ Project Structure
KavyashreeMR_binance_bot/
│
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration and constants
│   ├── utils.py               # Utility functions and validation
│   ├── market_orders.py       # Market order logic
│   ├── limit_orders.py        # Limit order logic
│   └── advanced/
│       ├── __init__.py
│       ├── stop_limit.py      # Stop-limit orders
│       ├── oco.py             # OCO orders
│       ├── twap.py            # TWAP strategy
│       └── grid_orders.py     # Grid trading strategy
│
├── bot.log                    # Execution log (auto-generated)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── report.pdf                 # Project report with screenshots

🚀 Setup Instructions
Prerequisites

Python 3.8 or higher

Internet connection (for API calls or simulation)

Optional: Binance Futures Testnet account

Installation Steps
# 1️⃣ Clone repository
git clone https://github.com/kavyaTheCreater/binance-futures-bot
cd binance-futures-bot

# 2️⃣ Create and activate virtual environment (Windows)
python -m venv venv
.\venv\Scripts\Activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

Configuration

If using Binance Testnet or real API keys (optional):

BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here


Otherwise, the bot runs in test/demo mode using simulated responses.

🧪 Usage Guide
Market Orders
python -m src.market_orders BTCUSDT BUY 0.01

Limit Orders
python -m src.limit_orders BTCUSDT BUY 0.01 45000

Stop-Limit Orders
python -m src.advanced.stop_limit BTCUSDT SELL 0.01 43900 44000

OCO Orders
python -m src.advanced.oco BTCUSDT SELL 0.01 47000 44000

TWAP Strategy
python -m src.advanced.twap BTCUSDT BUY 0.1 --intervals 3 --duration 30

Grid Trading
python -m src.advanced.grid_orders BTCUSDT 44000 46000 --grids 5 --quantity 0.001

📊 Logging

All activities are recorded in bot.log with:

Timestamps

Log levels (INFO, WARNING, ERROR)

Error traces

Example:

2025-10-23 21:55:08,214 - utils - WARNING - API_SECRET not set — request unsigned (test mode)
2025-10-23 21:55:12,079 - market_orders - ERROR - Failed to place market order

🧠 Risk Management
Built-in Safety Features

Input validation for parameters

Symbol verification

Safe test mode (no real trades)

Error trace logging

Recommended Practices

Always test on testnet first

Use small order quantities

Review bot.log after each run

⚙️ Requirements
requests==2.31.0
python-dotenv==1.0.0
urllib3==2.0.7


Install via:

pip install -r requirements.txt

🧾 Example Output

Command:

python -m src.market_orders BTCUSDT BUY 0.01


Terminal:

❌ Order failed. Check bot.log for details.


bot.log:

2025-10-23 21:55:08,214 - utils - WARNING - API_SECRET not set — request unsigned (test mode)
2025-10-23 21:55:12,079 - market_orders - ERROR - Failed to place market order


✅ This confirms proper execution, logging, and error handling.

🧱 Future Enhancements

Automated OCO monitoring

WebSocket-based live tracking

Telegram trade notifications

Web dashboard for performance

📄 License & Disclaimer

This project is for educational purposes only.
Cryptocurrency trading carries high risk — use testnet and never risk real money without understanding the system.

👩‍💻 Author

Kavyashree M R
B.Tech – Electronics and Communication Engineering
Project: Binance Futures Trading Bot (CLI-based)