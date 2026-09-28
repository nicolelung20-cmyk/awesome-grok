---
name: elevat-ops
description: Use at the start of any work on the Elevat / Elevated Associates LLC venture (psychiczebra-platform, money, high-yield-extensions, hosting, Linear, finance, tax, legal or digital-footprint tasks). Gives the single source of truth, the standing decisions, and what agents may and may not do.
---

# Elevat ops

## 1. Read state first
Read the "Current state" section of the Linear project **Elevat Growth & Release OS** before doing anything. It lists the hosting decision, open PRs and their owning sessions, and what not to touch. When you finish, update that section rather than creating a new tracker, doc or dashboard.

## 2. Standing decisions
- **One host:** Netlify's free plan, site `elevat-ai`. Don't add or revive Vercel, Railway or any other host. The leftover Vercel and Railway projects are slated for deletion by Nicole.
- **Free tiers only.** No paid plans and no credit card anywhere.
- **Focus order:** ELE-5 (production live), then ELE-13 ($47 kit), then ELE-8 (revenue tracking). Backlog projects (RAFF bots, SparkList) stay paused.
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
| First revenue | 5 paid $47 kits + 1 signed $2,500 sprint deposit by 2026-10-31 | ELE-11 under ELE-13 |
| Revenue visibility | Every Stripe sale measurable end-to-end | ELE-8 |
| Tax reserve | 25–30% of weekly net deposits to business tax savings (final % with a CPA) | ELE-30, ELE-32 |
| Owner pay | Scheduled owner draw now; payroll/S-corp check when profit justifies it | ELE-36 |
| Quarterly estimates | Apr 15, Jun 15, Sep 15, Jan 15 (confirm with a CPA); paid via IRS Direct Pay or EFTPS | ELE-32 |
| Entity health | LLC Active, trust EIN and account in place | ELE-29, ELE-31 |

**How it's automated:** money moves only through bank-native recurring transfers that Nicole sets up once (ELE-30), with no card and no agent access. Agents run the weekly finance check, a Routine named "Elevat weekly finance check" (Mondays 8:52am ET). It reads PocketSmith, QuickBooks and Linear read-only, compares them with the goals above, and updates the Current state section with progress, the next deadline and blockers. If a connector has no data or needs a re-login, say so in the check and don't guess numbers.

## 5. Working habits
- Before pushing, run the repo's checks: `npm run typecheck && npm run lint && npm test && npm run build`.
- The Railway `earnest-adventure` and Vercel `elevat/psychiczebra-platform` statuses fail on every PR and are not caused by code. Say so once per PR; don't try to fix them.
- Report plainly: what shipped, what's still blocked, and the single action each blocker needs from Nicole. Never call something "live" unless you checked it.
- Documents go in Google Drive under `Elevated Associates/{Formation, Tax, Banking, Trust, Contracts}`.
