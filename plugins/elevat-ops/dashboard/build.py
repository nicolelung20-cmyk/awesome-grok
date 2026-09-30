"""Build dashboard.html, a self-contained read-only home base (no scripts, no network).

Inputs are the prototype snapshot, the append-only ledger and agents.json. Every agent
listed in agents.json that writes to a ledger shows up here; nothing is filled in when a
source is missing ("not checked").
"""
import html, json, os, sys, time
from pathlib import Path

HERE = Path(__file__).parent
PROTO = HERE.parent / "prototype"
e = html.escape


def load(path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return default


def ledger(path, limit=15):
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return None
    rows = []
    for line in lines[-limit:]:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"status": "unreadable line"})
    return rows[::-1]


def killed():
    return os.environ.get("KILL") == "1" or (PROTO / "KILL").exists()


def card(title, body):
    return f"<section><h2>{e(title)}</h2>{body}</section>"


def render():
    snap = load(PROTO / "snapshot.json", None) or load(PROTO / "snapshot.sample.json", None)
    rows = ledger(PROTO / "ledger.jsonl")
    agents = load(HERE / "agents.json", {"agents": []})["agents"]
    kill = killed()

    parts = [f'<div class="kill {"on" if kill else "off"}">KILL SWITCH: {"ON, agents refuse to run" if kill else "off"}</div>']

    if snap:
        acct = "".join(f"<tr><td>{e(a['name'])}</td><td class=n>{a['balance_usd']:,.2f}</td></tr>" for a in snap["accounts"])
        total = sum(a["balance_usd"] for a in snap["accounts"])
        pt = snap.get("paper_trading", {})
        parts.append(card("Cash", f"<table>{acct}<tr class=t><td>Total (USD)</td><td class=n>{total:,.2f}</td></tr></table>"
                          f"<p class=m>as of {e(snap['as_of'])} · source: {e(snap['source'])}</p>"))
        parts.append(card("Revenue and trading",
                          f"<p>Revenue this month: <b>${snap.get('revenue_mtd_usd', 0):,.2f}</b> (goal: 5 kits + 1 sprint deposit by 2026-10-31)</p>"
                          f"<p>Paper trading: {pt.get('closed_trades', 'not checked')} closed trades of 30 needed · max drawdown {pt.get('max_drawdown_pct', 'not checked')}% (limit 10%)</p>"))
    else:
        parts.append(card("Cash", "<p>not checked: no snapshot found</p>"))

    arows = "".join(f"<tr><td>{e(a['name'])}</td><td>{e(a['tier'])}</td><td>{e(a['role'])}</td></tr>" for a in agents)
    parts.append(card("Agents synced", f"<table><tr><th>Agent<th>Tier<th>Role</tr>{arows}</table>"
                      "<p class=m>T0 observe · T1 paper · T2 prepare · T3 commit (Nicole only). Agents hold no T3 credentials.</p>"))

    if rows is None:
        lbody = "<p>not checked: no ledger yet. Run the agent once.</p>"
    else:
        lbody = "<table><tr><th>Time<th>Tier<th>Action<th>Status</tr>" + "".join(
            f"<tr><td>{e(str(r.get('time', '')))}</td><td>{e(str(r.get('tier', '')))}</td>"
            f"<td>{e(str(r.get('action', '')))}</td><td>{e(str(r.get('status', '')))}</td></tr>" for r in rows) + "</table>"
    parts.append(card("Ledger (latest first)", lbody))
    parts.append(card("Needs Nicole", "<ul><li>Alpaca paper keys in environment secrets</li><li>Reconnect QuickBooks and Gmail; add PocketSmith accounts</li>"
                      "<li>Bank-native recurring transfers (ELE-30)</li></ul><p class=m>Source: Linear P-ELE-5 Current state.</p>"))

    css = ("body{font:15px system-ui;margin:0;padding:16px;background:#0f1115;color:#e8e8ea}h1{font-size:20px}"
           "main{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}"
           "section{background:#1a1d24;border-radius:8px;padding:12px 16px}h2{font-size:14px;margin:0 0 8px;color:#9aa4b2}"
           "table{width:100%;border-collapse:collapse}td,th{padding:3px 6px;text-align:left}.n{text-align:right}.t{border-top:1px solid #333;font-weight:600}"
           ".m{color:#8b93a1;font-size:12px}.kill{grid-column:1/-1;padding:8px 12px;border-radius:8px;font-weight:600}"
           ".on{background:#7a1f1f}.off{background:#1f4d2e}")
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    csp = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"
    return (f'<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
            f'<meta http-equiv=Content-Security-Policy content="{csp}"><meta name=robots content=noindex>'
            f"<title>Home base</title><style>{css}</style><h1>Elevated Associates: home base</h1>"
            f"<p class=m>Built {stamp}. Read-only view; nothing here moves money.</p><main>{''.join(parts)}</main></html>")


if __name__ == "__main__":
    out = HERE / "dashboard.html"
    out.write_text(render() + "\n")
    print(f"wrote {out}")
    sys.exit(0)
