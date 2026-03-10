# BTC Monitor Skill

Monitor BTC/ETH market conditions with public APIs and optionally send a text report to Discord.

## What It Does

- Pulls weekly OHLCV data from Binance, with CoinGecko-derived weekly fallback when Binance is unavailable.
- Pulls market cap, volume, ATH/ATL, and price history from CoinGecko.
- Pulls the crypto Fear & Greed Index from Alternative.me.
- Computes 6 implemented signals:
  - RSI oversold
  - Volume washout
  - MACD histogram below zero
  - Price near lower Bollinger band
  - Extreme fear
  - Low MVRV proxy
- Prints a text report to stdout.
- Optionally posts the report to a Discord channel by bot token.

## What It Does Not Do

- It does not use Glassnode, Twitter, Reddit, or any LLM/Kimi integration.
- It does not execute trades.
- The MVRV value is a proxy based on CoinGecko history, not a true on-chain realized-cap metric.

## Files

- `scripts/monitor.py`: main executable
- `config.json`: runtime configuration
- `scripts/install.sh`: dependency install helper
- `scripts/setup_cron.sh`: cron registration helper
- `docs/TROUBLESHOOTING.md`: common failure modes

## Quick Start

```bash
bash scripts/install.sh
python3 scripts/monitor.py
```

To enable Discord delivery:

1. Set `"discord.enabled": true` in `config.json`
2. Set `"discord.channel_id"` in `config.json`
3. Export `DISCORD_TOKEN`

## Cron

The script does not self-schedule. Use cron with `scripts/setup_cron.sh` or another scheduler.
