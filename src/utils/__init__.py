"""Utility functions for the database agent system."""

import re
from typing import List, Dict, Any
from ..models.schemas import MetadataArgs

# ---------- Utilities ----------
_IDENT_OK = re.compile(r"^[A-Za-z0-9_.$]+$")

def ident(*parts: str) -> str:
    """Escape/validate simple identifiers. Adjust if using dialects with quotes."""
    p = [x for x in parts if x]
    for x in p:
        if not _IDENT_OK.match(x):
            raise ValueError(f"Unsafe identifier: {x}")
    return ".".join(p)

def safe_json_dumps(data: List[Dict[str, Any]], ensure_ascii: bool = False) -> str:
    """Safely serialize data to JSON, handling datetime objects."""
    import json
    return json.dumps(data, ensure_ascii=ensure_ascii, default=str)

def build_filter_clause(database: str = None, schema: str = None, table: str = None) -> Dict[str, str]:
    """Build filter clauses for database queries."""
    filters = {}
    
    if database:
        filters['database_filter'] = f"AND table_catalog = '{database}'"
    else:
        filters['database_filter'] = ""
    
    if schema:
        filters['schema_filter'] = f"AND table_schema = '{schema}'"
    else:
        filters['schema_filter'] = ""
    
    if table:
        filters['table_filter'] = f"AND table_name = '{table}'"
    else:
        filters['table_filter'] = ""
    
    return filters

def build_postgres_filter_clause(schema: str = None, table: str = None) -> Dict[str, str]:
    """Build filter clauses for PostgreSQL queries."""
    filters = {}
    
    if schema:
        filters['schema_filter'] = f"AND table_schema = '{schema}'"
    else:
        filters['schema_filter'] = ""
    
    if table:
        filters['table_filter'] = f"AND table_name = '{table}'"
    else:
        filters['table_filter'] = ""
    
    return filters
