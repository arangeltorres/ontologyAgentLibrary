"""Configuration and utilities for the LangChain database agent."""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AgentConfig:
    """Configuration for the database agent."""
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-4"
    temperature: float = 0.1
    max_tokens: Optional[int] = None
    
    def __post_init__(self):
        """Initialize configuration with environment variables if not provided."""
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError(
                "OpenAI API key is required. "
                "Set OPENAI_API_KEY environment variable or provide it in AgentConfig."
            )

class AgentUtils:
    """Utility functions for the database agent."""
    
    @staticmethod
    def validate_request(request: str) -> bool:
        """Validate that the request is not empty and contains meaningful content."""
        if not request or not request.strip():
            return False
        
        # Check for minimum length
        if len(request.strip()) < 10:
            return False
        
        return True
    
    @staticmethod
    def extract_database_hints(request: str) -> Dict[str, Any]:
        """Extract potential database hints from the request."""
        hints = {
            "database_type": None,
            "action_type": None,
            "has_connection_info": False
        }
        
        request_lower = request.lower()
        
        # Database type hints
        if any(word in request_lower for word in ["snowflake", "snow", "warehouse"]):
            hints["database_type"] = "snowflake"
        elif any(word in request_lower for word in ["postgres", "postgresql", "pg"]):
            hints["database_type"] = "postgres"
        elif any(word in request_lower for word in ["mysql", "my sql"]):
            hints["database_type"] = "mysql"
        elif any(word in request_lower for word in ["databricks", "spark"]):
            hints["database_type"] = "databricks"
        
        # Action type hints
        if any(word in request_lower for word in ["list", "show", "display", "schema", "tables", "columns"]):
            hints["action_type"] = "list_schema"
        elif any(word in request_lower for word in ["update", "modify", "change", "comment", "metadata"]):
            hints["action_type"] = "update_metadata"
        elif any(word in request_lower for word in ["query", "sql", "select", "execute", "run"]):
            hints["action_type"] = "execute_query"
        elif any(word in request_lower for word in ["ontology", "relationships", "foreign key", "fk"]):
            hints["action_type"] = "get_ontology"
        elif any(word in request_lower for word in ["current ontology", "knowledge graph", "kg"]):
            hints["action_type"] = "view_current_ontology"
        
        # Connection info hints
        connection_keywords = ["account", "host", "user", "password", "database", "schema", "warehouse"]
        hints["has_connection_info"] = any(word in request_lower for word in connection_keywords)
        
        return hints
    
    @staticmethod
    def format_error_response(error: str, request: str) -> str:
        """Format an error response in a consistent way."""
        return json.dumps({
            "error": error,
            "request": request,
            "suggestion": "Please provide more specific information about the database operation you want to perform."
        }, indent=2)
    
    @staticmethod
    def get_example_requests() -> Dict[str, str]:
        """Get example requests for different operations."""
        return {
            "list_schema": "Show me the schema for the PUBLIC schema in my Snowflake database",
            "update_metadata": "Add a comment to the CUSTOMERS table in PostgreSQL",
            "execute_query": "Run this SQL query: SELECT * FROM users WHERE active = true",
            "get_ontology": "Show me the foreign key relationships in my database",
            "view_current_ontology": "Get the current ontology from the knowledge graph storage"
        }
