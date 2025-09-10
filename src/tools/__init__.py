"""Database agent tools."""

from typing import Literal
from ..models.schemas import SchemaArgs, MetadataArgs, QueryArgs
from ..adapters.factory import get_adapter
from ..utils import safe_json_dumps

def list_schema(args: SchemaArgs) -> str:
    """List schema: tables/columns with types and comments."""
    adp = get_adapter(args.conn)
    data = adp.list_schema(args.database, args.schema_name, args.table)
    return safe_json_dumps(data)

def update_metadata(args: MetadataArgs) -> str:
    """Update comments (and tags in Snowflake) for table/column."""
    adp = get_adapter(args.conn)
    out = adp.update_metadata(args)
    return out

def execute_query(args: QueryArgs) -> str:
    """Execute SQL (use only with permitted roles)."""
    adp = get_adapter(args.conn)
    rows = adp.run_query(args.sql)
    return safe_json_dumps(rows)

def get_ontology(args: SchemaArgs) -> str:
    """Return foreign key relationships (simple graph)."""
    adp = get_adapter(args.conn)
    graph = adp.ontology(args.database, args.schema_name)
    return safe_json_dumps(graph)

def run_deterministic(action: Literal["list_schema","update_metadata","execute_query","get_ontology"], payload: dict) -> str:
    """Execute an action deterministically."""
    mapping = {
        "list_schema": list_schema,
        "update_metadata": update_metadata,
        "execute_query": execute_query,
        "get_ontology": get_ontology,
    }
    tool = mapping[action]
    # Pydantic validation
    model = {"list_schema": SchemaArgs, "update_metadata": MetadataArgs,
             "execute_query": QueryArgs, "get_ontology": SchemaArgs}[action]
    args = model.model_validate(payload)
    return tool(args)  # call the real function
