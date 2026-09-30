"""Read-only finance agent prototype (Alpha Finance OS, tier T0).

Uses the OpenAI Agents SDK against OpenRouter's OpenAI-compatible endpoint with a
free model, so no paid key is needed. It can only read a local JSON snapshot; it
has no tool that moves money, places orders or writes outside the ledger.

    python agent.py --dry-run                # no network, exercises tool + ledger + kill switch
    OPENROUTER_API_KEY=... python agent.py   # free-tier key from openrouter.ai
"""
import argparse, json, os, sys, time
from pathlib import Path

HERE = Path(__file__).parent
LEDGER = HERE / "ledger.jsonl"
MODEL = os.environ.get("ORI_MODEL", "meta-llama/llama-3.3-70b-instruct:free")


def killed() -> bool:
    return os.environ.get("KILL") == "1" or (HERE / "KILL").exists()


def record(entry: dict) -> None:
    entry["time"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with LEDGER.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def read_snapshot(path: str = str(HERE / "snapshot.sample.json")) -> str:
    """T0 tool: return the account snapshot as JSON text."""
    data = Path(path).read_text()
    record({"tier": "T0", "action": "read_snapshot", "ref": path, "status": "verified"})
    return data


def dry_run() -> int:
    if killed():
        record({"tier": "T0", "action": "dry_run", "status": "refused_kill_switch"})
        print("kill switch on: refusing")
        return 1
    snap = json.loads(read_snapshot())
    total = sum(a["balance_usd"] for a in snap["accounts"])
    print(f"total cash {total:.2f} USD as of {snap['as_of']} (source: {snap['source']})")
    return 0


def run_agent() -> int:
    if killed():
        print("kill switch on: refusing")
        return 1
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("set OPENROUTER_API_KEY (free key from openrouter.ai), or use --dry-run")
        return 2
    from openai import AsyncOpenAI
    from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
    import asyncio

    set_tracing_disabled(True)
    client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)
    agent = Agent(
        name="finance-reader",
        instructions=("You report on the account snapshot. Read-only. Quote numbers exactly as "
                      "returned with the snapshot date and source; say 'not checked' for anything "
                      "you cannot see. Never suggest moving money as if you had done it."),
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
        tools=[function_tool(read_snapshot)],
    )
    result = asyncio.run(Runner.run(agent, "Give today's cash position and revenue so far this month."))
    record({"tier": "T0", "action": "agent_report", "model": MODEL, "status": "executed"})
    print(result.final_output)
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    sys.exit(dry_run() if p.parse_args().dry_run else run_agent())
