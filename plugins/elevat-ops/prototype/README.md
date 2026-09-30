# Finance agent prototype

Read-only tier-T0 agent from `docs/alpha-finance-os.md`, built on the OpenAI Agents SDK and OpenRouter's free models (no payment). It reads a local sample snapshot only and appends to `ledger.jsonl`.

```sh
pip install openai-agents
python agent.py --dry-run                      # offline check
OPENROUTER_API_KEY=<free key> python agent.py  # live call, free model
touch KILL                                     # kill switch: agent refuses to run
```

Keep the key in environment secrets, never in the repo or chat. The agent has no tool that moves money or places orders. Model override: `ORI_MODEL`.
