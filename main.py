"""Main entry point for the database agent system."""

import json
import argparse
import asyncio
from agents import Agent, Runner

from src import run_deterministic

# ---------- Agent ----------
agent = Agent(
    name="DB-Agent",
    instructions=(
        "You are a database agent. If the user asks to list schema, update metadata, execute a query or get ontology, "
        "you must ALWAYS call the correct tool and return JSON."
    ),
    tools=[],  # Temporarily empty to avoid schema issues
)

# ---------- CLI Example ----------
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["agent","det"], default="det")
    p.add_argument("--action", choices=["list_schema","update_metadata","execute_query","get_ontology"])
    p.add_argument("--payload_json", required=True)
    a = p.parse_args()
    
    if a.mode == "det":
        print(run_deterministic(a.action, json.loads(a.payload_json)))
    else:
        # conversational mode (agent decides the tool)
        result = asyncio.run(Runner.run(agent, input=a.payload_json))
        print(result.final_output)