# Contributing

## Scope

Keep this repository honest:

- Do not document features that are not implemented
- Keep release archives in sync with the repository root
- Prefer small, testable changes

## Before Opening a PR

Run:

```bash
python3 -m py_compile scripts/monitor.py
```

If you changed docs or packaging, verify that:

- `README.md` matches the actual runtime entry point
- `config.json` fields are read by code or explicitly documented as unused
- release archives were rebuilt from the current tree

## Style

- Use Python 3.10+
- Keep dependencies minimal
- Favor explicit config over hardcoded thresholds
