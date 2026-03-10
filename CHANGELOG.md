# Changelog

## 4.0.0 - 2026-03-10

- Replaced the conflicting Node/Python layout with one canonical Python skill
- Made `scripts/monitor.py` the only runtime entry point
- Added real `config.json` loading
- Added optional Discord channel posting via bot token
- Replaced the placeholder indicator math with EMA-based MACD and Wilder RSI
- Fixed Fear & Greed signal direction to reward fear, not greed
- Removed unsupported claims from README and skill docs
- Added install and cron helper scripts
- Added `requirements.txt`, `SKILL.md`, and troubleshooting docs
- Prepared release artifacts from the same canonical source tree

## 3.x and earlier

Earlier revisions mixed multiple package layouts and documented features that were not implemented in the checked-in code.
