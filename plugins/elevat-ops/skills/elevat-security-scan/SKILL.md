---
name: elevat-security-scan
description: Use when Nicole asks for a security check of her repos, accounts, connectors or online footprint. Read-only audit that reports findings; replaces the old "security-scan" and "casst" skills.
---

# Elevat security scan

Audit and report only. Do not rotate keys, change permissions, delete or publish anything; list each fix as an action for Nicole or a draft PR.

1. Repos in scope (the venture repos listed in `elevat-ops`): search for committed secrets and keys, broad permission allowlists in `.claude/settings.json` (flag wildcards and "allow all"), `.env` files tracked in git, and workflows with write tokens.
2. Connectors and routines: list enabled routines and the connectors each holds; flag routines with no connectors, unneeded write access, or no owner.
3. Hosting and accounts: confirm only the approved hosts are in use (Netlify, plus Floot for Elevat Pro) and that nothing needs a card.
4. Report findings ranked high, medium, low with evidence (file path or setting name, never the secret value) and one recommended fix each. Never paste a secret into the report.
