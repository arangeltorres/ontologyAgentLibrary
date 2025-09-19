"""Factory For Creating Database Adapters."""

from .base import DBAdapter
from .snowflake import SnowflakeAdapter
from .postgres import PostgresAdapter
from ..models.schemas import Conn

def get_adapter(conn: Conn) -> DBAdapter:
    """Create a database adapter based on the connection type."""
    if conn.type == "snowflake":
        return SnowflakeAdapter(conn)
    if conn.type == "postgres":
        return PostgresAdapter(conn)
    # TODO: mysql, databricks. Just adde the same condition but changing the adapter name and the import
    raise ValueError(f"DB not supported yet: {conn.type}")
