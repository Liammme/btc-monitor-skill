# Security Notes

## Current State

This repository no longer claims a passed production security audit.

## What Was Fixed

- Removed sample IDs and misleading configuration from the published skill layout
- Removed unused Node dependencies and dead integration claims
- Moved Discord auth to an environment variable (`DISCORD_TOKEN` by default)

## Remaining Risks

- Discord bot tokens are powerful secrets; do not commit them
- Public market APIs can rate limit or fail transiently
- The script posts plain text to Discord and does not redact content beyond what it generates itself

## Safe Usage

- Keep `discord.enabled` set to `false` unless you need posting
- Export the bot token in the runtime environment instead of storing it in `config.json`
- Review cron environment handling before enabling unattended runs
