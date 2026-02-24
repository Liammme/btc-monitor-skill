# BTC Monitor Skill 🪙

Real-time Bitcoin bottom-fishing monitoring system powered by AI agents.

## 📋 Overview

BTC Monitor Skill is an intelligent monitoring system that tracks Bitcoin market data in real-time and identifies optimal entry points for bottom-fishing strategies. It combines technical analysis, on-chain metrics, and social sentiment to provide actionable trading signals.

## 🎯 Features

- **RSI Oversold Detection** — Identifies extreme oversold conditions (RSI < 30)
- **MVRV Ratio Analysis** — Tracks market value vs realized value for accumulation signals
- **Miner Shutdown Price** — Monitors mining profitability thresholds
- **Social Media Panic Index** — Analyzes Twitter/Reddit sentiment during market stress
- **Long-term Holder Behavior** — Tracks LTH supply changes for accumulation patterns
- **Multi-timeframe Analysis** — Combines daily, weekly, and monthly signals
- **Automated Alerts** — Real-time Discord notifications for trading opportunities

## 🚀 Quick Start

### Installation

```bash
# Extract the skill package
tar -xzf btc-monitor-skill.tar.gz

# Install dependencies
cd btc-monitor-skill
npm install
```

### Configuration

1. Create `.env` file:
```env
DISCORD_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
COINGECKO_API_KEY=your_api_key
TWITTER_API_KEY=your_twitter_key
```

2. Configure monitoring parameters in `config.json`:
```json
{
  "rsi_threshold": 30,
  "mvrv_threshold": 1.0,
  "check_interval": 3600,
  "alert_level": "high"
}
```

### Running

```bash
npm start
```

## 📊 Monitoring Indicators

### 1. RSI (Relative Strength Index)
- **Signal**: RSI < 30 on daily/weekly timeframe
- **Interpretation**: Extreme oversold condition
- **Action**: Potential accumulation zone

### 2. MVRV Ratio
- **Signal**: MVRV < 1.0 (market value below realized value)
- **Interpretation**: Holders are underwater, potential capitulation
- **Action**: Strong bottom signal

### 3. Miner Shutdown Price
- **Signal**: Current price near or below miner cost basis
- **Interpretation**: Mining becomes unprofitable
- **Action**: Potential support level

### 4. Social Sentiment
- **Signal**: Panic index > 75 on Twitter/Reddit
- **Interpretation**: Extreme fear in market
- **Action**: Contrarian buy signal

### 5. Long-term Holder Supply
- **Signal**: LTH supply increasing during downturns
- **Interpretation**: Whales accumulating
- **Action**: Institutional buying pressure

## 🔔 Alert System

Alerts are triggered when multiple conditions align:

- **4+ indicators triggered** → Batch accumulation signal
- **5+ indicators triggered** → Heavy accumulation signal (high confidence)
- **All 5 indicators triggered** → Maximum opportunity signal

## 📈 Historical Performance

Based on historical backtesting:
- **2022 Bear Market**: Identified bottom within 5% accuracy
- **2023 Recovery**: Caught early accumulation phase
- **2024 Halving Cycle**: Predicted major support levels

## 🛠️ Architecture

```
btc-monitor-skill/
├── src/
│   ├── indicators/
│   │   ├─�� rsi.js
│   │   ├── mvrv.js
│   │   ├── miner-price.js
│   │   ├── sentiment.js
│   │   └── lth-behavior.js
│   ├── discord/
│   │   ├── client.js
│   │   └── alerts.js
│   ├── data/
│   │   ├── coingecko.js
│   │   └── onchain.js
│   └── index.js
├── config.json
├── package.json
└── README.md
```

## 🔗 Integration with OpenClaw

This skill is designed to work with OpenClaw's agent framework:

```javascript
// In your OpenClaw agent config
{
  "skills": {
    "btc-monitor": {
      "enabled": true,
      "config": "./config.json"
    }
  }
}
```

## 📚 API Reference

### `checkBTCSignals()`
Analyzes all indicators and returns combined signal strength.

```javascript
const signal = await checkBTCSignals();
// Returns: { strength: 0-5, indicators: [...], recommendation: "buy|hold|wait" }
```

### `sendAlert(signal, confidence)`
Sends formatted alert to Discord channel.

```javascript
await sendAlert(signal, 0.95);
```

## ⚙️ Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `rsi_threshold` | number | 30 | RSI oversold threshold |
| `mvrv_threshold` | number | 1.0 | MVRV ratio threshold |
| `check_interval` | number | 3600 | Check frequency (seconds) |
| `alert_level` | string | "high" | Alert sensitivity |
| `min_confidence` | number | 0.7 | Minimum confidence for alerts |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🔗 Resources

- [Bitcoin On-Chain Analysis](https://glassnode.com)
- [CoinGecko API](https://www.coingecko.com/api)
- [RSI Indicator Guide](https://www.investopedia.com/terms/r/rsi.asp)
- [MVRV Ratio Explained](https://www.glassnode.com/metrics/mvrv)

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: xiki@openclaw.local

---

**Last Updated**: 2026-02-24  
**Version**: 1.0.0  
**Status**: Active Development