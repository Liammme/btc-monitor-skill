# BTC Monitor Skill

`btc-monitor-skill` is a Python skill that monitors BTC/ETH with public market APIs and can optionally post a plain-text report to Discord.

It is now aligned around one implementation:

- Runtime entry: `scripts/monitor.py`
- Config file: `config.json`
- Install helper: `scripts/install.sh`
- Scheduler helper: `scripts/setup_cron.sh`

## Implemented Features

- Weekly candle fetch for configured coins, preferring Binance, then Bybit, then CoinGecko-derived fallback
- CoinGecko market cap, 24h volume, ATH/ATL, and 365-day history fetch
- Fear & Greed Index fetch from Alternative.me
- 6 implemented signals:
  - RSI oversold
  - Volume washout
  - MACD histogram below zero
  - Price near lower Bollinger band
  - Extreme fear
  - Low MVRV proxy
- Plain-text report to stdout
- Optional Discord posting via bot token

## Not Implemented

The repository previously claimed several capabilities that were not present in code. Those claims have been removed. This project does not currently include:

- Glassnode integration
- Twitter/Reddit sentiment integration
- Miner shutdown price modeling
- Long-term holder analytics
- Kimi or any other LLM integration
- In-process scheduling beyond external cron/task schedulers

## Requirements

- Python 3.10+
- `requests` from `requirements.txt`
- Optional: a Discord bot token if you want channel delivery

## Quick Start

```bash
git clone https://github.com/Liammme/btc-monitor-skill
cd btc-monitor-skill
python3 -m pip install -r requirements.txt
python3 scripts/monitor.py
```

Or use the install helper:

```bash
bash scripts/install.sh
python3 scripts/monitor.py
```

## Configuration

Edit `config.json`:

```json
{
  "coins": [
    {"symbol": "BTCUSDT", "name": "Bitcoin", "coingecko_id": "bitcoin"},
    {"symbol": "ETHUSDT", "name": "Ethereum", "coingecko_id": "ethereum"}
  ],
  "thresholds": {
    "rsi_max": 30.0,
    "volume_ratio_max": 0.7,
    "fear_greed_max": 25,
    "mvrv_proxy_max": 1.0,
    "lower_band_buffer": 1.05
  },
  "discord": {
    "enabled": false,
    "token_env": "DISCORD_TOKEN",
    "channel_id": "",
    "mention_user_id": ""
  },
  "schedule": "0 8 * * *"
}
```

### Discord Delivery

To enable Discord delivery:

1. Set `"discord.enabled": true`
2. Set `"discord.channel_id"` to the destination channel
3. Export the token expected by `"discord.token_env"`:

```bash
export DISCORD_TOKEN=your_bot_token
python3 scripts/monitor.py
```

The script posts directly to the Discord channel using the bot token. It does not use `discord.js`.

## Scheduling

The script runs once per invocation. Use cron or another scheduler.

Linux/macOS cron helper:

```bash
bash scripts/setup_cron.sh
```

The helper reads the `schedule` field from `config.json` and appends a cron entry that logs to `logs/monitor.log`.

## Report Fields

- `Price`: latest close from the most recent market candle, preferring Binance, then Bybit, then CoinGecko-derived weekly candles
- `Weekly change`: percentage change from the previous weekly candle
- `RSI(14)`: Wilder RSI on close prices
- `MACD / signal / hist`: EMA-based MACD values
- `Bollinger lower / mid / upper`: 20-period Bollinger Bands
- `Volume ratio`: latest quote volume divided by the 30-period average
- `Support / resistance`: min/max close over the recent 20 candles
- `Fear & Greed`: latest Alternative.me value
- `MVRV proxy`: `market_cap / (365d average price * circulating_supply)`

## Example Run

```text
BTC Monitor Report
Generated: 2026-03-10 13:00:00 CST

Bitcoin (BTCUSDT)
  Price: $82,000.00
  Weekly change: -3.40%
  ...
```

## Repository Layout

```text
btc-monitor-skill/
├── SKILL.md
├── README.md
├── config.json
├── requirements.txt
├── scripts/
│   ├── monitor.py
│   ├── install.sh
│   └── setup_cron.sh
├── docs/
│   ├── README.md
│   └── TROUBLESHOOTING.md
└── releases/
```

## Development

Validate syntax:

```bash
python3 -m py_compile scripts/monitor.py
```

## Publish To ClawHub

This repository now includes a ClawHub-compatible `SKILL.md` with the OpenClaw frontmatter format.

Recommended publish command:

```bash
clawhub publish . --slug btc-monitor-talentversex --name "BTC Monitor TalentverseX" --version 4.0.0 --tags latest --changelog "Initial ClawHub release"
```

Later updates:

```bash
clawhub publish . --slug btc-monitor-talentversex --name "BTC Monitor TalentverseX" --version 4.0.1 --tags latest --changelog "Update skill implementation"
```

## Changelog

See `CHANGELOG.md`.
