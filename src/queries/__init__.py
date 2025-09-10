"""Query base management system for database operations."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache

class QueryManager:
    """Manages database queries loaded from JSON files."""
    
    def __init__(self, queries_dir: str = "src/queries"):
        self.queries_dir = Path(queries_dir)
        self._queries_cache: Dict[str, Dict[str, Any]] = {}
    
    @lru_cache(maxsize=128)
    def load_queries(self, db_type: str) -> Dict[str, Any]:
        """Load queries for a specific database type."""
        queries_file = self.queries_dir / db_type / "queries.json"
        
        if not queries_file.exists():
            raise FileNotFoundError(f"Queries file not found: {queries_file}")
        
        with open(queries_file, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        
        return queries
    
    def get_query(self, db_type: str, query_name: str, **params) -> str:
        """Get a query by name with parameter substitution."""
        queries = self.load_queries(db_type)
        
        if query_name not in queries:
            raise KeyError(f"Query '{query_name}' not found for database type '{db_type}'")
        
        query_template = queries[query_name]
        
        # Handle different query formats
        if isinstance(query_template, str):
            return self._substitute_params(query_template, **params)
        elif isinstance(query_template, dict):
            # Support for more complex query structures
            query_text = query_template.get('sql', query_template.get('query', ''))
            return self._substitute_params(query_text, **params)
        else:
            raise ValueError(f"Invalid query format for '{query_name}'")
    
    def _substitute_params(self, query: str, **params) -> str:
        """Substitute parameters in query template."""
        # Simple parameter substitution
        # Format: {param_name} or {param_name:default_value}
        for key, value in params.items():
            if value is not None:
                query = query.replace(f"{{{key}}}", str(value))
            else:
                # Handle default values in format {param:default}
                import re
                pattern = f"{{{key}:[^}}]+}}"
                query = re.sub(pattern, '', query)
        
        return query
    
    def list_available_queries(self, db_type: str) -> list:
        """List all available queries for a database type."""
        try:
            queries = self.load_queries(db_type)
            return list(queries.keys())
        except FileNotFoundError:
            return []

# Global query manager instance
query_manager = QueryManager()
