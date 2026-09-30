# Alpha Finance OS: target architecture

Status: design, nothing in this document is running. Sits under the `elevat-ops` standing rules; where they conflict, `elevat-ops` wins. Tracked in Linear P-ELE-5.

## 1. Non-negotiables

1. **Capital protection first.** No transfer, payment or order happens without the authority tier in section 2. Hard limits are enforced in code, not in prompts:
   - ≤5% of equity per position, ≤5 open positions, no leverage, 3% daily-loss halt (existing policy, ELE-39).
   - Max drawdown 10% on paper; breaching it halts the strategy.
   - **Kill switch:** one flag (`KILL=1` in the desk's config store) makes every executor refuse new orders and cancels open paper orders. Tested before each promotion gate and after every deploy.
   - Every financial action writes a ledger entry (section 5) before it runs and is verified after it.
2. **Continuous growth, by rule.** The system watches every connected account and proposes: idle cash, fees, yield, revenue leads, inefficiencies. It reallocates only under written rules with approval thresholds; any move of money is a proposal for Nicole. Gains are compounded only when realized and net of fees. No projected returns are reported as results.
3. **Smart-wallet layer** (section 4).
4. **Command layer** (section 3).
5. **Reality guarantee** (section 6). 6. **Failure handling** (section 7). 7. **Anti-Ouroboros** (section 8).

## 2. Authority tiers

| Tier | What | Who acts |
|---|---|---|
| T0 Observe | Read balances, transactions, positions, sales, logs | Agents, read-only credentials |
| T1 Paper | Orders on the Alpaca paper account inside the hard limits | Agents, automatically |
| T2 Prepare | Drafts: proposals, transfer instructions, filings, PRs, runbooks | Agents draft, Nicole reviews |
| T3 Commit | Live orders, money movement, account opening, signing, filing, key creation or rotation, merging to `main` | Nicole only |

Agents never hold T3 credentials. The paper-to-live gate stays: 90+ days and 30+ closed paper trades, positive after fees, drawdown under 10%, kill switch tested, then Nicole funds a capped personal live account.

## 3. Command loop

`COMMAND → PERCEIVE → MODEL STATE → GENERATE OPTIONS → RISK CHECK → EXECUTE IF AUTHORIZED → VERIFY → RECORD → LEARN`

| Stage | Output | Rule |
|---|---|---|
| Perceive | Raw snapshots from each source with timestamps | Missing or stale source is reported, never filled in |
| Model state | Unified balance sheet: accounts, positions, cash, reserves, liabilities | Numbers quoted as returned, with source and time |
| Options | 1–3 candidate actions with cost, expected effect, tier | Each option names its evidence |
| Risk check | Pass/fail against the hard limits and the tier | Deterministic code, separate from the model that proposed the option |
| Execute | Only T0/T1 actions, or T2 drafts | T3 becomes a request to Nicole naming the single action needed |
| Verify | Independent re-read of the system of record | Section 6 |
| Record | Ledger entry with inputs, decision, evidence | Append-only |
| Learn | Weekly review: what worked, what cost money, what changes | Changes ship as PRs, not silent prompt edits |

## 4. Smart-wallet layer

- **One state view:** a read-only aggregator over PocketSmith, QuickBooks, Stripe, Alpaca and wallet addresses (public addresses only, multi-chain via RPC reads). Output is the section 3 balance sheet.
- **Strategy wallets:** one wallet or sub-account per strategy, with its own cap. A strategy cannot draw on another's funds.
- **Custody separated from permission:** custody stays with Nicole's bank, broker or hardware wallet. Agents get trade or read permissions only; there are no withdrawal permissions and no private keys in any agent environment.
- **Least privilege:** read-only keys by default; paper-only trade keys for Alpaca; keys stored in environment secrets, never in chat or the repo. Rotation: the system tracks key age and proposes rotation at 90 days; Nicole rotates (T3).
- **Bank-native transfers** remain the only way tax reserve and owner draw move (ELE-30).

## 5. Ledger

Append-only record per action: `id, time, tier, source, command, options considered, risk-check result, action, external reference (order id, tx hash, Stripe id, deploy id), verification result, reconciler, status`. Status is `proposed`, `executed`, `verified`, `failed` or `escalated`. Nothing is `verified` without an external reference and a passing independent check.

## 6. Reality guarantee

"Done" requires evidence from the system of record, checked by a step that did not perform the action.

| Action | Evidence required |
|---|---|
| Blockchain transaction | Transaction hash, confirmed on the chain (Nicole executes; system verifies) |
| Trade | Broker or exchange order id and fill; positions and cash re-read and reconciled |
| Revenue | Stripe charge or payment id, cross-checked in QuickBooks |
| State change | Read-back query of the database row |
| Software deploy | Deploy id, live URL fetched, expected behavior observed |
| Any balance claim | Independent read from a second source, differences listed |

Reports use "not checked" for anything without evidence.

## 7. Failure handling

`FAILURE → diagnose → identify root dependency → generate alternatives → test safest viable path → execute authorized alternative → verify → escalate only when genuinely blocked`

- Alternatives must stay within the same tier; a failure never raises authority.
- Safest path first: read-only retry, then another read source, then a paper-mode dry run.
- Escalation message names the failing dependency and the single action Nicole must take (for example, re-login to QuickBooks).

## 8. Anti-Ouroboros

Every cycle must produce at least one of: a measurable improvement, evidence, an authorized action, or a strategy change. A cycle that produces none is logged as a no-op; three no-ops in a row stop the loop and report. Self-modification is limited to PRs on prompts and rules, reviewed by Nicole, with a measured before/after.

## 9. Build order

1. Ledger and kill switch in the paper desk (ELE-40), with tests that the switch halts orders.
2. Read-only state aggregator behind the daily finance check (needs PocketSmith, QuickBooks, Linear connectors on the routine).
3. Reconciliation step: second-source balance checks, feeding the daily report.
4. Opportunity scanner (idle cash, fees, yield) producing T2 proposals only.
5. Wallet monitoring (public addresses, multi-chain reads).
6. Paper-to-live gate review (ELE-40), then Nicole's decision.

## 10. Not in scope now

Autonomous live trading, agent-held keys, automatic money movement, leverage, and any projection of guaranteed returns.
