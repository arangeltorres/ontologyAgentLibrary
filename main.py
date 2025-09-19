"""Main entry point for the database agent system."""

import json
import argparse
import asyncio
import os
from agents import Agent, Runner

from src import run_deterministic, DatabaseAgentManager, AgentConfig

# ---------- Agent ----------
agent = Agent(
    name="DB-Agent",
    instructions=(
        "You are a database agent. If the user asks to list schema, update metadata, execute a query or get ontology, "
        "you must ALWAYS call the correct tool and return JSON."
    ),
    tools=[],  # Temporarily empty to avoid schema issues
)

# ---------- LangChain Agent Manager ----------
def get_langchain_agent():
    """Initialize and return the LangChain database agent manager."""
    try:
        config = AgentConfig()
        return DatabaseAgentManager(config.openai_api_key)
    except ValueError as e:
        print(f"Warning: {e}")
        print("LangChain mode will not be available. Set OPENAI_API_KEY environment variable.")
        return None

# ---------- CLI Example ----------
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Database Agent System with LangChain Integration")
    p.add_argument("--mode", choices=["agent","det","langchain"], default="det",
                   help="Execution mode: agent (conversational), det (deterministic), langchain (AI-powered)")
    p.add_argument("--action", choices=["list_schema","update_metadata","execute_query","get_ontology","view_current_ontology"],
                   help="Action to perform (required for det mode)")
    p.add_argument("--payload_json", help="JSON payload with connection and parameters")
    p.add_argument("--request", help="Natural language request (required for langchain mode)")
    p.add_argument("--api_key", help="OpenAI API key (optional, can use OPENAI_API_KEY env var)")
    
    a = p.parse_args()
    
    if a.mode == "det":
        if not a.action or not a.payload_json:
            print("Error: --action and --payload_json are required for deterministic mode")
            exit(1)
        print(run_deterministic(a.action, json.loads(a.payload_json)))
        
    elif a.mode == "langchain":
        if not a.request:
            print("Error: --request is required for langchain mode")
            print("Example: --request 'Show me the schema for my Snowflake database'")
            exit(1)
        
        # Initialize LangChain agent
        langchain_agent = get_langchain_agent()
        if not langchain_agent:
            exit(1)
        
        # Process the natural language request
        result = langchain_agent.process_natural_language_request(a.request)
        print(result)
        
    else:  # agent mode
        if not a.payload_json:
            print("Error: --payload_json is required for agent mode")
            exit(1)
        # conversational mode (agent decides the tool)
        result = asyncio.run(Runner.run(agent, input=a.payload_json))
        print(result.final_output)