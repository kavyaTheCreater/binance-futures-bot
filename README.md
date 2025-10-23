# Binance Futures Trading Bot

A comprehensive CLI-based trading bot for Binance USDT-M Futures with support for multiple order types, advanced strategies, and robust logging.

## 📋 Features

### Core Orders (Mandatory)
- ✅ **Market Orders** - Execute trades immediately at best available price
- ✅ **Limit Orders** - Place orders at specific price levels

### Advanced Orders (Bonus)
- ✅ **Stop-Limit Orders** - Trigger limit orders when stop price is hit
- ✅ **OCO (One-Cancels-the-Other)** - Simultaneous take-profit and stop-loss orders
- ✅ **TWAP (Time-Weighted Average Price)** - Split large orders over time
- ✅ **Grid Trading** - Automated buy-low/sell-high within price range

### Additional Features
- 🔒 Input validation (symbol, quantity, price thresholds)
- 📝 Structured logging with timestamps and error traces
- 🛡️ Error handling and recovery
- 📊 Order status tracking and management

## 🗂️ Project Structure

```
binance-futures-bot/
│
├── src/
│   ├── config.py              # Configuration and API credentials
│   ├── utils.py               # Utility functions and validation
│   ├── market_orders.py       # Market order implementation
│   ├── limit_orders.py        # Limit order implementation
│   │
│   └── advanced/              # Advanced order strategies
│       ├── __init__.py
│       ├── stop_limit.py      # Stop-limit orders
│       ├── oco.py             # OCO orders
│       ├── twap.py            # TWAP strategy
│       └── grid_orders.py     # Grid trading strategy
│
├── bot.log                    # Execution logs
├── .env                       # API credentials (not in git)
├── .env.example               # Example environment file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── report.pdf                 # Analysis and screenshots

```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Binance Futures account
- API key with Futures trading enabled

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/binance-futures-bot.git
cd binance-futures-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API credentials**

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

4. **Configure settings** (Optional)

Edit `src/config.py` to customize:
- Use testnet or mainnet
- Logging preferences
- Risk management parameters
- Default values

### Getting API Keys

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Login with your GitHub/Google account
3. Generate API Key and Secret
4. **For production**: Use [Binance](https://www.binance.com) and enable Futures API

⚠️ **Important**: Start with testnet to avoid real money loss!

## 📖 Usage Guide

### Basic Orders

#### Market Orders
Execute trades immediately at best available market price.

```bash
# Buy 0.01 BTC at market price
python src/market_orders.py BTCUSDT BUY 0.01

# Sell 0.1 ETH at market price
python src/market_orders.py ETHUSDT SELL 0.1

# Reduce-only order (close position)
python src/market_orders.py BTCUSDT SELL 0.01 --reduce-only
```

**Parameters:**
- `symbol`: Trading pair (e.g., BTCUSDT, ETHUSDT)
- `side`: BUY or SELL
- `quantity`: Order quantity
- `--reduce-only`: Only reduce existing position (optional)
- `--position-side`: BOTH, LONG, or SHORT for hedge mode (optional)

#### Limit Orders
Place orders at specific price that execute when market reaches that price.

```bash
# Buy 0.01 BTC at $45,000
python src/limit_orders.py BTCUSDT BUY 0.01 45000

# Sell 0.1 ETH at $2,500 (post-only)
python src/limit_orders.py ETHUSDT SELL 0.1 2500 --post-only

# List all open orders
python src/limit_orders.py --list-open BTCUSDT

# Cancel specific order
python src/limit_orders.py --cancel BTCUSDT 12345678
```

**Parameters:**
- `symbol`: Trading pair
- `side`: BUY or SELL
- `quantity`: Order quantity
- `price`: Limit price
- `--time-in-force`: GTC (default), IOC, FOK, or GTX
- `--post-only`: Order will only be maker
- `--reduce-only`: Only reduce existing position

### Advanced Orders

#### Stop-Limit Orders
Trigger a limit order when stop price is hit (useful for stop-loss and breakout entries).

```bash
# Stop-loss: Sell if price drops to 44000, execute at 43900
python src/advanced/stop_limit.py BTCUSDT SELL 0.01 43900 44000

# Stop-entry: Buy if price breaks 46000, execute at 46100
python src/advanced/stop_limit.py BTCUSDT BUY 0.01 46100 46000

# Use mark price instead of last price
python src/advanced/stop_limit.py BTCUSDT SELL 0.01 43900 44000 --working-type MARK_PRICE
```

**Parameters:**
- `symbol`: Trading pair
- `side`: BUY or SELL
- `quantity`: Order quantity
- `price`: Limit price (execution price)
- `stop_price`: Stop/trigger price
- `--working-type`: CONTRACT_PRICE (default) or MARK_PRICE
- `--reduce-only`: Only reduce position (for stop-loss)

#### OCO Orders (One-Cancels-the-Other)
Place both take-profit and stop-loss simultaneously. When one executes, the other is cancelled.

```bash
# Close long: TP at 47000, SL at 44000
python src/advanced/oco.py BTCUSDT SELL 0.01 47000 44000

# Close short: TP at 43000, SL at 46000
python src/advanced/oco.py BTCUSDT BUY 0.01 43000 46000

# With custom stop-limit price
python src/advanced/oco.py BTCUSDT SELL 0.01 47000 44000 --stop-limit 43900

# Cancel OCO orders
python src/advanced/oco.py --cancel BTCUSDT 12345678 12345679
```

**Parameters:**
- `symbol`: Trading pair
- `side`: BUY (close short) or SELL (close long)
- `quantity`: Order quantity
- `take_profit`: Take-profit price
- `stop_loss`: Stop-loss trigger price
- `--stop-limit`: Stop-loss limit price (optional)

⚠️ **Note**: Currently requires manual monitoring. When one order fills, manually cancel the other.

#### TWAP (Time-Weighted Average Price)
Split large orders into smaller chunks executed over time to minimize market impact.

```bash
# Split 1 BTC buy into 10 orders over 5 minutes
python src/advanced/twap.py BTCUSDT BUY 1.0 --intervals 10 --duration 300

# Split 0.5 BTC sell into 20 orders over 10 minutes
python src/advanced/twap.py BTCUSDT SELL 0.5 --intervals 20 --duration 600

# TWAP with limit orders at specific price
python src/advanced/twap.py BTCUSDT BUY 1.0 --intervals 10 --duration 300 --limit-price 45000

# Quick TWAP: 5 orders over 1 minute
python src/advanced/twap.py BTCUSDT BUY 0.1 --intervals 5 --duration 60
```

**Parameters:**
- `symbol`: Trading pair
- `side`: BUY or SELL
- `quantity`: Total quantity to trade
- `--intervals`: Number of orders (default: 10)
- `--duration`: Total time in seconds (default: 300)
- `--limit-price`: Use limit orders instead of market (optional)

**Use Cases:**
- Accumulating large positions without slippage
- Reducing market impact
- Dollar-cost averaging
- Executing institutional-sized orders

#### Grid Trading
Automated buy-low/sell-high strategy within a price range.

```bash
# Setup grid between 44000 and 46000 with 10 levels
python src/advanced/grid_orders.py BTCUSDT 44000 46000 --grids 10 --quantity 0.01

# Tighter grid with more levels
python src/advanced/grid_orders.py BTCUSDT 45000 45500 --grids 20 --quantity 0.005

# Check grid status
python src/advanced/grid_orders.py --status BTCUSDT

# Cancel all grid orders
python src/advanced/grid_orders.py --cancel BTCUSDT

# Rebalance grid to new range
python src/advanced/grid_orders.py --rebalance BTCUSDT 43000 47000 --grids 15 --quantity 0.01
```

**Parameters:**
- `symbol`: Trading pair
- `lower_price`: Lower price bound
- `upper_price`: Upper price bound
- `--grids`: Number of grid levels (default: 10)
- `--quantity`: Quantity per grid order
- `--status`: Show current grid status
- `--cancel`: Cancel all grid orders
- `--rebalance`: Cancel and recreate grid

**Strategy:**
- Places buy orders below current price
- Places sell orders above current price
- Profits from price oscillations
- Best for ranging markets

## 📊 Logging

All operations are logged to `bot.log` with:
- Timestamps
- Log levels (INFO, WARNING, ERROR)
- Detailed error traces
- API request/response details

Example log entry:
```
2025-10-23 10:30:45,123 - market_orders - INFO - Attempting to place market order: BUY 0.01 BTCUSDT
2025-10-23 10:30:45,234 - utils - INFO - Making POST request to /fapi/v1/order
2025-10-23 10:30:45,456 - utils - INFO - Request successful: /fapi/v1/order
2025-10-23 10:30:45,457 - market_orders - INFO - ✓ Market order placed successfully!
2025-10-23 10:30:45,457 - market_orders - INFO - Order ID: 123456789
```

## 🛡️ Risk Management

### Built-in Safety Features
- Input validation for all parameters
- Symbol existence verification
- Price and quantity sanity checks
- Testnet support for safe testing
- Reduce-only orders for position management

### Recommended Practices
1. **Start with testnet** - Never test with real money
2. **Use small quantities** - Start with minimum order sizes
3. **Set stop-losses** - Use OCO or stop-limit orders
4. **Monitor positions** - Check bot.log regularly
5. **Understand leverage** - Futures trading is high-risk

### Common Pitfalls
❌ Not using testnet first
❌ Incorrect API permissions
❌ Forgetting to cancel OCO orders manually
❌ Grid trading in trending markets
❌ TWAP with volatile assets
❌ Using production keys in code

## 🔧 Configuration

### Environment Variables (.env)
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

### config.py Settings
```python
# Switch between testnet and mainnet
USE_TESTNET = True  # Set to False for production

# Logging
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# Risk Management
MAX_POSITION_SIZE = 1.0
MIN_ORDER_SIZE = 0.001

# Grid Trading
GRID_LEVELS = 10
GRID_PROFIT_PERCENTAGE = 0.5

# TWAP
TWAP_DEFAULT_INTERVALS = 10
TWAP_DEFAULT_DURATION = 300
```

## 📝 Requirements

Create a `requirements.txt` file:
```
requests==2.31.0
python-dotenv==1.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

## 🧪 Testing

### Test with Testnet
1. Get testnet API keys from https://testnet.binancefuture.com
2. Set `USE_TESTNET = True` in config.py
3. Run commands normally

### Example Test Workflow
```bash
# 1. Test market order
python src/market_orders.py BTCUSDT BUY 0.001

# 2. Test limit order
python src/limit_orders.py BTCUSDT BUY 0.001 45000

# 3. Check open orders
python src/limit_orders.py --list-open BTCUSDT

# 4. Test stop-limit
python src/advanced/stop_limit.py BTCUSDT SELL 0.001 43900 44000

# 5. Test OCO
python src/advanced/oco.py BTCUSDT SELL 0.001 47000 44000

# 6. Test TWAP (small scale)
python src/advanced/twap.py BTCUSDT BUY 0.01 --intervals 3 --duration 30

# 7. Test Grid
python src/advanced/grid_orders.py BTCUSDT 44000 46000 --grids 5 --quantity 0.001
```

## 🐛 Troubleshooting

### Common Errors

**"Invalid API-key, IP, or permissions"**
- Check API key and secret in .env
- Verify Futures trading is enabled
- Check IP whitelist settings

**"Insufficient balance"**
- Fund your testnet/mainnet account
- Check available balance vs order size

**"Invalid symbol"**
- Use correct format (BTCUSDT, not BTC-USDT)
- Verify symbol exists on Futures

**"Order would immediately trigger"**
- Limit price crosses current market price
- Adjust price or use market order

**"MIN_NOTIONAL" error**
- Order value too small
- Increase quantity or use higher price

### Debug Mode
Enable debug logging in config.py:
```python
LOG_LEVEL = 'DEBUG'
```

Check bot.log for detailed information.

## 📚 API Reference

### Binance Futures API Documentation
- Official Docs: https://binance-docs.github.io/apidocs/futures/en/
- Testnet: https://testnet.binancefuture.com
- API Limits: https://binance-docs.github.io/apidocs/futures/en/#limits

### Rate Limits
- Orders: 300 requests per minute
- Weight-based limits per endpoint
- Bot includes automatic delays to avoid limits

## 🔐 Security

### Best Practices
✅ Never commit API keys to git
✅ Use .env file for credentials
✅ Enable IP whitelist on Binance
✅ Use read-only keys for monitoring
✅ Restrict API permissions to Futures only
✅ Use testnet for development

### API Permissions Required
- Enable Reading (required)
- Enable Futures (required)
- Enable Spot & Margin Trading (not required)
- Enable Withdrawals (DO NOT ENABLE)

## 📈 Strategy Tips

### Market Orders
**Best for:**
- Quick entries/exits
- High liquidity pairs
- Emergency position closing

**Avoid when:**
- Low liquidity
- High volatility
- Large order sizes

### Limit Orders
**Best for:**
- Patient entry/exit
- Better price control
- Market making

**Avoid when:**
- Need immediate execution
- Fast-moving markets

### Stop-Limit Orders
**Best for:**
- Stop-loss protection
- Breakout trading
- Risk management

**Avoid when:**
- Gap risk is high
- Need guaranteed execution

### OCO Orders
**Best for:**
- Position management
- Defined risk/reward
- Automated profit-taking

**Monitor:**
- Both orders regularly
- Manual cancellation needed

### TWAP
**Best for:**
- Large orders
- Reducing slippage
- DCA strategies

**Avoid when:**
- Strong trends
- Low liquidity
- Time-sensitive trades

### Grid Trading
**Best for:**
- Ranging markets
- Sideways price action
- Automated scalping

**Avoid when:**
- Strong trends
- Low liquidity
- High volatility

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes only. Use at your own risk.

## ⚠️ Disclaimer

**IMPORTANT**: 
- Cryptocurrency trading carries significant risk
- This bot is for educational purposes
- Always test on testnet first
- Never invest more than you can afford to lose
- Past performance doesn't guarantee future results
- The developers are not responsible for any financial losses

## 📞 Support

For questions or issues:
- Check bot.log for error details
- Review Binance API documentation
- Open an issue on GitHub
- Contact: [your_email@example.com]

## 📅 Version History

### v1.0.0 (Current)
- ✅ Market orders
- ✅ Limit orders
- ✅ Stop-limit orders
- ✅ OCO orders
- ✅ TWAP strategy
- ✅ Grid trading
- ✅ Comprehensive logging
- ✅ Input validation
- ✅ CLI interface

## 🎯 Future Enhancements

Potential improvements:
- [ ] Automated OCO monitoring
- [ ] WebSocket real-time updates
- [ ] Portfolio tracking
- [ ] Backtesting framework
- [ ] Web dashboard
- [ ] Position size calculator
- [ ] Multi-account support
- [ ] Telegram notifications
- [ ] Advanced analytics

---

**Happy Trading! 🚀**

Remember: Start small, test thoroughly, and never risk more than you can afford to lose.


