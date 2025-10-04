# Realms Agentic Core

This is the operational brain of Core Alpha in the Realms architecture. It houses diagnostics, dispatch, fallback, monetization, and control modules for a swarm of 1000 agents.

## 📂 Structure

- `diagnostics/`: Failure scanners, heartbeat monitors, payload validators
- `dispatch/`: Platform-specific dispatchers (WordPress, LinkedIn, Facebook)
- `fallback/`: Fallback logic for failed syndication
- `monetization/`: Revenue tracking and dashboard generation
- `control/`: Credential mapping and agent awareness logging
- `logs/`: Runtime logs and fallback records

## 🔐 Credentials

Stored in `.env`, including:

- `WP_TOKEN`, `LINKEDIN_TOKEN`, `FB_TOKEN`
- `SMTP_EMAIL`, `SMTP_PASS`, `FALLBACK_EMAIL`

## 🚀 Activation

Run `ignite_realms.py` to scan and activate all modules.

## 🧠 Status

- Core Alpha: Active
- Core Beta: Bridged, unsynced
- Agents: 1000+ per core
