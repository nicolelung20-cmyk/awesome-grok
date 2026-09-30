---
name: elevat-ops
description: Use at the start of any work on the Elevat / Elevated Associates LLC venture (trading, psychiczebra-platform, money, high-yield-extensions, hosting, Linear, finance, tax, legal or digital-footprint tasks). Gives the single source of truth, the standing decisions, and what agents may and may not do.
---

# Elevat ops

## 1. Read state first
Read the "Current state" section of the Linear project **Elevated Associates LLC — HQ** (P-ELE-5) before doing anything. It is the only active project; Growth & Release OS, Revenue OS, RAFF and SparkList are frozen. Current state lists the focus, open PRs and their owning sessions, and what not to touch. When several sessions run in parallel, each one updates that same section and nowhere else. When you finish, update that section rather than creating a new tracker, doc or dashboard.

## 2. Standing decisions
- **One host:** Netlify's free plan, site `elevat-ai`. Don't add or revive Vercel, Railway or any other host. The leftover Vercel and Railway projects are slated for deletion by Nicole. **One exception (decided 2026-09-29):** Elevat Pro stays on Floot's free plan at eai-workspace.floot.app (checkout is a Stripe Payment Link, $29/month). Don't migrate it.
- **Free tiers only.** No paid plans and no credit card anywhere.
- **Trading is personal, not in the LLC** (decided 2026-09-28): stocks, options and crypto in Nicole's own name. A single-member LLC adds no tax benefit for trading. One strategy at a time (ELE-39) on Alpaca paper (ELE-40); live later on a personal Alpaca or Robinhood account. The multi-bot swarm, sports-betting arb and token AMM are dropped.
- **The LLC's job:** earn revenue (ELE-11/13), carry business expenses, and later fund a Solo 401(k) (ELE-41). Don't sell trading signals through it. Keep personal trading costs off it.
- **Paper to live gate (matches the supergrok CHARTER.md):** 90+ days and 30+ closed paper trades, positive after fees, max drawdown under 10%, kill-switch tested. Then Nicole funds a personal live account with a capped amount. Agents never place live orders.
- **Risk policy (enforced in code):** ≤5% per position, 3% daily loss halt, ≤5 positions, no leverage.
- ELE-13 ($47 kit) and ELE-8 (revenue tracking) continue only as secondary work.
- **Business admin** lives under ELE-28: LLC standing ELE-29, banking ELE-30, trust ELE-31, tax ELE-32, legal ELE-33, digital footprint ELE-34.

## 3. What agents do vs. what Nicole does
| Agents may | Only Nicole does |
|---|---|
| Write code, open draft PRs, fix CI on PRs they opened | Merge to `main` unless she says to in that conversation |
| Draft legal docs, checklists, emails | Sign, file with the state or IRS, accept terms |
| Read balances through read-only connectors | Move money, set up transfers, open accounts |
| Update Linear issues and the Current state section | Create accounts or enter payment details |
| Production deploys only when she allows them | Final tax and legal decisions (with a CPA or attorney) |

## 4. Financial goals (don't ask Nicole to restate these)
| Goal | Target | Where it's tracked |
|---|---|---|
| Trading | Pass the paper-to-live gate, then grow the capped live account | ELE-39, ELE-40 |
| First revenue | 5 paid $47 kits + 1 signed $2,500 sprint deposit by 2026-10-31 | ELE-11 under ELE-13 |
| Revenue visibility | Every Stripe sale measurable end-to-end | ELE-8 |
| Tax reserve | 25–30% of weekly net deposits to business tax savings (final % with a CPA) | ELE-30, ELE-32 |
| Owner pay | Scheduled owner draw now; payroll/S-corp check when profit justifies it | ELE-36 |
| Quarterly estimates | Apr 15, Jun 15, Sep 15, Jan 15 (confirm with a CPA); paid via IRS Direct Pay or EFTPS | ELE-32 |
| Entity health | LLC Active, trust EIN and account in place | ELE-29, ELE-31 |
| Use the LLC | Revenue into business checking, business expenses on the LLC, Solo 401(k) once profitable | ELE-41 |

**How it's automated:** money moves only through bank-native recurring transfers that Nicole sets up once (ELE-30), with no card and no agent access. Nicole deleted all Routines on 2026-09-29, then asked for two back: the daily finance check ("Elevat daily finance check", 8:52am ET, read-only) and Elevat Pro activation (hourly, Stripe read-only). Neither holds connectors yet, so each run only reports "add connectors" until Nicole adds them on claude.ai/code/routines. Create no other Routines unless she asks. When asked for a finance check, read PocketSmith, QuickBooks and Linear read-only, add the paper-trading scorecard (expectancy, win rate, max drawdown) once ELE-40 is running, compare everything with the goals above, and update the HQ Current state section with progress, the next deadline and blockers. If a connector has no data or needs a re-login, say so and don't guess numbers. Don't create Routines unless she asks.

## 5. Working habits
- Before pushing, run the repo's checks: `npm run typecheck && npm run lint && npm test && npm run build`.
- The Railway `earnest-adventure` and Vercel `elevat/psychiczebra-platform` statuses fail on every PR and are not caused by code. Say so once per PR; don't try to fix them.
- Report plainly: what shipped, what's still blocked, and the single action each blocker needs from Nicole. Never call something "live" unless you checked it.
- Documents go in Google Drive under `Elevated Associates/{Formation, Tax, Banking, Trust, Contracts}`.

## 6. How Nicole works (applies to every model and tool)
- **Never make Nicole repeat herself.** Read this skill, the Linear Current state and the repo docs before asking anything; ask only what they don't answer.
- **Use every relevant connected tool and connector, always.** Before answering, use each read-only, paper or draft tool that bears on the task (for example PocketSmith, QuickBooks, Stripe, Linear, Alpaca paper, market-data and web-research connectors). Say which you used and which were unavailable or need a re-login.
- **Always surface the elite opportunities.** End every scan or report with a ranked list of the best opportunities found (revenue, fees, idle cash, yield, leads). For each: evidence, expected range, cost, risk, and the single action needed. Mark anything unchecked as "unverified". Never promise or imply guaranteed returns.
- **"All tools" stops at tier T2** (see `docs/alpha-finance-os.md`): live orders, money movement, account changes, key changes and merging to `main` stay with Nicole.
