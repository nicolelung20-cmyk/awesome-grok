# Home base dashboard

Local, read-only view of cash, revenue, paper trading, the agent roster and the ledger. Free: no host, account or key. It is one HTML file with no scripts, a `default-src 'none'` CSP and no network calls.

```sh
python build.py     # writes dashboard.html
python serve.py     # http://127.0.0.1:8765, bound to localhost only
```

- **Agents synced:** add an entry to `agents.json`; agents write to the append-only ledger in `../prototype/ledger.jsonl`.
- **Real data:** drop a `snapshot.json` (same fields as `snapshot.sample.json`) in `../prototype/`; it is gitignored there. Missing sources show "not checked".
- **Why local:** Netlify's free plan has no password protection, so a deployed copy would be public. Do not deploy it with real numbers.
