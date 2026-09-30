# Finance agent prototype

Read-only tier-T0 agent from `docs/alpha-finance-os.md`, built on the OpenAI Agents SDK and OpenRouter (default model `anthropic/claude-opus-latest`; this is a paid model, so usage is billed to your OpenRouter key). It reads a local sample snapshot only and appends to `ledger.jsonl`.

```sh
pip install openai-agents
python agent.py --dry-run                      # offline check
OPENROUTER_API_KEY=<key> python agent.py       # live call via OpenRouter
touch KILL                                     # kill switch: agent refuses to run
```

Keep the key in environment secrets, never in the repo or chat. The agent has no tool that moves money or places orders. Copy `.env.example` to `.env` for reference (export the variables yourself; the script does not load `.env`). Model override: `ORI_MODEL`.
