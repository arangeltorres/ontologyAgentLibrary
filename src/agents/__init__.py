"""LangChain intelligent agent for database operations."""

import json
import os
from typing import Dict, Any, Optional, List

# Conditional imports for LangChain
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from pydantic import BaseModel, Field
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    # Create dummy classes for when LangChain is not available
    class BaseModel:
        pass
    class Field:
        def __init__(self, **kwargs):
            pass

from ..models.schemas import Conn, DBType
from ..tools import run_deterministic

class DatabaseActionRequest(BaseModel):
    """Structured request for database operations."""
    action: str = Field(description="The action to perform: list_schema, update_metadata, execute_query, get_ontology, view_current_ontology")
    database_type: str = Field(description="The database type: snowflake, postgres, mysql, databricks")
    connection_params: Dict[str, Any] = Field(description="Database connection parameters")
    additional_params: Optional[Dict[str, Any]] = Field(default=None, description="Additional parameters for the action")

class DatabaseAgent:
    """Intelligent agent that processes natural language requests and determines database operations."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the database agent with OpenAI integration."""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain is not installed. Install with: pip install langchain langchain-openai langchain-core")
        
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=self.api_key
        )
        
        self.parser = JsonOutputParser(pydantic_object=DatabaseActionRequest)
        
        self.prompt = ChatPromptTemplate.from_template("""
You are an intelligent database agent that analyzes user requests and determines the appropriate database operation to perform.

Available Actions:
- list_schema: List database schema information (tables, columns, types, comments)
- update_metadata: Update comments or metadata for tables/columns
- execute_query: Execute custom SQL queries
- get_ontology: Get foreign key relationships between tables
- view_current_ontology: Get current ontology from knowledge graph storage

Supported Database Types:
- snowflake: Snowflake data warehouse
- postgres: PostgreSQL database
- mysql: MySQL database
- databricks: Databricks platform

User Request: {user_request}

Based on the user request, determine:
1. Which action should be performed
2. What type of database is being referenced
3. What connection parameters are needed
4. Any additional parameters required

Connection parameters should include:
- For Snowflake: account, user, password, warehouse, database, schema, role
- For PostgreSQL: host, port, user, password, dbname, sslmode
- For MySQL: host, port, user, password, database
- For Databricks: databricks_server_hostname, databricks_http_path, databricks_token

{format_instructions}

Respond with a JSON object containing the action, database_type, connection_params, and additional_params.
""")
        
        self.chain = self.prompt | self.llm | self.parser
    
    def process_request(self, user_request: str) -> DatabaseActionRequest:
        """Process a natural language request and return structured database operation."""
        try:
            result = self.chain.invoke({
                "user_request": user_request,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            raise ValueError(f"Failed to process request: {str(e)}")
    
    def execute_request(self, user_request: str) -> str:
        """Process and execute a user request, returning the result."""
        # Parse the user request
        parsed_request = self.process_request(user_request)
        
        # Build the connection object
        conn = Conn(
            type=parsed_request["database_type"],
            **parsed_request["connection_params"]
        )
        
        # Prepare the payload for the deterministic execution
        payload = {
            "conn": conn.model_dump(by_alias=True)
        }
        
        # Add additional parameters if any
        if parsed_request["additional_params"]:
            payload.update(parsed_request["additional_params"])
        
        # Execute the action
        result = run_deterministic(parsed_request["action"], payload)
        
        return result
    
    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return ["list_schema", "update_metadata", "execute_query", "get_ontology", "view_current_ontology"]
    
    def get_supported_databases(self) -> List[str]:
        """Get list of supported database types."""
        return ["snowflake", "postgres", "mysql", "databricks"]

class DatabaseAgentManager:
    """Manager class for database agents with configuration and error handling."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the agent manager."""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain is not installed. Install with: pip install langchain langchain-openai langchain-core")
        
        self.agent = DatabaseAgent(openai_api_key)
    
    def process_natural_language_request(self, request: str) -> str:
        """Process a natural language request and return the database operation result."""
        try:
            return self.agent.execute_request(request)
        except Exception as e:
            return json.dumps({
                "error": f"Failed to process request: {str(e)}",
                "request": request
            }, indent=2)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent capabilities."""
        return {
            "available_actions": self.agent.get_available_actions(),
            "supported_databases": self.agent.get_supported_databases(),
            "model": "gpt-4",
            "temperature": 0.1
        }

# Utility function to check if LangChain is available
def is_langchain_available() -> bool:
    """Check if LangChain is available for use."""
    return LANGCHAIN_AVAILABLE