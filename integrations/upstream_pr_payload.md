## Summary
Add a minimal, optional SIE enforcement integration slice for loader-time trust decisions.

## Behavior
- unsigned + warn => allow
- unsigned + strict => reject
- signed + valid => allow
- signed + invalid => reject

## Included files (14)
- `integrations/sie_enforcement.py`
- `integrations/openclaw_sie_config.py`
- `integrations/openclaw_hook.py`
- `integrations/openclaw_loader_reference.py`
- `integrations/__init__.py`
- `integrations/openclaw_loader_sim.py`
- `sie_verify.py`
- `tests/test_sie_enforcement.py`
- `tests/test_openclaw_sie_config.py`
- `tests/test_openclaw_hook.py`
- `tests/test_openclaw_loader_reference.py`
- `tests/test_loader_sim.py`
- `tests/test_verify_cli.py`
- `tests/test_integration_api.py`

## Validation
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Notes
- Backward compatible when SIE is disabled.
- Reason codes are stable constants for machine consumers.
