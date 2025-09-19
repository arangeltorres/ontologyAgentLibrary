"""Database Agent System."""

from .models import Conn, SchemaArgs, MetadataArgs, QueryArgs, OntologyArgs, DBType
from .adapters import DBAdapter, get_adapter
from .tools import list_schema, update_metadata, execute_query, get_ontology, view_current_ontology, run_deterministic
from .utils import ident, safe_json_dumps, build_filter_clause, build_postgres_filter_clause
from .queries import query_manager
from .agents import DatabaseAgent, DatabaseAgentManager, is_langchain_available
from .agents.config import AgentConfig, AgentUtils

__all__ = [
    # Models
    "Conn",
    "SchemaArgs", 
    "MetadataArgs",
    "QueryArgs",
    "OntologyArgs",
    "DBType",
    # Adapters
    "DBAdapter",
    "get_adapter",
    # Tools
    "list_schema",
    "update_metadata", 
    "execute_query",
    "get_ontology",
    "view_current_ontology",
    "run_deterministic",
    # Utils
    "ident",
    "safe_json_dumps",
    "build_filter_clause",
    "build_postgres_filter_clause",
    # Query Management
    "query_manager",
    # LangChain Agents
    "DatabaseAgent",
    "DatabaseAgentManager",
    "is_langchain_available",
    "AgentConfig",
    "AgentUtils"
]
