"""PostgreSQL database adapter."""

from typing import List, Dict, Any
from .base import DBAdapter
from ..models.schemas import Conn, MetadataArgs
from ..utils import build_postgres_filter_clause
from ..queries import query_manager

class PostgresAdapter(DBAdapter):
    """Adapter for PostgreSQL database connections."""
    
    def __init__(self, c: Conn):
        import psycopg
        self.pg = psycopg
        self.c = c

    def _conn(self):
        """Create a PostgreSQL connection."""
        return self.pg.connect(
            host=self.c.host, 
            port=self.c.port, 
            user=self.c.user, 
            password=self.c.password, 
            dbname=self.c.dbname, 
            sslmode=self.c.sslmode
        )

    def list_schema(self, database=None, schema=None, table=None):
        """List PostgreSQL schema information."""
        filters = build_postgres_filter_clause(schema, table)
        query = query_manager.get_query("postgres", "list_schema", **filters)
        
        with self._conn() as cn, cn.cursor() as cur:
            params = tuple([x for x in (schema, table) if x])
            cur.execute(query, params)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def update_metadata(self, args: MetadataArgs) -> str:
        """Update metadata in PostgreSQL."""
        with self._conn() as cn, cn.cursor() as cur:
            fq = f"{args.schema_name}.{args.table}"
            
            if args.level == "table" and args.comment is not None:
                query = query_manager.get_query("postgres", "update_table_comment",
                                               table_name=fq, comment=args.comment)
                cur.execute(query)
            if args.level == "column" and args.column and args.comment is not None:
                query = query_manager.get_query("postgres", "update_column_comment",
                                               table_name=fq, column_name=args.column, comment=args.comment)
                cur.execute(query)
            cn.commit()
            return "ok"

    def run_query(self, sql: str):
        """Execute a SQL query in PostgreSQL."""
        with self._conn() as cn, cn.cursor() as cur:
            cur.execute(sql)
            if cur.description:
                cols = [d[0] for d in cur.description]
                return [dict(zip(cols, r)) for r in cur.fetchall()]
            return []

    def ontology(self, database=None, schema=None):
        """Get foreign key relationships from PostgreSQL."""
        filters = build_postgres_filter_clause(schema=schema)
        query = query_manager.get_query("postgres", "get_foreign_keys", **filters)
        
        with self._conn() as cn, cn.cursor() as cur:
            cur.execute(query, (schema,) if schema else None)
            edges = [{"from": f"{r[0]}.{r[1]}.{r[2]}", "to": f"{r[3]}.{r[4]}.{r[5]}"} for r in cur.fetchall()]
        return {"edges": edges}
