"""Snowflake database adapter."""

import snowflake.connector as sf
from typing import List, Dict, Any
from .base import DBAdapter
from ..models.schemas import Conn, MetadataArgs
from ..utils import ident, build_filter_clause
from ..queries import query_manager

class SnowflakeAdapter(DBAdapter):
    """Adapter for Snowflake database connections."""
    
    def __init__(self, c: Conn):
        self._sf = sf
        self.c = c

    def _conn(self):
        """Create a Snowflake connection."""
        return self._sf.connect(
            account=self.c.account, 
            user=self.c.user, 
            password=self.c.password,
            warehouse=self.c.warehouse, 
            database=self.c.database, 
            schema=self.c.schema_name, 
            role=self.c.role
        )

    def list_schema(self, database=None, schema=None, table=None):
        """List Snowflake schema information."""
        print("Executing Snowflake list_schema")
        
        # Use custom query if available, otherwise use standard schema query
        try:
            query = query_manager.get_query("snowflake", "list_schema_custom")
        except (KeyError, FileNotFoundError):
            # Fallback to standard schema query
            filters = build_filter_clause(database, schema, table)
            query = query_manager.get_query("snowflake", "list_schema", **filters)
        
        with self._conn() as cn:
            cur = cn.cursor()
            cur.execute(query)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def update_metadata(self, args: MetadataArgs) -> str:
        """Update metadata in Snowflake."""
        with self._conn() as cn:
            cur = cn.cursor()
            fq = ident(args.database or self.c.database, args.schema_name, args.table)
            
            if args.level == "table":
                if args.comment is not None:
                    query = query_manager.get_query("snowflake", "update_table_comment", 
                                                  table_name=fq, comment=args.comment)
                    cur.execute(query)
                if args.tags:
                    for k, v in args.tags.items():
                        query = query_manager.get_query("snowflake", "set_table_tag",
                                                       table_name=fq, tag_name=k, tag_value=v)
                        cur.execute(query)
            else:  # column
                col = args.column or ""
                if not col:
                    raise ValueError("Column required for level=column")
                if args.comment is not None:
                    query = query_manager.get_query("snowflake", "update_column_comment",
                                                   table_name=fq, column_name=col, comment=args.comment)
                    cur.execute(query)
            return "ok"

    def run_query(self, sql: str):
        """Execute a SQL query in Snowflake."""
        with self._conn() as cn:
            cur = cn.cursor()
            cur.execute(sql)
            if cur.description:
                cols = [d[0] for d in cur.description]
                return [dict(zip(cols, r)) for r in cur.fetchall()]
            return []

    def ontology(self, database=None, schema=None):
        """Get foreign key relationships from Snowflake."""
        filters = build_filter_clause(schema=schema)
        query = query_manager.get_query("snowflake", "get_foreign_keys", **filters)
        
        with self._conn() as cn:
            cur = cn.cursor()
            cur.execute(query)
            edges = [{"from": f"{r[0]}.{r[1]}.{r[2]}", "to": f"{r[3]}.{r[4]}.{r[5]}"} for r in cur.fetchall()]
        return {"edges": edges}
