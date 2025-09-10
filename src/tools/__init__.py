"""Database agent tools."""

from typing import Literal
from ..models.schemas import SchemaArgs, MetadataArgs, QueryArgs, OntologyArgs
from ..adapters.factory import get_adapter
from ..utils import safe_json_dumps
from ..queries import query_manager

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

def view_current_ontology(args: OntologyArgs) -> str:
    """Get the current ontology from knowledge graph storage."""
    adp = get_adapter(args.conn)
    
    # Use the specific query for current ontology
    query = query_manager.get_query("snowflake", "view_current_ontology")
    
    with adp._conn() as cn:
        cur = cn.cursor()
        cur.execute(query)
        cols = [d[0] for d in cur.description]
        data = [dict(zip(cols, r)) for r in cur.fetchall()]
    
    return safe_json_dumps(data)

def run_deterministic(action: Literal["list_schema","update_metadata","execute_query","get_ontology","view_current_ontology"], payload: dict) -> str:
    """Execute an action deterministically."""
    mapping = {
        "list_schema": list_schema,
        "update_metadata": update_metadata,
        "execute_query": execute_query,
        "get_ontology": get_ontology,
        "view_current_ontology": view_current_ontology,
    }
    tool = mapping[action]
    # Pydantic validation
    model = {"list_schema": SchemaArgs, "update_metadata": MetadataArgs,
             "execute_query": QueryArgs, "get_ontology": SchemaArgs, 
             "view_current_ontology": OntologyArgs}[action]
    args = model.model_validate(payload)
    return tool(args)  # call the real function
